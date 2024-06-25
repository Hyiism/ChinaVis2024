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
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

# 预先读取所有数据，避免在循环中频繁查询数据库
query = """
    SELECT * FROM `students_features_reprocess_vis` 
"""

data = pd.read_sql_query(query, con=engine).drop('x', axis=1).drop('y', axis=1).drop('z', axis=1)
X = data.drop('student_id', axis=1).drop('total_score', axis=1).drop('rank_label', axis=1).drop('cluster_label', axis=1)
label_mapping = {"Top 1/3": 0, "Top 2/3": 1, "Top 3/3": 2,}
data['rank_label'] = data['rank_label'].map(label_mapping)
y = data['rank_label']
# y = data['total_score']

# 数据标准化
X_scaled = StandardScaler().fit_transform(X)

# 数据归一化
min_max_scaler = MinMaxScaler()
X_normalized = min_max_scaler.fit_transform(X_scaled)

# 数据分割
X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.3, random_state=42)

# 随机森林模型
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 预测
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# 特征重要性
importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]

# 可视化
plt.figure(figsize=(12, 6))
sns.barplot(x=importances[indices], y=np.array(X.columns)[indices])
plt.title('Feature Importances')
plt.show()

# 使用散点图查看特征与标签的关系
for feature in X.columns:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=data[feature], y=data['cluster_label'], alpha=0.6)
    plt.title(f'Relationship between {feature} and cluster_label')
    plt.xlabel(feature)
    plt.ylabel("cluster_label")
    plt.show()