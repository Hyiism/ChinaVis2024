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
import torch
import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim

# 固定随机数种子
seed = 42
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

# 预先读取所有数据，避免在循环中频繁查询数据库
query = """
    SELECT * FROM `students_features_reprocess` 
"""
features_df = pd.read_sql_query(query, con=engine)

# 打印DataFrame
print(features_df)


# 提取特征列
X = features_df.drop('student_id', axis=1).drop('rank_label', axis=1).drop('total_score', axis=1)
labels = features_df['rank_label']

label_mapping = {"Top 1/3": 0, "Top 2/3": 1, "Top 3/3": 2,}
labels = [label_mapping[label] for label in labels]

features_tensor = torch.tensor(np.array(X), dtype=torch.float32)
labels_tensor = torch.tensor(labels, dtype=torch.long)  # CrossEntropyLoss 需要 LongTensor 类型的标签

# 对特征进行标准化
features_tensor = F.normalize(features_tensor, dim=1)

# 定义 MLP 模型
class MLP(nn.Module):
    def __init__(self):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(11, 8)
        # self.fc2 = nn.Linear(8, 4)
        self.fc3 = nn.Linear(8, 3)  # 输出层的维度应与类别数量一致

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        # x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 初始化模型和优化器
model = MLP()
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# 训练模型
epochs = 30000
for epoch in range(epochs):
    # 前向传播
    outputs = model(features_tensor)
    loss = criterion(outputs, labels_tensor)

    # 反向传播与优化
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # 打印损失
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.15f}')
    
# 使用模型进行前向传播得到隐藏层输出
with torch.no_grad():
    # hidden_outputs = model.fc2(torch.relu(model.fc1(features_tensor))).numpy()
    hidden_outputs = model.fc3(model.fc1(features_tensor)).numpy()

# hidden_outputs 即为降维后的数据，它的形状为 (样本数, 隐藏层维度)


# # 使用 K-Means 聚类
kmeans = KMeans(n_clusters=3)  # 假设你想要将数据分成 4 类
clusters = kmeans.fit_predict(hidden_outputs)

# 使用层次聚类进行聚类
# agg_clustering = AgglomerativeClustering(n_clusters=3)
# clusters = agg_clustering.fit_predict(X_scaled)

# 使用 UMAP 进行降维
umap_reducer = umap.UMAP(n_components=2, random_state=42)
reduced_data = umap_reducer.fit_transform(hidden_outputs)

# 使用 t-SNE 将数据降到二维
# tsne = TSNE(n_components=2, random_state=42)
# reduced_data = tsne.fit_transform(X_scaled)

# # 使用 PCA 将数据降到二维
# pca = PCA(n_components=2)
# reduced_data = pca.fit_transform(X_scaled)

# 绘制散点图
plt.figure(figsize=(10, 8))
for i in range(3):
    plt.scatter(reduced_data[clusters == i, 0], reduced_data[clusters == i, 1], label=f'Cluster {i+1}')

plt.title('K-Means Clustering Results (Kmeans-UMAP)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.show()