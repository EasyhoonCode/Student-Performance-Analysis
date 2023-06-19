# -*- coding: utf-8 -*-
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTabWidget, QWidget,QGraphicsDropShadowEffect,QMessageBox)
import sys
import login.login_res

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
                Form.setObjectName(u"Form")
        Form.resize(715, 551)
        Form.setWindowFlags(Qt.FramelessWindowHint)
        Form.setAttribute(Qt.WA_TranslucentBackground)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 40, 550, 500))
        self.background_label = QLabel(self.widget)
        self.background_label.setObjectName(u"background_label")
        self.background_label.setGeometry(QRect(30, 20, 280, 430))
        self.background_label.setStyleSheet(u"background-image: url(:/res/res/img/background1.png);\n"
"background-color:rgba(0,0,0,80);\n"
"border-top-left-radius:50px;")
        self.login_background_label = QLabel(self.widget)
        self.login_background_label.setObjectName(u"login_background_label")
        self.login_background_label.setGeometry(QRect(310, 20, 240, 430))
        self.login_background_label.setStyleSheet(u"background-color:rgba(255,255,255,255);\n"
"border-bottom-right-radius:50px;")
        self.login_headine_label = QLabel(self.widget)
        self.login_headine_label.setObjectName(u"login_headine_label")
        self.login_headine_label.setGeometry(QRect(330, 40, 211, 61))
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.login_headine_label.setFont(font)
        self.login_headine_label.setStyleSheet(u"color:rgba(0,0,0,200);")
        self.headine_label = QLabel(self.widget)
        self.headine_label.setObjectName(u"headine_label")
        self.headine_label.setGeometry(QRect(60, 60, 180, 40))
        font1 = QFont()
        font1.setPointSize(20)
        font1.setBold(True)
        self.headine_label.setFont(font1)
        self.headine_label.setStyleSheet(u"color:rgba(255,255,255,200);")
        self.middle_heading_label = QLabel(self.widget)
        self.middle_heading_label.setObjectName(u"middle_heading_label")
        self.middle_heading_label.setGeometry(QRect(60, 130, 231, 31))
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        self.middle_heading_label.setFont(font2)
        self.middle_heading_label.setStyleSheet(u"color:rgba(255,255,255,170);")
        self.close_bth = QPushButton(self.widget)
        self.close_bth.setObjectName(u"close_bth")
        self.close_bth.setGeometry(QRect(520, 20, 31, 31))
        self.close_bth.setStyleSheet(u"border:none;")
        icon = QIcon()
        icon.addFile(u":/res/res/icon/close-fill.png", QSize(), QIcon.Normal, QIcon.Off)
        self.close_bth.setIcon(icon)
        self.tabWidget = QTabWidget(self.widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(320, 110, 221, 251))
        self.tabWidget.setStyleSheet(u"font: 900 9pt \"Source Han Sans SC\";")
        self.Login = QWidget()
        self.Login.setObjectName(u"Login")
        self.password_line = QLineEdit(self.Login)
        self.password_line.setObjectName(u"password_line")
        self.password_line.setGeometry(QRect(10, 60, 201, 41))
        font3 = QFont()
        font3.setFamilies([u"Source Han Sans SC"])
        font3.setPointSize(9)
        font3.setBold(True)
        font3.setItalic(False)
        self.password_line.setFont(font3)
        self.password_line.setStyleSheet(u"background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:7px;\n"
"")
        self.password_line.setFrame(True)
        self.password_line.setEchoMode(QLineEdit.Normal)
        self.username_line = QLineEdit(self.Login)
        self.username_line.setObjectName(u"username_line")
        self.username_line.setGeometry(QRect(10, 10, 201, 41))
        self.username_line.setFont(font3)
        self.username_line.setStyleSheet(u"background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:7px;\n"
"")
        self.remember_checkBox = QCheckBox(self.Login)
        self.remember_checkBox.setObjectName(u"remember_checkBox")
        self.remember_checkBox.setGeometry(QRect(10, 110, 91, 20))
        self.remember_checkBox.setFont(font3)
        self.remember_checkBox.setStyleSheet(u"background-color:rgba(0,0,0,0);\n"
"color:rgba(0,0,0,240);")
        self.login_btn = QPushButton(self.Login)
        self.login_btn.setObjectName(u"login_btn")
        self.login_btn.setGeometry(QRect(30, 150, 161, 41))
        self.login_btn.setFont(font3)
        self.login_btn.setStyleSheet(u"QPushButton#login_btn{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
"color:rgba(255, 255, 255, 210);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#login_btn:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));\n"
"}\n"
"QPushButton#login_btn:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(150, 123, 111, 255);\n"
"}\n"
"\n"
"")
        self.tabWidget.addTab(self.Login, "")
        self.Signin = QWidget()
        self.Signin.setObjectName(u"Signin")
        self.sigin_password_line_3 = QLineEdit(self.Signin)
        self.sigin_password_line_3.setObjectName(u"sigin_password_line_3")
        self.sigin_password_line_3.setGeometry(QRect(10, 110, 201, 41))
        self.sigin_password_line_3.setFont(font3)
        self.sigin_password_line_3.setStyleSheet(u"background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:7px;\n"
"")
        self.sigin_password_line_3.setFrame(True)
        self.sigin_password_line_3.setEchoMode(QLineEdit.Normal)
        self.sigin_password_line_2 = QLineEdit(self.Signin)
        self.sigin_password_line_2.setObjectName(u"sigin_password_line_2")
        self.sigin_password_line_2.setGeometry(QRect(10, 60, 201, 41))
        self.sigin_password_line_2.setFont(font3)
        self.sigin_password_line_2.setStyleSheet(u"background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:7px;\n"
"")
        self.sigin_password_line_2.setFrame(True)
        self.sigin_password_line_2.setEchoMode(QLineEdit.Normal)
        self.sigin_username_line = QLineEdit(self.Signin)
        self.sigin_username_line.setObjectName(u"sigin_username_line")
        self.sigin_username_line.setGeometry(QRect(10, 10, 201, 41))
        self.sigin_username_line.setFont(font3)
        self.sigin_username_line.setStyleSheet(u"background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:7px;\n"
"")
        self.sigin_btn = QPushButton(self.Signin)
        self.sigin_btn.setObjectName(u"sigin_btn")
        self.sigin_btn.setGeometry(QRect(30, 170, 161, 41))
        self.sigin_btn.setFont(font3)
        self.sigin_btn.setStyleSheet(u"QPushButton#sigin_btn{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
"color:rgba(255, 255, 255, 210);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#sigin_btn:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));\n"
"}\n"
"QPushButton#sigin_btn:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(150, 123, 111, 255);\n"
"}\n"
"\n"
"")
        self.tabWidget.addTab(self.Signin, "")
        QWidget.setTabOrder(self.username_line, self.password_line)
        QWidget.setTabOrder(self.password_line, self.login_btn)
        QWidget.setTabOrder(self.login_btn, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.sigin_username_line)
        QWidget.setTabOrder(self.sigin_username_line, self.sigin_password_line_2)
        QWidget.setTabOrder(self.sigin_password_line_2, self.sigin_password_line_3)
        QWidget.setTabOrder(self.sigin_password_line_3, self.sigin_btn)
        QWidget.setTabOrder(self.sigin_btn, self.remember_checkBox)
        QWidget.setTabOrder(self.remember_checkBox, self.close_bth)

        self.retranslateUi(Form)
        self.close_bth.clicked.connect(Form.close)

        self.tabWidget.setCurrentIndex(1)
        self.middle_heading_label.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.headine_label.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.login_btn.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=40, xOffset=6, yOffset=6))
        self.sigin_btn.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=40, xOffset=6, yOffset=6))


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.background_label.setText("")
        self.login_background_label.setText("")
        self.login_headine_label.setText(QCoreApplication.translate("Form", u"Dream Initiated", None))
        self.headine_label.setText(QCoreApplication.translate("Form", u"\u4f60\u597d\uff0c\u540c\u5b66\u3002", None))
        self.middle_heading_label.setText(QCoreApplication.translate("Form", u"\u6b22\u8fce\u8fdb\u5165\u5b66\u751f\u6210\u7ee9\u7ba1\u7406\u7cfb\u7edf", None))
        self.close_bth.setText("")
        self.password_line.setText("")
        self.password_line.setPlaceholderText(QCoreApplication.translate("Form", u"Password", None))
        self.username_line.setText("")
        self.username_line.setPlaceholderText(QCoreApplication.translate("Form", u"User Name", None))
        self.remember_checkBox.setText(QCoreApplication.translate("Form", u"Remember", None))
        self.login_btn.setText(QCoreApplication.translate("Form", u"Log In", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Login), QCoreApplication.translate("Form", u"Login", None))
        self.sigin_password_line_3.setText("")
        self.sigin_password_line_3.setPlaceholderText(QCoreApplication.translate("Form", u"Please confirm the Password", None))
        self.sigin_password_line_2.setText("")
        self.sigin_password_line_2.setPlaceholderText(QCoreApplication.translate("Form", u"Please enter your Password", None))
        self.sigin_username_line.setText("")
        self.sigin_username_line.setPlaceholderText(QCoreApplication.translate("Form", u"Please enter User Name", None))
        self.sigin_btn.setText(QCoreApplication.translate("Form", u"Sign in", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Signin), QCoreApplication.translate("Form", u"Sign in", None))
    # retranslateUi


