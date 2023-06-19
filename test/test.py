import json
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChartView, QPieSeries, QChart,QValueAxis,QLineSeries,QSplineSeries,QVXYModelMapper,QBarSeries,QBarSet,QBarCategoryAxis

class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        
        # 创建柱状图
        chart_view = QChartView(self)
        chart = QChart()
        chart.setTitle("Score Distribution")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # 获取数学、语文、英语成绩
        math_scores = [x['course_a'] for x in data['students']]
        chinese_scores = [x['course_b'] for x in data['students']]
        english_scores = [x['course_c'] for x in data['students']]
        
        # 创建数据序列
        math_series = QBarSeries()
        math_set = QBarSet("course_a")
        math_set.append(math_scores)
        math_series.append(math_set)
        chart.addSeries(math_series)

        chinese_series = QBarSeries()
        chinese_set = QBarSet("course_b")
        chinese_set.append(chinese_scores)
        chinese_series.append(chinese_set)
        chart.addSeries(chinese_series)
        
        english_series = QBarSeries()
        english_set = QBarSet("course_c")
        english_set.append(english_scores)
        english_series.append(english_set)
        chart.addSeries(english_series)
        
        # 设置坐标轴
        axis_x = QBarCategoryAxis()
        axis_x.append(["course_a", "course_b", "course_c"])
        chart.addAxis(axis_x, Qt.AlignBottom)
        math_series.attachAxis(axis_x)
        chinese_series.attachAxis(axis_x)
        english_series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignLeft)
        math_series.attachAxis(axis_y)
        chinese_series.attachAxis(axis_y)
        english_series.attachAxis(axis_y)
        
        # 设置图例
        legend = chart.legend()
        legend.setAlignment(Qt.AlignBottom)
        
        chart_view.setChart(chart)
        self.setCentralWidget(chart_view)

if __name__ == "__main__":
    # 读取JSON文件
    with open("output\students.json","r", encoding='utf-8') as f:
        data = json.load(f)
    
    app = QApplication([])
    main_window = MainWindow(data)
    main_window.show()
    app.exec_()
