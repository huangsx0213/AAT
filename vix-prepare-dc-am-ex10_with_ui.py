import sys
import os
import time
import configparser
import threading
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from datetime import datetime
from vix import VixHost, VixError, VixJob, VixVM
from win32com.shell import shell, shellcon


class AATPerform(threading.Thread):
    def __init__(self, qtn, aat_prompt_message_label):
        super().__init__()
        self.qtn = qtn
        self.aat_prompt_message_label = aat_prompt_message_label
        self.aat_prompt_message_label.setText("")

    def run(self):
        try:
            done = 0
            release_package_dirs = os.listdir(release_path)
            release_package_full_path = os.path.join(
                '{rp}\{rpd}\ArchiveManagerInstaller.msi'.format(rp=release_path, rpd=release_package_dirs[-1]))
            # Copy the latest mis packet from share path to host，if fail,it will retry 3 times
            i = 0
            while i < 3:
                copy_return = shell.SHFileOperation((0, shellcon.FO_COPY, release_package_full_path,
                                                     host_os_files_path_for_am,
                                                     shellcon.FOF_NOCONFIRMATION | shellcon.FOF_SILENT, None, None))
                if copy_return[0] == 0:
                    print(str(
                        datetime.now()) + " Copied the latest am msi from " + release_package_full_path + " to " + host_os_files_path_for_am)
                    break
                i += 1
                print(str(datetime.now()) + " Copy error with error code:{error}".format(error=copy_return))

            # new a VixHost instance
            _vm_host = VixHost()

            # open the dc vm
            vm_dc = _vm_host.open_vm(dc_vmx_path)

            # revert to a snapshot
            vm_dc_snapshot = vm_dc.snapshot_get_named(snapshot_name)
            vm_dc.snapshot_revert(snapshot=vm_dc_snapshot, options=VixVM.VIX_VMPOWEROP_LAUNCH_GUI)
            print(str(datetime.now()) + " Reverted to snapshot Base - Done.")

            # Login to dc guest for guest operation
            vm_dc.wait_for_tools()
            vm_dc.login(guest_login_name, guest_login_password, require_interactive=True)
            time.sleep(2.0)

            print(str(datetime.now()) + " Login to dc guest for guest operation - Done.")
            # copy vix folder from host to guest for dc
            vm_dc.copy_host_to_guest(host_os_files_path_for_dc, guest_os_files_path)
            print(str(datetime.now()) + " Copied vix folder from host to guest for dc - Done.")

            # run script to prepare email data on dc vm
            vm_dc.run_script(r"PowerShell.exe -file c:\vix\importPST.ps1", None, False)
            print(str(datetime.now()) + " Run powershell script to prepare email data on dc vm - Done.")

            # logout guest of dc
            vm_dc.logout()
            print(str(datetime.now()) + " Logout guest of dc - Done.")

            # open the am vm
            vm_am = _vm_host.open_vm(am_vmx_path)

            # revert to a snapshot
            vm_am_snapshot = vm_am.snapshot_get_named(snapshot_name)
            vm_am.snapshot_revert(snapshot=vm_am_snapshot, options=VixVM.VIX_VMPOWEROP_LAUNCH_GUI)
            print(str(datetime.now()) + " Reverted to snapshot Base - Done.")

            # Login to am guest for guest operation
            vm_am.wait_for_tools()
            vm_am.login(guest_login_name, guest_login_password, require_interactive=True)
            time.sleep(2.0)
            print(str(datetime.now()) + " Login to am guest for guest operation - Done.")

            # copy vix folder from host to guest for am
            vm_am.copy_host_to_guest(host_os_files_path_for_am, guest_os_files_path)
            print(str(datetime.now()) + " Copy vix folder from host to guest for am - Done.")

            # run script to install am on am vm
            vm_am.proc_run(guest_os_files_path + "\Install_AM.bat", None, True)
            print(str(datetime.now()) + " Run script to install am on am vm - Done.")

            # run script to config CC on am vm
            vm_am.proc_run(guest_os_files_path + "\ConfigurationConsoleSilent.bat", None, True)
            print(str(datetime.now()) + " Run script to config CC on am vm - Done.")

            # run script to start am service
            vm_am.proc_run(guest_os_files_path + "\StartService.bat", None, True)
            print(str(datetime.now()) + " Run script to start am service - Done.")

            # run script to install Chrome
            vm_am.proc_run(guest_os_files_path + "\ChromeStandaloneSetupEn 57.0.2987.110.exe", None, True)
            print(str(datetime.now()) + " Run script to install Chrome - Done.")

            # logout guest of am
            vm_am.logout()
            print(str(datetime.now()) + " Logout guest of am - Done.")
            done = 1

        except Exception as ex:
            print(str(datetime.now()) + " Exception,Operatation failed: {0}".format(ex), file=log_file)
            print(str(datetime.now()) + " " + ex.__traceback__, file=log_file)
        finally:
            log_file.close()
            _vm_host.disconnect()
            self.qtn.setEnabled(True)
            self.qtn.setText("Run")
            if done == 1:
                self.aat_prompt_message_label.setStyleSheet("QLabel {font-family:Arial;color : green; }")
                self.aat_prompt_message_label.setText(
                    "{s}".format(s=release_package_dirs[-1] + " installed successfully."))
            else:
                self.aat_prompt_message_label.setStyleSheet("QLabel {font-family:Arial;color : red; }")
                self.aat_prompt_message_label.setText(
                    "{s}".format(s=release_package_dirs[-1] + " install failed."))


