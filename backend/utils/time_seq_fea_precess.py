"""
以每天为单位 提取每个学生 每天的做题信息 作为时序特征:

1. 提交时间相关特征
    平均提交时间间隔：每个学生在做每道题的时候会多次提交，计算当天所有做题记录的平均提交时间间隔。
    提交的时间段分布：先构造函数判断每道题目的提交时间段，计算每个学生早 中 下 晚 的提交百分比，即计算当天每次提交得到[早 早 中 中 晚 晚],然后对所有题目合并出[早 早 中 中 晚 晚....],再统计比例；
    
2. 得分相关特征
    平均得分：计算当天学生所有做题的平均纸面得分。
。
3. 提交次数相关特征
    提交次数：计算学生当天的提交次数


4. 题目状态相关特征
    各状态比例：计算当天学生各种状态（正确、错误、部分正确等）的比例。有状态：Absoulutly Error, error1-error9, partial correct, Absoulutly correct，我们算这四种状态的比例。同样每题目构建一个列表，题目循环时列表相加，最后统计比例。

构建出这么多特征后，我们可以使用时序算法进行映射，得到的是时序数据；再使用之前的各种平均数据作为静态数据，拼接两种数据作为特征进行分类任务！也可以进行聚类任务！

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
    ORDER BY `student_ID`, `time`;
"""
all_submit_record_df = pd.read_sql_query(query, con=engine).drop('id', axis=1)
all_submit_record_df['date'] = pd.to_datetime(all_submit_record_df['time'], unit='s').dt.date
all_submit_record_df['time'] = pd.to_numeric(all_submit_record_df['time'], errors='coerce')
all_submit_record_df['score'] = pd.to_numeric(all_submit_record_df['score'], errors='coerce')
all_submit_record_df['memory'] = pd.to_numeric(all_submit_record_df['memory'], errors='coerce')
all_submit_record_df['timeconsume'] = pd.to_numeric(all_submit_record_df['timeconsume'], errors='coerce')

# 转换状态名称
state_mapping = {
    'Absoulutly_Error': 'ae',
    'Absolutely_Correct': 'ac',
    'Partially_Correct': 'pc',
    'Error1': 'e',
    'Error2': 'e',
    'Error3': 'e',
    'Error4': 'e',
    'Error5': 'e',
    'Error6': 'e',
    'Error7': 'e',
    'Error8': 'e',
    'Error9': 'e'
}
all_submit_record_df['state'] = all_submit_record_df['state'].map(state_mapping)
student_ids = all_submit_record_df['student_ID'].unique()

# 定义特征字典
features_dict = {
    'student_id': [],
    # 'time': [],
    'date': [],
    'time_difference_mean': [],
    'time_split_0_percentage': [],
    'time_split_1_percentage': [],
    'time_split_2_percentage': [],
    'submit_times': [],
    'total_syth_score_avg': [],
    'all_memory_avg': [],
    'all_timeconsume_avg': [],
    'state_ae_percentage': [],
    'state_e_percentage': [],
    'state_pc_percentage': [],
    'state_ac_percentage': []
}


# 遍历每个学生，对每个学生进行操作！
for student_id in tqdm(student_ids, desc="Processing students"):

    # 获取一个学生的提交记录
    student_data = all_submit_record_df[all_submit_record_df['student_ID'] == student_id]

    # student_all_timeconsume_avg_list = []
    # time_difference_mean_list = []

    # 针对当前学生，按照日期进行分组，再计算每天的统计数据
    # date为日期 date_data为当天的所有提交记录
    for date, date_data in student_data.groupby('date'):

        features_dict['student_id'].append(student_id)
        features_dict['date'].append(date)

        # 计算平均提交时间间隔
        # 如果只提交了一次，那么时间间隔为0
        time_difference_mean = date_data['time'].diff().mean()
        if np.isnan(time_difference_mean):
            time_difference_mean = 0
        # time_difference_mean_list.append(time_difference_mean)
        features_dict['time_difference_mean'].append(time_difference_mean)
        # print(time_difference_mean)

        # 计算提交时间段分布比例
        time_split_counts = date_data['time'].apply(time_split).value_counts(normalize=True)
        for i in range(3):
            features_dict[f'time_split_{i}_percentage'].append(time_split_counts.get(i, 0))
        # print(time_split_counts)

        # 计算当天的提交次数
        submit_times = len(date_data)
        features_dict['submit_times'].append(submit_times)
        # print(submit_times)

        # 计算当天的平均综合得分
        total_syth_score_avg = date_data['score'].mean()
        features_dict['total_syth_score_avg'].append(total_syth_score_avg)
        # print(total_syth_score_avg)

        # 计算当天的平均内存消耗
        all_memory_avg = date_data['memory'].mean()
        features_dict['all_memory_avg'].append(all_memory_avg)
        # print(all_memory_avg)

        # 计算当天的平均时间复杂度消耗
        all_timeconsume_avg = date_data['timeconsume'].mean()
        if np.isnan(all_timeconsume_avg):
            all_timeconsume_avg = 0
        features_dict['all_timeconsume_avg'].append(all_timeconsume_avg)
        # 每个学生存一下每一天的时间平局时间复杂度消耗，后去用最大值填充空白值
        # student_all_timeconsume_avg_list.append(all_timeconsume_avg)
        # print(all_timeconsume_avg)

        # 计算当天的状态比例
        state_counts = date_data['state'].value_counts(normalize=True)
        for state in ['ae', 'e', 'pc', 'ac']:
            features_dict[f'state_{state}_percentage'].append(state_counts.get(state, 0))
        # print(state_counts)

    # 日期为2023.8.31-2024.1.25,对每个学生没有出现的日期进行填充
    # 日期范围
    start_date = pd.to_datetime('2023-08-31')
    end_date = pd.to_datetime('2024-01-25')
    date_range = pd.date_range(start=start_date, end=end_date)
    existing_dates = student_data['date'].unique()
    # 遍历时间范围内的所有日期
    for the_date in date_range:
        if the_date.date() not in existing_dates:
            features_dict['student_id'].append(student_id)
            # features_dict['time'].append(0)
            features_dict['date'].append(the_date.date())
            # 还是让模型自己学吧
            # features_dict['time_difference_mean'].append(max(time_difference_mean_list))
            features_dict['time_difference_mean'].append(0)
            features_dict['time_split_0_percentage'].append(0)
            features_dict['time_split_1_percentage'].append(0)
            features_dict['time_split_2_percentage'].append(0)
            features_dict['submit_times'].append(0)
            features_dict['total_syth_score_avg'].append(0)
            # 填0 让模型自己学
            features_dict['all_memory_avg'].append(0)
            # 填0 让模型自己学
            # features_dict['all_timeconsume_avg'].append(max(student_all_timeconsume_avg_list))
            features_dict['all_timeconsume_avg'].append(0)
            features_dict['state_ae_percentage'].append(0)
            features_dict['state_e_percentage'].append(0)
            features_dict['state_pc_percentage'].append(0)
            features_dict['state_ac_percentage'].append(0)


# 将特征字典转换为 DataFrame
features_df = pd.DataFrame(features_dict)
features_df.to_sql(name='time_seq_data', con=engine, if_exists='replace', index=False)
print(features_df)
# print(features_df.isnull().any(axis=0))



