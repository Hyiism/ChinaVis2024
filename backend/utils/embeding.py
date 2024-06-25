import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap.umap_ as umap
import random
import torch
import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim


# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

# 预先读取所有数据，避免在循环中频繁查询数据库
query = """
    SELECT * FROM `students_features_reprocess`
"""
features_df = pd.read_sql_query(query, con=engine)
features_df.to_csv('student_embeddings_tongji.csv', index=False)
print("over!!!!!")

# features_df = features_df[features_df['class'] == 'Class1']
# 打印DataFrame
print(features_df)

    # features_dict['student_id'].append(student_id)
    # features_dict['title_counts'].append(len(student_title_ids))
    # features_dict['time_difference_mean'].append(time_difference_mean)
    # features_dict['time_difference_std'].append(time_difference_std)
    # features_dict['time_split_0_percentage'].append(counts[0])
    # features_dict['time_split_1_percentage'].append(counts[1])
    # features_dict['time_split_2_percentage'].append(counts[2])
    # features_dict['submit_times_avg'].append(all_submit_times_avg)
    # features_dict['submit_times_std'].append(all_submit_times_std)
    # features_dict['submit_times_max'].append(all_submit_times_max)
    # features_dict['total_syth_score_avg'].append(total_syth_score_avg)
    # features_dict['total_syth_score_std'].append(total_syth_score_std)
    # features_dict['all_memory_avg'].append(all_memory_avg)
    # features_dict['all_timeconsume_avg'].append(all_timeconsume_avg)
    # features_dict['all_memory_std'].append(all_memory_std)
    # features_dict['all_timeconsume_std'].append(all_timeconsume_std)
    # features_dict['state_ae_percentage'].append(state_counts['ae'])
    # features_dict['state_e_percentage'].append(state_counts['e'])
    # features_dict['state_pc_percentage'].append(state_counts['pc'])
    # features_dict['state_ac_percentage'].append(state_counts['ac'])
# 提取特征列
X = features_df.drop('student_id', axis=1).drop('total_score', axis=1).drop('class', axis=1)
label_mapping = {"Top 1/3": 0, "Top 2/3": 1, "Top 3/3": 2,}
X['rank_label'] = X['rank_label'].map(label_mapping)
# 数据标准化
X_scaled = StandardScaler().fit_transform(X)

# 数据归一化
min_max_scaler = MinMaxScaler()
X_normalized = min_max_scaler.fit_transform(X_scaled)

# # 使用 K-Means 聚类
# kmeans = KMeans(n_clusters=4)  # 假设你想要将数据分成 4 类
# clusters = kmeans.fit_predict(X_normalized)

# 使用层次聚类进行聚类
# agg_clustering = AgglomerativeClustering(n_clusters=4)
# clusters = agg_clustering.fit_predict(X_scaled)

# 使用 UMAP 进行降维
umap_reducer = umap.UMAP(n_components=2, random_state=42)
reduced_data_umap = umap_reducer.fit_transform(X_normalized) # [[x,y,z]...]坐标值
# reduced_data_df_umap = pd.DataFrame(reduced_data_umap, columns=['x_umap', 'y_umap'])
# reduced_data_df = pd.DataFrame(reduced_data, columns=['x', 'y', 'z'])
# 将新列添加到原 DataFrame
# features_df[['x_umap', 'y_umap']] = reduced_data_df_umap
# features_df[['x', 'y', 'z']] = reduced_data_df

# 使用 t-SNE 将数据降到二维
# tsne = TSNE(n_components=2, random_state=42)
# reduced_data_tsne = tsne.fit_transform(X_scaled)

# reduced_data_df_tsne = pd.DataFrame(reduced_data_tsne, columns=['x_tsne', 'y_tsne'])
# features_df[['x_tsne', 'y_tsne']] = reduced_data_df_tsne

# # 使用 PCA 将数据降到二维
pca = PCA(n_components=2)
reduced_data_pca = pca.fit_transform(X_scaled)
# reduced_data_df_pca = pd.DataFrame(reduced_data_pca, columns=['x_pca', 'y_pca'])
# features_df[['x_pca', 'y_pca']] = reduced_data_df_pca

kmeans = KMeans(n_clusters=4)  # 假设你想要将数据分成 4 类
clusters_umap = kmeans.fit_predict(reduced_data_umap) #[0, 1, 2, 3]cluster_label值
# clusters_tsne = kmeans.fit_predict(reduced_data_tsne) #[0, 1, 2, 3]cluster_label值
# clusters_pca = kmeans.fit_predict(reduced_data_pca) #[0, 1, 2, 3]cluster_label值

# features_df['cluster_label_umap'] = clusters_umap
# features_df['cluster_label_tsne'] = clusters_tsne
# features_df['cluster_label_pca'] = clusters_pca

# 将坐标和聚类标签存入数据库
# features_df.to_sql(name='students_features_reprocess_vis_2d_aa', con=engine, if_exists='replace', index=False)
# print(features_df)

# 绘制二维散点图
plt.figure(figsize=(10, 8))
for i in range(4):
    plt.scatter(reduced_data[clusters == i, 0], reduced_data[clusters == i, 1], label=f'Cluster {i+1}')

plt.title('K-Means Clustering Results (Kmeans-UMAP)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.show()

# # 绘制三维散点图
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')

# 根据标签绘制不同颜色的点
# for i in range(4):  # 假设共有 3 个标签类别
#     ax.scatter(reduced_data[clusters == i, 0], 
#                reduced_data[clusters == i, 1], 
#                reduced_data[clusters == i, 2], 
#                label=f'Cluster {i+1}')

# ax.set_title('UMAP Dimensionality Reduction to 3D and Label Coloring')
# ax.set_xlabel('UMAP Dimension 1')
# ax.set_ylabel('UMAP Dimension 2')
# ax.set_zlabel('UMAP Dimension 3')
# ax.legend()
# plt.show()