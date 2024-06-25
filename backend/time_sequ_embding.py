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
import scipy.stats as stats

features_df_time = pd.read_csv("student_embeddings_classf.csv")
features_df_tongji = pd.read_csv("student_embeddings_tongji.csv")
features_df_all = pd.read_csv("student_embeddings_all.csv")

# features_vis_seq作为从这里提取的时序可视化特征
#student_id class x_uamp y_umap x_tsne y_tsne x_pca y_pca cluster_label_umap cluster_label_tsne cluster_label_pca 

# 提取特征列
X_time_seq = features_df_time.drop('student_id', axis=1)

X_tongji = features_df_tongji.drop('student_id', axis=1).drop('total_score', axis=1).drop('class', axis=1).drop('all_memory_avg', axis=1).drop('all_timeconsume_avg', axis=1).drop('all_memory_std', axis=1).drop('all_timeconsume_std', axis=1).drop('total_syth_score_avg', axis=1).drop('title_counts', axis=1).drop('total_syth_score_std', axis=1)
label_mapping = {"Top 1/3": 0, "Top 2/3": 1, "Top 3/3": 2,}
X_tongji['rank_label'] = X_tongji['rank_label'].map(label_mapping)
# 数据标准化
X_tongji = StandardScaler().fit_transform(X_tongji)
# 数据归一化
min_max_scaler = MinMaxScaler()
X_tongji = min_max_scaler.fit_transform(X_tongji)

X_concat = np.concatenate((X_time_seq, X_tongji), axis=1)
X_all = features_df_all.drop('student_id', axis=1)

# X = X_concat
# X = X_time_seq
# X = X_all


# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

############################concat特征#################################
features_vis_concat = pd.DataFrame()
features_vis_concat['student_id'] = features_df_tongji['student_id']
features_vis_concat['class'] = features_df_tongji['class']
# 使用 UMAP 进行降维 使用kmeans聚类
umap_reducer = umap.UMAP(n_components=2, random_state=42)
reduced_data_umap = umap_reducer.fit_transform(X_concat) # [[x,y]...]坐标值
reduced_data_df_umap = pd.DataFrame(reduced_data_umap, columns=['x_umap', 'y_umap'])
features_vis_concat[['x_umap', 'y_umap']] = reduced_data_df_umap

kmeans = KMeans(n_clusters=4)  # 假设你想要将数据分成 4 类
clusters_umap = kmeans.fit_predict(reduced_data_umap) #[0, 1, 2, 3]cluster_label值
features_vis_concat['cluster_label_umap'] = clusters_umap

# 使用 t-SNE 进行降维 使用kmeans聚类
tsne = TSNE(n_components=2, random_state=42)
reduced_data_tsne = tsne.fit_transform(X_concat)
reduced_data_df_tsne = pd.DataFrame(reduced_data_tsne, columns=['x_tsne', 'y_tsne'])
features_vis_concat[['x_tsne', 'y_tsne']] = reduced_data_df_tsne

kmeans = KMeans(n_clusters=4)  # 假设你想要将数据分成 4 类
clusters_tsne = kmeans.fit_predict(reduced_data_tsne) #[0, 1, 2, 3]cluster_label值
features_vis_concat['cluster_label_tsne'] = clusters_tsne

# 使用 PCA 进行降维 使用kmeans聚类
pca = PCA(n_components=2)
reduced_data_pca = pca.fit_transform(X_concat)
reduced_data_df_pca = pd.DataFrame(reduced_data_pca, columns=['x_pca', 'y_pca'])
features_vis_concat[['x_pca', 'y_pca']] = reduced_data_df_pca

kmeans = KMeans(n_clusters=4)  # 假设你想要将数据分成 4 类
clusters_pca = kmeans.fit_predict(reduced_data_pca) #[0, 1, 2, 3]cluster_label值
features_vis_concat['cluster_label_pca'] = clusters_pca

# features_vis_concat.to_sql('features_vis_concat', con=engine, if_exists='replace', index=False)
features_vis_concat.to_csv('features_vis_concat.csv', index=False)


############################time_seq特征#################################
features_vis_seq = pd.DataFrame()
features_vis_seq['student_id'] = features_df_tongji['student_id']
features_vis_seq['class'] = features_df_tongji['class']
# 使用 UMAP 进行降维 使用kmeans聚类
umap_reducer = umap.UMAP(n_components=2, random_state=42)
reduced_data_umap = umap_reducer.fit_transform(X_time_seq) # [[x,y]...]坐标值
reduced_data_df_umap = pd.DataFrame(reduced_data_umap, columns=['x_umap', 'y_umap'])
features_vis_seq[['x_umap', 'y_umap']] = reduced_data_df_umap

