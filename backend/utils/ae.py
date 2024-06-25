import torch
from torch import nn, optim
import matplotlib.pyplot as plt
import pymysql
import torch
import torch.nn as nn
import torch.optim as optim
import numpy
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import torch.nn.functional as F
import umap.umap_ as umap
import pandas as pd
import numpy as np



# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

# 预先读取所有数据，避免在循环中频繁查询数据库
query = """
    SELECT * FROM `students_features_reprocess` 
"""

data = pd.read_sql_query(query, con=engine)
features = data.drop('student_id', axis=1).drop('total_score', axis=1).drop('rank_label', axis=1)
label_mapping = {"Top 1/3": 0, "Top 2/3": 1, "Top 3/3": 2,}
data['rank_label'] = data['rank_label'].map(label_mapping)
labels = data['rank_label']

features_tensor = torch.tensor(np.array(features), dtype=torch.float32)
labels_tensor = torch.tensor(labels, dtype=torch.long)  # CrossEntropyLoss 需要 LongTensor 类型的标签

# 对特征进行标准化
features_tensor = F.normalize(features_tensor, dim=1)


class autoencoder(nn.Module):
    def __init__(self):
        super(autoencoder, self).__init__()
        self.encoder = nn.Sequential(nn.Linear(19, 16),
                                     nn.ReLU(True),
                                     nn.Linear(16, 8)
        )
        
        self.decoder = nn.Sequential(nn.Linear(8, 16),
                                     nn.ReLU(True),
                                     nn.Linear(16, 19),
                                     nn.Tanh())
    def forward(self, x):
        encode = self.encoder(x)
        decode = self.decoder(encode)
        return encode, decode

if __name__ == "__main__":
    # 超参数设置
    lr = 1e-2
    epoches = 4000
    model = autoencoder()

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)


    for epoch in range(epoches):
        # 前向传播
        outputs = model(features_tensor)
        # print(outputs[0].shape)
        loss = criterion(outputs[1], features_tensor)

        # 反向传播与优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 打印损失
        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{epoches}], Loss: {loss.item():.9f}')
        
# 使用模型进行前向传播得到隐藏层输出
with torch.no_grad():
    hidden_outputs = model(features_tensor)[0].numpy()
    # hidden_outputs = model.fc1(features_tensor).numpy()  # 提取隐藏层输出

# hidden_outputs 即为降维后的数据，它的形状为 (样本数, 隐藏层维度)
print("降维后的数据维度：", hidden_outputs.shape)


# 使用 UMAP 进行降维
umap_reducer = umap.UMAP(n_components=2, random_state=0)
reduced_data = umap_reducer.fit_transform(hidden_outputs)

# 使用 K-Means 聚类
kmeans = KMeans(n_clusters=4)  # 假设你想要将数据分成 4 类
clusters = kmeans.fit_predict(reduced_data)

# 绘制散点图
plt.figure(figsize=(8, 6))

# 根据聚类标签绘制不同颜色的点
for i in range(4):  # 假设共有 3 个聚类
    plt.scatter(hidden_outputs[clusters == i, 0], hidden_outputs[clusters == i, 1], label=f'Cluster {i+1}')

plt.title('Clustering Results')
plt.xlabel('Dimension 1')
plt.ylabel('Dimension 2')
plt.legend()
plt.show()


    