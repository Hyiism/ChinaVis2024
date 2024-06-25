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
        SELECT `student_ID`, `time`, `state`, `score`, `title_ID`, `method`, `memory`, `timeconsume` 
        FROM `submit_record` 
        ORDER BY `time` ;
    """
all_submit_record_df = pd.read_sql_query(query, con=engine)\

student_ids = all_submit_record_df['student_ID'].unique()

# 时间列表处理
def adjust_time_list(start_idx, lst):
    # 找到第一个差值大于5400的位置,一个半小时
    next_start_index = None
    for i in range(start_idx + 1, len(lst)):
        if lst[i] - lst[i - 1] > 5400:  # 认为他在休息
            next_start_index = i
            break

    # 如果没有找到这样的差值，处理完成
    if next_start_index is None:
        return lst

    # 处理当前段的时间
    base_time = lst[next_start_index]
    adjusted_times = [time - base_time for time in lst[next_start_index:]]
    adjusted_times = [time + 300 + lst[next_start_index - 1] for time in adjusted_times]

    # 合并结果并递归处理
    new_list = lst[:next_start_index] + adjusted_times
    return adjust_time_list(next_start_index, new_list)

def process_time_list(time_list):
    return adjust_time_list(0, time_list)

# 定义特征字典
features_dict = {
    'student_id': [],
    'title_id': [],
    'state': [],
    'time': [],
    'time_consume': [],
    'memory_consume': [],
    'errortype': [],
    'method': [],
    # 提交时间戳 用来数据库查询排序用
    'original_time': []
}

# 对每个学生分别进行计算
# 每个题目单独统计数据！
for student_id in tqdm(student_ids, desc="Processing titles"):

    # 获取此学生的所有提交记录
    student_data = all_submit_record_df[all_submit_record_df['student_ID'] == student_id]



    # 对此学生做过的每道题目进行统计状态
    title_ids = student_data['title_ID'].unique()

    for title_id in title_ids:

        # 获取此学生在此题目的做题记录
        title_student_data = student_data[student_data['title_ID'] == title_id].reset_index(drop=True)
        # print(title_student_data)

        # 在这里处理一下时间范围，让第一条记录的时间为0 后面的时间为相对时间
        time_list = title_student_data['time'].astype(int)
        time_list_new = [i - time_list.min() for i in time_list]
        # 得到新的时间列表 类似于 adjusted_time_list [0, 300, 306, 368, 395]；但是第二次递归调用就会出问题
        adjusted_time_list = process_time_list(time_list_new)
        # 将adjusted_time_list转化为分钟形式的字符串列表
        adjusted_time_list_new = [f"{time // 60}:{time % 60}" for time in adjusted_time_list]

        # 对每一条记录进行处理 每一条记录都对应一个统计信息 放入数据库后面查询
        for index, row in title_student_data.iterrows():
            # 将学生id 题目id放入此条记录
            features_dict['student_id'].append(student_id)
            features_dict['title_id'].append(title_id)
            # 处理state到所需格式
            state_mapping = {
                'Absolutely_Error': 'ae',
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
            features_dict['state'].append(state_mapping[row['state']])

            # 将前面计算的时间列表按照index放入字典内
            features_dict['time'].append(adjusted_time_list_new[index])
            # 将时间复杂度和空间复杂度放入字典内
            features_dict['time_consume'].append(row['timeconsume'])
            features_dict['memory_consume'].append(row['memory'])
            # 映射错误类型 如果为Error1 到Error9 则映射到error1 到 error9 否则设为null
            if row['state'] == 'Error1' or row['state'] == 'Error2' or row['state'] == 'Error3' or row['state'] == 'Error4' or row['state'] == 'Error5' or row['state'] == 'Error6' or row['state'] == 'Error7' or row['state'] == 'Error8' or row['state'] == 'Error9':
                features_dict['errortype'].append(f"error{int(row['state'][-1])}")
            else:
                features_dict['errortype'].append('null')

            # 将method放入字典内
            features_dict['method'].append(row['method'])
            # 将原始时间戳放入字典内
            features_dict['original_time'].append(row['time'])


# 创建DataFrame
features_df = pd.DataFrame(features_dict)
# 保存 DataFrame 为 CSV 文件
# features_df.to_csv('data.csv', index=False)  # 如果不想保存索引，可以将参数 index 设置为 False
# 将最终的 DataFrame 保存到数据库中
features_df.to_sql(name='student_title_process', con=engine, if_exists='replace', index=False)
print("Data saved to the database successfully.")
# 打印DataFrame
print(features_df)