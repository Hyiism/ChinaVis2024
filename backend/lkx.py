import pandas as pd
import pymysql

class Lkx:
    def get_data_from_class_knowledge_summary():
        # 配置数据库连接信息
        db_config = {
            'host': 'localhost',  # 数据库地址
            'user': 'root',  # 数据库用户名
            'password': 'qyh443012.',  # 数据库密码
            'database': 'chinavis2024'  # 数据库名称
        }

        # 连接数据库
        connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # 执行查询
                sql_query = """
                                SELECT class_id, b3C9s_score, g7R2j_score, k4W1c_score, m3D1v_score,
                                    r8S3g_score, s8Y2f_score, t5V9e_score, y9W5d_score, class_average_score
                                FROM class_knowledge_summary
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
        # # 配置数据库连接信息
        # db_config = {
        #     'host': 'localhost',  # 数据库地址
        #     'user': 'root',  # 数据库用户名
        #     'password': '13957724109@lkx',  # 数据库密码
        #     'database': 'chinavis_data'  # 数据库名称
        # }
        #
        # # 连接数据库
        # connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        #
        # try:
        #     with connection.cursor() as cursor:
        #         # 执行查询，只获取前9行
        #         sql_query = """
        #                         SELECT student_id, Question_VgKw8PjY1FR6cm2QI9XW_score, Question_q7OpB2zCMmW9wS8uNt3H_score,
        #                                Question_fZrP3FJ4ebUogW9V7taS_score, Question_BW0ItEaymH3TkD6S15JF_score,
        #                                Question_rvB9mVE6Kbd8jAY4NwPx_score, Question_3oPyUzDmQtcMfLpGZ0jW_score,
        #                                Question_3MwAFlmNO8EKrpY5zjUd_score, Question_x2L7AqbMuTjCwPFy6vNr_score,
        #                                Question_tgOjrpZLw4RdVzQx85h6_score, Question_s6VmP1G4UbEQWRYHK9Fd_score,
        #                                Question_h7pXNg80nJbw1C4kAPRm_score, Question_6RQj2gF3OeK5AmDvThUV_score,
        #                                Question_4nHcauCQ0Y6Pm8DgKlLo_score, Question_TmKaGvfNoXYq4FZ2JrBu_score,
        #                                Question_NixCn84GdK2tySa5rB1V_score, Question_n2BTxIGw1Mc3Zo6RLdUe_score,
        #                                Question_7NJzCXUPcvQF4Mkfh9Wr_score, Question_ZTbD7mxr2OUp8Fz6iNjy_score,
        #                                Question_Jr4Wz5jLqmN01KUwHa7g_score, Question_QRm48lXxzdP7Tn1WgNOf_score,
        #                                Question_pVKXjZn0BkSwYcsa7C31_score, Question_Ej5mBw9rsOUKkFycGvz2_score,
        #                                Question_lU2wvHSZq7m43xiVroBc_score, Question_Mh4CZIsrEfxkP1wXtOYV_score,
        #                                Question_62XbhBvJ8NUSnApgDL94_score, Question_x2Fy7rZ3SwYl9jMQkpOD_score,
        #                                Question_UXqN1F7G3Sbldz02vZne_score, Question_Ou3f2Wt9BqExm5DpN7Zk_score,
        #                                Question_Az73sM0rHfWVKuc4X2kL_score, Question_EhVPdmlB31M8WKGqL0wc_score,
        #                                Question_oCjnFLbIs4Uxwek9rBpu_score, Question_5fgqjSBwTPG7KUV3it6O_score,
        #                                Question_X3wF8QlTyi4mZkDp9Kae_score, Question_YWXHr4G6Cl7bEm9iF2kQ_score,
        #                                Question_xqlJkmRaP0otZcX4fK3W_score, Question_bumGRTJ0c8p4v5D6eHZa_score,
        #                                Question_hZ5wXofebmTlzKB1jNcP_score, Question_FNg8X9v5zcbB1tQrxHR3_score
        #                         FROM chinavis_data.student_scores_summary
        #                         LIMIT 9
        #                         """
        #         cursor.execute(sql_query)
        #         # 获取结果
        #         result = cursor.fetchall()
        #         return result
        # finally:
        #     # 关闭连接
        #     connection.close()