kmeans = KMeans(n_clusters=4)  # 假设你想要将数据分成 4 类
clusters_umap = kmeans.fit_predict(reduced_data_umap) #[0, 1, 2, 3]cluster_label值
features_vis_seq['cluster_label_umap'] = clusters_umap

# 使用 t-SNE 进行降维 使用kmeans聚类
tsne = TSNE(n_components=2, random_state=42)
reduced_data_tsne = tsne.fit_transform(X_time_seq)
reduced_data_df_tsne = pd.DataFrame(reduced_data_tsne, columns=['x_tsne', 'y_tsne'])
features_vis_seq[['x_tsne', 'y_tsne']] = reduced_data_df_tsne

kmeans = KMeans(n_clusters=4)  # 假设你想要将数据分成 4 类
clusters_tsne = kmeans.fit_predict(reduced_data_tsne) #[0, 1, 2, 3]cluster_label值
features_vis_seq['cluster_label_tsne'] = clusters_tsne

# 使用 PCA 进行降维 使用kmeans聚类
pca = PCA(n_components=2)
reduced_data_pca = pca.fit_transform(X_time_seq)
reduced_data_df_pca = pd.DataFrame(reduced_data_pca, columns=['x_pca', 'y_pca'])
features_vis_seq[['x_pca', 'y_pca']] = reduced_data_df_pca

kmeans = KMeans(n_clusters=4)  # 假设你想要将数据分成 4 类
clusters_pca = kmeans.fit_predict(reduced_data_pca) #[0, 1, 2, 3]cluster_label值
features_vis_seq['cluster_label_pca'] = clusters_pca

# features_vis_seq.to_sql('features_vis_seq', con=engine, if_exists='replace', index=False)
features_vis_seq.to_csv('features_vis_seq.csv', index=False)



############################all特征#################################
features_vis_all = pd.DataFrame()
features_vis_all['student_id'] = features_df_tongji['student_id']
features_vis_all['class'] = features_df_tongji['class']
# 使用 UMAP 进行降维 使用kmeans聚类
umap_reducer = umap.UMAP(n_components=2, random_state=42)
reduced_data_umap = umap_reducer.fit_transform(X_all) # [[x,y]...]坐标值
reduced_data_df_umap = pd.DataFrame(reduced_data_umap, columns=['x_umap', 'y_umap'])
features_vis_all[['x_umap', 'y_umap']] = reduced_data_df_umap

kmeans = KMeans(n_clusters=4)  # 假设你想要将数据分成 4 类
clusters_umap = kmeans.fit_predict(reduced_data_umap) #[0, 1, 2, 3]cluster_label值
features_vis_all['cluster_label_umap'] = clusters_umap

# 使用 t-SNE 进行降维 使用kmeans聚类
tsne = TSNE(n_components=2, random_state=42)
reduced_data_tsne = tsne.fit_transform(X_all)
reduced_data_df_tsne = pd.DataFrame(reduced_data_tsne, columns=['x_tsne', 'y_tsne'])
features_vis_all[['x_tsne', 'y_tsne']] = reduced_data_df_tsne

kmeans = KMeans(n_clusters=4)  # 假设你想要将数据分成 4 类
clusters_tsne = kmeans.fit_predict(reduced_data_tsne) #[0, 1, 2, 3]cluster_label值
features_vis_all['cluster_label_tsne'] = clusters_tsne

# 使用 PCA 进行降维 使用kmeans聚类
pca = PCA(n_components=2)
reduced_data_pca = pca.fit_transform(X_all)
reduced_data_df_pca = pd.DataFrame(reduced_data_pca, columns=['x_pca', 'y_pca'])
features_vis_all[['x_pca', 'y_pca']] = reduced_data_df_pca

kmeans = KMeans(n_clusters=4)  # 假设你想要将数据分成 4 类
clusters_pca = kmeans.fit_predict(reduced_data_pca) #[0, 1, 2, 3]cluster_label值
features_vis_all['cluster_label_pca'] = clusters_pca

# features_vis_all.to_sql('features_vis_all', con=engine, if_exists='replace', index=False)
features_vis_all.to_csv('features_vis_all.csv', index=False)


# # 绘制二维散点图
# plt.figure(figsize=(10, 8))
# for i in range(4):
#     plt.scatter(reduced_data_umap[clusters_umap == i, 0], reduced_data_umap[clusters_umap == i, 1], label=f'Cluster {i+1}')

# plt.title('K-Means Clustering Results (Kmeans-UMAP)')
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 2')
# plt.legend()
# plt.show()
