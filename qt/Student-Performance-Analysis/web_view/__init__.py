import random
import sys
import os
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

 
class Web_view(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout_QV_group = QGroupBox()
        self.layout_QV = QVBoxLayout()
        # 添加动图窗口
        self.gif_label = QLabel(self)
        self.web_label = QLabel(self)
        self.movie = QMovie("qt\Student-Performance-Analysis\leftmenu\pic\cat.gif")
        self.gif_label.setMovie(self.movie)
        self.movie.start()
        self.web_label.setText("<a href='http://127.0.0.1:8000/docs' style='text-decoration:none; color:white'>点我进入Web后台OvO</a>")
        self.web_label.setOpenExternalLinks(True)
        self.web_label.setStyleSheet("font-size:25px")
        self.web_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 将动图窗口添加到布局中
        self.layout_QV.addWidget(self.gif_label)
        self.layout_QV.addWidget(self.web_label)
        self.layout_QV.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_QV_group.setLayout(self.layout_QV)
