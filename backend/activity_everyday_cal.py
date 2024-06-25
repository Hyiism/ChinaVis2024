"""
计算每天 每小时的提交次数 并保存到数据库中 由此作为每小时的活跃度
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


# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

# 预先读取所有数据，避免在循环中频繁查询数据库
query = """
    SELECT `student_id`, `class`, `time` 
    FROM `submit_record` 
    ORDER BY `student_id`, `time`;
"""

all_submit_record_df = pd.read_sql_query(query, con=engine)
all_submit_record_df['day'] = pd.to_datetime(all_submit_record_df['time'], unit='s').dt.date
all_submit_record_df['time_detail'] = pd.to_datetime(all_submit_record_df['time'], unit='s').dt.time

# print(all_submit_record_df)

# 获取所有学生ID
student_ids = all_submit_record_df['student_id'].unique()

# 定义特征字典
features_dict = {
    'student_id': [],
    'class': [],
    'day': [],
    'time_detail': [],
    '00_submit_times': [],
    '01_submit_times': [],
    '02_submit_times': [],
    '03_submit_times': [],
    '04_submit_times': [],
    '05_submit_times': [],
    '06_submit_times': [],
    '07_submit_times': [],
    '08_submit_times': [],
    '09_submit_times': [],
    '10_submit_times': [],
    '11_submit_times': [],
    '12_submit_times': [],
    '13_submit_times': [],
    '14_submit_times': [],
    '15_submit_times': [],
    '16_submit_times': [],
    '17_submit_times': [],
    '18_submit_times': [],
    '19_submit_times': [],
    '20_submit_times': [],
    '21_submit_times': [],
    '22_submit_times': [],
    '23_submit_times': [],
    'all_submit_times': []

}

# 遍历每个学生，对每个学生进行操作！
for student_id in tqdm(student_ids, desc="Processing students"):

    # 获取一个学生的所有提交记录
    student_data = all_submit_record_df[all_submit_record_df['student_id'] == student_id]

    # 针对当前学生，按照日期进行分组，再计算每天的统计数据
    # date为日期 date_data为当天的所有提交记录
    for date, date_data in student_data.groupby('day'):

        features_dict['student_id'].append(student_id)
        features_dict['class'].append(date_data['class'].values[0])
        features_dict['day'].append(date_data['day'].values[0])
        features_dict['time_detail'].append(date_data['time_detail'].values[0])

        # 初始化每个小时的提交次数为0
        for hour in range(24):
            features_dict[f'{hour:02d}_submit_times'].append(0)
        
        # 计算当天 每个小时的提交次数
        # 查看每次提交所在的小时
        hour = date_data['time_detail'].apply(lambda x: x.hour)
        # 统计每个小时的提交次数
        hour_counts = hour.value_counts()
        
        # 将统计结果填写到对应的列中
        for hr, count in hour_counts.items():
            features_dict[f'{hr:02d}_submit_times'][-1] = count
        
        # 统计当天的总提交次数
        all_submit_times = len(date_data)
        features_dict['all_submit_times'].append(all_submit_times)

# 将特征字典转换为 DataFrame
features_df = pd.DataFrame(features_dict)
features_df.to_sql(name='submit_times_every_hour', con=engine, if_exists='replace', index=False)
print(features_df)
# print(features_df.isnull().any(axis=0))
