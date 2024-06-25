import pymysql
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.cluster import KMeans
import torch.nn.functional as F
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap.umap_ as umap
import random

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

# 连接数据库
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='qyh443012.',
                       database='chinavis2024')

# 创建游标对象
cursor = conn.cursor()

# 执行 SQL 查询
sql = "SELECT student_id, features, rank_label_1 FROM student_features"
cursor.execute(sql)

# 提取数据
data = cursor.fetchall()

# 将数据转换成特征和标签
student_ids = []
features = []
labels = []

for row in data:
    student_ids.append(row[0])
    features.append(eval(row[1]))  # 将字符串转换为列表
    labels.append(row[2])

# 创建标签到数字的映射
label_mapping = {"Top 1/3": 0, "Top 2/3": 1, "Top 3/3": 2}
labels = [label_mapping[label] for label in labels]

features_tensor = torch.tensor(features, dtype=torch.float32)
labels_tensor = torch.tensor(labels, dtype=torch.long)  # CrossEntropyLoss 需要 LongTensor 类型的标签

# 对特征进行标准化
features_tensor = F.normalize(features_tensor, dim=1)

# 定义 MLP 模型
class MLP(nn.Module):
    def __init__(self):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(190, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 3)  # 输出层的维度应与类别数量一致

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 初始化模型和优化器
model = MLP()
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# 训练模型
epochs = 19000
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
    hidden_outputs = model.fc2(torch.relu(model.fc1(features_tensor))).numpy()

# 使用 UMAP 进行降维
umap_reducer = umap.UMAP(n_components=3, random_state=0)
reduced_data = umap_reducer.fit_transform(hidden_outputs)

# 使用 K-Means 聚类
kmeans = KMeans(n_clusters=4)  # 假设你想要将数据分成 4 类
clusters = kmeans.fit_predict(reduced_data)

# # 更新数据库，添加新的字段
# add_columns_sql = """
# ALTER TABLE student_features 
# ADD COLUMN x FLOAT,
# ADD COLUMN y FLOAT,
# ADD COLUMN z FLOAT,
# ADD COLUMN cluster_label INT;
# """
# cursor.execute(add_columns_sql)
# conn.commit()

# 更新数据库，插入降维和聚类后的数据
update_sql = """
UPDATE student_features
SET x = %s, y = %s, z = %s, cluster_label = %s
WHERE student_id = %s;
"""
for i, (coords, label) in enumerate(zip(reduced_data, clusters)):
    cursor.execute(update_sql, (coords[0], coords[1], coords[2], int(label), student_ids[i]))

conn.commit()

# 关闭游标和连接
cursor.close()
conn.close()
