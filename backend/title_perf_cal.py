"""
计算学生的做题的时间复杂度 空间复杂度 的分布情况

"""
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
import random

# 固定随机数种子
seed = 42
np.random.seed(seed)


# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

# 预先读取所有数据，避免在循环中频繁查询数据库
query = """
    SELECT * FROM `submit_record_ac` 
    ORDER BY `student_ID`, `title_ID`, `timeconsume`, `memory`;
"""
all_submit_record_ac_df = pd.read_sql_query(query, con=engine).drop('class', axis=1).drop('state', axis=1).drop('score', axis=1).drop('method', axis=1)

# 每个学生做每个题目的记录只保留timeconsume最小的那条！！
# 根据student_ID和class进行分组，并选择timeconsume最小的记录
all_submit_record_ac_df = all_submit_record_ac_df.loc[all_submit_record_ac_df.groupby(['student_ID', 'title_ID'])['timeconsume'].idxmin()]
# print(all_submit_record_ac_df)

student_ids = all_submit_record_ac_df['student_ID'].unique()
title_ids = all_submit_record_ac_df['title_ID'].unique()


# 定义特征字典
features_dict = {
    'student_id': [],
    'title_id': [],
    'timeconsume': [],
    'memory': [],
    'timeconsume_1_per': [],
    'timeconsume_2_per': [],
    'timeconsume_3_per': [],
    'timeconsume_4_per': [],
    'timeconsume_5_per': [],
    'timeconsume_6_per': [],
    'timeconsume_7_per': [],
    'timeconsume_8_per': [],
    'timeconsume_9_per': [],
    'timeconsume_10_per': [],
    'timeconsume_>10_per': [],
    'memory_160_235_per': [],
    'memory_236_310_per': [],
    'memory_311_385_per': [],
    'memory_386_460_per': [],
    'memory_461_535_per': [],
    'memory_536_610_per': [],
    'memory_611_685_per': [],
    'memory_686_760_per': [],
    'memory_761_835_per': [],
    'memory_836_910_per': [],
    'memory_911_1980_per': [],
    'memory_>1980_per': [],
    'time_beat': [],
    'memory_beat': []
}

