import json
import pymysql

class ForgetCur:
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

    def get_students_knowledge_timeconsume(self, student_id: str, knowledge_id: str):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = f"""
                        SELECT *
                        FROM `forget_data_all_0.5`
                        WHERE `student_id` = "{student_id}" AND `knowledge_id` = "{knowledge_id}"
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
    def reformat_student_submit_data(self, students_knowledge_timeconsume):
        # print(students_knowledge_timeconsume)
        T_list = []
        K_list = []
        for item in students_knowledge_timeconsume:
            T_list.append(item['time_diff'])
            K_list.append(item['k'])
        reformatted_data_json = { 'T_list': T_list, 'K_list': K_list }
        return reformatted_data_json

    def data_to_json(self, data):
        return json.dumps(data, indent=4)

# 使用示例
if __name__ == "__main__":
    
    # 创建Parallel类的实例，指定本地数据库连接信息
    forgetcur = ForgetCur(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    students_knowledge_timeconsume = forgetcur.get_students_knowledge_timeconsume('0088dc183f73c83f763e', 't5V9e')
    reformatted_data_json = forgetcur.reformat_student_submit_data(students_knowledge_timeconsume)
    data_json = forgetcur.data_to_json(reformatted_data_json)
    print(data_json)
    
