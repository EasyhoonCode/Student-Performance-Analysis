import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import json
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

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
plt.show()

print(f'Math Scores: std={math_std:.2f}, skewness={math_skew:.2f}, kurtosis={math_kurtosis:.2f}')
print(f'English Scores: std={chinese_std:.2f}, skewness={english_skew:.2f}, kurtosis={english_kurtosis:.2f}')
print(f'Chinese Scores: std={english_std:.2f}, skewness={chinese_skew:.2f}, kurtosis={chinese_kurtosis:.2f}')