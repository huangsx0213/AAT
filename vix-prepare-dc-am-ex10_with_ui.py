import sys
import os
import time
import configparser
import threading
from PyQt5 import QtWidgets, QtCore

from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import *
from datetime import datetime
from vix import VixHost, VixError, VixJob, VixVM
from win32com.shell import shell, shellcon
from GlobalLogging import GlobalLogging
import logging

class AATPerform(threading.Thread):
    def __init__(self, main_window):
        super().__init__()
        self.run_button = main_window.run_button
        self._change_logcolour_signal = main_window._change_logcolour_signal
        self.console_win = main_window.console_win
        self._change_logcolour_signal.emit("blue")


    def run(self):
        try:
            done = 0
            GlobalLogging.getInstance().info('Copying the latest build.')
            #self.aat_prompt_message_label.setText("Copying the latest build.")
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
            GlobalLogging.getInstance().info('Opening the dc vm.')
            #self.aat_prompt_message_label.setText("Opening the dc vm.")
            vm_dc = _vm_host.open_vm(dc_vmx_path)

            # revert to a snapshot
            GlobalLogging.getInstance().info('Reverting to a snapshot.')
            #self.aat_prompt_message_label.setText("Reverting to a snapshot.")
            vm_dc_snapshot = vm_dc.snapshot_get_named(snapshot_name)
            vm_dc.snapshot_revert(snapshot=vm_dc_snapshot, options=VixVM.VIX_VMPOWEROP_LAUNCH_GUI)
            print(str(datetime.now()) + " Reverted to snapshot Base - Done.")
            GlobalLogging.getInstance().info('Reverted to snapshot Base - Done.')

            # Login to dc guest for guest operation
            GlobalLogging.getInstance().info('Waiting for tools.')
            #self.aat_prompt_message_label.setText("Waiting for tools.")
            vm_dc.wait_for_tools()
            GlobalLogging.getInstance().info('Login dc guest.')
            #self.aat_prompt_message_label.setText("Login dc guest.")
            vm_dc.login(guest_login_name, guest_login_password, require_interactive=True)
            time.sleep(2.0)

            print(str(datetime.now()) + " Login to dc guest for guest operation - Done.")
            GlobalLogging.getInstance().info('Login to dc guest for guest operation - Done.')
            # copy vix folder from host to guest for dc
            #self.aat_prompt_message_label.setText("Copying vix folder from host to guest for dc.")
            GlobalLogging.getInstance().info('Copying vix folder from host to guest for dc.')
            vm_dc.copy_host_to_guest(host_os_files_path_for_dc, guest_os_files_path)
            print(str(datetime.now()) + " Copied vix folder from host to guest for dc - Done.")
            GlobalLogging.getInstance().info('Copied vix folder from host to guest for dc - Done.')

            # run script to prepare email data on dc vm
            #self.aat_prompt_message_label.setText("Running script to prepare email data on dc vm.")
            GlobalLogging.getInstance().info('Running script to prepare email data on dc vm.')
            vm_dc.run_script(r"PowerShell.exe -file c:\vix\importPST.ps1", None, False)
            print(str(datetime.now()) + " Run powershell script to prepare email data on dc vm - Done.")
            GlobalLogging.getInstance().info('Run powershell script to prepare email data on dc vm - Done.')

            # logout guest of dc
            vm_dc.logout()
            print(str(datetime.now()) + " Logout guest of dc - Done.")
            GlobalLogging.getInstance().info('Logout guest of dc - Done.')
            # open the am vm
            vm_am = _vm_host.open_vm(am_vmx_path)

            # revert to a snapshot
            #self.aat_prompt_message_label.setText("Reverting to a snapshot.")
            GlobalLogging.getInstance().info('Reverting to a snapshot.')
            vm_am_snapshot = vm_am.snapshot_get_named(snapshot_name)
            vm_am.snapshot_revert(snapshot=vm_am_snapshot, options=VixVM.VIX_VMPOWEROP_LAUNCH_GUI)
            print(str(datetime.now()) + " Reverted to snapshot Base - Done.")
            GlobalLogging.getInstance().info('Reverted to snapshot Base - Done.')

            # Login to am guest for guest operation
            #self.aat_prompt_message_label.setText("Waiting for tools.")
            GlobalLogging.getInstance().info('Waiting for tools.')
            vm_am.wait_for_tools()
            #self.aat_prompt_message_label.setText("Login am guest.")
            GlobalLogging.getInstance().info('Login am guest.')
            vm_am.login(guest_login_name, guest_login_password, require_interactive=True)
            time.sleep(2.0)
            print(str(datetime.now()) + " Login to am guest for guest operation - Done.")
            GlobalLogging.getInstance().info('Login to am guest for guest operation - Done.')

            # copy vix folder from host to guest for am
            #self.aat_prompt_message_label.setText("Copying vix folder from host to guest for am.")
            GlobalLogging.getInstance().info('Copying vix folder from host to guest for am.')
            vm_am.copy_host_to_guest(host_os_files_path_for_am, guest_os_files_path)
            print(str(datetime.now()) + " Copy vix folder from host to guest for am - Done.")
            GlobalLogging.getInstance().info('Copy vix folder from host to guest for am - Done.')

            # run script to install am on am vm
            #self.aat_prompt_message_label.setText("Running script to install am on am vm.")
            GlobalLogging.getInstance().info('Running script to install am on am vm.')
            vm_am.proc_run(guest_os_files_path + r"\am_cmd.bat", None, True)
            print(str(datetime.now()) + " Run script to install,config am on am vm - Done.")
            GlobalLogging.getInstance().info('Run script to install,config am on am vm - Done.')

            # run script to install Chrome
            #self.aat_prompt_message_label.setText("Running script to install Chrome.")
            GlobalLogging.getInstance().info('Running script to install Chrome.')
            vm_am.proc_run(guest_os_files_path + "\ChromeStandaloneSetupEn 57.0.2987.110.exe", None, True)
            print(str(datetime.now()) + " Run script to install Chrome - Done.")
            GlobalLogging.getInstance().info('Run script to install Chrome - Done.')

            # logout guest of am
            vm_am.logout()
            print(str(datetime.now()) + " Logout guest of am - Done.")
            GlobalLogging.getInstance().info('Logout guest of am - Done.')
            done = 1

        except Exception as ex:
            print(str(datetime.now()) + " Exception,Operatation failed: {0}".format(ex), file=log_file)
            print(str(datetime.now()) + " " + ex.__traceback__, file=log_file)
            GlobalLogging.getInstance().exception("Error:")
        finally:
            log_file.close()
            _vm_host.disconnect()
            self.run_button.setEnabled(True)
            self.run_button.setText("Run")
            if done == 1:
                #self.aat_prompt_message_label.setStyleSheet("QLabel {font-family:Arial;color : green; }")
                self._change_logcolour_signal.emit("green")
                GlobalLogging.getInstance().info(release_package_dirs[-1]+" installed successfully.")
                #self.aat_prompt_message_label.setText(
                 #   "{s}".format(s=release_package_dirs[-1] + " installed successfully."))
            else:
                #self.aat_prompt_message_label.setStyleSheet("QLabel {font-family:Arial;color : red; }")
                self._change_logcolour_signal.emit("red")
                GlobalLogging.getInstance().info(release_package_dirs[-1] + " install failed.")
                #self.aat_prompt_message_label.setText(
                 #   "{s}".format(s=release_package_dirs[-1] + " install failed."))


