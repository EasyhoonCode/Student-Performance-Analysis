import enum
import random
import sys
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtCharts import *
import sqlite3
#import charts.data as static
import json
from PySide6.QtCharts import QChartView, QPieSeries, QChart,QValueAxis,QLineSeries,QVXYModelMapper,QChart, QChartView, QBarSet, QBarSeries, QValueAxis
from PySide6 import QtWidgets,QtCharts,QtCore
import csv



class grade_barchart(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout_group = QGroupBox()
        self.layout_QH = QHBoxLayout()
        self.layout_QH.setContentsMargins(0,0,0,0)

        # 连接到 SQLite 数据库
        conn = sqlite3.connect('output\students.db')
        cur = conn.cursor()
        # 从数据库中获取数据
        cur.execute('SELECT classname, MAX(course_a), MIN(course_a), MAX(course_b), MIN(course_b), MAX(course_c), MIN(course_c) FROM students GROUP BY classname')
        data = cur.fetchall()
        # 创建一个包含三个班级的字典
        class_scores = {'2005班': [], '2007班': [], '2008班': [],'2009班': []}
        # 遍历数据，并将每个班级的最高分和最低分添加到对应的列表中
        for row in data:
            class_name = row[0]
            max_course_a = row[1]
            min_course_a = row[2]
            max_course_b = row[3]
            min_course_b = row[4]
            max_course_c = row[5]
            min_course_c = row[6]

            class_scores[class_name].append(max_course_a)
            class_scores[class_name].append(min_course_a)
            class_scores[class_name].append(max_course_b)
            class_scores[class_name].append(min_course_b)
            class_scores[class_name].append(max_course_c)
            class_scores[class_name].append(min_course_c)

        # 创建一个 QBarSeries 对象来表示三个班级的成绩数据
        series = QBarSeries()
        # 遍历每个班级的成绩，并将最高分和最低分添加到对应的 QBarSet 对象中
        for class_name, scores in class_scores.items():
            bar_set = QBarSet(class_name)
            bar_set.append(scores[0])
            bar_set.append(scores[1])
            bar_set.append(scores[2])
            bar_set.append(scores[3])
            bar_set.append(scores[4])
            bar_set.append(scores[5])
            series.append(bar_set)

        # 创建一个 QChart 对象并将 QBarSeries 添加到其中
        chart = QChart()
        chart.addSeries(series)
        axis_x = QBarCategoryAxis()
        axis_y = QBarCategoryAxis()
        # 设置图表标题和轴标签
        chart.setTitle('班级各科成绩最大值最小值统计')
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setAnimationDuration(1000)
        chart.createDefaultAxes()
        axis_x = chart.axisX() # 获取对x轴的引用
        axis_x.setCategories(["A最大值", "A最小值", "B最大值", "B最小值", "C最大值", "C最小值"])

        chart.axisY().setTitleText('分数')
        chart.axisY().setRange(0,100)
        series.setLabelsVisible(True)

        # 创建一个 QChartView 对象并将 QChart 添加到其中
        chart_view = QChartView()
        chart_view.setChart(chart)
        self.layout_QH.addWidget(chart_view)
        self.layout_group.setLayout(self.layout_QH)


        # 关闭数据库连接
        conn.close()













