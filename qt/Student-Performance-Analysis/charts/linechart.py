import enum
import random
import sys
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
import sqlite3
import json

class Linechart(QWidget):
    def __init__(self):
        super().__init__()

        self.layout_group = QGroupBox()
        self.layout_QH = QHBoxLayout()
        self.layout_QH.setContentsMargins(0,0,0,0)
        # 班级分数折线图的各项设置
        # Initialize empty series
        course_a_series = []
        course_b_series = []
        course_c_series = []
        course_a_series = QLineSeries()  
        course_b_series = QLineSeries()  
        course_c_series = QLineSeries()  
        course_a_series.setName("课程A")
        course_b_series.setName("课程B")
        course_c_series.setName("课程C")
        course_a_series.setPointsVisible(True)
        course_b_series.setPointsVisible(True)
        course_c_series.setPointsVisible(True)

        # 解析json数据并将其添加到折线图中
        with open('output\students.json', 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
        for i, student in enumerate(data['students']):
            x = i
            cou_a_point = QPointF(x, student['course_a'])
            course_a_series.append(cou_a_point)
            cou_b_point = QPointF(x, student['course_b'])
            course_b_series.append(cou_b_point)
            cou_c_point = QPointF(x, student['course_c'])
            course_c_series.append(cou_c_point)

        # 设置折线图的属性和轴
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)

        self.chart.addSeries(course_a_series)
        self.chart.addSeries(course_b_series)
        self.chart.addSeries(course_c_series)
        self.chart.legend().show()

        axisX = QValueAxis()
        axisX.setRange(0, len(data['students'])-1)
        axisX.setTitleText("总人数")
        axisX.setLabelFormat("%d")
        self.chart.addAxis(axisX, Qt.AlignBottom)
        course_a_series.attachAxis(axisX)
        course_b_series.attachAxis(axisX)
        course_c_series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setRange(0, 100)
        axisY.setTitleText("分数")
        self.chart.addAxis(axisY, Qt.AlignLeft)
        self.chart.setMinimumSize(600,400)
        course_a_series.attachAxis(axisY)
        course_b_series.attachAxis(axisY)
        course_c_series.attachAxis(axisY)


        # 创建一个 QChartView 对象并将 QChart 添加到其中
        chart_view = QChartView()
        chart_view.setChart(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.layout_QH.addWidget(chart_view)
        self.layout_group.setLayout(self.layout_QH)

