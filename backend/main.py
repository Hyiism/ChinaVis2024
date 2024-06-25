from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware  #引入 CORS中间件模块
from parallel import Parallel
from scater import Scater
from rank import Rank
from classrank import ClassRank
from table import Table
from lkx import Lkx
from scatter_ring import ScatterRing
from check import Check, CheckRing, CheckRadar
from stack import Stack
from scatterMatrix import ScatterMatrix
from boxplot import BoxPlot
from aitool import AiTool
from bubpie import BubPie
from studentshow import StudentShow
from title_perf import TitlePerf
from heatmap import HeatMap
from student_title_process import TitleProcess
from foget_cur import ForgetCur
import json
import uvicorn
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

#设置允许访问的域名
origins = ["*"]  #也可以设置为"*"，即为所有。

#设置跨域传参
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,  #设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])  #允许跨域的headers，可以用来鉴别来源等作用。

parallel = Parallel(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)

scater = Scater(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)

rank = Rank(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)

classrank = ClassRank(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
table = Table(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
scatter_ring = ScatterRing(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
check = Check(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
checkring = CheckRing(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
checkradar = CheckRadar(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
stack = Stack(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
scaterMatrix = ScatterMatrix(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
boxplot = BoxPlot(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
aitool = AiTool(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
bubpie = BubPie(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
studentshow = StudentShow(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
titleperf = TitlePerf(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
heatmap = HeatMap(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
titleprocess = TitleProcess(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)
forgetcur = ForgetCur(
    host='localhost',
    user='root',
    password='qyh443012.',
    database='chinavis2024'
)

@app.get("/test")
def read_root():
    return {"Hello": "FastAPI"}

@app.get("/topstudents")
def get_top_n_students():
    # 获取前15名总分最高的学生
    top_students = parallel.get_top_n_students(15)
    top_students_format = parallel.reformat_student_data(top_students)
    # 截取前5、前10、前15条数据
    top5_values = [top_students_format[key] for key in list(top_students_format.keys())[:5]]
    top10_values = [top_students_format[key] for key in list(top_students_format.keys())[5:10]]
    top15_values = [top_students_format[key] for key in list(top_students_format.keys())[10:15]]
    # 组装成最终的 JSON 结构
    final_json = {
        "top5": top5_values,
        "top10": top10_values,
        "top15": top15_values
    }
    top_students_json = parallel.data_to_json(final_json)
    # print(top_students_json)

    return top_students_json

@app.get("/scaterVis/")
def get_students_vis_data(class_id: str):

    students_data = scater.get_students_vis_data(class_id)
    reformatted_data_json = scater.reformat_student_data(students_data)
    data_json = scater.data_to_json(reformatted_data_json)

    return data_json

@app.get("/scaterVis_2d/")
def get_students_vis_data(class_id: str, method: str):

    students_data = scater.get_students_vis_data_2d(class_id, method)
    reformatted_data_json = scater.reformat_student_data_2d(students_data, method)
    data_json = scater.data_to_json(reformatted_data_json)

    return data_json

@app.get("/ranking")
def get_student_ranking_data():
    students_data = rank.get_students_ranking_data()
    reformatted_data_json = rank.reformat_student_data(students_data)
    data_json = rank.data_to_json(reformatted_data_json)

    return data_json

@app.get("/ranking_per_class/")
async def get_student_ranking_data(class_id: str):
    students_data = rank.get_students_ranking_data_class(class_id)
    reformatted_data_json = rank.reformat_student_data(students_data)
    data_json = rank.data_to_json(reformatted_data_json)

    return data_json

@app.get("/classranking")
def get_class_ranking_data():
    students_data = classrank.get_class_ranking_data()
    reformatted_data_json = classrank.reformat_student_data(students_data)
    data_json = classrank.data_to_json(reformatted_data_json)
    return data_json

@app.get("/table/")
def get_students_info(class_id: str):
    students_data = table.get_students_info(class_id)
    reformatted_data_json = table.reformat_student_data(students_data)
    data_json = table.data_to_json(reformatted_data_json)
    return data_json


@app.get("/get_student_scores_data")
def get_data_from_student_scores_summary():
    return Lkx.get_data_from_student_scores_summary()

@app.get("/get_class_knowledge_data")
def get_class_knowledge_data():
    data = Lkx.get_data_from_class_knowledge_summary()
    return data

# @app.get("/get_projection_data")
# def get_projection_data():
#     # 读取 JSON 文件
#     with open('output_pred.json', 'r') as file:
#         data = json.load(file)
#     return data

@app.get("/get_projection_data/")
def get_projection_data(class_id: str, method: str, embedding: str):
    print(f"get_students_vis_data_2d: {class_id}, {method}, {embedding}")
    students_data = scatter_ring.get_students_vis_data_2d(class_id, method, embedding)
    reformatted_data_json = scatter_ring.reformat_student_data_2d(students_data, method)
    data_json = scatter_ring.data_to_json(reformatted_data_json)
    return data_json

@app.get("/get_check_data/")
def get_projection_data(student_id: str):
    time_level_data = check.get_students_time_level(student_id)
    reformatted_data_json = check.reformat_student_data(time_level_data)
    data_json = check.data_to_json(reformatted_data_json)
    return data_json

@app.get("/get_checkring_data/")
def get_checkring_data(student_id: str, year: int, month: int, date: int):
    submit_data_by_date = checkring.get_state_percentage_by_date(student_id, year, month, date)
    # print(submit_data_by_date)
    reformatted_data_json = checkring.reformat_ring_data(submit_data_by_date)
    data_json = checkring.data_to_json(reformatted_data_json)
    return data_json

@app.get("/get_checkradar_data/")
def get_checkring_data(student_id: str, year: int, month: int, date: int):
    submit_data_by_date = checkradar.get_submit_times_hour_by_date(student_id, year, month, date)
    reformatted_data_json = checkradar.reformat_radar_data(submit_data_by_date)
    data_json = checkradar.data_to_json(reformatted_data_json)
    return data_json

@app.get("/get_stack_data/")
def get_projection_data():
    students_datas = stack.get_students_knowledge_norm()
    reformatted_data_json = stack.reformat_student_data(students_datas)
    data_json = stack.data_to_json(reformatted_data_json)
    return data_json

@app.get("/scatterMatrix/")
def get_students_scatter_matrix_data(class_id: str):
    students_data = scaterMatrix.get_students_ranking_data(class_id)
    reformatted_data_json = scaterMatrix.reformat_student_data(students_data)
    data_json = scaterMatrix.data_to_json(reformatted_data_json)
    return data_json

@app.get("/boxplot/")
def get_students_scatter_matrix_data(cluster_id: str, class_id: str):
    students_data = boxplot.get_students_ranking_data(cluster_id,class_id)
    reformatted_data_json = boxplot.reformat_student_data(students_data)
    data_json = boxplot.data_to_json(reformatted_data_json)
    return data_json

# 不使用流式传输
@app.get("/getComments/") 
def get_comments_data(student_id: str):
    students_data = aitool.get_students_info(student_id)
    comments = aitool.get_comment_from_kimi(students_data)
    reformatted_data_json = aitool.reformat_student_data(comments)
    data_json = aitool.data_to_json(reformatted_data_json)
    return data_json

# 成功实现了流式传输
@app.get("/getComments_stream/")
async def get_comments_data_stream(student_id: str):

    students_data = aitool.get_students_info(student_id)
    comment_stream = aitool.get_comment_from_kimi_stream(students_data)
    # 应该是等一秒传一次流
    # await asyncio.sleep(1)
    return StreamingResponse(comment_stream, media_type="text/event-stream")

@app.get("/bubpie/")
def get_students_scatter_matrix_data(student_id: str):
    student_title_score = bubpie.get_students_title_score(student_id)
    reformatted_data_json = bubpie.reformat_student_title_score(student_title_score)
    data_json = bubpie.data_to_json(reformatted_data_json)
    return data_json

@app.get("/getStudentByClass/")
def get_studentbyclass(className: str):
    student4class_data = studentshow.get_studentbyclass(className)
    reformatted_data_json = studentshow.reformat_student_data(student4class_data)
    data_json = studentshow.data_to_json(reformatted_data_json)
    return data_json

@app.get("/getStudentByTime/")
def get_studentbyclass(startTime: str, endTime: str, className: str):
    student_data_by_time = studentshow.get_student_by_time(startTime, endTime, className)
    reformat_student_data_by_time = studentshow.reformat_student_data_by_time(student_data_by_time)
    data_json = studentshow.data_to_json(reformat_student_data_by_time)
    return data_json

@app.get("/titleperf/")
def get_studentbyclass(student_id: str, title_id: str):
    student_submit_data = titleperf.get_student_submit_data(student_id, title_id)
    reformatted_data_json = titleperf.reformat_student_submit_data(student_submit_data)
    data_json = titleperf.data_to_json(reformatted_data_json)
    return data_json

@app.get("/heatmap/")
def get_studentbyclass(class_id: str):
    students_knowledge_timeconsume = heatmap.get_students_knowledge_timeconsume(class_id)
    data_json = heatmap.data_to_json(students_knowledge_timeconsume)
    return data_json

@app.get("/titleprocess/")
def get_student_submit_process(student_id: str, title_id: str):
    student_submit_data = titleprocess.get_student_submit_data(student_id, title_id)
    reformatted_data_json = titleprocess.reformat_student_submit_data(student_submit_data, title_id)
    data_json = titleprocess.data_to_json(reformatted_data_json)
    return data_json

@app.get("/forget/")
def get_student_submit_process(student_id: str, knowledge_id: str):
    students_knowledge_timeconsume = forgetcur.get_students_knowledge_timeconsume(student_id, knowledge_id)
    reformatted_data_json = forgetcur.reformat_student_submit_data(students_knowledge_timeconsume)
    data_json = forgetcur.data_to_json(reformatted_data_json)
    # print(data_json)
    return data_json

if __name__ == '__main__':
    uvicorn.run("Run:app", host="0.0.0.0", port=8080)