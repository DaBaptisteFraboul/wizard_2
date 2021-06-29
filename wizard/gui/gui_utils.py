# coding: utf-8
# Author: Leo BRUNEL
# Contact: contact@leobrunel.com

# Python modules
from PyQt5 import QtWidgets, QtCore, QtGui

def move_ui(widget):
    desktop = QtWidgets.QApplication.desktop()
    screenRect = desktop.screenGeometry()

    screen_minX = screenRect.topLeft().x()
    screen_minY = screenRect.topLeft().y()
    screen_maxX = screenRect.bottomRight().x()
    screen_maxY = screenRect.bottomRight().y()
    cursor_x = QtGui.QCursor.pos().x()
    cursor_y = QtGui.QCursor.pos().y()
    win_width = widget.frameSize().width()
    win_heigth = widget.frameSize().height()

    if (cursor_y - 20 - win_heigth) <= screen_minY:
        posy = cursor_y - 10
        angley = 'top'
    else:
        posy = cursor_y - win_heigth + 10
        angley = 'bottom'
    if (cursor_x + 20 + win_width) >= screen_maxX:
        posx = cursor_x - win_width + 10
        anglex = 'right'
    else:
        posx = cursor_x - 10
        anglex = 'left'

    widget.move(posx, posy)
    return f"{angley}-{anglex}"

class password_lineEdit(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(password_lineEdit, self).__init__(parent)
        self.build_ui()
        self.connect_functions()
        self.toggle_password_visibility()

    def build_ui(self):
        self.setObjectName('password_lineEdit_frame')
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(0,0,10,0)

        self.setLayout(self.main_layout)

        self.password_lineEdit = QtWidgets.QLineEdit()
        self.main_layout.addWidget(self.password_lineEdit)

        self.toggle_visibility_button = QtWidgets.QPushButton()
        self.toggle_visibility_button.setObjectName('password_visibility_button')
        self.toggle_visibility_button.setCheckable(True)
        self.toggle_visibility_button.setFixedSize(16,16)
        self.main_layout.addWidget(self.toggle_visibility_button)

    def connect_functions(self):
        self.toggle_visibility_button.clicked.connect(self.toggle_password_visibility)

    def toggle_password_visibility(self):
        if not self.toggle_visibility_button.isChecked():
            self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        else:
            self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)

    def text(self):
        return self.password_lineEdit.text()

    def setPlaceholderText(self, placeholderText):
        self.password_lineEdit.setPlaceholderText(placeholderText)


