import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# 读取数据
features_df_tongji = pd.read_csv("student_embeddings_tongji.csv")

# 删除不需要的列
ai_data = features_df_tongji.drop(['time_difference_std', 'submit_times_std', 'total_syth_score_std', 'all_memory_std', 'all_timeconsume_std'], axis=1)

# 对特定列计算班级内均值和所有人均值
features_cal = ['title_counts', 'time_difference_mean', 'submit_times_avg', 'submit_times_max', 'total_syth_score_avg', 'all_memory_avg', 'all_timeconsume_avg', 'total_score']
for feat in features_cal:
    ai_data[feat + '_class_mean'] = ai_data.groupby('class')[feat].transform('mean')
    ai_data[feat + '_all_mean'] = ai_data[feat].mean()

# 计算total_score击败了班级内学生的比例
ai_data['total_score_class_rank'] = ai_data.groupby('class')['total_score'].rank(pct=True)

# 计算total_score击败了所有学生的比例
ai_data['total_score_all_rank'] = ai_data['total_score'].rank(pct=True)

# print(ai_data)

# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

# 将数据保存到数据库
ai_data.to_sql('ai_data', con=engine, if_exists='replace', index=False)
