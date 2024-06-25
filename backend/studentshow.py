import json
import pymysql
from datetime import datetime

class StudentShow:
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

    def get_studentbyclass(self, class_id: str):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = f"""
            SELECT `student_id`
            FROM `student_info`
            WHERE class = "{class_id}"
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
    def reformat_student_data(self, student4class_data):
        # print(student4class_data)

        # reformatted_data_json = { 'infos': time_level_data }
        # return reformatted_data_json
        student_id_list = []
        for student in student4class_data:
            student_id_list.append(student['student_id'])
        reformatted_data_json = {'students':student_id_list}

        return reformatted_data_json

    def data_to_json(self, data):
        return json.dumps(data, separators=(',', ':'))
    
    # 转换前端传过来的时间格式
    def trans_time(self, date_string):
        date_obj = datetime.strptime(date_string, "%a %b %d %Y %H:%M:%S")
        timestamp = date_obj.timestamp()
        return int(timestamp)
    
    # 根据时间获取学生的信息# startTime=${startTime}&endTime=${endTime}&className=${className}
    def get_student_by_time(self, startTime, endTime, className):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # 时间格式转化操作
            interval_seconds = 1800
            startTime = self.trans_time(startTime)
            endTime = self.trans_time(endTime)

            query = f"""
                SELECT DISTINCT `student_id` 
                FROM student_activity 
                WHERE `class` = "{className}"
                AND (
                    TIME BETWEEN {startTime}
                    AND {endTime}
                ) 
                OR (
                    next_time IS NOT NULL 
                    AND TIME <= {startTime} 
                    AND next_time >= {endTime}
                    AND (next_time - TIME) <= {interval_seconds}
                ) ;
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
    def reformat_student_data_by_time(self, student_data_by_time):
        # print(student_data_by_time)
        student_id_list = []
        for student in student_data_by_time:
            student_id_list.append(student['student_id'])
        reformatted_data_json = {'students':student_id_list}

        return reformatted_data_json

# 使用示例
if __name__ == "__main__":

    studentshow = StudentShow(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    # student4class_data = studentshow.get_student4class('Class1')
    # reformatted_data_json = studentshow.reformat_student_data(student4class_data)
    # data_json = studentshow.data_to_json(reformatted_data_json)
    # print(data_json)
    # Thu Sep 14 2023 14:32:25 GMT+0800 (中国标准时间) Thu Sep 14 2023 21:59:33 GMT+0800 (中国标准时间)
    student_data_by_time = studentshow.get_student_by_time('Thu Sep 14 2023 14:32:25', 'Thu Sep 14 2023 21:59:33', 'Class1')
    reformat_student_data_by_time = studentshow.reformat_student_data_by_time(student_data_by_time)
    data_json = studentshow.data_to_json(reformat_student_data_by_time)