import random
import json
import numpy.random as np_random
import sqlite3
import configparser

class Student:
    """
    学生类 
    """
    def __init__(self, id, name, age, classname, course_a, course_b, 
                course_c,pattern_a,pattern_b,pattern_c,average_score
                ,max_score,min_score,passing_rate):
        # NOTE:第十周作业 要求完成main函数调用utils，实现students输出到output
        """
        创建对象并初始化属性。

        Args:
            id (_int_): 学号
            name (_str_): 姓名
            age (_int_): 年龄
            classname (_str_): 班级名
            course_a (_int_): 成绩a
            course_b (_int_): 成绩b
            course_c (_int_): 成绩c
            pattern_a (_str_): 成绩a模式
            pattern_b (_str_): 成绩b模式
            pattern_c (_str_): 成绩c模式
            average_score (_float_): 平均分
            max_score (_int_): 最高分
            min_score (_int_): 最低分
            passing_rate (_str_): 及格率
        """
        self.id = id
        self.name = name
        self.age = age
        self.classname = classname
        self.course_a = course_a
        self.course_b = course_b
        self.course_c = course_c
        self.pattern_a = pattern_a
        self.pattern_b = pattern_b
        self.pattern_c = pattern_c
        self.average_score = average_score
        self.max_score = max_score
        self.min_score = min_score
        self.passing_rate = passing_rate