class Exp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def work(self, qtn, aat_prompt_message_label):
        qtn.setEnabled(False)
        qtn.setText("Running")
        aat = AATPerform(qtn, aat_prompt_message_label)
        aat.start()

    def save(self, dc_vmx_path_edit, am_vmx_path_edit, release_path_edit, snapshot_path_edit, guest_login_name_edit,
             guest_login_passwordEdit):
        config_parser.set("config", "dc_vmx_path", dc_vmx_path_edit.text())
        config_parser.set("config", "am_vmx_path", am_vmx_path_edit.text())
        config_parser.set("config", "release_path", release_path_edit.text())
        config_parser.set("config", "snapshot_name", snapshot_path_edit.text())
        config_parser.set("config", "guest_login_name", guest_login_name_edit.text())
        config_parser.set("config", "guest_login_password", guest_login_passwordEdit.text())
        config_parser.write(open(r'.\config\myapp.conf', "w"))

    def initUI(self):
        self.setWindowIcon(QIcon('.\images\logo.png'))
        self.resize(600, 100)
        self.setWindowTitle('AAT')

        dc_vmx_path_label = QLabel('dc_vmx_path:')
        am_vmx_path_label = QLabel('am_vmx_path:')
        release_path_label = QLabel('release_path:')
        snapshot_label = QLabel('snapshot_name:')
        guest_login_name_label = QLabel('guest_login_name:')
        guest_login_password_label = QLabel('guest_login_password:')
        aat_prompt_message_label = QLabel("")

        dc_vmx_path_edit = QLineEdit()
        dc_vmx_path_edit.setText(dc_vmx_path)
        am_vmx_path_edit = QLineEdit()
        am_vmx_path_edit.setText(am_vmx_path)
        release_path_edit = QLineEdit()
        release_path_edit.setText(release_path)
        snapshot_path_edit = QLineEdit()
        snapshot_path_edit.setText(snapshot_name)
        guest_login_name_edit = QLineEdit()
        guest_login_name_edit.setText(guest_login_name)
        guest_login_password_edit = QLineEdit()
        guest_login_password_edit.setText(guest_login_password)
        guest_login_password_edit.setEchoMode(QLineEdit.Password)

        save_button = QPushButton('Save', self)
        run_button = QPushButton('Run', self)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(dc_vmx_path_label, 1, 0)
        grid.addWidget(dc_vmx_path_edit, 1, 1, 1, 6)

        grid.addWidget(am_vmx_path_label, 2, 0)
        grid.addWidget(am_vmx_path_edit, 2, 1, 1, 6)

        grid.addWidget(release_path_label, 3, 0)
        grid.addWidget(release_path_edit, 3, 1, 1, 6)

        grid.addWidget(snapshot_label, 4, 0)
        grid.addWidget(snapshot_path_edit, 4, 1, 1, 6)

        grid.addWidget(guest_login_name_label, 5, 0)
        grid.addWidget(guest_login_name_edit, 5, 1, 1, 6)

        grid.addWidget(guest_login_password_label, 6, 0)
        grid.addWidget(guest_login_password_edit, 6, 1, 1, 6)

        grid.addWidget(aat_prompt_message_label, 7, 1, 1, 5)
        grid.addWidget(save_button, 7, 5)
        grid.addWidget(run_button, 7, 6)

        self.setLayout(grid)

        save_button.clicked.connect(
            lambda: self.save(dc_vmx_path_edit, am_vmx_path_edit, release_path_edit, snapshot_path_edit,
                              guest_login_name_edit, guest_login_password_edit))
        run_button.clicked.connect(lambda: self.work(run_button, aat_prompt_message_label))


if __name__ == '__main__':
    log_file = open("./logs/log.txt", 'w+')

    config_parser = configparser.ConfigParser()

    config_parser.read(r'.\config\myapp.conf')

    dc_vmx_path = str(config_parser.get('config', 'dc_vmx_path'))
    print("dc_vmx_path:%s" % (dc_vmx_path))

    am_vmx_path = str(config_parser.get('config', 'am_vmx_path'))
    print("dc_vmx_path:%s" % (am_vmx_path))

    release_path = config_parser.get('config', 'release_path')
    print("release_path:%s" % (release_path))

    snapshot_name = config_parser.get('config', 'snapshot_name')
    print("snapshot_name:%s" % (snapshot_name))

    guest_login_name = config_parser.get('config', 'guest_login_name')
    guest_login_password = config_parser.get('config', 'guest_login_password')

    host_os_files_path_for_dc = r".\vix\dc"
    host_os_files_path_for_am = r".\vix\am"
    guest_os_files_path = r"C:\vix"

    app = QApplication(sys.argv)
    ex = Exp()
    ex.show()

    sys.exit(app.exec_())
