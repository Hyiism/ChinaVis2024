from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import pandas as pd  # 添加导入 pandas 模块

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})  # 在Flask应用上启用CORS
# CORS(app, resources={r"/*": {"origins": "*"}})  # 确保CORS允许所有源访问

def get_data_from_class_knowledge_summary():
    # 配置数据库连接信息
    db_config = {
        'host': 'localhost',  # 数据库地址
        'user': 'root',  # 数据库用户名
        'password': '13957724109@lkx',  # 数据库密码
        'database': 'chinavis_data'  # 数据库名称
    }

    # 连接数据库
    connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # 执行查询
            # sql_query = "SELECT * FROM class_knowledge_summary"  # 替换为你的查询语句
            sql_query = """
                            SELECT student_id, b3C9s_score, g7R2j_score, k4W1c_score, m3D1v_score,
                                   r8S3g_score, s8Y2f_score, t5V9e_score, y9W5d_score
                            
                            FROM chinavis_data.students_knowledge_timeconsume
                            # LIMIT 9
                        """
            cursor.execute(sql_query)
            # 获取结果
            result = cursor.fetchall()
            # for row in result:
            #     print(row)
            return result
    finally:
        # 关闭连接
        connection.close()


# 从CSV文件获取数据
def get_data_from_student_scores_summary():
    try:
        # Read data from hello.csv
        df = pd.read_csv('hello.csv')
        # Convert DataFrame to list of dictionaries
        result = df.to_dict(orient='records')
        return result
    except Exception as e:
        return {'error': str(e)}

@app.route('/get_class_knowledge_data', methods=['GET'])
def get_class_knowledge_data():
    data = get_data_from_class_knowledge_summary()
    # 将数据转换为JSON格式
    return jsonify(data)

@app.route('/get_student_scores_data', methods=['GET'])
def get_student_scores_data():
    data = get_data_from_student_scores_summary()
    # 将数据转换为JSON格式
    return jsonify(data)

# 添加路由处理根路径 '/'
@app.route('/')
def index():
    return 'Hello, this is the index page'

# 添加路由处理 '/favicon.ico'
@app.route('/favicon.ico')
def favicon():
    # 返回一个简单的空白响应，或者你可以提供一个占位图标
    return ''

if __name__ == '__main__':
    app.run(port=5000,debug=True)