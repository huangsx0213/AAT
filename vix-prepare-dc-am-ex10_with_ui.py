import time, os, configparser, sys,threading
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from datetime import datetime
from vix import VixHost, VixError, VixJob, VixVM


class AATPerform(threading.Thread):
    def __init__(self,qtn,aat_prompt_message_label):
        super().__init__()
        self.qtn=qtn
        self.aat_prompt_message_label=aat_prompt_message_label
        self.aat_prompt_message_label.setText("")

    def run(self):
        try:
            done = 0
            release_package_dirs = os.listdir(release_path)
            # copy the latest am msi to host machine
            release_package_full_path = os.path.join(
                '%s\%s\ArchiveManagerInstaller.msi' % (release_path, release_package_dirs[-1]))
            os.system("copy /y %s %s" % (release_package_full_path, host_os_files_path_for_am))
            print(str(
                datetime.now()) + " Copied the latest am msi from " + release_package_full_path + " to " + host_os_files_path_for_am)

            # new a VixHost instance

            _vm_host = VixHost()
            time.sleep(2.0)

            # open the dc vm
            vm_dc = _vm_host.open_vm(dc_vmx_path)
            # power on dc vm and sleep 5 seconds

            is_power_on = vm_dc.power_on(launch_gui=True)
            time.sleep(2.0)
            print(str(datetime.now()) + " Power on dc vm - Done.")

            # revert to a snapshot
            vm_dc_snapshot = vm_dc.snapshot_get_named(snapshot_name)
            vm_dc.snapshot_revert(snapshot=vm_dc_snapshot, options=VixVM.VIX_VMPOWEROP_LAUNCH_GUI)
            time.sleep(2.0)
            print(str(datetime.now()) + " Reverted to snapshot Base - Done.")

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
            time.sleep(10.0)
            # power on am vm and sleep 5 seconds
            vm_am.power_on(launch_gui=True)
            time.sleep(10.0)
            print(str(datetime.now()) + " Power on am vm and sleep 5 seconds - Done.")

            # revert to a snapshot
            vm_am_snapshot = vm_am.snapshot_get_named(snapshot_name)
            vm_am.snapshot_revert(snapshot=vm_am_snapshot, options=VixVM.VIX_VMPOWEROP_LAUNCH_GUI)
            time.sleep(2.0)
            print(str(datetime.now()) + " Reverted to snapshot Base - Done.")

            # Login to am guest for guest operation
            # vm_am.login("dc2k8\\administrator", "Pa$$word", require_interactive=True)
            # time.sleep(2.0)
            # print(str(datetime.now()) + " Login to am guest for guest operation - Done.")
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
            done=1

        except Exception as ex:
            print(str(datetime.now()) + " Exception,Operatation failed: {0}".format(ex), file=f)
            print(str(datetime.now()) + " " + ex.__traceback__, file=f)
        finally:
            f.close()
            _vm_host.disconnect()
            self.qtn.setEnabled(True)
            self.qtn.setText("Run")
            if done==1:
                self.aat_prompt_message_label.setText(
                    "{s}".format(s=release_package_dirs[-1] + " Installed successfully."))
            else:
                self.aat_prompt_message_label.setText(
                    "{s}".format(s=release_package_dirs[-1] + " Install fail."))

