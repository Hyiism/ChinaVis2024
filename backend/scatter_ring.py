import json
import pymysql
import random

class ScatterRing:
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
    
    def get_students_vis_data_2d(self, class_id, method, embedding):
        print(f"get_students_vis_data_2d: {class_id}, {method}, {embedding}")
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            x_name = "x_" + method
            y_name = "y_" + method
            class_label_name = "cluster_label_" + method
            query_axis = f"""
            SELECT student_id, {x_name}, {y_name}, {class_label_name}
            FROM {embedding} WHERE class = "{class_id}"
            """
            cursor.execute(query_axis)
            axis_results = cursor.fetchall()

            query_ring = f"""
            SELECT student_id, b3C9s_score, g7R2j_score, k4W1c_score, m3D1v_score, r8S3g_score, s8Y2f_score, t5V9e_score, y9W5d_score, total_score,
                state_ae_percentage, state_e_percentage, state_pc_percentage, state_ac_percentage, 01_activity, 02_activity, 03_activity, 04_activity, 05_activity, 06_activity, 07_activity, 08_activity, 09_activity, 10_activity, 11_activity, 12_activity, 13_activity, 14_activity, 15_activity, 16_activity, 17_activity, 18_activity, 19_activity, 20_activity, 21_activity, 22_activity, 23_activity, 24_activity
            FROM students_features_reprocess_vis_2d_aa WHERE class = "{class_id}"
            """
            cursor.execute(query_ring)
            ring_results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            axis_results = []
            ring_results = []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return (axis_results, ring_results)
    
    # 格式化成需要的数据
    def reformat_student_data_2d(self, students_data, method):
        axis_data, ring_data = students_data
        # 按照student_id合并两个数据
        students_data_comb = []
        for axis_item in axis_data:
            for ring_item in ring_data:
                if axis_item['student_id'] == ring_item['student_id']:
                    combined_data = {**axis_item, **ring_item}
                    students_data_comb.append(combined_data)
                    break
        
        x_name = "x_" + method
        y_name = "y_" + method
        cluster_label_name = "cluster_label_" + method
        # 生成随机活跃度数据 填充students_features_reprocess_vis_2d_aa暂时还没计算的活跃度数据
        # for item in students_data_comb:
        #     for i in range(1, 25):
        #         item[str(i).zfill(2) + '_activity'] = random.random()
                # print(item[str(i).zfill(2) + '_activity'] )

        reformatted_data = [{'student_id': item['student_id'], "x": item[x_name], "y": item[y_name], "cluster_label": item[cluster_label_name],
            'ring_data': {"b3C9s_score": item['b3C9s_score'], "g7R2j_score": item['g7R2j_score'], "k4W1c_score": item['k4W1c_score'], "m3D1v_score": item['m3D1v_score'], "r8S3g_score": item['r8S3g_score'], "s8Y2f_score": item['s8Y2f_score'], "t5V9e_score": item['t5V9e_score'], "y9W5d_score": item['y9W5d_score']},
            'total_score': item['total_score'],
            'state_data': {"state_ae_percentage": item['state_ae_percentage'], "state_e_percentage": item['state_e_percentage'], "state_pc_percentage": item['state_pc_percentage'], "state_ac_percentage": item['state_ac_percentage']},
            'time_data': {"01:00": item['01_activity'], "02:00": item['02_activity'], "03:00": item['03_activity'], "04:00": item['04_activity'], "05:00": item['05_activity'], "06:00": item['06_activity'], "07:00": item['07_activity'], "08:00": item['08_activity'], "09:00": item['09_activity'], "10:00": item['10_activity'], "11:00": item['11_activity'], "12:00": item['12_activity'], "13:00": item['13_activity'], "14:00": item['14_activity'], "15:00": item['15_activity'], "16:00": item['16_activity'], "17:00": item['17_activity'], "18:00": item['18_activity'], "19:00": item['19_activity'], "20:00": item['20_activity'], "21:00": item['21_activity'], "22:00": item['22_activity'], "23:00": item['23_activity'], "24:00": item['24_activity']},
         } for item in students_data_comb]
        reformatted_data_json = {'nodes': reformatted_data}
        return reformatted_data_json

    def data_to_json(self, data):
        json_str = json.dumps(data, separators=(',', ':'))
        # print(json_str)
        return json_str

# 使用示例
if __name__ == "__main__":
    
    # 创建ScatterRing类的实例，指定本地数据库连接信息
    scatter_ring = ScatterRing(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    students_data = scatter_ring.get_students_vis_data_2d('Class1', 'umap','features_vis_seq')
    reformatted_data_json = scatter_ring.reformat_student_data_2d(students_data, 'umap')
    data_json = scatter_ring.data_to_json(reformatted_data_json)
    print(data_json)
