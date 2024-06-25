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
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

# 构造连接引擎
engine = create_engine('mysql+pymysql://root:qyh443012.@localhost:3306/chinavis2024?charset=utf8')

# 预先读取所有数据，避免在循环中频繁查询数据库
query = """
    SELECT * FROM `time_seq_data` 
    ORDER BY `student_ID`, `date`;
"""
query_label = """
    SELECT `student_ID`, `total_score` FROM `student_scores_summary_1`
    ORDER BY `student_ID`;
"""
query_rank_label = """
    SELECT `student_ID`, `rank_label_1` FROM `student_features_vis`
    ORDER BY `student_ID`;
"""

all_time_seq_df = pd.read_sql_query(query, con=engine)
total_score_df = pd.read_sql_query(query_label, con=engine)
rank_label_df = pd.read_sql_query(query_rank_label, con=engine)

# all_time_seq_df.to_csv('all_time_seq_df.csv', index=False)
# total_score_df.to_csv('total_score_df.csv', index=False)
rank_label_df.to_csv('rank_label_df.csv', index=False)
print("over!!!!!")

# 将日期转换为时间戳
all_time_seq_df['date'] = pd.to_datetime(all_time_seq_df['date'])
# 以学生id和日期为索引
all_time_seq_df.set_index(['student_id', 'date'], inplace=True)
# 将total_score_df的student_id设置为index，后续好合并
total_score_df.set_index('student_ID', inplace=True)
# 获取所有学生ID
student_ids = all_time_seq_df.index.get_level_values(0).unique()

# 创建一个字典来保存每个学生的时序数据
student_data = {}

for student_id in student_ids:
    student_df = all_time_seq_df.loc[student_id]
    student_df = student_df.sort_index()  # 确保日期排序
    student_data[student_id] = student_df.values

# 将数据转换为适合LSTM输入的格式
sequence_length = 60  # 共148天, 假设使用过去100天的数据来预测，时间步越大 计算越困难
features = all_time_seq_df.shape[1]  # 获取特征w维度 

X = []
y = []

for student_id in student_ids:
    data = student_data[student_id]
    total_score = total_score_df.loc[student_id].values[0]  # 获取对应的total_score
    for i in range(len(data) - sequence_length):
        X.append(data[i:i+sequence_length])
        y.append(total_score)

X = np.array(X)
y = np.array(y)

# 对输入数据进行归一化
scaler = StandardScaler()
X_shape = X.shape
X = scaler.fit_transform(X.reshape(-1, X_shape[-1])).reshape(X_shape)

# 转换为PyTorch的张量
X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32)

# 构建数据集和数据加载器
class StudentDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

dataset = StudentDataset(X, y)
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

# 定义LSTM模型
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, embed_size, output_size, num_layers=1):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc_embed = nn.Linear(hidden_size, embed_size)
        self.fc_out = nn.Linear(embed_size, output_size)
        self.embedding = None

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        out, _ = self.lstm(x, (h0, c0))
        out = self.fc_embed(out[:, -1, :])
        self.embedding = out  # 保存嵌入层的输出
        out = self.fc_out(out)
        return out

input_size = features
hidden_size = 50  # 你可以调整这个参数
embed_size = 20  # 嵌入层的大小，可以调整
output_size = 1  # total_score是一个标量
model = LSTMModel(input_size, hidden_size, embed_size, output_size)

# 模型训练
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 3  # 你可以调整这个参数

model.train()

for epoch in range(num_epochs):
    for i, (inputs, labels) in enumerate(dataloader):
        outputs = model(inputs)
        loss = criterion(outputs.squeeze(), labels)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# 构建单个学生的数据集和数据加载器
class SingleStudentDataset(Dataset):
    def __init__(self, student_data, student_ids):
        self.student_data = student_data
        self.student_ids = student_ids

    def __len__(self):
        return len(self.student_ids)

    def __getitem__(self, idx):
        student_id = self.student_ids[idx]
        data = self.student_data[student_id]
        total_score = total_score_df.loc[student_id].values[0]
        return torch.tensor(data, dtype=torch.float32), student_id

single_student_dataset = SingleStudentDataset(student_data, student_ids)
single_student_dataloader = DataLoader(single_student_dataset, batch_size=1, shuffle=False)


# 模型评估
model.eval()
with torch.no_grad():
    total_loss = 0
    embeddings = []
    for inputs, labels in dataloader:
        outputs = model(inputs)
        loss = criterion(outputs.squeeze(), labels)
        total_loss += loss.item()
        embeddings.append(model.embedding.cpu().numpy())  # 保存嵌入表示
    
    print(f'Average Loss: {total_loss / len(dataloader):.4f}')

# 提取嵌入表示
embeddings = np.vstack(embeddings)
print("Embeddings shape:", embeddings.shape)

# # 模型评估
# model.eval()
# with torch.no_grad():
#     total_loss = 0
#     embeddings = []
#     student_ids_list = []
#     for inputs, student_id in single_student_dataloader:
#         inputs = inputs.squeeze(0)  # Remove the batch dimension
#         inputs = inputs.unsqueeze(0)  # Add a batch dimension
#         inputs = inputs.to(torch.float32)  # 确保输入为 float32 类型
#         outputs = model(inputs)
#         embeddings.append(model.embedding.cpu().numpy())  # 保存嵌入表示
#         # print("#################")
#         # print(student_id)
#         student_ids_list.append(student_id[0])  # 保存学生ID
    
#     print(f'Average Loss: {total_loss / len(dataloader):.4f}')
        
# 提取嵌入表示
# embeddings = np.vstack(embeddings)
# embedding_df = pd.DataFrame(embeddings, index=student_ids_list)
# embedding_df.index.name = 'student_id'
# print("Embeddings DataFrame shape:", embedding_df.shape)

# # 保存 DataFrame 为 CSV 文件
# embedding_df.to_csv('student_embeddings.csv')