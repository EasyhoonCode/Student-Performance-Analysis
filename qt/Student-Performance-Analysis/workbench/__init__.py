import random
import sys
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from charts.Pie_chart_of_class_size import Pie_chart_of_class_size
from charts.linechart import Linechart
from charts.piechart import Piechart
from charts.grade_barchart import grade_barchart



class Workbench(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout_QV_group = QGroupBox()
        self.layout_QH = QGridLayout()
        
        self.layout_QH.addWidget(Pie_chart_of_class_size().layout_group,1,2)
        self.layout_QH.addWidget(Linechart().layout_group,1,1)
        self.layout_QH.addWidget(Piechart().layout_group,3,1)
        self.layout_QH.addWidget(grade_barchart().layout_group,3,2)

        
        self.layout_QV_group.setLayout(self.layout_QH)