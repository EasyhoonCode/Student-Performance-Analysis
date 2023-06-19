import subprocess

# 指定成绩分布

command = 'python "main.py" --course_a "uniform" --course_b "uniform" --course_c normal'
subprocess.run(command, shell=True, check=True)


