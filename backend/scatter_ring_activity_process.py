"""
计算学生的做题的时间复杂度 空间复杂度 的分布情况

"""
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
import random
from sklearn.preprocessing import MinMaxScaler

# 固定随机数种子
seed = 42
np.random.seed(seed)


# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

# 预先读取所有数据，避免在循环中频繁查询数据库
query = """
    SELECT * FROM `student_activity_summary` 
    ORDER BY `student_ID`;
"""
all_student_activity_df= pd.read_sql_query(query, con=engine).drop('class', axis=1).drop('all_submit_times', axis=1)

# print(all_student_activity_df)

# 选择要归一化的列
columns_to_normalize = [f'{i:02d}_submit_times' for i in range(24)]
# 初始化MinMaxScaler
scaler = MinMaxScaler()
# 对选择的列进行最大最小归一化
all_student_activity_df[columns_to_normalize] = scaler.fit_transform(all_student_activity_df[columns_to_normalize])

# 将00_submit_times 到 23_submit_times的数据 按行进行最大最小归一化
# all_student_activity_df.iloc[:, 2:] = all_student_activity_df.iloc[:, 2:].apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)), axis=1)

print(all_student_activity_df)
all_student_activity_df.to_sql(name='student_activity_summary_norm', con=engine, if_exists='replace', index=False)