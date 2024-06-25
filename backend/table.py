import json
import pymysql

class Table:
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

    def get_students_info(self, class_id: str):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if class_id == "all":
                query = f"""
                SELECT *
                FROM student_info
                ORDER BY total_score DESC
                """
            else:
                query = f"""
                SELECT *
                FROM student_info
                WHERE class = "{class_id}"
                ORDER BY total_score DESC
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
        for item in students_datas:
            item['student_ID'] = item['student_ID'][:3] + '...'
            item['total_score'] = round(item['total_score'], 2)
        reformatted_data_json = { 'data': students_datas }

        return reformatted_data_json

    def data_to_json(self, data):
        return json.dumps(data, indent=4)

# 使用示例
if __name__ == "__main__":
    
    # 创建Parallel类的实例，指定本地数据库连接信息
    table = Table(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    students_data = table.get_students_info()
    reformatted_data_json = table.reformat_student_data(students_data)
    data_json = table.data_to_json(reformatted_data_json)

    
