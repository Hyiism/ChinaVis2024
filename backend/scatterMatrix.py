import json
import pymysql

class ScatterMatrix:
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

    def get_students_ranking_data(self, class_id):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            query = f"""
            SELECT *
            FROM features_label_analy
            WHERE class = "{class_id}"
            ORDER BY student_id
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
        # data_need = []
        # for item in students_datas:
        #     data_need.append({
        #         "cluster_label_tsne": item["cluster_label_tsne"],
        #         "time_difference_mean": item["time_difference_mean"],
        #         "time_split_2_percentage": item["time_split_2_percentage"],
        #         "submit_times_avg": item["submit_times_avg"],
        #         "total_score": item["total_score"],
        #     })
        data_need = students_datas
        return data_need

    def data_to_json(self, data):
        return json.dumps(data, indent=4)

# 使用示例
if __name__ == "__main__":
    
    # 创建Parallel类的实例，指定本地数据库连接信息
    scatterMatrix = ScatterMatrix(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    students_data = scatterMatrix.get_students_ranking_data()
    reformatted_data_json = scatterMatrix.reformat_student_data(students_data)
    data_json = scatterMatrix.data_to_json(reformatted_data_json)
    print(data_json)
    
