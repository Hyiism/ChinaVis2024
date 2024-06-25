import json
import pymysql
from datetime import datetime

class Check:
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

    def get_students_time_level(self, student_id: str):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = f"""
            SELECT `date`, `activity_level`,`submission_count`
            FROM `students_time_level`
            WHERE student_ID = "{student_id}"
            ORDER BY `date`
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
    def reformat_student_data(self, time_level_data):
        for item in time_level_data:
            item['year'] = item['date'].year
            item['month'] = item['date'].month
            item['date'] = item['date'].day
            item["level"] = item["activity_level"]
            item['isToday'] = "false"
            del item['activity_level']
            # del item['date']

        # for item in students_datas:
        #     item['student_ID'] = item['student_ID'][:3] + '...'
        #     item['total_score'] = round(item['total_score'], 2)
        reformatted_data_json = { 'infos': time_level_data }

        return reformatted_data_json

    def data_to_json(self, data):
        return json.dumps(data, separators=(',', ':'))

class CheckRing:
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

    def get_state_percentage_by_date(self, student_id: str, year: int, month: int, date: int):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = f"""
            SELECT *
            FROM `time_seq_data`
            WHERE student_ID = "{student_id}" AND `date` = DATE(CONCAT({year}, '-', {month}, '-', {date}));
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
    def reformat_ring_data(self, submit_data_by_date):
        # submit_data_by_date= 
        # [{'student_id': '0088dc183f73c83f763e', 'date': datetime.date(2023, 12, 6), 
        # 'time_difference_mean': 438.5, 'time_split_0_percentage': 1.0, 'time_split_1_percentage': 0.0, 
        # 'time_split_2_percentage': 0.0, 'submit_times': 25, 'total_syth_score_avg': 0.76, 
        # 'all_memory_avg': 402.56, 'all_timeconsume_avg': 3.16, 'state_ae_percentage': 0, 
        # 'state_e_percentage': 0.5, 'state_pc_percentage': 0.375, 'state_ac_percentage': 0.125}]
        submit_data_by_date = submit_data_by_date[0]
        # 保留两位小数
        state_per = {"ae":round(submit_data_by_date["state_ae_percentage"]*100, 2), "e":round(submit_data_by_date["state_e_percentage"]*100, 2),"pc":round(submit_data_by_date["state_pc_percentage"]*100, 2),"ac":round(submit_data_by_date["state_ac_percentage"]*100, 2)}

        reformatted_data_json = {"piedata": state_per}
        return reformatted_data_json

    def data_to_json(self, data):
        return json.dumps(data, separators=(',', ':'))
    
