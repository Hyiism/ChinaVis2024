import json
import pymysql

class TitlePerf:
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
            SELECT DISTINCT *
            FROM `student_submit_ac_vis`
            WHERE student_id = "{student_id}" AND title_id = "{title_id}"
            ORDER BY `timeconsume`, `memory`
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
    def reformat_student_submit_data(self, student_submit_data):
        # print(student_submit_data)
        student_id  = student_submit_data[0]['student_id']
        title_id = student_submit_data[0]['title_id']
        time_consume = student_submit_data[0]['timeconsume']
        memory_consume = student_submit_data[0]['memory']
        time_beat = student_submit_data[0]['time_beat']
        memory_beat = student_submit_data[0]['memory_beat']
        time_distribution = {
            '1': student_submit_data[0]['timeconsume_1_per'],
            '2': student_submit_data[0]['timeconsume_2_per'],
            '3': student_submit_data[0]['timeconsume_3_per'],
            '4': student_submit_data[0]['timeconsume_4_per'],
            '5': student_submit_data[0]['timeconsume_5_per'],
            '6': student_submit_data[0]['timeconsume_6_per'],
            '7': student_submit_data[0]['timeconsume_7_per'],
            '8': student_submit_data[0]['timeconsume_8_per'],
            '9': student_submit_data[0]['timeconsume_9_per'],
            '10': student_submit_data[0]['timeconsume_10_per'],
            '>10': student_submit_data[0]['timeconsume_>10_per'],
        }
        memory_distribution = {
            "160~235": student_submit_data[0]['memory_160_235_per'],
            "236~310": student_submit_data[0]['memory_236_310_per'],
            "311~385": student_submit_data[0]['memory_311_385_per'],
            "386~460": student_submit_data[0]['memory_386_460_per'],
            "461~535": student_submit_data[0]['memory_461_535_per'],
            "536~610": student_submit_data[0]['memory_536_610_per'],
            "611~685": student_submit_data[0]['memory_611_685_per'],
            "686~760": student_submit_data[0]['memory_686_760_per'],
            "761~835": student_submit_data[0]['memory_761_835_per'],
            "836~910": student_submit_data[0]['memory_836_910_per'],
            "911~1980": student_submit_data[0]['memory_911_1980_per'],
            ">1980": student_submit_data[0]['memory_>1980_per'],
        }
        data = {'student_id': student_id, 'title_id': title_id, 'time_consume': time_consume, 'memory_consume': memory_consume, 'time_beat': time_beat, 'memory_beat': memory_beat, 'time_distribution': time_distribution, 'memory_distribution': memory_distribution}
        reformatted_data_json = {"data": data}
        return reformatted_data_json

    def data_to_json(self, data):
        return json.dumps(data, indent=4)

# 使用示例
if __name__ == "__main__":
    
    # 创建Parallel类的实例，指定本地数据库连接信息
    titleperf = TitlePerf(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    student_submit_data = titleperf.get_student_submit_data('0088dc183f73c83f763e', 'Question_7NJzCXUPcvQF4Mkfh9Wr')
    reformatted_data_json = titleperf.reformat_student_submit_data(student_submit_data)
    data_json = titleperf.data_to_json(reformatted_data_json)
    print(data_json)
    
