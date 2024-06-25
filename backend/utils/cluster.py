"""
从学生做38道题目的提交记录中 提取有用特征 用于学生聚类:

1. 提交时间相关特征
    平均提交时间间隔：每个学生在做每道题的时候会多次提交，计算每题的平均提交间隔，再计算38道题目的平均提交间隔；
    提交的时间段分布：先构造函数判断每道题目的提交时间段，计算每个学生早 中 下 晚 的提交百分比，即计算每次提交得到[早 早 中 中 晚 晚],然后对所有题目合并出[早 早 中 中 晚 晚....],再统计比例；
    
    提交时间的标准差：计算每个学生提交时间间隔的标准差。
2. 得分相关特征
    平均得分：计算每个学生38道题目的平均纸面得分。
    得分标准差：计算每个学生得分的标准差

    最高得分和最低得分：计算每个学生的最高和最低纸面得分。
    得分趋势：分析每个学生的得分趋势（如前20道题目与后18道题目的平均得分变化）。
。
3. 提交次数相关特征
    平均提交次数：计算每个学生每道题目的平均提交次数。

    提交次数的标准差：计算每个学生提交次数的标准差。
    最多提交次数和最少提交次数：计算每个学生提交次数的最大值和最小值。

4. 题目状态相关特征
    各状态比例：计算每个学生各种状态（正确、错误、部分正确等）的比例。有状态：Absoulutly Error, error1-error9, partial correct, Absoulutly correct，我们算这四种状态的比例。同样每题目构建一个列表，题目循环时列表相加，最后统计比例。

    状态转移矩阵：计算每个学生在不同状态之间的转移频率。

"""
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap.umap_ as umap
import random

# 固定随机数种子
seed = 42
np.random.seed(seed)

def time_split(timestamp):
    # 转换时间戳为 datetime 对象
    timestamp = pd.to_datetime(timestamp, unit='s')

    # 获取小时信息
    hour = timestamp.hour

    # 判断时间段
    if 0 <= hour < 12:
        period = 0
    elif 12 <= hour < 18:
        period = 1
    else:
        period = 2
    
    return period



# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

# 预先读取所有数据，避免在循环中频繁查询数据库
query = """
    SELECT * FROM `submit_record` 
    ORDER BY `student_ID`, `title_ID`, `time`;
"""
all_submit_record_df = pd.read_sql_query(query, con=engine)
student_ids = all_submit_record_df['student_ID'].unique()

# 定义一个空的列表，用于存储所有行的数据
df_rows = []

# 定义特征字典
features_dict = {
    'student_id': [],
    'title_counts': [],
    'time_difference_mean': [],
    'time_difference_std': [],
    'time_split_0_percentage': [],
    'time_split_1_percentage': [],
    'time_split_2_percentage': [],
    'submit_times_avg': [],
    'submit_times_std': [],
    'submit_times_max': [],
    'total_syth_score_avg': [],
    'total_syth_score_std': [],
    'all_memory_avg': [],
    'all_timeconsume_avg': [],
    'all_memory_std': [],
    'all_timeconsume_std': [],
    'state_ae_percentage': [],
    'state_e_percentage': [],
    'state_pc_percentage': [],
    'state_ac_percentage': []
}


