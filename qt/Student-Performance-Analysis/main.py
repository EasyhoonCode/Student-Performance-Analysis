import random
import sys
from PySide6 import *
from PySide6.QtWidgets import QSizePolicy,QApplication,QDialog,QVBoxLayout,QLineEdit,QHBoxLayout,QPushButton,QMessageBox
from PySide6.QtCore import *
from mainwindow import MainWindow
from PySide6.QtGui import QScreen
from PySide6.QtUiTools import QUiLoader
import login.login_res
import requests

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        loader = QUiLoader()
        ui_file = QFile('qt\Student-Performance-Analysis\login\login_2.ui')
        ui_file.open(QFile.ReadOnly)
        self.dialog = loader.load(ui_file, self)
        ui_file.close()
        # 隐藏边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.login_btn = self.dialog.findChild(QPushButton, 'login_btn')
        self.username_edit = self.dialog.findChild(QLineEdit, 'username_line')
        self.password_edit = self.dialog.findChild(QLineEdit, 'password_line')
        self.sigin_username_edit = self.dialog.findChild(QLineEdit, 'sigin_username_line')
        self.sigin_password_edit = self.dialog.findChild(QLineEdit, 'sigin_password_line_2')
        self.sigin_once_password_edit = self.dialog.findChild(QLineEdit, 'sigin_password_line_3')
        self.sigin_btn = self.dialog.findChild(QPushButton, 'sigin_btn')
        self.close_bth = self.dialog.findChild(QPushButton, 'close_bth')
        self.login_btn.clicked.connect(self.handle_login)
        self.close_bth.clicked.connect(self.handle_close)
        self.sigin_btn.clicked.connect(self.handle_signup)


    def handle_close(self):
        # 处理窗口关闭事件
        self.close()

    def handle_login(self):
        # 获取用户名和密码
        username = self.username_edit.text()
        password = self.password_edit.text()

        # 调用登录接口
        response = requests.post("http://127.0.0.1:8000/login", json={"username": username, "password": password})

        if response.status_code == 200:
            # 登录成功，弹出提示框
            name = response.json()["data"]["username"]
            QMessageBox.information(self, '登录成功！', '欢迎回来, {}'.format(name))

            # 跳转到主窗口界面
            main_window = MainWindow()
            main_window.show()
            self.accept()

        else:
            # 登录失败，弹出错误提示框
            error_message = response.json()["detail"]
            QMessageBox.warning(self, '登录失败！', error_message)

    def handle_signup(self):
        # 获取用户名和密码
        username = self.sigin_username_edit.text()
        password = self.sigin_password_edit.text()
        once_password = self.sigin_once_password_edit.text()

        # 调用注册接口
        response = requests.post(
            "http://localhost:8000/signin",
            json={"username": username, "password": password, "once_password": once_password}
        )

        # 检查响应JSON中是否有名为"data"的键
        if response.status_code == 200:
            QMessageBox.information(self, '注册成功！', '欢迎, {}'.format(username))
            main_window = MainWindow()
            main_window.show()
            self.accept()

        # 如果没有，则显示错误消息
        else:
            error_message = response.json()["detail"]
            QMessageBox.warning(self, "注册失败！", error_message)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建登录对话框
    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.Accepted:
        # 如果登录成功，显示主窗口
        main_window = MainWindow()
        main_window.resize(1500,800)
        main_window.show()

    #window.resize(1400,1000)
        # 将主窗口移到屏幕中央
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = main_window.frameGeometry()
        geo.moveCenter(center)
        main_window.move(geo.topLeft())
    
        sys.exit(app.exec())
