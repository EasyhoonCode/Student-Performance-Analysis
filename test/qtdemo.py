# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial

import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QPainter, QFont, QColor
from PySide6.QtWidgets import (QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget,QComboBox)
from PySide6.QtCharts import QChartView, QChart, QValueAxis, QSplineSeries

import sqlite3

class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items = 0

        # Left
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["班级", "课程", "均值","最大值","最小值","及格率"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.table2 = QTableWidget()
        self.table2.setColumnCount(7)
        self.table2.setHorizontalHeaderLabels(["学号", "姓名", "年龄", "班级", "课程a","课程b","课程c"])
        self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        

        # Chart
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Right
        self.quit = QPushButton("退出")
        self.plot = QPushButton("统计分析")
        self.combox = QComboBox()
        self.combox.addItems(["选择班级","一班","二班","三班"])

        self.right = QVBoxLayout()
        self.right.addWidget(self.combox)
        self.right.addWidget(self.plot)
        self.right.addWidget(self.chart_view)


        # QWidget Layout
        self.hlayout = QHBoxLayout() # 水平
        self.vlayout = QVBoxLayout() # 垂直

        #self.table_view.setSizePolicy(size)
        self.hlayout.addWidget(self.table)
        self.hlayout.addLayout(self.right)
        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addWidget(self.table2)
        self.vlayout.addWidget(self.quit)

        # Set the layout to the QWidget
        self.setLayout(self.vlayout)

        # Signals and Slots
        self.quit.clicked.connect(self.quit_application)
        self.plot.clicked.connect(self.plot_data)

        self.conn = sqlite3.connect(r"output\Student.db")
        # Fill example data
        self.fill_table2()
        self.fill_table()


    
    def fill_table(self):
        
        cur = self.conn.cursor()
        
        # 存放课程a、课程b、课程c的成绩分布值  
        clas_value_lis = []
  
        # 计算分布值
        for i in ["一班","二班","三班"]:
            for j in ["course_a","course_b","course_c"]:
                lis = []
                # 课程及格人数 fetchone:返回单条记录 没有结果返回None
                cur.execute(f"select count(*) from Student where classname = '{i}' and {j} >= 60")
                passnum = list(cur.fetchone())
                # 课程总人数
                cur.execute(f"select count(*) from Student where classname = '{i}'")
                total = list(cur.fetchone())
                # 及格率
                #passrate = round((int(passnum[0])/int(total[0])),2)
                
                cur.execute(f"select avg({j}), max({j}), min({j}) from Student where classname = '{i}'")
                
                lis.append(i)
                lis.append(j)
                # extend 将[]中的值添加进去 而不是添加一整个列表
                lis.extend([round(x,2) for x in list(cur.fetchone())])
                #lis.append(passrate)
                
                # 每个班 平均值、最大值、最小值、及格率 保留两位小数
                clas_value_lis.append(lis)
        
        # print(clas_value_lis)
        self.conn.commit()
        cur.close()
        self.conn.close()
        
        # 将数据添加到表格中
        rows = 0
        for j in clas_value_lis:
            clasitem = QTableWidgetItem(j[0])
            cositem = QTableWidgetItem(j[1])
            avg = QTableWidgetItem(f"{j[2]:.2f}")
            max = QTableWidgetItem(f"{j[3]:.2f}")
            min = QTableWidgetItem(f"{j[4]:.2f}")
            rate = QTableWidgetItem(f"{j[5]:.2f}")

            
            self.table.insertRow(rows)
            
            self.table.setItem(rows, 0,clasitem)
            self.table.setItem(rows, 1,cositem)
            self.table.setItem(rows, 2,avg)
            self.table.setItem(rows, 3, max)
            self.table.setItem(rows, 4, min)
            self.table.setItem(rows, 5, rate)
            rows += 1
            # print(j)
            
                
        return clas_value_lis
        
        
    
    @Slot()
    def plot_data(self):
        # Get table information
        chart = QChart()
        chart.setTitleFont(QFont("微软雅黑"))
        chart.setAnimationOptions(QChart.AllAnimations)
        
        if self.combox.currentIndex() == 0:   # 班级对比展示
            pass
        elif self.combox.currentIndex() == 1: # 一班
            chart.setTitle("一班学生成绩曲线图")
            temp = self.getData("一班")                         
        elif self.combox.currentIndex() == 2: # 二班
            chart.setTitle("二班学生成绩曲线图")
            temp = self.getData("二班")
        elif self.combox.currentIndex() == 3: # 三班
            chart.setTitle("三班学生成绩曲线图")
            temp = self.getData("三班")
            
        c_a = temp[0]
        c_b = temp[1]
        c_c = temp[2]
        

        # X轴 第n个学生
        axisX = QValueAxis()
        axisX.setRange(0,max(len(c_a),len(c_b),len(c_c))) # 设置X轴范围
        axisX.setLabelFormat("%d")
        axisX.setLabelsColor(QColor(0,0,0))
        # Y轴 分数
        axisY = QValueAxis()
        axisY.setRange(0,100)
        
        chart.addAxis(axisX,Qt.AlignBottom)
        chart.addAxis(axisY,Qt.AlignLeft)
        
        seri_a = QSplineSeries()
        seri_b = QSplineSeries()
        seri_c = QSplineSeries()
        seri_a.setName("课程a")
        seri_b.setName("课程b")
        seri_c.setName("课程c")


        # 添加曲线上的点 (x,y) x:第n个学生  y:第n个学生的分数
        for i in c_a:
            seri_a.append(i[0],i[1])
        for i in c_b:
            seri_b.append(i[0],i[1])
        for i in c_c:
            seri_c.append(i[0],i[1])

        # 将曲线显示出来
        seri_a.setVisible(True)
        seri_b.setVisible(True)
        seri_c.setVisible(True)
        
        chart.addSeries(seri_a)
        chart.addSeries(seri_b)
        chart.addSeries(seri_c)
        # 曲线与坐标轴对应
        seri_a.attachAxis(axisX)
        seri_a.attachAxis(axisY)
        seri_b.attachAxis(axisX)
        seri_b.attachAxis(axisY)
        seri_c.attachAxis(axisX)
        seri_c.attachAxis(axisY)
        self.chart_view.setChart(chart)
    
    def getData(self,clas_name:str):
        num = 0
        c_a = []
        c_b = []
        c_c = []
        for i in range(self.table2.rowCount()):
            if self.table2.item(i,3).text() == clas_name: # 按班级获取三门课程的数据
                score_a = float(self.table2.item(i,4).text())
                score_b = float(self.table2.item(i,5).text())
                score_c = float(self.table2.item(i,6).text())
                c_a.append([num,score_a])
                c_b.append([num,score_b])
                c_c.append([num,score_c])
                num += 1
        # print(c_a)
        # print(c_b)
        # print(c_c)
        return c_a,c_b,c_c

    @Slot()
    def quit_application(self):
        QApplication.quit()

    def fill_table2(self, data=None):
        cur = self.conn.cursor()
        cur.execute(f"select * from Student")
        # fetchall返回所有结果 二元元组
        studata = list(cur.fetchall())
        # print(studata)
        
        rows = 0
        for i in studata:
            # 数字需要 f"{i[0]}" 转字符
            sno = QTableWidgetItem(f"{i[0]}")
            name = QTableWidgetItem(i[1])
            age = QTableWidgetItem(f"{i[2]}")
            clasitem = QTableWidgetItem(i[3])
            course_a = QTableWidgetItem(f"{i[4]:.2f}")
            course_b = QTableWidgetItem(f"{i[5]:.2f}")
            course_c = QTableWidgetItem(f"{i[6]:.2f}")

            self.table2.insertRow(rows)
            
            self.table2.setItem(rows, 0,sno)
            self.table2.setItem(rows, 1,name)
            self.table2.setItem(rows, 2,age)
            self.table2.setItem(rows, 3, clasitem)
            self.table2.setItem(rows, 4, course_a)
            self.table2.setItem(rows, 5, course_b)
            self.table2.setItem(rows, 6, course_c)
            rows += 1
                
            




class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("学生成绩分析")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)
        self.setCentralWidget(widget)

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    widget = Widget()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    window.resize(1200, 800)
    window.show()

    # Execute application
    sys.exit(app.exec())