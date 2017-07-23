from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import * #要使用quit首先要调用QCoreApplication
import time,os,configparser,sys
from datetime import datetime
from vix import VixHost, VixError, VixJob, VixVM

class Exp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def prepare_environment(self):
        try:
            f = open("./logs/log.txt", 'w+')

            # dc_vmx_path = r'D:\Virtual Machines\AM\EX 2010\ITF_Single_Exch2K10_DC\ITF_Single_Exch2K10_DC.vmx'
            # am_vmx_path = r'D:\Virtual Machines\AM\EX 2010\ITF_Single_Exch2K10_AM\ITF_Single_Exch2K10_AM.vmx'
            # release_path = r"\\10.30.150.149\buildoutput\Website\release"
            cp = configparser.RawConfigParser()

            cp.read(r'.\config\myapp.conf')

            dc_vmx_path = str(cp.get('config', 'dc_vmx_path'))
            print("dc_vmx_path:%s" % (dc_vmx_path))

            am_vmx_path = str(cp.get('config', 'am_vmx_path'))
            print("dc_vmx_path:%s" % (am_vmx_path))

            release_path = cp.get('config', 'release_path')
            print("release_path:%s" % (release_path))

            snapshot_name = cp.get('config', 'snapshot')
            print("snapshot_name:%s" % (snapshot_name))

            release_package_dirs = os.listdir(release_path)

            host_os_files_path_for_dc = r".\vix\dc"
            host_os_files_path_for_am = r".\vix\am"
            guest_os_files_path = r"C:\vix"

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
            vm_dc.login("dc2k8\\administrator", "Pa$$word", require_interactive=True)
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
            vm_am.login("dc2k8\\administrator", "Pa$$word", require_interactive=True)
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

        except VixError as ex:
            print(str(datetime.now()) + " VixError,Operatation failed: {0}".format(ex), file=f)
        except IOError as ex:
            print(str(datetime.now()) + " IOError,Operatation failed: {0}".format(ex), file=f)
        except Exception as ex:
            print(str(datetime.now()) + " Exception,Operatation failed: {0}".format(ex), file=f)
            print(str(datetime.now()) + " " + ex.__traceback__, file=f)
        finally:
            f.close()
            _vm_host.disconnect()
    def initUI(self):

        #创建一个按钮，qtn是QPushButton类的一个实例，QPushButton的第一个参数是按钮上的文字，第二个参数指明这个按钮的父部件，在这里是Exp
        qtn = QPushButton('Run', self)
        qtn.resize(qtn.sizeHint())

        # Qt 也好，Pyqt 也好，处理事件的核心机制都是信号槽。当我们按下这个按钮时，就释放了clicked这个信号，
        # 槽可以是 Qt 或者 Python（只要能调用就行）。QCoreApplication包含了主要的事件循环，它可以处理传递任何事件。
        # clicked信号连接了quit这个方法，从而结束进程。
        # 整个过程由两个对象完成，发射器和接收器，按钮是发射器，这个应用是接收器。
        qtn.clicked.connect(self.prepare_environment)
        qtn.move(10, 10)

        self.setWindowIcon(QIcon('.\images\logo.png'))
        self.resize(300, 50)

        self.setWindowTitle('ArchiveManager Auto App')
        self.show()

if __name__ == '__main__':
    f=0
    threads=None
    release_path=0
    release_package_dirs=0
    host_os_files_path_for_am=0
    app = QApplication(sys.argv)
    ex = Exp()
    sys.exit(app.exec_())