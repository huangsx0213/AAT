from PyQt5.QtWidgets import QGroupBox


class CustomGroupBox(QGroupBox):
    def __init__(self, str=None):
        super().__init__(str)
        self.setCheckable(True)
        self.setStyleSheet("QGroupBox::indicator { width: 22px; height:22px;}"
                           "QGroupBox::indicator:unchecked { image: url(./images/expand.png);}"
                           "QGroupBox::indicator:checked { image: url(./images/collapse.png);}")
        self.toggled.connect(
            lambda: self.toggleGroup(self))

    def toggleGroup(self, ctrl):
        state = ctrl.isChecked()
        if state:
            ctrl.setFixedHeight(self.h)
            ctrl.setFlat(False)
        else:
            self.h = ctrl.height()
            #print(self.h)
            ctrl.setFixedHeight(15)
            ctrl.setFlat(True)