import sys
import os
import time
import configparser
import threading
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import *
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
            get_allconfig()
            GlobalLogging.getInstance().info('-'*50)
            GlobalLogging.getInstance().info('Copying the '+build_number+' build to host.')

            release_package_full_path = os.path.join(
                '{rp}\{rpd}\ArchiveManagerInstaller.msi'.format(rp=release_path, rpd=build_number))
            # Copy the latest mis packet from share path to host，if fail,it will retry 3 times
            i = 0
            while i < 3:
                copy_return = shell.SHFileOperation((0, shellcon.FO_COPY, release_package_full_path,
                                                     host_os_files_path_for_am,
                                                     shellcon.FOF_NOCONFIRMATION | shellcon.FOF_SILENT, None, None))
                if copy_return[0] == 0:
                    GlobalLogging.getInstance().info("Copied the "+ build_number + " build from " + release_package_full_path + " to " + host_os_files_path_for_am)
                    break
                i += 1
                GlobalLogging.getInstance().error("Copy error with error code:{error}".format(error=copy_return))

            # new a VixHost instance
            _vm_host = VixHost()

            # open the dc vm
            GlobalLogging.getInstance().info('Opening the dc vm.')
            vm_dc = _vm_host.open_vm(dc_vmx_path)
            GlobalLogging.getInstance().info('Power on the dc vm.')
            vm_dc.power_on(launch_gui=True)
            GlobalLogging.getInstance().info('Power on the dc vm - Done.')
            # revert to a snapshot
            GlobalLogging.getInstance().info('Reverting to snapshot.')
            vm_dc_snapshot = vm_dc.snapshot_get_named(snapshot_name)
            vm_dc.snapshot_revert(snapshot=vm_dc_snapshot, options=VixVM.VIX_VMPOWEROP_LAUNCH_GUI)
            GlobalLogging.getInstance().info('Reverted to snapshot Base - Done.')

            # Login to dc guest for guest operation
            GlobalLogging.getInstance().info('Waiting for tools.')
            vm_dc.wait_for_tools()
            GlobalLogging.getInstance().info('Login dc guest.')
            vm_dc.login(guest_login_name, guest_login_password, require_interactive=True)
            time.sleep(2.0)
            GlobalLogging.getInstance().info('Login to dc guest for guest operation - Done.')

            # copy vix folder from host to guest for dc
            GlobalLogging.getInstance().info('Copying vix folder from host to dc guest.')
            vm_dc.copy_host_to_guest(host_os_files_path_for_dc, guest_os_files_path)
            GlobalLogging.getInstance().info('Copied vix folder from host to dc guest - Done.')

            # run program on am dc
            dc_program_name = program_run_on_dc.split(',')
            dc_program_block = not (program_run_on_dc_imme == str(True))
            for dc_program in dc_program_name:
                if dc_program is not '':
                    GlobalLogging.getInstance().info('Running program ' + dc_program + '.')
                    vm_dc.proc_run(guest_os_files_path + "\\" + dc_program, None,dc_program_block)
                    GlobalLogging.getInstance().info('Running program ' + dc_program + ' - Done.')

            # run script on am dc
            dc_script = script_run_on_dc.split(',')
            dc_scr_block = not (script_run_on_dc_imme == str(True))
            for dc_scr in dc_script:
                if dc_scr is not '':
                    GlobalLogging.getInstance().info('Running script ' + dc_scr + '.')
                    vm_dc.run_script(dc_scr, None,dc_scr_block )
                    GlobalLogging.getInstance().info('Running script ' + dc_scr + ' - Done.')

            # logout guest of dc
            vm_dc.logout()
            GlobalLogging.getInstance().info('Logout dc guest - Done.')

            # open the am vm
            GlobalLogging.getInstance().info('Opening the am vm.')
            vm_am = _vm_host.open_vm(am_vmx_path)
            GlobalLogging.getInstance().info('Power on the am vm.')
            vm_am.power_on(launch_gui=True)
            GlobalLogging.getInstance().info('Power on the am vm - Done.')
            # revert to a snapshot
            GlobalLogging.getInstance().info('Reverting to snapshot.')
            vm_am_snapshot = vm_am.snapshot_get_named(snapshot_name)
            vm_am.snapshot_revert(snapshot=vm_am_snapshot, options=VixVM.VIX_VMPOWEROP_LAUNCH_GUI)
            GlobalLogging.getInstance().info('Reverted to snapshot Base - Done.')

            # Login to am guest for guest operation
            GlobalLogging.getInstance().info('Waiting for tools.')
            vm_am.wait_for_tools()

            GlobalLogging.getInstance().info('Login am guest.')
            vm_am.login(guest_login_name, guest_login_password, require_interactive=True)
            time.sleep(2.0)
            GlobalLogging.getInstance().info('Login to am guest for guest operation - Done.')

            # copy vix folder from host to guest for am
            GlobalLogging.getInstance().info('Copying vix folder from host to am guest.')
            vm_am.copy_host_to_guest(host_os_files_path_for_am, guest_os_files_path)
            GlobalLogging.getInstance().info('Copy vix folder from host to am guest - Done.')

            # run program on am vm
            am_program_name = program_run_on_am.split(',')
            am_program_block = not (program_run_on_am_imme == str(True))
            for am_program in am_program_name:
                if am_program is not '':
                    GlobalLogging.getInstance().info('Running program ' + am_program + '.')
                    vm_am.proc_run(guest_os_files_path + "\\" + am_program, None,am_program_block )
                    GlobalLogging.getInstance().info('Running program ' + am_program + ' - Done.')

            # run script on am vm
            am_script = script_run_on_am.split(',')
            am_scr_block = not (script_run_on_am_imme == str(True))
            for am_scr in am_script:
                if am_scr is not '':
                    GlobalLogging.getInstance().info('Running script ' + am_scr + '.')
                    vm_am.run_script(am_scr, None,am_scr_block )
                    GlobalLogging.getInstance().info('Running script ' + am_scr + ' - Done.')

            # logout guest of am
            vm_am.logout()
            GlobalLogging.getInstance().info('Logout am guest - Done.')
            done = 1

        except Exception as ex:
            GlobalLogging.getInstance().exception("Catch a exception.")
        finally:
            _vm_host.disconnect()
            self.run_button.setEnabled(True)
            self.run_button.setText("Run")
            if done == 1:
                self._change_logcolour_signal.emit("green")
                GlobalLogging.getInstance().info(build_number+" installed successfully.")
            else:
                self._change_logcolour_signal.emit("red")
                GlobalLogging.getInstance().info(build_number + " install failed.")


