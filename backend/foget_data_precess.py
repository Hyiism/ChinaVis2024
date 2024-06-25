"""
计算学生的做题的时间复杂度 空间复杂度 的分布情况

"""
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
import random
from datetime import datetime

# 固定随机数种子
seed = 42
np.random.seed(seed)


# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

# 预先读取所有数据，避免在循环中频繁查询数据库
query = """
        SELECT *
        FROM `forget_tool` 
        ORDER BY `student_id`, `formatted_time` ;
    """
all_submit_record_df = pd.read_sql_query(query, con=engine)\

student_ids = all_submit_record_df['student_ID'].unique()

# 定义特征字典
features_dict = {
    'student_id': [],
    'knowledge_id': [],
    'formatted_time': [],
    'time_diff': [],
    'mean_score': [],
    'k': [],
}
k0 = 1
alpha = 2.5
Emax = 4

# 对每个学生分别进行计算
for student_id in tqdm(student_ids, desc="Processing titles"):

    # 获取此学生的所有提交记录
    student_data = all_submit_record_df[all_submit_record_df['student_ID'] == student_id]

    # 对此学生做过的所有知识点进行处理
    knowlede_ids = student_data['knowledge'].unique()

    for knowlede_id in knowlede_ids:

        # 获取此学生在此知识点下的所有提交记录并且按照时间排序
        knowlede_student_data = student_data[student_data['knowledge'] == knowlede_id].sort_values(by='formatted_time')
        # print(knowlede_student_data)
        # 按照formatted_time分组 对每个分组统计记录数量以及score的平均值
        kno_cal = knowlede_student_data.groupby('formatted_time').agg({'score': ['mean', 'count']})
        # 将上面查询到的formatted_time mean count 保存到字典中

        # 第一个数据的formatted_time 作为0点，后面的时间减去第一个formatted_time
        time0 = datetime.strptime(kno_cal.index[0], '%Y-%m-%d')

        # # 纯用来计算Emax
        # mean_score_list = []
        # for index, row in kno_cal.iterrows():
        #     mean_score_list.append(row['score']['mean'])
        # Emax = max(mean_score_list)

        inderCal_list = []
        for index, row in kno_cal.iterrows():
            Ei = row['score']['mean']
            if Ei == 0:
                Ei = 0.001
            innerCal = 1-alpha*(Ei/Emax)
            inderCal_list.append(innerCal)

        cnt = 0
        for index, row in kno_cal.iterrows():
            features_dict['student_id'].append(student_id)
            features_dict['knowledge_id'].append(knowlede_id)
            # index转化为时间格式
            index = datetime.strptime(index, '%Y-%m-%d')
            features_dict['formatted_time'].append(index)
            # 将features_dict['formatted_time']中的时间转化为时间格式
            features_dict['time_diff'].append((index - time0).days)

            features_dict['mean_score'].append(row['score']['mean'])

            # 根据这次的mean_score来计算k值 第一天对应的k值为1
            # 判断当前row是不是第一条数据
            if (cnt == 0):
                features_dict['k'].append(k0)
            else:
                # 计算k值
                # Ei = row['score']['mean']
                # 将inderCal_list中的值 从第一条数据开始乘到第cnt位置
                innerCal_i = inderCal_list[1]
                i = 2
                while i <= cnt:
                    innerCal_i *= inderCal_list[i]
                    i = i + 1
                k = k0 * innerCal_i
                features_dict['k'].append(k)

            cnt = cnt+1


        # print(features_dict)

# 创建DataFrame
features_df = pd.DataFrame(features_dict)
features_df = features_df.dropna(axis=0, how='any')
# 保存 DataFrame 为 CSV 文件
# features_df.to_csv('data.csv', index=False)  # 如果不想保存索引，可以将参数 index 设置为 False
# 将最终的 DataFrame 保存到数据库中
features_df.to_sql(name='forget_data_all_2.5', con=engine, if_exists='replace', index=False)
print("Data saved to the database successfully.")
# 打印DataFrame
print(features_df)