# 每个题目单独统计数据！
for title_id in tqdm(title_ids, desc="Processing titles"):

    # 获取此题目的所有学生的提交记录
    title_data = all_submit_record_ac_df[all_submit_record_ac_df['title_ID'] == title_id]
    # 计算此题目所有学生的做题时间复杂度和空间复杂度的分布情况
    # 此题目一共有多少条数据
    title_submit_times = title_data.shape[0]

    # 此题目的时间复杂度从小到大排序列表
    title_data_timecon = title_data.sort_values(by='timeconsume').reset_index(drop=True)
    # 此题目的空间复杂度从小到大排序列表
    title_data_memory = title_data.sort_values(by='memory').reset_index(drop=True)

    # 做此题目的所有学生列表
    title_student_ids = title_data['student_ID'].unique()

    for student_id in title_student_ids:
        # 获取此学生的提交记录
        student_title_data = title_data[title_data['student_ID'] == student_id]

        features_dict['student_id'].append(student_id)
        features_dict['title_id'].append(title_id)
        features_dict['timeconsume'].append(student_title_data['timeconsume'].values[0])
        features_dict['memory'].append(student_title_data['memory'].values[0])

        # 此题目的时间复杂度分布 timeconsume 值记录到对应特征中
        features_dict["timeconsume_1_per"].append(title_data[(title_data['timeconsume'] == 1)].shape[0] / title_submit_times)
        features_dict["timeconsume_2_per"].append(title_data[(title_data['timeconsume'] == 2)].shape[0] / title_submit_times)
        features_dict["timeconsume_3_per"].append(title_data[(title_data['timeconsume'] == 3)].shape[0] / title_submit_times)
        features_dict["timeconsume_4_per"].append(title_data[(title_data['timeconsume'] == 4)].shape[0] / title_submit_times)
        features_dict["timeconsume_5_per"].append(title_data[(title_data['timeconsume'] == 5)].shape[0] / title_submit_times)
        features_dict["timeconsume_6_per"].append(title_data[(title_data['timeconsume'] == 6)].shape[0] / title_submit_times)
        features_dict["timeconsume_7_per"].append(title_data[(title_data['timeconsume'] == 7)].shape[0] / title_submit_times)
        features_dict["timeconsume_8_per"].append(title_data[(title_data['timeconsume'] == 8)].shape[0] / title_submit_times)
        features_dict["timeconsume_9_per"].append(title_data[(title_data['timeconsume'] == 9)].shape[0] / title_submit_times)
        features_dict["timeconsume_10_per"].append(title_data[(title_data['timeconsume'] == 10)].shape[0] / title_submit_times)
        features_dict["timeconsume_>10_per"].append(title_data[(title_data['timeconsume'] > 10)].shape[0] / title_submit_times)
        
        # 此题目的空间复杂度分布 memory-235之间就记录到memory_160_235_per
        features_dict["memory_160_235_per"].append(title_data[(title_data['memory'] >= 160) & (title_data['memory'] <= 235)].shape[0] / title_submit_times)
        features_dict["memory_236_310_per"].append(title_data[(title_data['memory'] >= 236) & (title_data['memory'] <= 310)].shape[0] / title_submit_times)
        features_dict["memory_311_385_per"].append(title_data[(title_data['memory'] >= 311) & (title_data['memory'] <= 385)].shape[0] / title_submit_times)
        features_dict["memory_386_460_per"].append(title_data[(title_data['memory'] >= 386) & (title_data['memory'] <= 460)].shape[0] / title_submit_times)
        features_dict["memory_461_535_per"].append(title_data[(title_data['memory'] >= 461) & (title_data['memory'] <= 535)].shape[0] / title_submit_times)
        features_dict["memory_536_610_per"].append(title_data[(title_data['memory'] >= 536) & (title_data['memory'] <= 610)].shape[0] / title_submit_times)
        features_dict["memory_611_685_per"].append(title_data[(title_data['memory'] >= 611) & (title_data['memory'] <= 685)].shape[0] / title_submit_times)
        features_dict["memory_686_760_per"].append(title_data[(title_data['memory'] >= 686) & (title_data['memory'] <= 760)].shape[0] / title_submit_times)
        features_dict["memory_761_835_per"].append(title_data[(title_data['memory'] >= 761) & (title_data['memory'] <= 835)].shape[0] / title_submit_times)
        features_dict["memory_836_910_per"].append(title_data[(title_data['memory'] >= 836) & (title_data['memory'] <= 910)].shape[0] / title_submit_times)
        features_dict["memory_911_1980_per"].append(title_data[(title_data['memory'] >= 911) & (title_data['memory'] <= 1980)].shape[0] / title_submit_times)
        features_dict["memory_>1980_per"].append(title_data[(title_data['memory'] > 1980)].shape[0] / title_submit_times)
      

        # 查看当前提交记录时间复杂度排名
        time_rank = title_data_timecon[title_data_timecon['student_ID'] == student_id].index[0] + 1
        time_beat = 1 - (time_rank / title_submit_times)
        
        # 查看当前提交记录空间复杂度排名
        memory_rank = title_data_memory[title_data_memory['student_ID'] == student_id].index[0] + 1
        memory_beat = 1 - (memory_rank / title_submit_times)
        
        features_dict['time_beat'].append(time_beat)
        features_dict['memory_beat'].append(memory_beat)

        # 另外为了显示更加好看，我们在title_data_memory提取当前记录空间复杂度 的前面5个比其小的记录 和后面5个比其大的记录

# 创建DataFrame
features_df = pd.DataFrame(features_dict)
# 保存 DataFrame 为 CSV 文件
# features_df.to_csv('data.csv', index=False)  # 如果不想保存索引，可以将参数 index 设置为 False
# 将最终的 DataFrame 保存到数据库中
# features_df.to_sql(name='student_submit_ac_vis', con=engine, if_exists='replace', index=False)
print("Data saved to the database successfully.")
# 打印DataFrame
print(features_df)