import random
import sys
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
 
 
class Bottombar(QWidget):
    def __init__(self):
        super().__init__()
        
        
        #顶部导航栏
        self.bottombar_group = QGroupBox("")
        self.bottombar_group.setFixedHeight(50)
        self.bottombar_group.setStyleSheet("background-color:rgba(31,29,27,82);border-radius:10px;")
        self.bottombar_layout = QHBoxLayout()


        #导航栏标签
        #self.bottombardesc = bottombardesc("By Easyhoon(ZhongKaiwei) 小组成员:钟凯威、吴榕辉、曾铨葳、刘伟晗、蓝鼎、陈泳君、林浩明、黄志鑫")
        self.bottombardesc = bottombardesc("By Easyhoon(ZhongKaiwei)")
        self.bottombar_layout.addWidget(self.bottombardesc)
        self.bottombar_layout.addStretch()

        #导航栏右侧用户设置
        self.bottombarversion = bottombardesc("Version 1.0.0")
        self.bottombar_layout.addWidget(self.bottombarversion)
        
        
        self.bottombar_group.setLayout(self.bottombar_layout)


class bottombardesc(QLabel):
    def __init__(self,arg):
        super().__init__()
        self.setText(arg)
        self.setStyleSheet("color:rgb(255,255,255);")