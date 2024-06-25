import json
import pymysql

class Rank:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_connection(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def get_students_ranking_data(self, class_id=None):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = f"""
            SELECT *
            FROM students_knowledge_summary
            ORDER BY total_score DESC
            LIMIT 100
            """
            cursor.execute(query)
            results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            results = []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return results
    
    def get_students_ranking_data_class(self, class_id):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # print(class_id)

            query = f"""
                SELECT *
                FROM students_knowledge_summary
                WHERE class = "{class_id}"
                ORDER BY knowledge_total_score DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            results = []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return results
    
    # 格式化成需要数据
    def reformat_student_data(self, students_datas):
        student_id = []
        subject_1 = []
        subject_2 = []
        subject_3 = []
        subject_4 = []
        subject_5 = []
        subject_6 = []
        subject_7 = []
        subject_8 = []
        total_score = []

        for data in students_datas:
            student_id.append(data['student_ID'][:3] + '...')
            subject_1.append(round(data['b3C9s_score'], 1))
            subject_2.append(round(data['g7R2j_score'], 1))
            subject_3.append(round(data['k4W1c_score'], 1))
            subject_4.append(round(data['m3D1v_score'], 1))
            subject_5.append(round(data['r8S3g_score'], 1))
            subject_6.append(round(data['s8Y2f_score'], 1))
            subject_7.append(round(data['t5V9e_score'], 1))
            subject_8.append(round(data['y9W5d_score'], 1))
            total_score.append(round(data['total_score'], 1))
        reformatted_data_json = { 
            'student_id': student_id,
            'subject_1': subject_1,
            'subject_2': subject_2,
            'subject_3': subject_3,
            'subject_4': subject_4,
            'subject_5': subject_5,
            'subject_6': subject_6,
            'subject_7': subject_7,
            'subject_8': subject_8,
            'total_score': total_score
        }
        return reformatted_data_json

    def data_to_json(self, data):
        return json.dumps(data, indent=4)

# 使用示例
if __name__ == "__main__":
    
    # 创建Parallel类的实例，指定本地数据库连接信息
    rank = Rank(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    students_data = rank.get_students_ranking_data()
    reformatted_data_json = rank.reformat_student_data(students_data)
    data_json = rank.data_to_json(reformatted_data_json)
    
