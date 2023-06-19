import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import normaltest

# 读取CSV文件并选择需要的列
df = pd.read_csv('D:\\__easyHelper__\\test.csv', usecols=['课程a', '课程b', '课程c'])

# 计算均值和标准差
mean = df.mean()
std = df.std()

# 正态性检验
result = df.apply(normaltest)
stat = result[0]
p = result[1]

# 绘制直方图
plt.hist(df, bins=20, density=True)

if p.min() < 0.05:
    # 如果数据不呈正态分布，只绘制直方图
    plt.title('Histogram of Grades (not normally distributed)')
else:
    # 如果数据呈正态分布，绘制直方图和正态概率图
    plt.title('Histogram and Normal Probability Plot of Grades')
    x = np.linspace(mean - 3*std, mean + 3*std, 100)
    y = norm.pdf(x, mean, std)
    plt.plot(x, y)

plt.show()