class CheckRadar:
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

    def get_submit_times_hour_by_date(self, student_id: str, year: int, month: int, date: int):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = f"""
            SELECT *
            FROM `submit_times_every_hour`
            WHERE student_ID = "{student_id}" AND `day` = DATE(CONCAT({year}, '-', {month}, '-', {date}));
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
    def reformat_radar_data(self, submit_tiems_hour_by_date):
        # submit_tiems_hour_by_date= 
        # [{'student_id': '0088dc183f73c83f763e', 'date': datetime.date(2023, 12, 6), 
        # 'time_difference_mean': 438.5, 'time_split_0_percentage': 1.0, 'time_split_1_percentage': 0.0, 
        # 'time_split_2_percentage': 0.0, 'submit_times': 25, 'total_syth_score_avg': 0.76, 
        # 'all_memory_avg': 402.56, 'all_timeconsume_avg': 3.16, 'state_ae_percentage': 0, 
        # 'state_e_percentage': 0.5, 'state_pc_percentage': 0.375, 'state_ac_percentage': 0.125}]
        print(submit_tiems_hour_by_date)
        if (submit_tiems_hour_by_date == []):
            {'student_id': '0088dc183f73c83f763e', 'class': 'Class2', 'day': datetime.date(2023, 12, 6), 'time_detail': datetime.timedelta(seconds=31471), '00_submit_times': 0, '01_submit_times': 0, '02_submit_times': 0, '03_submit_times': 0, '04_submit_times': 0, '05_submit_times': 0, '06_submit_times': 0, '07_submit_times': 0, '08_submit_times': 0, '09_submit_times': 0, '10_submit_times': 0, '11_submit_times': 0, '12_submit_times': 0, '13_submit_times': 0, '14_submit_times': 0, '15_submit_times': 0, '16_submit_times': 0, '17_submit_times': 0, '18_submit_times': 0, '19_submit_times': 0, '20_submit_times': 0, '21_submit_times': 0, '22_submit_times': 0, '23_submit_times': 0, 'all_submit_times': 1}
        else:
            submit_data_by_date = submit_tiems_hour_by_date[0]
        # 保留两位小数
        submit_data_every_hour = {"1:00": submit_data_by_date["01_submit_times"]/submit_data_by_date["all_submit_times"], "2:00": submit_data_by_date["02_submit_times"]/submit_data_by_date["all_submit_times"], "3:00": submit_data_by_date["03_submit_times"]/submit_data_by_date["all_submit_times"], "4:00": submit_data_by_date["04_submit_times"]/submit_data_by_date["all_submit_times"], "5:00": submit_data_by_date["05_submit_times"]/submit_data_by_date["all_submit_times"], "6:00": submit_data_by_date["06_submit_times"]/submit_data_by_date["all_submit_times"], "7:00": submit_data_by_date["07_submit_times"]/submit_data_by_date["all_submit_times"], "8:00": submit_data_by_date["08_submit_times"]/submit_data_by_date["all_submit_times"], "9:00": submit_data_by_date["09_submit_times"]/submit_data_by_date["all_submit_times"], "10:00": submit_data_by_date["10_submit_times"]/submit_data_by_date["all_submit_times"], "11:00": submit_data_by_date["11_submit_times"]/submit_data_by_date["all_submit_times"], "12:00": submit_data_by_date["12_submit_times"]/submit_data_by_date["all_submit_times"], "13:00": submit_data_by_date["13_submit_times"]/submit_data_by_date["all_submit_times"], "14:00": submit_data_by_date["14_submit_times"]/submit_data_by_date["all_submit_times"], "15:00": submit_data_by_date["15_submit_times"]/submit_data_by_date["all_submit_times"], "16:00": submit_data_by_date["16_submit_times"]/submit_data_by_date["all_submit_times"], "17:00": submit_data_by_date["17_submit_times"]/submit_data_by_date["all_submit_times"], "18:00": submit_data_by_date["18_submit_times"]/submit_data_by_date["all_submit_times"], "19:00": submit_data_by_date["19_submit_times"]/submit_data_by_date["all_submit_times"], "20:00": submit_data_by_date["20_submit_times"]/submit_data_by_date["all_submit_times"], "21:00": submit_data_by_date["21_submit_times"]/submit_data_by_date["all_submit_times"], "22:00": submit_data_by_date["22_submit_times"]/submit_data_by_date["all_submit_times"], "23:00": submit_data_by_date["23_submit_times"]/submit_data_by_date["all_submit_times"], "24:00": submit_data_by_date["00_submit_times"]/submit_data_by_date["all_submit_times"]}
        reformatted_data_json = {"radardata": submit_data_every_hour}

        return reformatted_data_json

    def data_to_json(self, data):
        return json.dumps(data, separators=(',', ':'))

# 使用示例
if __name__ == "__main__":
    
    # 创建Parallel类的实例，指定本地数据库连接信息
    # check = Check(
    #     host='localhost',
    #     user='root',
    #     password='qyh443012.',
    #     database='chinavis2024'
    # )
    # time_level_data = check.get_students_time_level('r3uk44zat2tcyj5wmojt')
    # reformatted_data_json = check.reformat_student_data(time_level_data)
    # data_json = check.data_to_json(reformatted_data_json)
    # print(data_json)

    # checkring = CheckRing(c
    # submit_data_by_date = checkring.get_state_percentage_by_date('0088dc183f73c83f763e', 2023, 12, 6)
    # reformatted_data_json = checkring.reformat_ring_data(submit_data_by_date)
    # data_json = checkring.data_to_json(reformatted_data_json)

    checkradar = CheckRadar(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    submit_data_by_date = checkradar.get_submit_times_hour_by_date('0088dc183f73c83f763e', 2023, 12, 6)
    reformatted_data_json = checkradar.reformat_radar_data(submit_data_by_date)
    data_json = checkradar.data_to_json(reformatted_data_json)
    # print(data_json)
