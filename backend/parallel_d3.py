import json
import pymysql

class Parallel:
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

    def get_top_n_students(self, n):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = f"""
            SELECT *
            FROM student_scores_summary_1
            ORDER BY total_score DESC
            LIMIT 50
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
    def reformat_student_data(self, students_data):
        # 创建一个新的字典，用于存储格式化后的数据
        # reformatted_data = {"data": students_data}

        new_students_data = []
        for data in students_data:
            data.pop('student_id')
            new_data = {}
            for key, value in data.items():
                if key != 'total_score':
                    new_key = key[9:29]
                    new_data[new_key] = value
                else:
                    new_data['total_score'] = value
            new_students_data.append(new_data)
        reformatted_data = {"data": new_students_data}

        return reformatted_data

    def data_to_json(self, data):
        return json.dumps(data, indent=4)

# 使用示例
if __name__ == "__main__":
    
    # 创建Parallel类的实例，指定本地数据库连接信息
    parallel = Parallel(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    
    # 获取前15名总分最高的学生
    top_students = parallel.get_top_n_students(15)
    top_students_format = parallel.reformat_student_data(top_students)
    # # 截取前5、前10、前15条数据
    # top5_values = [top_students_format[key] for key in list(top_students_format.keys())[:5]]
    # top10_values = [top_students_format[key] for key in list(top_students_format.keys())[:10]]
    # top15_values = [top_students_format[key] for key in list(top_students_format.keys())[:15]]
    # # 组装成最终的 JSON 结构
    # final_json = {
    #     "top5": top5_values,
    #     "top10": top10_values,
    #     "top15": top15_values
    # }
    top_students_json = parallel.data_to_json(top_students_format)
    # print(top_students_json)
    
