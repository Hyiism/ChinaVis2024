import json
import pymysql

class Stack:
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

    def get_students_knowledge_norm(self):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = f"""
            SELECT `student_ID`, `b3C9s_score`, `g7R2j_score`, `k4W1c_score`, `m3D1v_score`, `r8S3g_score`, `s8Y2f_score`, `t5V9e_score`, `y9W5d_score`
            FROM students_knowledge_summary_norm
            ORDER BY total_score
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

        reformatted_data_json = { 'data': students_datas }

        return reformatted_data_json

    def data_to_json(self, data):
        return json.dumps(data, separators=(',', ':'))

# 使用示例
if __name__ == "__main__":
    
    # 创建Parallel类的实例，指定本地数据库连接信息
    stack = Stack(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    students_data = stack.get_students_knowledge_norm()
    # print(students_data)
    reformatted_data_json = stack.reformat_student_data(students_data)
    data_json = stack.data_to_json(reformatted_data_json)

    
