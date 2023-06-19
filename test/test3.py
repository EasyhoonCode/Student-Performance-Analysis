import requests
from PySide6 import QtWidgets

class RegisterDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建用户名、密码和确认密码输入框
        self.username_edit = QtWidgets.QLineEdit()
        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.once_password_edit = QtWidgets.QLineEdit()
        self.once_password_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        # 创建注册按钮
        self.register_button = QtWidgets.QPushButton("注册")
        self.register_button.clicked.connect(self.handle_register)

        # 创建布局并添加控件
        layout = QtWidgets.QFormLayout()
        layout.addRow("用户名:", self.username_edit)
        layout.addRow("密码:", self.password_edit)
        layout.addRow("确认密码:", self.once_password_edit)
        layout.addRow(self.register_button)
        self.setLayout(layout)

    def handle_register(self):
        # 获取用户名和密码
        username = self.username_edit.text()
        password = self.password_edit.text()
        once_password = self.once_password_edit.text()

        # 调用注册接口
        response = requests.post(
            "http://localhost:8000/signin",
            json={"username": username, "password": password, "once_password": once_password}
        )

        # 检查响应JSON中是否有名为"data"的键
        if "data" in response.json():
            name = response.json()["data"]["username"]
            QtWidgets.QMessageBox.information(self, "注册成功！", f"欢迎加入, {name}")
            self.accept()

        # 如果没有，则显示错误消息
        else:
            error_message = response.json()["detail"]
            QtWidgets.QMessageBox.warning(self, "注册失败！", error_message)


# 在 main 函数中创建一个应用并显示 RegisterDialog 对话框
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    dialog = RegisterDialog()
    dialog.exec_()
