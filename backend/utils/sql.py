import pymysql

# 建立数据库连接
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='qyh443012.',
                             database='chinavis2024')

question_ids = [
    'Question_3MwAFlmNO8EKrpY5zjUd',
    'Question_3oPyUzDmQtcMfLpGZ0jW',
    'Question_4nHcauCQ0Y6Pm8DgKlLo',
    'Question_5fgqjSBwTPG7KUV3it6O',
    'Question_62XbhBvJ8NUSnApgDL94',
    'Question_6RQj2gF3OeK5AmDvThUV',
    'Question_7NJzCXUPcvQF4Mkfh9Wr',
    'Question_Az73sM0rHfWVKuc4X2kL',
    'Question_bumGRTJ0c8p4v5D6eHZa',
    'Question_BW0ItEaymH3TkD6S15JF',
    'Question_EhVPdmlB31M8WKGqL0wc',
    'Question_Ej5mBw9rsOUKkFycGvz2',
    'Question_FNg8X9v5zcbB1tQrxHR3',
    'Question_fZrP3FJ4ebUogW9V7taS',
    'Question_h7pXNg80nJbw1C4kAPRm',
    'Question_hZ5wXofebmTlzKB1jNcP',
    'Question_Jr4Wz5jLqmN01KUwHa7g',
    'Question_lU2wvHSZq7m43xiVroBc',
    'Question_Mh4CZIsrEfxkP1wXtOYV',
    'Question_n2BTxIGw1Mc3Zo6RLdUe',
    'Question_NixCn84GdK2tySa5rB1V',
    'Question_oCjnFLbIs4Uxwek9rBpu',
    'Question_Ou3f2Wt9BqExm5DpN7Zk',
    'Question_pVKXjZn0BkSwYcsa7C31',
    'Question_q7OpB2zCMmW9wS8uNt3H',
    'Question_QRm48lXxzdP7Tn1WgNOf',
    'Question_rvB9mVE6Kbd8jAY4NwPx',
    'Question_s6VmP1G4UbEQWRYHK9Fd',
    'Question_tgOjrpZLw4RdVzQx85h6',
    'Question_TmKaGvfNoXYq4FZ2JrBu',
    'Question_UXqN1F7G3Sbldz02vZne',
    'Question_VgKw8PjY1FR6cm2QI9XW',
    'Question_x2Fy7rZ3SwYl9jMQkpOD',
    'Question_x2L7AqbMuTjCwPFy6vNr',
    'Question_X3wF8QlTyi4mZkDp9Kae',
    'Question_xqlJkmRaP0otZcX4fK3W',
    'Question_YWXHr4G6Cl7bEm9iF2kQ',
    'Question_ZTbD7mxr2OUp8Fz6iNjy'
]


try:
    with connection.cursor() as cursor:
        # 初始化SQL查询
        sql_query = "create table student_features_detail as SELECT student_id,"
        
        # 遍历题目ID列表并添加到查询中
        for question_id in question_ids:
            sql_query += f" MAX(CASE WHEN title_id = '{question_id}' THEN submit_times ELSE NULL END) AS {question_id}_submit_times,"
            sql_query += f" MAX(CASE WHEN title_id = '{question_id}' THEN elapsed_time ELSE NULL END) AS {question_id}_elapsed_time,"
            sql_query += f" MAX(CASE WHEN title_id = '{question_id}' THEN paper_score_max ELSE NULL END) AS {question_id}_paper_score_max,"
            sql_query += f" MAX(CASE WHEN title_id = '{question_id}' THEN memory_min ELSE NULL END) AS {question_id}_memory_min,"
            sql_query += f" MAX(CASE WHEN title_id = '{question_id}' THEN timeconsume_min ELSE NULL END) AS {question_id}_timeconsume_min,"
        
        # 移除最后一个逗号
        sql_query = sql_query[:-1]
        
        # 添加剩余部分的查询语句
        sql_query += " FROM students_summary_1 GROUP BY student_id;"
        
        # 执行SQL查询
        cursor.execute(sql_query)
        
        # 获取查询结果
        results = cursor.fetchall()
        
        print(results)
            
finally:
    # 关闭数据库连接
    connection.close()