class MainWindow(QTabWidget):
    _change_logcolour_signal = QtCore.pyqtSignal(str)
    _append_text_signal = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()

    def work(self):
        self.run_button.setEnabled(False)
        self.run_button.setText("Running")
        aat = AATPerform(self)
        aat.start()

    def save(self):
        config_parser.set("config", "dc_vmx_path", self.dc_vmx_path_edit.text())
        config_parser.set("config", "am_vmx_path", self.am_vmx_path_edit.text())
        config_parser.set("config", "release_path", self.release_path_edit.text())
        config_parser.set("config", "snapshot_name", self.snapshot_path_edit.text())
        config_parser.set("config", "guest_login_name", self.guest_login_name_edit.text())
        config_parser.set("config", "guest_login_password", self.guest_login_password_edit.text())
        config_parser.write(open(r'.\config\myapp.conf', "w"))
    def auto_scroll(self):
        self.cursor = self.console_win.textCursor()
        self.cursor.movePosition(QTextCursor.End)
        self.console_win.setTextCursor(self.cursor)
    def append_text(self,msg):
        self.console_win.append(msg)
        self.cursor = self.console_win.textCursor()
        self.cursor.movePosition(QTextCursor.End)
        self.console_win.setTextCursor(self.cursor)
        self.aat_prompt_message_label.setText(msg)
    def change_logcolour(self,col):
        self.aat_prompt_message_label.setStyleSheet("QLabel {font-family:Arial;color : "+col+"; }")
    def initUI(self):
        self.setWindowIcon(QIcon('.\images\logo.png'))
        self.resize(600,275)
        self.setWindowTitle('AAT')

        self.dc_vmx_path_label = QLabel('dc_vmx_path:')
        self.am_vmx_path_label = QLabel('am_vmx_path:')
        self.release_path_label = QLabel('release_path:')
        self.snapshot_label = QLabel('snapshot_name:')
        self.guest_login_name_label = QLabel('guest_login_name:')
        self.guest_login_password_label = QLabel('guest_login_password:')
        self.run_time_message_label = QLabel("run_time_message:")
        self.aat_prompt_message_label = QLabel("")

        self.dc_vmx_path_edit = QLineEdit()
        self.dc_vmx_path_edit.setText(dc_vmx_path)
        self.am_vmx_path_edit = QLineEdit()
        self.am_vmx_path_edit.setText(am_vmx_path)
        self.release_path_edit = QLineEdit()
        self.release_path_edit.setText(release_path)
        self.snapshot_path_edit = QLineEdit()
        self.snapshot_path_edit.setText(snapshot_name)
        self.guest_login_name_edit = QLineEdit()
        self.guest_login_name_edit.setText(guest_login_name)
        self.guest_login_password_edit = QLineEdit()
        self.guest_login_password_edit.setText(guest_login_password)
        self.guest_login_password_edit.setEchoMode(QLineEdit.Password)

        self.save_button = QPushButton('Save', self)
        self.run_button = QPushButton('Run', self)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid2 = QGridLayout()
        self.grid2.setSpacing(10)

        self.grid.addWidget(self.dc_vmx_path_label, 1, 0)
        self.grid.addWidget(self.dc_vmx_path_edit, 1, 1, 1, 6)

        self.grid.addWidget(self.am_vmx_path_label, 2, 0)
        self.grid.addWidget(self.am_vmx_path_edit, 2, 1, 1, 6)

        self.grid.addWidget(self.release_path_label, 3, 0)
        self.grid.addWidget(self.release_path_edit, 3, 1, 1, 6)

        self.grid.addWidget(self.snapshot_label, 4, 0)
        self.grid.addWidget(self.snapshot_path_edit, 4, 1, 1, 6)

        self.grid.addWidget(self.guest_login_name_label, 5, 0)
        self.grid.addWidget(self.guest_login_name_edit, 5, 1, 1, 6)

        self.grid.addWidget(self.guest_login_password_label, 6, 0)
        self.grid.addWidget(self.guest_login_password_edit, 6, 1, 1, 6)

        self.grid.addWidget(self.run_time_message_label, 7, 0)
        self.grid.addWidget(self.aat_prompt_message_label, 7, 1, 1, 6)
        self.grid.addWidget(self.save_button, 8, 5)
        self.grid.addWidget(self.run_button, 8, 6)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.addTab(self.tab, " Console")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.addTab(self.tab1, "TaskManagement")
        self.tab1.setLayout(self.grid)
        self.tab.setLayout(self.grid2)
        self.setCurrentIndex(1)

        self.save_button.clicked.connect(self.save)
        self.run_button.clicked.connect(lambda: self.work())

        self.console_win = QtWidgets.QTextBrowser()
        self.grid2.addWidget(self.console_win,1,0,7,7)
        self.clear_logs_button = QPushButton('Clear', self)
        self.grid2.addWidget(self.clear_logs_button,8,6)
        self.clear_logs_button.clicked.connect(self.console_win.clear)


        self._change_logcolour_signal.connect(self.change_logcolour)
        self._append_text_signal.connect(self.append_text)

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
    main_window = MainWindow()
    main_window.show()
    GlobalLogging.getInstance().setLoggingToFile(r'./logs/log2.txt')
    GlobalLogging.getInstance().setLoggingToQTextBrowserHanlder(main_window)
    GlobalLogging.getInstance().setLoggingLevel(logging.INFO)
    sys.exit(app.exec_())
