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

# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

features_tongji_df = pd.read_csv('./student_embeddings_tongji.csv').drop('class', axis=1)
seq_cluster_df = pd.read_csv('./features_vis_seq.csv')

# 将模型学习到的嵌入的聚类标签与学生统计数据中的学生特征按照student_id进行拼接 后续分析不同聚类标签的学生特征
features_tongji_df = features_tongji_df.set_index('student_id')
seq_cluster_df = seq_cluster_df.set_index('student_id')
# 按照 student_id 进行拼接
feat_label_analy_df = pd.concat([features_tongji_df, seq_cluster_df], axis=1, join='inner').reset_index()
print(feat_label_analy_df.columns)

feat_label_analy_df.to_sql('features_label_analy', con=engine, if_exists='replace', index=False)


# 1. 分析不同聚类标签的学生特征, 比较有意义的特征有: time_split_2_percentage,submit_times_avg,state_ae_percentagetotal_score
features = [ "title_counts","time_difference_mean","time_split_0_percentage","time_split_2_percentage","submit_times_avg","total_syth_score_avg","all_memory_avg","all_timeconsume_avg","state_ae_percentage","state_e_percentage","state_pc_percentage","state_ac_percentage","total_score"]
for feature in features:
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='cluster_label_tsne', y=feature, data=feat_label_analy_df)
    plt.title(f'{feature} Distribution of Different Clusters')
    plt.show()

# 2. 分析不同特征之间的关系，比如 time_split_2_percentage 和 total_score 之间的关系，以及submit_times_avg 和 total_score 之间的关系等等。
plt.figure(figsize=(12, 6))
sns.scatterplot(x='time_split_2_percentage', y='total_score', hue='cluster_label_tsne', data=feat_label_analy_df)
plt.title('time_split_2_percentage vs total_score')
plt.show()
# 发现平均提交次数少的学生分数高，且提交次数高的很多都是cluster_label_tsne=3的学生
plt.figure(figsize=(12, 6))
sns.scatterplot(x='submit_times_avg', y='total_score', hue='cluster_label_tsne', data=feat_label_analy_df)
plt.title('time_split_2_percentage vs total_score')
plt.show()

# 3. 特征相关性分析 通过相关性矩阵来分析不同特征之间的相关性 绘制热力图展示
# total_syth_score_avg 和 time_difference_mean 之间的相关性很高！
heat_feat = feat_label_analy_df.drop('class', axis=1).drop('rank_label', axis=1).drop('x_pca', axis=1).drop('y_pca', axis=1).drop('x_tsne', axis=1).drop('y_tsne', axis=1).drop('x_umap', axis=1).drop('y_umap', axis=1)
plt.figure(figsize=(12, 6))
sns.heatmap(heat_feat.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()