class MainWindow(QTabWidget):
    _change_logcolour_signal = QtCore.pyqtSignal(str)
    _append_text_signal = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()
        self.read_txt_to_help()
        self.refresh_build_number()
    def work(self):
        global build_number
        build_number = self.build_number_combobox.currentText()
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
        config_parser.set("config", "program_run_on_dc", self.program_run_on_dc_edit.text())
        config_parser.set("config", "script_run_on_dc", self.script_run_on_dc_edit.text())
        config_parser.set("config", "program_run_on_am", self.program_run_on_am_edit.text())
        config_parser.set("config", "script_run_on_am", self.script_run_on_am_edit.text())

        config_parser.set("config", "program_run_on_dc_imme", str(self.program_run_on_dc_check.isChecked()))
        config_parser.set("config", "script_run_on_dc_imme", str(self.script_run_on_dc_check.isChecked()))
        config_parser.set("config", "program_run_on_am_imme", str(self.program_run_on_am_check.isChecked()))
        config_parser.set("config", "script_run_on_am_imme", str(self.script_run_on_am_check.isChecked()))
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
    def browse_dc_vmx_dialog(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open file','','*.vmx')
        if file_path[0] is not '':
            self.dc_vmx_path_edit.setText(file_path[0])

    def browse_am_vmx_dialog(self):
        file_path2 = QFileDialog.getOpenFileName(self, 'Open file', '', '*.vmx')
        if file_path2[0] is not '':
            self.am_vmx_path_edit.setText(file_path2[0])

    def browse_release_path_dialog(self):
        file_path3 = QFileDialog.getExistingDirectory(self, 'Open directory', '' )
        if file_path3 is not '':
            self.release_path_edit.setText(file_path3)

    def read_txt_to_help(self):
        lines = f.readlines()
        for line in lines:
            self.help_win.append(line)
        f.close()

    def refresh_build_number(self):
        get_release_package_dirs()
        M = QStringListModel(release_package_dirs)
        self.build_number_combobox.setModel(M)
        self.build_number_combobox.setCurrentIndex(len(release_package_dirs)-1)

    def initUI(self):
        self.setWindowIcon(QIcon('.\images\logo.png'))
        self.resize(800,350)
        self.setWindowTitle('AAT')

        self.dc_vmx_path_label = QLabel('dc_vmx_path:')
        self.am_vmx_path_label = QLabel('am_vmx_path:')
        self.release_path_label = QLabel('release_path:')
        self.build_number_label = QLabel('build_number:')
        self.snapshot_label = QLabel('snapshot_name:')
        self.guest_login_name_label = QLabel('guest_login:')
        self.guest_login_password_label = QLabel('guest_password:')
        self.run_time_message_label = QLabel("run_time_message:")
        self.program_run_on_dc_label = QLabel("program_run_on_dc:")
        self.program_run_on_am_label = QLabel("program_run_on_am:")
        self.script_run_on_dc_label = QLabel("script_run_on_dc:")
        self.script_run_on_am_label = QLabel("script_run_on_am:")
        self.aat_prompt_message_label = QLabel("")

        self.dc_vmx_path_edit = QLineEdit()
        self.dc_vmx_path_edit.setText(dc_vmx_path)
        self.am_vmx_path_edit = QLineEdit()
        self.am_vmx_path_edit.setText(am_vmx_path)
        self.release_path_edit = QLineEdit()
        self.release_path_edit.setText(release_path)
        self.build_number_combobox = QComboBox()
        self.snapshot_path_edit = QLineEdit()
        self.snapshot_path_edit.setText(snapshot_name)
        self.guest_login_name_edit = QLineEdit()
        self.guest_login_name_edit.setText(guest_login_name)
        self.guest_login_password_edit = QLineEdit()
        self.guest_login_password_edit.setText(guest_login_password)
        self.guest_login_password_edit.setEchoMode(QLineEdit.Password)
        self.program_run_on_dc_edit = QLineEdit()
        self.program_run_on_dc_edit.setText(program_run_on_dc)
        self.program_run_on_dc_check = QCheckBox('return_immediately')
        self.program_run_on_dc_check.setChecked(program_run_on_dc_imme == str(True))
        self.script_run_on_dc_edit = QLineEdit()
        self.script_run_on_dc_edit.setText(script_run_on_dc)
        self.script_run_on_dc_check = QCheckBox('return_immediately')
        self.script_run_on_dc_check.setChecked(script_run_on_dc_imme == str(True))
        self.program_run_on_am_edit = QLineEdit()
        self.program_run_on_am_edit.setText(program_run_on_am)
        self.program_run_on_am_check = QCheckBox('return_immediately')
        self.program_run_on_am_check.setChecked(program_run_on_am_imme == str(True))
        self.script_run_on_am_edit = QLineEdit()
        self.script_run_on_am_edit.setText(script_run_on_am)
        self.script_run_on_am_check = QCheckBox('return_immediately')
        self.script_run_on_am_check.setChecked(script_run_on_am_imme == str(True))

        self.save_button = QPushButton('Save', self)
        self.run_button = QPushButton('Run', self)
        self.refresh_build_number_button = QPushButton('Refresh build no.', self)
        self.browse_dc_vmx_button = QPushButton('Browse...', self)
        self.browse_am_vmx_button = QPushButton('Browse...', self)
        self.browse_release_path_button = QPushButton('Browse...', self)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid2 = QGridLayout()
        self.grid2.setSpacing(10)
        self.grid2.setContentsMargins(0,0,0,0)

        self.grid3 = QGridLayout()
        self.grid3.setSpacing(10)
        self.grid3.setContentsMargins(0, 0, 0, 0)

        self.grid.addWidget(self.dc_vmx_path_label, 1, 0)
        self.grid.addWidget(self.dc_vmx_path_edit, 1, 1, 1,6)
        self.grid.addWidget(self.browse_dc_vmx_button, 1, 7)

        self.grid.addWidget(self.am_vmx_path_label, 2, 0)
        self.grid.addWidget(self.am_vmx_path_edit, 2, 1, 1,6)
        self.grid.addWidget(self.browse_am_vmx_button, 2, 7)

        self.grid.addWidget(self.release_path_label, 3, 0)
        self.grid.addWidget(self.release_path_edit, 3, 1, 1,4)
        self.grid.addWidget(self.build_number_label, 3, 5)
        self.grid.addWidget(self.build_number_combobox, 3, 6)
        self.grid.addWidget(self.browse_release_path_button, 3, 7)

        self.grid.addWidget(self.snapshot_label, 4, 0)
        self.grid.addWidget(self.snapshot_path_edit, 4,1)

        self.grid.addWidget(self.guest_login_name_label, 4,2)
        self.grid.addWidget(self.guest_login_name_edit, 4,3)

        self.grid.addWidget(self.guest_login_password_label, 4,5)
        self.grid.addWidget(self.guest_login_password_edit,4,6)

        self.grid.addWidget(self.refresh_build_number_button, 4, 7)

        self.grid.addWidget(self.program_run_on_dc_label, 5, 0)
        self.grid.addWidget(self.program_run_on_dc_edit, 5, 1, 1, 6)
        self.grid.addWidget(self.program_run_on_dc_check, 5,7)

        self.grid.addWidget(self.script_run_on_dc_label, 6, 0)
        self.grid.addWidget(self.script_run_on_dc_edit, 6, 1, 1, 6)
        self.grid.addWidget(self.script_run_on_dc_check, 6, 7)

        self.grid.addWidget(self.program_run_on_am_label,7, 0)
        self.grid.addWidget(self.program_run_on_am_edit, 7,1, 1, 6)
        self.grid.addWidget(self.program_run_on_am_check, 7, 7)

        self.grid.addWidget(self.script_run_on_am_label, 8, 0)
        self.grid.addWidget(self.script_run_on_am_edit, 8, 1, 1, 6)
        self.grid.addWidget(self.script_run_on_am_check, 8, 7)

        self.grid.addWidget(self.run_time_message_label, 9, 0)
        self.grid.addWidget(self.aat_prompt_message_label, 9, 1, 1,7)


        self.grid.addWidget(self.save_button,10,6)
        self.grid.addWidget(self.run_button, 10,7)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.addTab(self.tab, " Console")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.addTab(self.tab1, "TaskManagement")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.addTab(self.tab2, "Help")
        self.tab1.setLayout(self.grid)
        self.tab.setLayout(self.grid2)
        self.tab2.setLayout(self.grid3)
        self.setCurrentIndex(1)

        self.save_button.clicked.connect(self.save)
        self.run_button.clicked.connect(lambda: self.work())
        self.refresh_build_number_button.clicked.connect(self.refresh_build_number)

        self.console_win = QtWidgets.QTextBrowser()
        self.grid2.addWidget(self.console_win,1,0,7,7)
        self.clear_logs_button = QPushButton('Clear', self)
        self.grid2.addWidget(self.clear_logs_button,8,6)

        self.help_win = QtWidgets.QTextBrowser()
        self.grid3.addWidget(self.help_win, 1, 0, 7, 7)

        self.clear_logs_button.clicked.connect(self.console_win.clear)
        self.browse_dc_vmx_button.clicked.connect(self.browse_dc_vmx_dialog)
        self.browse_am_vmx_button.clicked.connect(self.browse_am_vmx_dialog)
        self.browse_release_path_button.clicked.connect(self.browse_release_path_dialog)

        self._change_logcolour_signal.connect(self.change_logcolour)
        self._append_text_signal.connect(self.append_text)

def get_allconfig():
    global dc_vmx_path, am_vmx_path, release_path, snapshot_name, guest_login_name, guest_login_password
    global program_run_on_dc,script_run_on_dc,program_run_on_am,script_run_on_am
    global program_run_on_dc_imme,script_run_on_dc_imme,program_run_on_am_imme,script_run_on_am_imme,f
    dc_vmx_path = str(config_parser.get('config', 'dc_vmx_path'))
    am_vmx_path = str(config_parser.get('config', 'am_vmx_path'))
    release_path = config_parser.get('config', 'release_path')
    snapshot_name = config_parser.get('config', 'snapshot_name')
    guest_login_name = config_parser.get('config', 'guest_login_name')
    guest_login_password = config_parser.get('config', 'guest_login_password')
    program_run_on_dc  = config_parser.get('config', 'program_run_on_dc')
    script_run_on_dc  = config_parser.get('config', 'script_run_on_dc')
    program_run_on_am  = config_parser.get('config', 'program_run_on_am')
    script_run_on_am  = config_parser.get('config', 'script_run_on_am')
    program_run_on_dc_imme = config_parser.get('config', 'program_run_on_dc_imme')
    script_run_on_dc_imme = config_parser.get('config', 'script_run_on_dc_imme')
    program_run_on_am_imme = config_parser.get('config', 'program_run_on_am_imme')
    script_run_on_am_imme = config_parser.get('config', 'script_run_on_am_imme')
def get_release_package_dirs():
    global release_package_dirs
    release_path = config_parser.get('config', 'release_path')
    release_package_dirs = os.listdir(release_path)


if __name__ == '__main__':
    f = open(r'.\config\help.txt', "r")
    config_parser = configparser.ConfigParser()

    config_parser.read(r'.\config\myapp.conf')

    get_allconfig()
    get_release_package_dirs()
    host_os_files_path_for_dc = r".\vix\dc"
    host_os_files_path_for_am = r".\vix\am"
    guest_os_files_path = r"C:\vix"

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    GlobalLogging.getInstance().setLoggingToFile(r'./logs/log.txt')
    GlobalLogging.getInstance().setLoggingToQTextBrowserHanlder(main_window)
    GlobalLogging.getInstance().setLoggingLevel(logging.INFO)
    sys.exit(app.exec_())
