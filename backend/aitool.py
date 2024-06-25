import json
import pymysql
from openai import OpenAI

class AiTool:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        # 设置自定义的 kimi 密钥和URL
        self.OPENAI_API_KEY = 'sk-JWfeJHPSDqFWNkwg21VZ0vFAdTXamZ4HyMlQ8Ij0quCcw1F4'
        self.OPENAI_URL = 'https://kimi-free-api***.com/v1/chat/completions'

    def get_connection(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def get_students_info(self, student_id: str):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = f"""
            SELECT *
            FROM ai_data
            WHERE student_id = "{student_id}"
            """
            cursor.execute(query)
            results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            results = []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        
        # 获取学生统计数据后 编辑提示词 接入大模型生成评价
        return results
    
    def get_comment_from_kimi_stream(self, students_data):
        client = OpenAI(
        api_key = "sk-JWfeJHPSDqFWNkwg21VZ0vFAdTXamZ4HyMlQ8Ij0quCcw1F4",
        base_url = "https://api.moonshot.cn/v1",
        )
        student = students_data[0]
        description = (f"学生ID: {student['student_id']}, 所在班级: {student['class']}\n"
               f"提交题目数量: {student['title_counts']} 班级内提交题目数量均值: {student['title_counts_class_mean']}, 所有人提交题目数量均值: {student['title_counts_all_mean']}\n"
               f"平均每题提交时间差: {student['time_difference_mean']} 班级内平均每题提交时间差均值: {student['time_difference_mean_class_mean']}, 所有人平均每题提交时间差均值: {student['time_difference_mean_all_mean']}\n"
               f"上午提交次数占比: {student['time_split_0_percentage']}, 下午提交次数占比: {student['time_split_1_percentage']}, 晚上提交次数占比: {student['time_split_2_percentage']}\n"
               f"平均每题提交次数: {student['submit_times_avg']} 班级内平均每题提交次数均值: {student['submit_times_avg_class_mean']}, 所有人平均每题提交次数均值: {student['submit_times_avg_all_mean']}\n"
               f"单个题目最大提交次数: {student['submit_times_max']} 班级内单个题目最大提交次数均值: {student['submit_times_max_class_mean']}, 所有人单个题目最大提交次数均值: {student['submit_times_max_all_mean']})\n"
               f"所有题目平均纸面得分: {student['total_syth_score_avg']} 班级内所有题目平均纸面得分均值: {student['total_syth_score_avg_class_mean']}, 所有人所有题目平均纸面得分均值: {student['total_syth_score_avg_all_mean']},其中纸面得分范围为0-4分\n"
               f"所有题目平均空间复杂度: {student['all_memory_avg']} 班级所有题目平均空间复杂度均值: {student['all_memory_avg_class_mean']}, 所有人所有题目平均空间复杂度均值: {student['all_memory_avg_all_mean']}\n"
               f"所有题目平均运行时间消耗: {student['all_timeconsume_avg']} 班级所有题目平均运行时间消耗均值: {student['all_timeconsume_avg_class_mean']}, 所有人所有题目平均运行时间消耗均值: {student['all_timeconsume_avg_all_mean']}\n"
               f"绝对错误状态提交占比: {student['state_ae_percentage']}, 错误状态提交占比: {student['state_e_percentage']}, 部分正确状态提交占比: {student['state_pc_percentage']}, 完全正确状态提交占比: {student['state_ac_percentage']}\n"
               f"总分: {student['total_score']} 班级总分均值: {student['total_score_class_mean']}, 所有人总分均值: {student['total_score_all_mean']})\n"
               f"班级内排名百分比: {student['total_score_class_rank']}, 所有人中排名百分比: {student['total_score_all_rank']}\n")
        
        prompt_sys = "你是编程课堂可视化系统中的智能学生分析助手，你可以根据学生的做题数据生成评价与建议。"
        prompt_user = "你是编程课堂可视化系统中的智能学生分析助手，你可以根据学生的做题数据生成评价与建议。下面是当前学生的做题数据，请生成详细评价与建议：\n" + description + "\n"

        response = client.chat.completions.create(
            model = "moonshot-v1-8k",
            # "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
            messages = [
                {"role": "system", "content": prompt_sys},
                {"role": "user", "content": prompt_user}
            ],
            temperature = 0.3,
            max_tokens = 1024,
            # 流式调用
            stream=True
        )
        # 成功将数据流式传到前端 现在之需要解决流式传输问题
        for chunk in response:
            # print("Chunk received, value: ", chunk)
            chunk_message = chunk.choices[0].delta
            if not chunk_message.content:
                continue
            yield chunk_message.content
    
    def get_comment_from_kimi(self, students_data):
        client = OpenAI(
        api_key = "sk-JWfeJHPSDqFWNkwg21VZ0vFAdTXamZ4HyMlQ8Ij0quCcw1F4",
        base_url = "https://api.moonshot.cn/v1",
        )
        student = students_data[0]
        description = (f"学生ID: {student['student_id']}, 所在班级: {student['class']}\n"
               f"提交题目数量: {student['title_counts']} 班级内提交题目数量均值: {student['title_counts_class_mean']}, 所有人提交题目数量均值: {student['title_counts_all_mean']}\n"
               f"平均每题提交时间差: {student['time_difference_mean']} 班级内平均每题提交时间差均值: {student['time_difference_mean_class_mean']}, 所有人平均每题提交时间差均值: {student['time_difference_mean_all_mean']}\n"
               f"上午提交次数占比: {student['time_split_0_percentage']}, 下午提交次数占比: {student['time_split_1_percentage']}, 晚上提交次数占比: {student['time_split_2_percentage']}\n"
               f"平均每题提交次数: {student['submit_times_avg']} 班级内平均每题提交次数均值: {student['submit_times_avg_class_mean']}, 所有人平均每题提交次数均值: {student['submit_times_avg_all_mean']}\n"
               f"单个题目最大提交次数: {student['submit_times_max']} 班级内单个题目最大提交次数均值: {student['submit_times_max_class_mean']}, 所有人单个题目最大提交次数均值: {student['submit_times_max_all_mean']})\n"
               f"所有题目平均纸面得分: {student['total_syth_score_avg']} 班级内所有题目平均纸面得分均值: {student['total_syth_score_avg_class_mean']}, 所有人所有题目平均纸面得分均值: {student['total_syth_score_avg_all_mean']},其中纸面得分范围为0-4分\n"
               f"所有题目平均空间复杂度: {student['all_memory_avg']} 班级所有题目平均空间复杂度均值: {student['all_memory_avg_class_mean']}, 所有人所有题目平均空间复杂度均值: {student['all_memory_avg_all_mean']}\n"
               f"所有题目平均运行时间消耗: {student['all_timeconsume_avg']} 班级所有题目平均运行时间消耗均值: {student['all_timeconsume_avg_class_mean']}, 所有人所有题目平均运行时间消耗均值: {student['all_timeconsume_avg_all_mean']}\n"
               f"绝对错误状态提交占比: {student['state_ae_percentage']}, 错误状态提交占比: {student['state_e_percentage']}, 部分正确状态提交占比: {student['state_pc_percentage']}, 完全正确状态提交占比: {student['state_ac_percentage']}\n"
               f"总分: {student['total_score']} 班级总分均值: {student['total_score_class_mean']}, 所有人总分均值: {student['total_score_all_mean']})\n"
               f"班级内排名百分比: {student['total_score_class_rank']}, 所有人中排名百分比: {student['total_score_all_rank']}\n")
        
        prompt_sys = "你是编程课堂可视化系统中的智能学生分析助手，你可以根据学生的做题数据生成评价与建议。"
        prompt_user = "你是编程课堂可视化系统中的智能学生分析助手，你可以根据学生的做题数据生成评价与建议。下面是当前学生的做题数据，请生成详细评价与建议：\n" + description + "\n"

        response = client.chat.completions.create(
            model = "moonshot-v1-8k",
            # "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
            messages = [
                {"role": "system", "content": prompt_sys},
                {"role": "user", "content": prompt_user}
            ],
            temperature = 0.3,
        )

        return response.choices[0].message.content
    
    # 格式化成需要数据
    def reformat_student_data(self, comments):
        reformatted_data_json = {"text": comments}

        return reformatted_data_json

    def data_to_json(self, data):
        return json.dumps(data, indent=4)

# 使用示例
if __name__ == "__main__":
    
    # 创建Parallel类的实例，指定本地数据库连接信息
    aiTool = AiTool(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    students_data = aiTool.get_students_info('0088dc183f73c83f763e')
    comments = aiTool.get_comment_from_kimi(students_data)
    reformatted_data_json = aiTool.reformat_student_data(comments)
    data_json = aiTool.data_to_json(reformatted_data_json)
