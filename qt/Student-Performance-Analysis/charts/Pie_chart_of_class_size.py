import enum
import random
import sys
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
import tablewid
import json

class Pie_chart_of_class_size(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout_group = QGroupBox()
        self.layout_QH = QHBoxLayout()
        self.layout_QH.setContentsMargins(0, 0, 0, 0)

        # 加载数据
        with open('output\students.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 统计每个班级的人数
        class_counts = {}
        for student in data['students']:
            class_name = student['classname']
            if class_name in class_counts:
                class_counts[class_name] += 1
            else:
                class_counts[class_name] = 1

        # 创建 QPieSeries 对象
        series = QPieSeries()
        for class_name, count in class_counts.items():
            series.append(class_name + " " + str(count) + "人", count)

        # 创建 QChart 对象，并添加 QPieSeries 对象
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.chart.addSeries(series)
        series.setLabelsVisible(True)
        self.chart.setTitle('各班级人数统计')
        self.chart_view = QChartView(self.chart)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        # 设置图例和布局
        self.chart.legend().setVisible(True)
        self.layout_QH.addWidget(self.chart_view)
        self.layout_group.setLayout(self.layout_QH)
