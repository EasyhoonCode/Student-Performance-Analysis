import sys
import json
import random
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import json
import numpy as np
from matplotlib.font_manager import FontProperties

class Distribution_statistics(QWidget):
    def __init__(self):
        super().__init__()

        self.layout_QV_group = QGroupBox()
        self.layout_QV = QVBoxLayout()
        self.tip_lab = QLabel()
        self.button_plot = QPushButton()

        self.tip_lab.setText("分布值计算")
        self.tip_lab.setStyleSheet("font-size:25px;color:white")

        self.button_plot.clicked.connect(self.plot_graphs)

        self.layout_QV.addWidget(self.button_plot)
        self.layout_QV.addWidget(self.tip_lab)
        self.layout_QV_group.setLayout(self.layout_QV)
        self.layout_QV.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tip_lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_plot.setFixedSize(150, 40)
        self.button_plot.setText("弱水三千，吾独取一瓢。")
        self.button_plot.setStyleSheet("background-color: white")
        self.add_shadow()


    def add_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(3, 3)
        shadow.setColor(Qt.gray)
        self.button_plot.setGraphicsEffect(shadow)


    def plot_graphs(self):
        # 启用GUI模式
        plt.switch_backend('Qt5Agg')

        # 设置中文字体
        font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

        # 读取JSON文件并转换为DataFrame对象
        with open("output\students.json","r", encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data['students'])

        # 计算每门课程的标准差、偏度、峰度等统计量
        math_std = df['course_a'].std()
        chinese_std = df['course_b'].std()
        english_std = df['course_c'].std()

        math_skew = stats.skew(df['course_a'])
        chinese_skew = stats.skew(df['course_b'])
        english_skew = stats.skew(df['course_c'])

        math_kurtosis = stats.kurtosis(df['course_a'])
        chinese_kurtosis = stats.kurtosis(df['course_b'])
        english_kurtosis = stats.kurtosis(df['course_c'])

        # 绘制直方图
        fig, axs = plt.subplots(3, 2, figsize=(10, 10))
        axs[0, 0].hist(df['course_a'], bins=20, density=True, alpha=0.7)
        axs[0, 0].set_title('数学成绩直方图', fontproperties=font)
        x = np.linspace(df['course_a'].min(), df['course_a'].max(), 100)
        axs[0, 0].plot(x, stats.norm.pdf(x, df['course_a'].mean(), df['course_a'].std()), 'r--')

        axs[0, 1].hist(df['course_b'], bins=20, density=True, alpha=0.7)
        axs[0, 1].set_title('英语成绩直方图', fontproperties=font)
        x = np.linspace(df['course_b'].min(), df['course_b'].max(), 100)
        axs[0, 1].plot(x, stats.norm.pdf(x, df['course_b'].mean(), df['course_b'].std()), 'r--')

        axs[1, 0].hist(df['course_c'], bins=20, density=True, alpha=0.7)
        axs[1, 0].set_title('语文成绩直方图', fontproperties=font)
        x = np.linspace(df['course_c'].min(), df['course_c'].max(), 100)
        axs[1, 0].plot(x, stats.norm.pdf(x, df['course_c'].mean(), df['course_c'].std()), 'r--')

        # 绘制箱线图
        df.boxplot(column=['course_a', 'course_b', 'course_c'], ax=axs[1, 1])
        axs[1, 1].set_title('箱形图', fontproperties=font)

        # 绘制QQ图
        stats.probplot(df['course_a'], dist="norm", plot=axs[2, 0])
        axs[2, 0].set_title('数学成绩QQ图', fontproperties=font)

        stats.probplot(df['course_b'], dist="norm", plot=axs[2, 1])
        axs[2, 1].set_title('英语成绩QQ图', fontproperties=font)

        plt.tight_layout()

        # 创建提示框
        msg_box = QMessageBox()
        msg_box.setWindowTitle("成绩统计")
        message = f'数学成绩的标准差为：{math_std:.2f}\n偏度为：{math_skew:.2f}\n峰度为：{math_kurtosis:.2f}\n\n'
        message += f'英语成绩的标准差为：{chinese_std:.2f}\n偏度为：{chinese_skew:.2f}\n峰度为：{chinese_kurtosis:.2f}\n\n'
        message += f'语文成绩的标准差为：{english_std:.2f}\n偏度为：{english_skew:.2f}\n峰度为：{english_kurtosis:.2f}'
        msg_box.setText(message)
        msg_box.exec_()     # 显示消息框
        plt.show(block=False)