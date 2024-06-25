import json
import pymysql

class TitleProcess:
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

    def get_student_submit_data(self, student_id, title_id):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = f"""
            SELECT * 
            FROM `student_title_process`
            WHERE student_id = "{student_id}" AND title_id = "{title_id}"
            ORDER BY 'oringinal_time'
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
    def reformat_student_submit_data(self, student_submit_data, title_id):
        print(student_submit_data)
        # [{'student_id': '0088dc183f73c83f763e', 'title_id': 'Question_7NJzCXUPcvQF4Mkfh9Wr', 
        #   'state': 'e', 'time': '0:0', 'time_consume': '4', 'memory_consume': '0', 'errortype': 'error1', 
        #   'method': 'Method_m8vwGkEZc3TSW2xqYUoR', 'original_time': '1698765881'}...]
        titlestate = []
        for item in student_submit_data:
            titlestate.append({
                "state": item["state"],
                "time": item["time"],
                "time_consume": item["time_consume"],
                "memory_consume": item["memory_consume"],
                "errortype": item["errortype"],
                "method": item["method"]
            })
        # 前端本来想列表中放多个题目信息 但是这里就传一个题目信息 让前端只显示一个就可以！
        reformatted_data_json = [{ 'title_id': title_id, 'titlestate': titlestate }]
        return reformatted_data_json

    def data_to_json(self, data):
        return json.dumps(data, indent=4)

# 使用示例
if __name__ == "__main__":
    
    # 创建Parallel类的实例，指定本地数据库连接信息
    titleprocess = TitleProcess(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    student_submit_data = titleprocess.get_student_submit_data('0088dc183f73c83f763e', 'Question_oCjnFLbIs4Uxwek9rBpu')
    reformatted_data_json = titleprocess.reformat_student_submit_data(student_submit_data, 'Question_oCjnFLbIs4Uxwek9rBpu')
    data_json = titleprocess.data_to_json(reformatted_data_json)
    print(data_json)
    
