# NOTE:第十二周作业 PYQT实现学生成绩客户端
import sys
from PySide6.QtCore import Qt, Slot,QSortFilterProxyModel,QRegularExpression,QPointF
from PySide6 import QtWidgets,QtCharts,QtCore
from PySide6.QtGui import QAction, QPainter,QIcon,QRegularExpressionValidator,QStandardItem,QStandardItemModel,QPen,QBrush,QFont,QColor
from PySide6.QtWidgets import (QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,QVBoxLayout, QWidget,QAbstractItemView,QGraphicsSimpleTextItem, QComboBox)
from PySide6.QtCharts import QChartView, QPieSeries, QChart,QValueAxis,QLineSeries,QSplineSeries,QVXYModelMapper
from qt_material import apply_stylesheet 
import json
import sqlite3
class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items = 0

        # 左侧界面
        self.table_1 = QTableWidget()
        self.table_1.setColumnCount(6)
        self.table_1.setHorizontalHeaderLabels(["班级","课程","平均分","最大值","最小值","及格率"])
        self.table_1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #随着窗口大小的变化而自动调整宽度
        
        self.table_2 =QTableWidget()
        self.table_2.setColumnCount(7)
        self.table_2.setHorizontalHeaderLabels(["班级", "学号", "姓名", "年龄", "课程a","课程b","课程c"])
        self.table_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 搜索框
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("我是搜索框QAQ")
        self.search_box.setStyleSheet("color:white")
        search_layout.addWidget(self.search_box)

        #下拉列表
        self.combo_box = QComboBox(self)

        with open("output\students.json","r", encoding='utf-8') as f:
            data = json.load(f)

            # 获取所有班级
            classes = set([item["classname"] for item in data["students"]])
            
            # 将班级添加到下拉列表中
            self.combo_box.addItem("全部班级")
            self.combo_box.setStyleSheet("color:white")
            for c in sorted(classes):
                self.combo_box.addItem(c)
        
        
        # 显示图表的视图的渲染属性
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # 右侧界面 按钮的名称
        self.clear = QPushButton("清空数据")
        self.quit = QPushButton("退出")
        self.plot = QPushButton("生成分数曲线图")
        self.pass_plot = QPushButton("生成班级及格率饼图")
        self.GeneratedData = QPushButton("生成班级成绩数据分析")
        self.stu_mark = QPushButton("生成学生成绩")

        self.right = QVBoxLayout()  #右侧界面水平排序
        # 右侧界面 按钮位置 
        self.right.addWidget(QLabel("选择班级:"))
        self.right.addWidget(self.combo_box)
        self.right.addWidget(self.search_box)
        self.right.addWidget(self.stu_mark)
        self.right.addWidget(self.plot)
        self.right.addWidget(self.chart_view)
        self.right.addWidget(self.GeneratedData)
        self.right.addWidget(self.pass_plot)
        self.right.addWidget(self.clear)
        self.right.addWidget(self.quit)

        """
        NOTE:
        这段代码定义了一个水平布局 QHBoxLayout，并向其中添加了两个子部件，一个是名为 self.table 的表格视图，
        另一个是右侧布局 self.right。添加的顺序是先添加表格视图，再添加右侧布局。这样，在界面上呈现出来时，
        这两个子控件将会并排排列在一起，按照从左到右的顺序显示。
        """
        self.left = QVBoxLayout()
        self.left.addWidget(self.table_2)
        self.left.addWidget(self.table_1)

        # QWidget Layout
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.left)
        self.layout.addLayout(self.right)
        self.setLayout(self.layout)

        # 信号槽功能
        self.GeneratedData.clicked.connect(self.handle_button_click_2)  #生成数据
        self.quit.clicked.connect(self.quit_application) #退出
        self.plot.clicked.connect(self.plot_data) #生成分数曲线图
        self.pass_plot.clicked.connect(self.plot_pass_data) #生成及格饼图
        self.clear.clicked.connect(self.clear_table) #清空数据
        self.search_box.textChanged.connect(self.on_filter_text_changed) #搜索框
        self.combo_box.currentIndexChanged.connect(self.update_display) #下拉列表
        self.stu_mark.clicked.connect(self.handle_button_click) #学生成绩


    @Slot()
    def handle_button_click(self):
        #self.GeneratedData.setEnabled(False) #TAG:这个功能是限制生成数据按钮的点击次数，只要点击一次，按钮就会变黑，看需求是否加入现在的布局
        self.fill_table()

    def handle_button_click_2(self):
        #self.GeneratedData.setEnabled(False) #TAG:这个功能是限制生成数据按钮的点击次数，只要点击一次，按钮就会变黑，看需求是否加入现在的布局
        self.stu_mark_data()

    @Slot()
    def plot_data(self, class_name):
        # Get table information

        # 班级分数折线图的各项设置
        course_a_series = QLineSeries()  # 平均分线
        course_b_series = QLineSeries()  # 最高分线
        course_c_series = QLineSeries()  # 最低分线
        course_a_series.setName("课程A")
        course_b_series.setName("课程B")
        course_c_series.setName("课程C")
        course_a_series.setPointsVisible(True)
        course_b_series.setPointsVisible(True)
        course_c_series.setPointsVisible(True)

        # 解析数据并将其添加到折线图中
        course_a = [float(self.table_2.item(i, 4).text()) for i in range(self.table_2.rowCount())]
        course_b = [float(self.table_2.item(i, 5).text()) for i in range(self.table_2.rowCount())]
        course_c = [float(self.table_2.item(i, 6).text()) for i in range(self.table_2.rowCount())]
        for i in range(self.table_2.rowCount()):
            x = i
            cou_a_point = QPointF(x, course_a[i])
            course_a_series.append(cou_a_point)
            cou_b_point = QPointF(x, course_b[i])
            course_b_series.append(cou_b_point)
            cou_c_point = QPointF(x, course_c[i])
            course_c_series.append(cou_c_point)

        # 设置折线图的属性和轴
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)

        self.chart.addSeries(course_a_series)
        self.chart.addSeries(course_b_series)
        self.chart.addSeries(course_c_series)
        self.chart.legend().show()
        if class_name:
            self.chart.setTitle(f"{class_name} 分数曲线图")
        else:
            # 设置默认的标题
            self.chart.setTitle("分数曲线图")

        axisX = QValueAxis()
        axisX.setRange(0, self.table_2.rowCount()-1)
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

        self.chart_view.visibleRegion
        self.chart_view.setChart(self.chart) 

        
    @Slot() #退出
    def quit_application(self):
        QApplication.quit()

    #XXX:重要代码,读取json数据，json数据添加到表格中
    def fill_table(self, classname=None):
        if self.table_2.rowCount()>0:
            self.table_2.clearContents()
            self.table_2.setRowCount(0)

        self.items = 0 # 初始化为0
        with open("output\students.json","r", encoding='utf-8') as f:
            data = json.load(f)

            if classname is None:
                classnames = set(item["classname"] for item in data["students"])

                for classname in sorted(classnames):
                    for item in data["students"]:
                        if item["classname"] == classname:
                            stu_id = item["id"]
                            name = item["name"]
                            age = item["age"]
                            course_a = item["course_a"]
                            course_b = item["course_b"]
                            course_c = item["course_c"]

                            classname_item = QTableWidgetItem(classname)
                            classname_item.setTextAlignment(Qt.AlignCenter)

                            stu_id_item = QTableWidgetItem(f"{stu_id:.0f}")
                            stu_id_item.setTextAlignment(Qt.AlignCenter)

                            name_item = QTableWidgetItem(name)
                            name_item.setTextAlignment(Qt.AlignCenter)

                            age_item = QTableWidgetItem(f"{age:.0f}")
                            age_item.setTextAlignment(Qt.AlignCenter)

                            course_a_item = QTableWidgetItem(f"{course_a:.0f}")
                            course_a_item.setTextAlignment(Qt.AlignCenter)

                            course_b_item = QTableWidgetItem(f"{course_b:.0f}")
                            course_b_item.setTextAlignment(Qt.AlignCenter)

                            course_c_item = QTableWidgetItem(f"{course_c:.0f}")
                            course_c_item.setTextAlignment(Qt.AlignCenter)


                            row_position = self.table_2.rowCount()
                            self.table_2.insertRow(row_position)
                            self.table_2.setItem(self.items, 0, classname_item)
                            self.table_2.setItem(self.items, 1, stu_id_item)
                            self.table_2.setItem(self.items, 2, name_item)
                            self.table_2.setItem(self.items, 3, age_item)
                            self.table_2.setItem(self.items, 4, course_a_item)
                            self.table_2.setItem(self.items, 5, course_b_item)
                            self.table_2.setItem(self.items, 6, course_c_item)

                            self.items += 1
                            self.table_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
            else:
                for item in data["students"]:
                    if item["classname"] == classname:
                        stu_id = item["id"]
                        name = item["name"]
                        age = item["age"]
                        course_a = item["course_a"]
                        course_b = item["course_b"]
                        course_c = item["course_c"]

                        classname_item = QTableWidgetItem(classname)
                        classname_item.setTextAlignment(Qt.AlignCenter)

                        stu_id_item = QTableWidgetItem(f"{stu_id:.0f}")
                        stu_id_item.setTextAlignment(Qt.AlignCenter)

                        name_item = QTableWidgetItem(name)
                        name_item.setTextAlignment(Qt.AlignCenter)

                        age_item = QTableWidgetItem(f"{age:.0f}")
                        age_item.setTextAlignment(Qt.AlignCenter)

                        course_a_item = QTableWidgetItem(f"{course_a:.0f}")
                        course_a_item.setTextAlignment(Qt.AlignCenter)

                        course_b_item = QTableWidgetItem(f"{course_b:.0f}")
                        course_b_item.setTextAlignment(Qt.AlignCenter)

                        course_c_item = QTableWidgetItem(f"{course_c:.0f}")
                        course_c_item.setTextAlignment(Qt.AlignCenter)


                        row_position = self.table_2.rowCount()
                        self.table_2.insertRow(row_position)
                        self.table_2.setItem(self.items, 0, classname_item)
                        self.table_2.setItem(self.items, 1, stu_id_item)
                        self.table_2.setItem(self.items, 2, name_item)
                        self.table_2.setItem(self.items, 3, age_item)
                        self.table_2.setItem(self.items, 4, course_a_item)
                        self.table_2.setItem(self.items, 5, course_b_item)
                        self.table_2.setItem(self.items, 6, course_c_item)

                        self.items += 1
                        self.table_2.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # @Slot()# 获取当前选中的下拉框选项
    # def update_table(self):
    #     current_class = self.combo_box.currentText()

    #     # 根据选项更新表格数据
    #     if current_class == "全部班级":
    #         self.fill_table(None)
    #     elif current_class == "2005班":
    #         self.fill_table("2005班")
    #     elif current_class == "2008班":
    #         self.fill_table("2008班")
    #     elif current_class == "2007班":
    #         self.fill_table("2007班")

    @Slot()
    def update_display(self):
        current_class = self.combo_box.currentText()

        # 根据选项更新表格和折线图数据
        if current_class == "全部班级":
            self.fill_table(None)
            self.plot_data("全部班级")
        elif current_class == "2005班":
            self.fill_table("2005班")
            self.plot_data("2005班")
        elif current_class == "2008班":
            self.fill_table("2008班")
            self.plot_data("2008班")
        elif current_class == "2007班":
            self.fill_table("2007班")
            self.plot_data("2007班")  



    @Slot()# 清空数据
    def clear_table(self):
        self.table_1.setRowCount(0)
        self.table_2.setRowCount(0)
        self.items = 0

    def stu_mark_data(self):
        if self.table_1.rowCount()>0:
            self.table_1.clearContents()
            self.table_1.setRowCount(0)

        self.items = 0 # 初始化为0
        # 连接到数据库
        self.conn = sqlite3.connect('output\students.db')
        # 获取游标
        cur = self.conn.cursor()
        clas_value_lis = []
        # 执行查询语句并获取结果
        for i in ["2005班","2008班","2007班"]:
            for j in ["course_a","course_b","course_c"]:
                lis = []
                cur.execute(f"select count(*) from students where classname = '{i}' and {j} >= 60")
                passnum = list(cur.fetchone())
                cur.execute(f"select count(*) from students where classname = '{i}'")
                total = list(cur.fetchone())
                passrate = round((int(passnum[0])/int(total[0])),2)
                cur.execute(f"select avg({j}), max({j}), min({j}) from students where classname = '{i}'")
                lis.append(i)
                lis.append(j)
                lis.extend([round(x,2) for x in list(cur.fetchone())])
                lis.append(passrate)
                clas_value_lis.append(lis)

        self.conn.commit()
        cur.close()
        self.conn.close()

        # 将数据添加到表格中
        rows = 0
        for j in clas_value_lis:
            class_item = QTableWidgetItem(j[0])
            cos_item = QTableWidgetItem(j[1])
            avg = QTableWidgetItem(f"{j[2]:.2f}")
            max = QTableWidgetItem(f"{j[3]:.0f}")
            min = QTableWidgetItem(f"{j[4]:.0f}")
            ratepass = QTableWidgetItem(f"{j[5]:.0%}")
            self.table_1.insertRow(rows)

            self.table_1.setItem(rows, 0, class_item)
            class_item.setTextAlignment(Qt.AlignCenter)
            
            self.table_1.setItem(rows, 1, cos_item)
            cos_item.setTextAlignment(Qt.AlignCenter)
            
            self.table_1.setItem(rows, 2, avg)
            avg.setTextAlignment(Qt.AlignCenter)
            
            self.table_1.setItem(rows, 3, max)
            max.setTextAlignment(Qt.AlignCenter)

            self.table_1.setItem(rows, 4, min)
            min.setTextAlignment(Qt.AlignCenter)

            self.table_1.setItem(rows, 5, ratepass)
            ratepass.setTextAlignment(Qt.AlignCenter)

            rows += 1
            
        return clas_value_lis


    @Slot() #搜索功能文本过滤器
    def on_filter_text_changed(self, filter_text):
        # 遍历表格中的每一行
        for i in range(self.table_2.rowCount()):
            classname = self.table_2.item(i, 0).text()
            name = self.table_2.item(i, 2).text()

            # 检查班级和名称是否匹配过滤器文本
            class_match = filter_text.lower() in classname.lower()
            name_match = filter_text.lower() in name.lower()

            # 根据匹配结果设置行的可见性
            self.table_2.setRowHidden(i, not (class_match or name_match))

    @Slot() #班级及格率饼图
    def plot_pass_data(self):
        with open('output/students.json', 'r', encoding='utf-8') as f:
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

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)
        # 在它被初始化后添加系列到图表中
        self.chart.addSeries(series)
        self.chart.setTitle('所有班级平均分及格率对比')
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)
        self.chart_view.setChart(self.chart)

class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("成绩管理系统Ver1.0")
        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("Please click me!")
        # Exit QAction
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)
        self.setCentralWidget(widget)

    @Slot() #退出功能
    def exit_app(self, checked):
        QApplication.quit()
if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    widget = Widget()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    window.resize(1400, 900)
    
    apply_stylesheet(app, theme='dark_cyan.xml')

    window.show()

    # Execute application
    sys.exit(app.exec())