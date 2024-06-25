import json
import pymysql

class HeatMap:
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

    def get_students_knowledge_timeconsume(self, class_id: str):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            # "b3C9s_score": "1.01",
            # "g7R2j_score": "0.89",
            # "k4W1c_score": "1.23",
            # "m3D1v_score": "2.00",
            # "r8S3g_score": "1.22",
            # "s8Y2f_score": "0.85",
            # "student_id": "8b6d1125760bd3939b6e",
            # "t5V9e_score": "0.36",
            # "y9W5d_score": "0.45"

            query = f"""
                        SELECT b3C9s_score, g7R2j_score, k4W1c_score, m3D1v_score, r8S3g_score,
                                s8Y2f_score, student_id, t5V9e_score, y9W5d_score
                        FROM `student_knowledge_spent`
                        WHERE `class_id` = "{class_id}"
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
    # def reformat_student_submit_data(self, students_knowledge_timeconsume):
    #     print(students_knowledge_timeconsume)
     
        # return reformatted_data_json

    def data_to_json(self, data):
        return json.dumps(data, indent=4)

# 使用示例
if __name__ == "__main__":
    
    # 创建Parallel类的实例，指定本地数据库连接信息
    heatmap = HeatMap(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    students_knowledge_timeconsume = heatmap.get_students_knowledge_timeconsume('Class1')
    # reformatted_data_json = heatmap.reformat_student_submit_data(students_knowledge_timeconsume)
    data_json = heatmap.data_to_json(students_knowledge_timeconsume)
    # print(data_json)
    
