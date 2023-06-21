import enum
import random
import sys
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
import json

class Piechart(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout_group = QGroupBox()
        self.layout_QH = QHBoxLayout()
        self.layout_QH.setContentsMargins(0,0,0,0)
        with open('output\students.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        class_names = list(set([student['classname'] for student in data['students']]))
        class_pass_counts = [0] * len(class_names)
        class_total_counts = [0] * len(class_names)
        # 在这里初始化 QPieSeries
        series = QPieSeries()
        for i, class_name in enumerate(class_names):
            for student in data['students']:
                if student['classname'] == class_name:
                    class_total_counts[i] += 1
                    if student['passing_rate'] == '及格':
                        class_pass_counts[i] += 1

            pass_rate = class_pass_counts[i] / class_total_counts[i]
            series.append(f'{class_name} ({pass_rate:.0%})', class_pass_counts[i])
            series.setLabelsVisible(True)

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)
        # 在它被初始化后添加系列到图表中
        self.chart.addSeries(series)
        self.chart.createDefaultAxes()
        self.chart.setTitle('各班级平均分及格率对比')
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart_view = QChartView()
        self.chart_view.setChart(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.layout_QH.addWidget(self.chart_view)
        self.layout_group.setLayout(self.layout_QH)