# 使用 tqdm 包裹外层循环以显示进度条
for student_id in tqdm(student_ids, desc="Processing students"):
    
    all_time_difference = 0
    all_time_split_list = []
    submit_times_more_than_one = 0
    all_submit_times_list = []
    all_time_difference_list = []
    total_syth_score = 0
    total_syth_max_score_list = []
    total_syth_score_list = []
    all_memory_list = []
    all_timeconsume_list = []
    all_state_list = []

    # 获取一个学生的提交记录
    student_data = all_submit_record_df[all_submit_record_df['student_ID'] == student_id]
    student_title_ids = student_data['title_ID'].unique()

    for title_id in student_title_ids:

        submit_record_df = student_data[student_data['title_ID'] == title_id]
        submit_record_df['time'] = pd.to_numeric(submit_record_df['time'], errors='coerce')

        # 本题提交次数
        all_submit_times_list.append(submit_record_df.shape[0])

        # print(submit_record_df.shape)
        previous_time = submit_record_df['time'].shift()
        # 计算时间间隔
        time_difference = submit_record_df['time'] - previous_time
        if submit_record_df.shape[0] > 1:
            submit_times_more_than_one += 1
            time_difference_avg = time_difference.mean()
        else:
            time_difference_avg = 0
        # print("每题的平均提交时间间隔")
        # print(time_difference_avg)

        all_time_difference_list.append(time_difference_avg)

        all_time_split_list += submit_record_df['time'].apply(time_split).tolist()
        # print("每题的时间段分布")
        # print(all_time_split_list)

        # 计算总纸面得分，最高得分，最低得分
        submit_record_df['score'] = pd.to_numeric(submit_record_df['score'], errors='coerce')
        # 先获得纸面得分列表
        # 应该获得此题的最高得分，再求 所有题目的平均最高得分
        total_syth_max_score_list += [max(submit_record_df['score'].tolist())]

        # total_syth_score += submit_record_df['score']

        submit_record_df['memory'] = pd.to_numeric(submit_record_df['memory'], errors='coerce')
        submit_record_df['timeconsume'] = pd.to_numeric(submit_record_df['timeconsume'], errors='coerce')
        # 空间复杂度列表
        all_memory_list += submit_record_df['memory'].tolist()
        # 时间复杂度列表
        # 有的题目的时间复杂度是 '--'  用99代替
        submit_record_df['timeconsume'].fillna(99, inplace=True)
        all_timeconsume_list += submit_record_df['timeconsume'].tolist()

        # 计算题目状态占比
        # 状态列表
        all_state_list += submit_record_df['state'].tolist()


    # 所做题目数量
    # print("所做题目数量")
    # print(len(student_title_ids))

    # 所有题目的平均提交次数,以及提交次数标准差
    if len(student_title_ids) == 0:
        all_submit_times_avg = 0
        time_difference_mean = 0
        counts = {0:0, 1:0, 2:0, 3:0}
        all_submit_times_std = 0
        all_submit_times_max = 0
        time_difference_std = 0

    else:
        # 平均提交次数以及标准差
        all_submit_times_avg = sum(all_submit_times_list) / len(student_title_ids)
        all_submit_times_std = np.std(all_submit_times_list)
        all_submit_times_max = max(all_submit_times_list)
        # all_submit_times_min = min(all_submit_times_list)
        # print("38道题目的平均提交次数")
        # print(all_submit_times_avg)
        # print("38道题目的最大提交次数")
        # print(all_submit_times_max)
        # print("38道题目的最小提交次数")
        # print(all_submit_times_min)

        # 计算所做的所有题目的平均提交时间间隔, 多于一次提交的题目的平均提交间隔; 如果是0次就间隔为0
        if submit_times_more_than_one == 0:
            time_difference_mean = 0
            time_difference_std = 0
        else:
            time_difference_mean = sum(all_time_difference_list) / submit_times_more_than_one
            time_difference_std = np.std(all_time_difference_list)
        # print("38道题目的平均提交时间间隔")
        # print(time_difference_mean)

        # 计算每个学生早 中 下 晚 的提交百分比
        counts = {0:0, 1:0, 2:0}
        for item in all_time_split_list:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1
        
        total_length = len(all_time_split_list)
        for key in counts.keys():
            counts[key] = counts[key] / total_length

        # print("提交时间段的分布") 
        # print(counts) #{0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25}

        # 计算每个学生的平均最高纸面得分，以及标准差
        total_syth_score_avg = sum(total_syth_max_score_list) / len(student_title_ids)
        total_syth_score_std = np.std(total_syth_max_score_list)

        # 平均时间复杂度和空间复杂度 以及标准差
        all_memory_avg = sum(all_memory_list) / len(all_memory_list)
        all_timeconsume_avg = sum(all_timeconsume_list) / len(all_timeconsume_list)
        all_memory_std = np.std(all_memory_list)
        all_timeconsume_std = np.std(all_timeconsume_list)

        # 计算每个学生ae e pc ac的提交百分比
        state_counts = {'ae':0, 'e':0, 'pc':0, 'ac':0}
        for item in all_state_list:
            if item == 'Absolutely_Correct':
                state_counts['ac'] += 1
            elif item == 'Partially_Correct':
                state_counts['pc'] += 1
            elif item == 'Absolutely_Error':
                state_counts['ae'] += 1
            else:
                state_counts['e'] += 1
        
        total_state_length = len(all_state_list)
        for key in state_counts.keys():
            state_counts[key] = state_counts[key] / total_state_length
        # print("状态分布")
        # print(state_counts)


    # 以 student_id 为键，填入各种特征值...
    features_dict['student_id'].append(student_id)
    features_dict['title_counts'].append(len(student_title_ids))
    features_dict['time_difference_mean'].append(time_difference_mean)
    features_dict['time_difference_std'].append(time_difference_std)
    features_dict['time_split_0_percentage'].append(counts[0])
    features_dict['time_split_1_percentage'].append(counts[1])
    features_dict['time_split_2_percentage'].append(counts[2])
    features_dict['submit_times_avg'].append(all_submit_times_avg)
    features_dict['submit_times_std'].append(all_submit_times_std)
    features_dict['submit_times_max'].append(all_submit_times_max)
    features_dict['total_syth_score_avg'].append(total_syth_score_avg)
    features_dict['total_syth_score_std'].append(total_syth_score_std)
    features_dict['all_memory_avg'].append(all_memory_avg)
    features_dict['all_timeconsume_avg'].append(all_timeconsume_avg)
    features_dict['all_memory_std'].append(all_memory_std)
    features_dict['all_timeconsume_std'].append(all_timeconsume_std)
    features_dict['state_ae_percentage'].append(state_counts['ae'])
    features_dict['state_e_percentage'].append(state_counts['e'])
    features_dict['state_pc_percentage'].append(state_counts['pc'])
    features_dict['state_ac_percentage'].append(state_counts['ac'])


# 创建DataFrame
features_df = pd.DataFrame(features_dict)
# 保存 DataFrame 为 CSV 文件
# features_df.to_csv('data.csv', index=False)  # 如果不想保存索引，可以将参数 index 设置为 False
# 将最终的 DataFrame 保存到数据库中
# features_df.to_sql(name='students_features_reprocess', con=engine, if_exists='replace', index=False)
print("Data saved to the database successfully.")
# 打印DataFrame
print(features_df)