class Exp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def work(self, qtn,aat_prompt_message_label):
        qtn.setEnabled(False)
        qtn.setText("Running")
        aat = AATPerform(qtn,aat_prompt_message_label)
        aat.start()
    def save(self,dc_vmx_pathEdit,am_vmx_pathEdit,release_pathEdit,snapshot_pathEdit,guest_login_nameEdit,guest_login_passwordEdit):
        cp.set("config","dc_vmx_path",dc_vmx_pathEdit.text())
        cp.set("config", "am_vmx_path", am_vmx_pathEdit.text())
        cp.set("config", "release_path", release_pathEdit.text())
        cp.set("config", "snapshot_name", snapshot_pathEdit.text())
        cp.set("config", "guest_login_name", guest_login_nameEdit.text())
        cp.set("config", "guest_login_password", guest_login_passwordEdit.text())
        cp.write(open(r'.\config\myapp.conf', "w"))
    def initUI(self):

        self.setWindowIcon(QIcon('.\images\logo.png'))
        self.resize(600, 100)
        self.setWindowTitle('AAT')

        dc_vmx_path_label = QLabel('dc_vmx_path:')
        am_vmx_path_label = QLabel('am_vmx_path:')
        release_path_label= QLabel('release_path:')
        snapshot_label = QLabel('snapshot_name:')
        guest_login_name_label = QLabel('guest_login_name:')
        guest_login_password_label = QLabel('guest_login_password:')
        aat_prompt_message_label= QLabel("")

        dc_vmx_pathEdit = QLineEdit()
        dc_vmx_pathEdit.setText(dc_vmx_path)
        am_vmx_pathEdit = QLineEdit()
        am_vmx_pathEdit.setText(am_vmx_path)
        release_pathEdit = QLineEdit()
        release_pathEdit.setText(release_path)
        snapshot_pathEdit = QLineEdit()
        snapshot_pathEdit.setText(snapshot_name)
        guest_login_nameEdit = QLineEdit()
        guest_login_nameEdit.setText(guest_login_name)
        guest_login_passwordEdit = QLineEdit()
        guest_login_passwordEdit.setText(guest_login_password)
        guest_login_passwordEdit.setEchoMode(QLineEdit.Password)

        save_button = QPushButton('Save', self)
        run_button = QPushButton('Run', self)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(dc_vmx_path_label, 1, 0)
        grid.addWidget(dc_vmx_pathEdit, 1, 1,1,6)

        grid.addWidget(am_vmx_path_label, 2, 0)
        grid.addWidget(am_vmx_pathEdit, 2, 1,1,6)

        grid.addWidget(release_path_label, 3, 0)
        grid.addWidget(release_pathEdit, 3, 1,1,6)

        grid.addWidget(snapshot_label, 4, 0)
        grid.addWidget(snapshot_pathEdit, 4, 1,1,6)

        grid.addWidget(guest_login_name_label, 5, 0)
        grid.addWidget(guest_login_nameEdit, 5, 1, 1, 6)

        grid.addWidget(guest_login_password_label, 6, 0)
        grid.addWidget(guest_login_passwordEdit, 6, 1, 1, 6)

        grid.addWidget(aat_prompt_message_label, 7, 1,1,5)
        grid.addWidget(save_button, 7, 5)
        grid.addWidget(run_button, 7, 6)

        self.setLayout(grid)

        save_button.clicked.connect(lambda: self.save(dc_vmx_pathEdit,am_vmx_pathEdit,release_pathEdit,snapshot_pathEdit,guest_login_nameEdit,guest_login_passwordEdit))
        run_button.clicked.connect(lambda: self.work(run_button,aat_prompt_message_label))

if __name__ == '__main__':

    f = open("./logs/log.txt", 'w+')

    cp = configparser.ConfigParser()

    cp.read(r'.\config\myapp.conf')

    dc_vmx_path = str(cp.get('config', 'dc_vmx_path'))
    print("dc_vmx_path:%s" % (dc_vmx_path))

    am_vmx_path = str(cp.get('config', 'am_vmx_path'))
    print("dc_vmx_path:%s" % (am_vmx_path))

    release_path = cp.get('config', 'release_path')
    print("release_path:%s" % (release_path))

    snapshot_name = cp.get('config', 'snapshot_name')
    print("snapshot_name:%s" % (snapshot_name))

    guest_login_name = cp.get('config', 'guest_login_name')
    guest_login_password = cp.get('config', 'guest_login_password')

    host_os_files_path_for_dc = r".\vix\dc"
    host_os_files_path_for_am = r".\vix\am"
    guest_os_files_path = r"C:\vix"

    app = QApplication(sys.argv)
    ex = Exp()
    ex.show()

    sys.exit(app.exec_())
