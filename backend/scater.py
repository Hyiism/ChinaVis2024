import json
import pymysql

class Scater:
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

    def get_students_vis_data(self, class_id):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
    # features_dict['student_id'].append(student_id)
    # features_dict['title_counts'].append(len(student_title_ids))
    # features_dict['time_difference_mean'].append(time_difference_mean)
    # features_dict['time_difference_std'].append(time_difference_std)
    # features_dict['time_split_0_percentage'].append(counts[0])
    # features_dict['time_split_1_percentage'].append(counts[1])
    # features_dict['time_split_2_percentage'].append(counts[2])
    # features_dict['submit_times_avg'].append(all_submit_times_avg)
    # features_dict['submit_times_std'].append(all_submit_times_std)
    # features_dict['submit_times_max'].append(all_submit_times_max)
    # features_dict['total_syth_score_avg'].append(total_syth_score_avg)
    # features_dict['total_syth_score_std'].append(total_syth_score_std)
    # features_dict['all_memory_avg'].append(all_memory_avg)
    # features_dict['all_timeconsume_avg'].append(all_timeconsume_avg)
    # features_dict['all_memory_std'].append(all_memory_std)
    # features_dict['all_timeconsume_std'].append(all_timeconsume_std)
    # features_dict['state_ae_percentage'].append(state_counts['ae'])
    # features_dict['state_e_percentage'].append(state_counts['e'])
    # features_dict['state_pc_percentage'].append(state_counts['pc'])
    # features_dict['state_ac_percentage'].append(state_counts['ac'])
            if class_id == "all":
                query = f"""
                SELECT student_id, x, y, z, cluster_label, total_score, title_counts,time_difference_mean, time_split_0_percentage, time_split_1_percentage,time_split_2_percentage,
                submit_times_avg,submit_times_max,total_syth_score_avg,all_memory_avg,all_timeconsume_avg,state_ae_percentage,state_e_percentage,state_pc_percentage,state_ac_percentage
                FROM students_features_reprocess_vis
                """
            else:
                query = f"""
                SELECT student_id, x, y, z, cluster_label, total_score, title_counts,time_difference_mean, time_split_0_percentage, time_split_1_percentage,time_split_2_percentage,
                    submit_times_avg,submit_times_max,total_syth_score_avg,all_memory_avg,all_timeconsume_avg,state_ae_percentage,state_e_percentage,state_pc_percentage,state_ac_percentage
                FROM students_features_reprocess_vis where class = "{class_id}"
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
    
    def get_students_vis_data_2d(self, class_id, method):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            x_name = "x_" + method
            y_name = "y_" + method
            class_label_name = "cluster_label_" + method
            query = f"""
            SELECT student_id, {x_name}, {y_name}, {class_label_name}, total_score, title_counts,time_difference_mean, time_split_0_percentage, time_split_1_percentage,time_split_2_percentage,
                submit_times_avg,submit_times_max,total_syth_score_avg,all_memory_avg,all_timeconsume_avg,state_ae_percentage,state_e_percentage,state_pc_percentage,state_ac_percentage
            FROM students_features_reprocess_vis_2d_aa where class = "{class_id}"
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
# title_counts,time_difference_mean, time_split_0_percentage, time_split_1_percentage,time_split_2_percentage,
#                 submit_times_avg,submit_times_max,total_syth_score_avg,all_memory_avg,all_timeconsume_avg,state_ae_percentage,state_e_percentage,state_pc_percentage,state_ac_percentage
        reformatted_data = [[item['student_id'], item['x'], item['y'], item['z'], item['cluster_label'], item['total_score'], item['title_counts'], 
                             item['time_difference_mean'], item['time_split_0_percentage'], item['time_split_1_percentage'], item['time_split_2_percentage'], 
                             item['submit_times_avg'], item['submit_times_max'], item['total_syth_score_avg'], item['all_memory_avg'], item['all_timeconsume_avg'], item['state_ae_percentage'], item['state_e_percentage'], item['state_pc_percentage'], item['state_ac_percentage']] for item in students_data]
        reformatted_data_json = { 'data': reformatted_data }
        return reformatted_data_json
    
        # 格式化成需要数据
    def reformat_student_data_2d(self, students_data, method):
        x_name = "x_" + method
        y_name = "y_" + method
        cluster_label_name = "cluster_label_" + method
# title_counts,time_difference_mean, time_split_0_percentage, time_split_1_percentage,time_split_2_percentage,
#                 submit_times_avg,submit_times_max,total_syth_score_avg,all_memory_avg,all_timeconsume_avg,state_ae_percentage,state_e_percentage,state_pc_percentage,state_ac_percentage
        reformatted_data = [[item['student_id'], item[x_name], item[y_name], item[cluster_label_name], item['total_score'], item['title_counts'], 
                             item['time_difference_mean'], item['time_split_0_percentage'], item['time_split_1_percentage'], item['time_split_2_percentage'], 
                             item['submit_times_avg'], item['submit_times_max'], item['total_syth_score_avg'], item['all_memory_avg'], item['all_timeconsume_avg'], item['state_ae_percentage'], item['state_e_percentage'], item['state_pc_percentage'], item['state_ac_percentage']] for item in students_data]
        reformatted_data_json = { 'data': reformatted_data }
        return reformatted_data_json

    def data_to_json(self, data):
        return json.dumps(data, indent=4)

# 使用示例
if __name__ == "__main__":
    
    # 创建Parallel类的实例，指定本地数据库连接信息
    scater = Scater(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    students_data = scater.get_students_vis_data()
    reformatted_data_json = scater.reformat_student_data(students_data)
    data_json = scater.data_to_json(reformatted_data_json)
    # print(data_json)
    
