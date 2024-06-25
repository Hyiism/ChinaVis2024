"""
计算github打卡表中的活跃度等级 映射到颜色的深浅上，用提交次数排序成0 1 2 3四个等级 ß
"""

from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime

# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

# 预先读取所有数据，避免在循环中频繁查询数据库
query = """
    SELECT * FROM `submit_record` 
    ORDER BY `student_ID`, `time`;
"""
all_submit_record_df = pd.read_sql_query(query, con=engine).drop('id', axis=1).drop('state', axis=1).drop('score', axis=1).drop('method', axis=1).drop('memory', axis=1).drop('timeconsume', axis=1).drop('title_ID', axis=1)

# 将时间戳转换为日期
all_submit_record_df['date'] = pd.to_datetime(all_submit_record_df['time'], unit='s').dt.date

# 按student_ID和date分组，计算每组的最小和最大时间戳
all_submit_record_result = all_submit_record_df.groupby(['class', 'student_ID', 'date']).agg(
    start_time=('time', 'min'),
    end_time=('time', 'max')
).reset_index()
all_submit_record_result['start_time'] = pd.to_numeric(all_submit_record_result['start_time'], errors='coerce')
all_submit_record_result['end_time'] = pd.to_numeric(all_submit_record_result['end_time'], errors='coerce')
all_submit_record_result['time_difference'] = all_submit_record_result['end_time'] - all_submit_record_result['start_time']

# 计算每个学生每天的提交次数
daily_submission_counts = all_submit_record_df.groupby(['class', 'student_ID', 'date']).size().reset_index(name='submission_count')

# 将每日提交次数合并到all_submit_record_result
all_submit_record_result = pd.merge(all_submit_record_result, daily_submission_counts, on=['class', 'student_ID', 'date'])

# 计算每个学生的每天的活跃度评分 就只用提交次数算rank
# all_submit_record_result['activity_score'] = 0.9* all_submit_record_result['submission_count'] / max(all_submit_record_result['submission_count']) + 0.1* all_submit_record_result['time_difference'] / max(all_submit_record_result['time_difference'])
all_submit_record_result['activity_score'] = all_submit_record_result['submission_count']

# 计算每个学生的每天的活跃度评分等级
# 将活跃度评分进行排序，并计算分位数
all_submit_record_result['score_rank'] = all_submit_record_result.groupby('student_ID')['activity_score'].rank(pct=True)

# 根据分位数分配等级

all_submit_record_result['activity_level'] = pd.cut(all_submit_record_result['score_rank'],
                                                bins=[0, 1/4, 2/4, 3/4, 1],
                                                labels=[1, 2, 3, 4],
                                                include_lowest=True,
                                                right=True)

# 对所有没做题的空余时间进行0填充
# 将'date'列转换为日期时间类型，如果尚未转换
all_submit_record_result['date'] = pd.to_datetime(all_submit_record_result['date'])

# 定义你的时间范围
start_date = datetime(2023, 8, 27)
end_date = datetime(2024, 1, 25)

# 创建一个包含指定范围内所有日期的列表
date_range = pd.date_range(start=start_date, end=end_date)

# 创建一个用于存储结果的DataFrame
results = []

# 按student_ID分组处理
for student_id, group in all_submit_record_result.groupby('student_ID'):
    existing_dates = group['date'].dt.date.unique()  # 获取已有的唯一日期
    
    # 遍历时间范围内的所有日期
    for date in date_range:
        if date.date() not in existing_dates:
            # 创建一个新的行，设置默认值
            new_row = {
                'class': 0,  # 假设对于每个学生ID，'class'都是相同的
                'student_ID': student_id,
                'date': date.date(),
                'start_time': 0,
                'end_time': 0,
                'time_difference': 0,
                'submission_count': 0,
                'activity_score': 0,
                'score_rank': 0,  # 假设也要设置score_rank为0
                'activity_level': 0  # 假设也要设置activity_level为0
            }
            results.append(new_row)

# 将新生成的行添加到原始DataFrame中
if results:
    all_submit_record_result = pd.concat([all_submit_record_result, pd.DataFrame(results)], ignore_index=True)

# 确保'date'列仍然是日期时间类型
all_submit_record_result['date'] = pd.to_datetime(all_submit_record_result['date'])

all_submit_record_result.to_sql(name='students_time_level', con=engine, if_exists='replace', index=False)
# print(all_submit_record_result)