def generate_students(num_students, score_distributions={},config_path='cfg\config.ini'):
    students = []
    id = 1001
    classnames = ["2008班", "2007班", "2005班"]
    pattern_a = ''
    pattern_b = ''
    pattern_c = ''

    #读取配置文件中各门课程对应的分布参数
    config = configparser.ConfigParser()
    if config_path:
        config.read(config_path)
        math_mean = float(config['math']['mean'])
        math_std_dev = float(config['math']['std_dev'])
        english_mean = float(config['english']['mean'])
        english_std_dev = float(config['english']['std_dev'])
        chinese_mean = float(config['chinese']['mean'])
        chinese_std_dev = float(config['chinese']['std_dev'])
    else:
        math_mean, math_std_dev = 50, 20
        english_mean, english_std_dev = 50, 20
        chinese_mean, chinese_std_dev = 50, 20

    for i in range(num_students):
        name_length = random.randint(1, 10)
        name = ''.join(random.choices(list('abcdefghijklmnopqrstuvwxyz'), k=name_length))
        age = random.randint(10, 18)
        classname = random.choice(classnames)
        
        """
        TODO:成绩分布功能
        生成三门课程的成绩，并根据输入的成绩分布情况进行生成
        期望输入的成绩分布情况应该包含'course_a', 'course_b', 'course_c'三个键值对
        如果分布方式是'uniform'，那么使用np_random.uniform()函数来生成对应课程的成绩；
        否则，则使用np_random.normal()函数来生成对应课程的成绩
        如果没有提供成绩分布情况，则使用默认的均值和标准差，使用np_random.normal()函数来生成每门课程的成绩
        """
        if score_distributions and all(key in score_distributions for key in ['course_a', 'course_b', 'course_c']):
            # 从成绩分布字典中提取出每门课程的参数信息
            scores_a_params = score_distributions['course_a']
            scores_b_params = score_distributions['course_b']
            scores_c_params = score_distributions['course_c']

            # 生成课程A的成绩
            if scores_a_params['distribution'] == 'uniform':
                # 如果分布方式为'uniform'，设置默认的最小值和最大值
                try:
                    low = config.getint('math', 'low')
                    high = config.getint('math', 'high')
                except (configparser.NoSectionError, configparser.NoOptionError):
                    low, high = 0, 100

                # 使用 np_random.uniform() 函数来生成成绩
                scores_a = int(np_random.uniform(low, high, 1))

            else:
                # 如果不是'uniform'分布，从参数字典中提取均值和标准差
                scores_a_mean = scores_a_params.get('mean', math_mean)
                scores_a_std_dev = scores_a_params.get('std_dev', math_std_dev)

                # 使用np_random.normal()函数来生成成绩
                scores_a = int(np_random.normal(scores_a_mean, scores_a_std_dev, 1))
                
            pattern_a = 'uniform' if scores_a_params['distribution'] == 'uniform' else 'normal'

            # 生成课程B的成绩
            if scores_b_params['distribution'] == 'uniform':
                # 如果分布方式为'uniform'，设置默认的最小值和最大值
                try:
                    low = config.getint('english', 'low')
                    high = config.getint('english', 'high')
                
                except (configparser.NoSectionError, configparser.NoOptionError):
                    low, high = 0, 100

                # 使用np_random.uniform()函数来生成成绩
                scores_b = int(np_random.uniform(low, high, 1))

            else:
                # 如果不是'uniform'分布，从参数字典中提取均值和标准差
                scores_b_mean = scores_b_params.get('mean', math_mean)
                scores_b_std_dev = scores_b_params.get('std_dev', math_std_dev)

                # 使用np_random.normal()函数来生成成绩
                scores_b = int(np_random.normal(scores_b_mean, scores_b_std_dev, 1))
                
            pattern_b = 'uniform' if scores_b_params['distribution'] == 'uniform' else 'normal'

            # 生成课程C的成绩
            if scores_c_params['distribution'] == 'uniform':
                # 如果分布方式为'uniform'，设置默认的最小值和最大值
                try:
                    low = config.getint('chinese', 'low')
                    high = config.getint('chinese', 'high')
                
                except (configparser.NoSectionError, configparser.NoOptionError):
                    low, high = 0, 100

                    # 使用np_random.uniform()函数来生成成绩
                scores_c = int(np_random.uniform(low, high, 1))
            else:
                # 如果不是'uniform'分布，从参数字典中提取均值和标准差
                scores_c_mean = scores_c_params.get('mean', math_mean)
                scores_c_std_dev = scores_c_params.get('std_dev', math_std_dev)

                # 使用np_random.normal()函数来生成成绩
                scores_c = int(np_random.normal(scores_c_mean, scores_c_std_dev, 1))
            pattern_c = 'uniform' if scores_c_params['distribution'] == 'uniform' else 'normal'
        else:
            # 如果没有提供成绩分布情况，使用默认的均值和标准差来生成每门课程的成绩
            scores_a = int(np_random.normal(math_mean, math_std_dev, 1))
            scores_b = int(np_random.normal(english_mean, english_std_dev, 1))
            scores_c = int(np_random.normal(chinese_mean, chinese_std_dev, 1))
        
        #NOTE:增加需求 计算三门成绩的平均分
        average_score =  (scores_a + scores_b + scores_c) / 3
        average_score = round(average_score * 100) / 100

        #NOTE:增加需求 生成三门成绩的最高分和最低分
        scores_list = [scores_a, scores_b, scores_c]
        max_score = max(scores_list)
        min_score = min(scores_list)
        
        #NOTE:增加需求 生成班级的及格率
        passing_scores = 60 #及格分数线
        if average_score < passing_scores:
            passing_rate = "不及格"
        else:
            passing_rate = "及格"

        student = Student(id, name, age, classname, scores_a, scores_b, 
                        scores_c,pattern_a,pattern_b,pattern_c,average_score,max_score,min_score,passing_rate)
        students.append(student)
        id += 1

    data = {'students': []}
    for student in students:
        data['students'].append({
            'id': student.id,
            'name': student.name,
            'age': student.age,
            'classname': student.classname,
            'course_a': student.course_a,
            'course_b': student.course_b,
            'course_c': student.course_c,
            'pattern_a': student.pattern_a,
            'pattern_b': student.pattern_b,
            'pattern_c': student.pattern_c,
            'average_score' :student.average_score,
            'max_score' : student.max_score,
            'min_score' : student.min_score,
            'passing_rate' : student.passing_rate
        })
        
    with open('output/students.json', 'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    #NOTE:第十一周作业 要求把生成的数据导入到数据库
    con = sqlite3.connect('output\students.db') #生成并连接数据库students.db
    
    cur = con.cursor() #创建游标

    cur.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT,
                    age INTEGER,
                    classname TEXT,
                    course_a INTEGER,
                    course_b INTEGER,
                    course_c INTEGER,
                    average_score FOLAT,
                    max_score INTEGER,
                    min_score INTEGER
                )''')
    #TAG：主键自增 所以后面省略insert id

    #将学生数据插入到表中
    for student in students:
        cur.execute("INSERT INTO students (name, age, classname, course_a, course_b, course_c,average_score,max_score,min_score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        (student.name, student.age, student.classname, student.course_a, student.course_b, student.course_c,student.average_score,student.max_score,student.min_score))
    
    #提交更改并关闭数据库连接
    con.commit()
    con.close()

    return students