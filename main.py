from utils.data_gen import generate_students
import argparse



if __name__ == '__main__':

    # TAG:创建参数解析器并设置默认参数

    parser = argparse.ArgumentParser(description='Generate data for student.')
    parser.add_argument('--num_students', type=int, default=100, help='Number of students to generate')
    parser.add_argument('--config_path', type=str, default='cfg\config.ini', help='Path to configuration file')
    parser.add_argument('--course_a', type=str, default='normal', help='Distribution type for course A')
    parser.add_argument('--course_b', type=str, default='normal', help='Distribution type for course B')
    parser.add_argument('--course_c', type=str, default='normal', help='Distribution type for course C')
    args = parser.parse_args()

    score_distributions = {
        'course_a': {'distribution': args.course_a},
        'course_b': {'distribution': args.course_b},
        'course_c': {'distribution': args.course_c}
    }


    students = generate_students(args.num_students, score_distributions)

    print(f"已生成{len(students)}名学生的信息并存储在output/students.json中。")
