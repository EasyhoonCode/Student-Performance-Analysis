import random
import sys
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import json
import csv
import sqlite3

class Tablewid(QWidget):
    def __init__(self):
        super().__init__()

        
        self.tablewid_group = QGroupBox() #小工具的容器
        self.tablewid_layout2 = QVBoxLayout() #小工具的垂直布局
        #下拉列表
        self.combo_box = QComboBox(self)
        self.combo_box.setFixedWidth(200)
        self.combo_box.setFixedHeight(30)
        self.combo_box.setToolTip("可以任意选择班级显示成绩")

        #搜索框
        self.search_box = QLineEdit(self)
        self.search_box.setFixedSize(250, 30)
        self.search_box.setPlaceholderText("搜索(支持班级或者姓名)")
        self.search_box.setClearButtonEnabled(True)
        #self.search_box.setStyleSheet("color:black;background-color:white;")
        self.search_box.setStyleSheet("""
            QLineEdit {
            background-color:white;
            border: 1px solid lightgray;
            border-radius: 5px;
            padding-left: 5px;
            padding-right: 60px;
        }
        """)

        #导出数据按钮
        self.data_btn = QPushButton(self)
        self.data_btn.setText("导出数据")
        self.data_btn.setToolTip("输入班级或名字的关键字")
        self.data_btn.setFixedSize(60,30)
        self.data_btn.setCursor(Qt.PointingHandCursor)
        self.data_btn.move(self.width()-self.data_btn.width(), 0)
        self.data_btn.setStyleSheet("""
        QPushButton {
            background-color: #2a70f4;
            color: white; 
            font-size: 13px;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
        }

        QPushButton:hover {
            background-color: #2361d0;
        }
        
        QPushButton:pressed {
            background-color: #2058bc;
        }

        QToolTip {
        color: #ffffff;
        background-color: #2a70f4;
        border: 1px solid #ffffff;
        }
        """)

        search_icon = QIcon("qt\Student-Performance-Analysis\leftmenu\pic\search_img.svg")
        search_action = QAction(search_icon,"",self.search_box)
        self.search_box.addAction(search_action,QLineEdit.TrailingPosition)



        with open("output\students.json","r", encoding='utf-8') as f:
            data = json.load(f)

            # 获取所有班级
            classes = set([item["classname"] for item in data["students"]])
            
            # 将班级添加到下拉列表中
            self.combo_box.addItem("全部班级")
            self.combo_box.setStyleSheet("color:black;background-color:white;")
            for c in sorted(classes):
                self.combo_box.addItem(c)
                
        # self.tablewid_group = QVBoxLayout()
        self.table_1 =QTableWidget()
        self.table_1.setColumnCount(7)
        self.table_1.setHorizontalHeaderLabels(["班级", "学号", "姓名", "年龄", "课程a","课程b","课程c"])
        self.table_1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.table_2.setStyleSheet("background-color:white;font-family:Microsoft YaHei;font-size:14px;")
        self.table_1.setStyleSheet("""selection-background-color:transparent;selection-color:black;background-color: aliceblue;""")


        self.table_2 = QTableWidget()
        self.table_2.setColumnCount(5)
        self.table_2.setHorizontalHeaderLabels(["班级","姓名","个人平均分","个人成绩最大值","个人成绩最小值"])
        self.table_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #随着窗口大小的变化而自动调整宽度
        self.table_2.setStyleSheet("""selection-background-color:transparent;selection-color:black;background-color: aliceblue;""")



        # self.tablewid_layout.addWidget(self.combo_box)
        self.tablewid_layout = QHBoxLayout()  #水平布局
        self.tablewid_layout.addWidget(self.combo_box) #下拉 水平
        self.tablewid_layout.addWidget(self.search_box)# 搜索 水平
        self.tablewid_layout.addWidget(self.data_btn)
        self.tablewid_layout.setAlignment(Qt.AlignLeft)

        
        self.tablewid_layout2.addLayout(self.tablewid_layout) 
        self.tablewid_layout2.addWidget(self.table_1) #表格
        self.tablewid_layout2.addWidget(self.table_2)
        # self.tablewid_layout2.addLayout(self.tablewid_layout2)
        self.tablewid_group.setLayout(self.tablewid_layout2)



        self.combo_box.currentIndexChanged.connect(self.update_table) #下拉列表
        self.search_box.textChanged.connect(self.on_filter_text_changed)
        self.data_btn.clicked.connect(self.on_export_button_click)

    def fill_table(self, classname=None):
        if self.table_1.rowCount()>0:
                self.table_1.clearContents()
                self.table_1.setRowCount(0)

        self.items = 0 # 初始化为0
        conn = sqlite3.connect("D:\project\project\output\students.db")
        cursor = conn.cursor()
        if classname is None:
            cursor.execute("SELECT DISTINCT classname FROM students")
            classnames = [row[0] for row in cursor.fetchall()]

            for classname in sorted(classnames):
                cursor.execute("SELECT * FROM students WHERE classname=?", (classname,))
                rows = cursor.fetchall()

                for row in rows:
                    stu_id = row[0]
                    name = row[1]
                    age = row[2]
                    course_a = row[4]
                    course_b = row[5]
                    course_c = row[6]

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


                    row_position = self.table_1.rowCount()
                    self.table_1.insertRow(row_position)
                    self.table_1.setItem(self.items, 0, classname_item)
                    self.table_1.setItem(self.items, 1, stu_id_item)
                    self.table_1.setItem(self.items, 2, name_item)
                    self.table_1.setItem(self.items, 3, age_item)
                    self.table_1.setItem(self.items, 4, course_a_item)
                    self.table_1.setItem(self.items, 5, course_b_item)
                    self.table_1.setItem(self.items, 6, course_c_item)

                    self.items += 1
                    self.table_1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            cursor.execute("SELECT * FROM students WHERE classname=?", (classname,))
            rows = cursor.fetchall()

            for row in rows:
                stu_id = row[0]
                name = row[1]
                age = row[2]
                course_a = row[4]
                course_b = row[5]
                course_c = row[6]

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


                row_position = self.table_1.rowCount()
                self.table_1.insertRow(row_position)
                self.table_1.setItem(self.items, 0, classname_item)
                self.table_1.setItem(self.items, 1, stu_id_item)
                self.table_1.setItem(self.items, 2, name_item)
                self.table_1.setItem(self.items, 3, age_item)
                self.table_1.setItem(self.items, 4, course_a_item)
                self.table_1.setItem(self.items, 5, course_b_item)
                self.table_1.setItem(self.items, 6, course_c_item)

                self.items += 1
                self.table_1.setEditTriggers(QAbstractItemView.NoEditTriggers)

        conn.close()

    def fill_table_2(self, classname=None):
        if self.table_2.rowCount() > 0:
            self.table_2.clearContents()
            self.table_2.setRowCount(0)

        self.items = 0 # 初始化为0
        conn = sqlite3.connect("D:\project\project\output\students.db")
        cursor = conn.cursor()

        if classname is None:
            cursor.execute("SELECT DISTINCT classname FROM students")
            classnames = [row[0] for row in cursor.fetchall()]

            for classname in sorted(classnames):
                if self.table_2.findItems(classname, Qt.MatchExactly):
                    continue

                cursor.execute("SELECT * FROM students WHERE classname=?", (classname,))
                rows = cursor.fetchall()
                for row in rows:
                    name = row[1]
                    average_score = row[7]
                    max_score = row[8]
                    min_score = row[9]

                    classname_item = QTableWidgetItem(classname)
                    classname_item.setTextAlignment(Qt.AlignCenter)

                    name_item = QTableWidgetItem(name)
                    name_item.setTextAlignment(Qt.AlignCenter)

                    average_score_item = QTableWidgetItem(f"{average_score:.2f}")
                    average_score_item.setTextAlignment(Qt.AlignCenter)

                    max_score_item = QTableWidgetItem(f"{max_score:.0f}")
                    max_score_item.setTextAlignment(Qt.AlignCenter)

                    min_score_item = QTableWidgetItem(f"{min_score:.0f}")
                    min_score_item.setTextAlignment(Qt.AlignCenter)


                    row_position = self.table_2.rowCount()
                    self.table_2.insertRow(row_position)
                    self.table_2.setItem(self.items, 0, classname_item)
                    self.table_2.setItem(self.items, 1, name_item)
                    self.table_2.setItem(self.items, 2, average_score_item)
                    self.table_2.setItem(self.items, 3, max_score_item)
                    self.table_2.setItem(self.items, 4, min_score_item)

                    self.items += 1
                    self.table_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            if not self.table_2.findItems(classname, Qt.MatchExactly):
                cursor.execute("SELECT * FROM students WHERE classname=?", (classname,))
                rows = cursor.fetchall()
                for row in rows:
                    name = row[1]
                    average_score = row[7]
                    max_score = row[8]
                    min_score = row[9]

                    classname_item = QTableWidgetItem(classname)
                    classname_item.setTextAlignment(Qt.AlignCenter)

                    name_item = QTableWidgetItem(name)
                    name_item.setTextAlignment(Qt.AlignCenter)

                    average_score_item = QTableWidgetItem(f"{average_score:.2f}")
                    average_score_item.setTextAlignment(Qt.AlignCenter)

                    max_score_item = QTableWidgetItem(f"{max_score:.0f}")
                    max_score_item.setTextAlignment(Qt.AlignCenter)

                    min_score_item = QTableWidgetItem(f"{min_score:.0f}")
                    min_score_item.setTextAlignment(Qt.AlignCenter)


                    row_position = self.table_2.rowCount()
                    self.table_2.insertRow(row_position)
                    self.table_2.setItem(self.items, 0, classname_item)
                    self.table_2.setItem(self.items, 1, name_item)
                    self.table_2.setItem(self.items, 2, average_score_item)
                    self.table_2.setItem(self.items, 3, max_score_item)
                    self.table_2.setItem(self.items, 4, min_score_item)

                    self.items += 1
                    self.table_2.setEditTriggers(QAbstractItemView.NoEditTriggers)

        conn.close()

    def on_export_button_click(self):
        table_data = []
        header_data = []
        
        # 获取表格数据
        for row in range(self.table_1.rowCount()):
            table_row = []
            for column in range(self.table_1.columnCount()):
                item = self.table_1.item(row, column)
                if item is not None:
                    table_row.append(item.text())
                else:
                    table_row.append('')
                    
                # 获取表头数据
                if row == 0:
                    header_item = self.table_1.horizontalHeaderItem(column)
                    if header_item is not None:
                        header_data.append(header_item.text())
                    else:
                        header_data.append('')

            table_data.append(table_row)

        # 打开文件对话框，让用户选择保存CSV文件的位置
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(None,"保存为CSV文件", "", "CSV Files (*.csv)", options=options)
        if fileName:
            # 将数据写入CSV文件
            with open(fileName, 'w', newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                # 写入表头部分
                writer.writerow(header_data)
                # 写入数据部分
                writer.writerows(table_data)

            # 显示成功的消息框
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("CSV文件已成功导出！")
            msgBox.setWindowTitle("导出成功")
            msgBox.exec_()



    @Slot()# 获取当前选中的下拉框选项
    def update_table(self):
        current_class = self.combo_box.currentText()

        # 根据选项更新表格数据
        if current_class == "全部班级":
            self.fill_table(None)
            self.fill_table_2(None)
        elif current_class == "2005班":
            self.fill_table("2005班")
            self.fill_table_2("2005班")
        elif current_class == "2008班":
            self.fill_table("2008班")
            self.fill_table_2("2008班")
        elif current_class == "2007班":
            self.fill_table("2007班")
            self.fill_table_2("2007班")

    def on_filter_text_changed(self,filter_text):
        # 遍历 table_1 中的每一行
        for i in range(self.table_1.rowCount()):
            classname = self.table_1.item(i, 0).text()
            name = self.table_1.item(i, 2).text()

            # 检查班级和名称是否匹配过滤器文本
            class_match = filter_text.lower() in classname.lower()
            name_match = filter_text.lower() in name.lower()

            # 根据匹配结果设置行的可见性
            self.table_1.setRowHidden(i, not (class_match or name_match))

        # 遍历 table_2 中的每一行
        for i in range(self.table_2.rowCount()):
            id = self.table_2.item(i, 0).text()
            name = self.table_2.item(i, 1).text()

            # 检查 ID 和名称是否匹配过滤器文本
            id_match = filter_text.lower() in id.lower()
            name_match = filter_text.lower() in name.lower()

            # 根据匹配结果设置行的可见性
            self.table_2.setRowHidden(i, not (id_match or name_match))