import json
import pymysql

class BubPie:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_connection(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def get_students_title_score(self, student_id):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = f"""
            SELECT *
            FROM student_scores_summary_1
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
        return results
    
    
    # 格式化成需要数据
    def reformat_student_title_score(self, student_titel_score):
        # # print(student_titel_score)
        # score_list = []
        # title_list = [
        #             "Question_lU2wvHSZq7m43xiVroBc_score",
        #             "Question_FNg8X9v5zcbB1tQrxHR3_score",
        #             "Question_hZ5wXofebmTlzKB1jNcP_score",
        #             "Question_bumGRTJ0c8p4v5D6eHZa_score",
        #             "Question_VgKw8PjY1FR6cm2QI9XW_score",
        #             "Question_rvB9mVE6Kbd8jAY4NwPx_score",
        #             "Question_BW0ItEaymH3TkD6S15JF_score",
        #             "Question_fZrP3FJ4ebUogW9V7taS_score",
        #             "Question_q7OpB2zCMmW9wS8uNt3H_score",
        #             "Question_q7OpB2zCMmW9wS8uNt3H_score",
        #             "Question_oCjnFLbIs4Uxwek9rBpu_score",
        #             "Question_pVKXjZn0BkSwYcsa7C31_score",
        #             "Question_h7pXNg80nJbw1C4kAPRm_score",
        #             "Question_6RQj2gF3OeK5AmDvThUV_score",
        #             "Question_4nHcauCQ0Y6Pm8DgKlLo_score",
        #             "Question_TmKaGvfNoXYq4FZ2JrBu_score",
        #             "Question_NixCn84GdK2tySa5rB1V_score",
        #             "Question_n2BTxIGw1Mc3Zo6RLdUe_score",
        #             "Question_7NJzCXUPcvQF4Mkfh9Wr_score",
        #             "Question_ZTbD7mxr2OUp8Fz6iNjy_score",
        #             "Question_Jr4Wz5jLqmN01KUwHa7g_score",
        #             "Question_QRm48lXxzdP7Tn1WgNOf_score",
        #             "Question_Ej5mBw9rsOUKkFycGvz2_score",
        #             "Question_lU2wvHSZq7m43xiVroBc_score",
        #             "Question_Mh4CZIsrEfxkP1wXtOYV_score",
        #             "Question_62XbhBvJ8NUSnApgDL94_score",
        #             "Question_x2Fy7rZ3SwYl9jMQkpOD_score",
        #             "Question_UXqN1F7G3Sbldz02vZne_score",
        #             "Question_Ou3f2Wt9BqExm5DpN7Zk_score",
        #             "Question_Az73sM0rHfWVKuc4X2kL_score",
        #             "Question_EhVPdmlB31M8WKGqL0wc_score",
        #             "Question_pVKXjZn0BkSwYcsa7C31_score",
        #             "Question_s6VmP1G4UbEQWRYHK9Fd_score",
        #             "Question_tgOjrpZLw4RdVzQx85h6_score",
        #             "Question_x2L7AqbMuTjCwPFy6vNr_score",
        #             "Question_3MwAFlmNO8EKrpY5zjUd_score",
        #             "Question_3oPyUzDmQtcMfLpGZ0jW_score",
        #             "Question_xqlJkmRaP0otZcX4fK3W_score",
        #             "Question_YWXHr4G6Cl7bEm9iF2kQ_score",
        #             "Question_X3wF8QlTyi4mZkDp9Kae_score",
        #             "Question_5fgqjSBwTPG7KUV3it6O_score",
        #             "Question_oCjnFLbIs4Uxwek9rBpu_score",
        #             "Question_x2Fy7rZ3SwYl9jMQkpOD_score"
        #             ]
        # for title in title_list:
        #     # print(round(float(student_titel_score[0][title]), 3))
        #     score_list.append(round(float(student_titel_score[0][title]), 3))
        
        # reformatted_data_json = { 'data': score_list }
        rawdata = [
                {
                "knowl": "k4W1c",
                "title": "Question_lU2wvHSZq7m43xiVroBc",
                "score": 0,
                "index": 0,
                "x": 39.445354829121925,
                "y": 194.81755109337433,
                "vy": 0.000020138042427761092,
                "vx": 0.0003180788166611488
                },
                {
                "knowl": "b3C9s",
                "title": "Question_FNg8X9v5zcbB1tQrxHR3",
                "score": 0,
                "index": 1,
                "x": 180.45986610763407,
                "y": 241.59651921385895,
                "vy": 0.00006611057301751824,
                "vx": 0.00010941705356985378
                },
                {
                "knowl": "b3C9s",
                "title": "Question_hZ5wXofebmTlzKB1jNcP",
                "score": 0,
                "index": 2,
                "x": 179.86083260228725,
                "y": 162.7844995033854,
                "vy": 0.000035512553822727995,
                "vx": 0.0002073639834474341
                },
                {
                "knowl": "b3C9s",
                "title": "Question_bumGRTJ0c8p4v5D6eHZa",
                "score": 0,
                "index": 3,
                "x": 207.31113832817238,
                "y": 227.37095295042124,
                "vy": 0.00000651861653412188,
                "vx": -0.00010165866170747482
                },
                {
                "knowl": "r8S3g",
                "title": "Question_VgKw8PjY1FR6cm2QI9XW",
                "score": 0,
                "index": 4,
                "x": 322.1047376408532,
                "y": 180.86767813745018,
                "vy": -0.000019755169167727393,
                "vx": 0.0002680463713620922
                },
                {
                "knowl": "r8S3g",
                "title": "Question_rvB9mVE6Kbd8jAY4NwPx",
                "score": 0,
                "index": 5,
                "x": 326.36701991926145,
                "y": 220.94508620897693,
                "vy": 0.0000010635720258903656,
                "vx": 0.00007229661596812174
                },
                {
                "knowl": "r8S3g",
                "title": "Question_BW0ItEaymH3TkD6S15JF",
                "score": 0,
                "index": 6,
                "x": 343.4069133966621,
                "y": 250.6008296808931,
                "vy": 0.00009233125706010915,
                "vx": -0.000465141264613036
                },
                {
                "knowl": "r8S3g",
                "title": "Question_fZrP3FJ4ebUogW9V7taS",
                "score": 0,
                "index": 7,
                "x": 348.9533943836583,
                "y": 153.6036802688698,
                "vy": 0.000003353258529835879,
                "vx": 0.00010743117380966453
                },
                {
                "knowl": "r8S3g",
                "title": "Question_q7OpB2zCMmW9wS8uNt3H",
                "score": 0,
                "index": 8,
                "x": 356.37628095750375,
                "y": 224.87349536726376,
                "vy": 0.00021636787838558944,
                "vx": -0.00021865339550835864
                },
                {
                "knowl": "r8S3g",
                "title": "Question_q7OpB2zCMmW9wS8uNt3H",
                "score": 0,
                "index": 9,
                "x": 348.91249686637474,
                "y": 201.98423993503846,
                "vy": 0.00009672590929710767,
                "vx": 0.0001476237880146358
                },
                {
                "knowl": "m3D1v",
                "title": "Question_oCjnFLbIs4Uxwek9rBpu",
                "score": 0,
                "index": 10,
                "x": 464.5465146868178,
                "y": 192.62954611479466,
                "vy": 0.00001471599832497447,
                "vx": 0.00003428240251702747
                },
                {
                "knowl": "m3D1v",
                "title": "Question_pVKXjZn0BkSwYcsa7C31",
                "score": 0,
                "index": 11,
                "x": 467.3108751203343,
                "y": 230.25154423450078,
                "vy": 0.000005783495071556107,
                "vx": 0.0001558704177228545
                },
                {
                "knowl": "m3D1v",
                "title": "Question_h7pXNg80nJbw1C4kAPRm",
                "score": 0,
                "index": 12,
                "x": 468.45953371225573,
                "y": 155.33757980152478,
                "vy": 0.000018182286984408968,
                "vx": 0.00006734926935817606
                },
                {
                "knowl": "m3D1v",
                "title": "Question_6RQj2gF3OeK5AmDvThUV",
                "score": 0,
                "index": 13,
                "x": 493.12966043616797,
                "y": 243.32137529893055,
                "vy": 0.00004632929481480715,
                "vx": -0.00003820819408568119
                },
                {
                "knowl": "m3D1v",
                "title": "Question_4nHcauCQ0Y6Pm8DgKlLo",
                "score": 0,
                "index": 14,
                "x": 493.0875455852879,
                "y": 169.69846389759962,
                "vy": -0.00001717208630548129,
                "vx": -0.00011165511542159286
                },
                {
                "knowl": "m3D1v",
                "title": "Question_TmKaGvfNoXYq4FZ2JrBu",
                "score": 0,
                "index": 15,
                "x": 491.6025595054193,
                "y": 216.24530780884947,
                "vy": 0.00004694588496452593,
                "vx": -0.000057527131966372054
                },
                {
                "knowl": "m3D1v",
                "title": "Question_NixCn84GdK2tySa5rB1V",
                "score": 0,
                "index": 16,
                "x": 471.0690157995491,
                "y": 256.69741050663254,
                "vy": 0.00003206101653993269,
                "vx": -0.00004704450755615086
                },
                {
                "knowl": "m3D1v",
                "title": "Question_n2BTxIGw1Mc3Zo6RLdUe",
                "score": 0,
                "index": 17,
                "x": 491.6423338553399,
                "y": 145.4144495496668,
                "vy": -0.00002518050023300566,
                "vx": 0.000014476402260325024
                },
                {
                "knowl": "m3D1v",
                "title": "Question_7NJzCXUPcvQF4Mkfh9Wr",
                "score": 0,
                "index": 18,
                "x": 497.8106141228157,
                "y": 193.50442967911124,
                "vy": 0.0000041308149941253536,
                "vx": -0.00021436182806509375
                },
                {
                "knowl": "m3D1v",
                "title": "Question_ZTbD7mxr2OUp8Fz6iNjy",
                "score": 0,
                "index": 19,
                "x": 512.8106141228157,
                "y": 220.50442967911124,
                "vy": 0.0000041308149941253536,
                "vx": -0.00021436182806509375
                },
                {
                "knowl": "m3D1v",
                "title": "Question_Jr4Wz5jLqmN01KUwHa7g",
                "score": 0,
                "index": 20,
                "x": 525.8106141228157,
                "y": 250.50442967911124,
                "vy": 0.0000041308149941253536,
                "vx": -0.00021436182806509375
                },
                {
                "knowl": "m3D1v",
                "title": "Question_QRm48lXxzdP7Tn1WgNOf",
                "score": 0,
                "index": 21,
                "x": 540.8106141228157,
                "y": 270.50442967911124,
                "vy": 0.0000041308149941253536,
                "vx": -0.00021436182806509375
                },
                {
                "knowl": "y9W5d",
                "title": "Question_QRm48lXxzdP7Tn1WgNOf",
                "score": 0,
                "index": 22,
                "x": 587.0411019585084,
                "y": 187.7952551215696,
                "vy": -0.000020542899074185056,
                "vx": 0.00022049805106379416
                },
                {
                "knowl": "y9W5d",
                "title": "Question_Ej5mBw9rsOUKkFycGvz2",
                "score": 0,
                "index": 23,
                "x": 647.7929947494189,
                "y": 138.90998733720693,
                "vy": -0.000035626437969656074,
                "vx": -0.0002128384637587492
                },
                {
                "knowl": "y9W5d",
                "title": "Question_lU2wvHSZq7m43xiVroBc",
                "score": 0,
                "index": 24,
                "x": 627.5878730231259,
                "y": 295.36988344003026,
                "vy": 0.00002237448644833396,
                "vx": -0.00006559463142151784
                },
                {
                "knowl": "y9W5d",
                "title": "Question_Mh4CZIsrEfxkP1wXtOYV",
                "score": 0,
                "index": 25,
                "x": 617.6277720435905,
                "y": 104.5010443467315,
                "vy": -0.0000851315582476257,
                "vx": 0.000043993442222414514
                },
                {
                "knowl": "y9W5d",
                "title": "Question_62XbhBvJ8NUSnApgDL94",
                "score": 0,
                "index": 26,
                "x": 620.1956585696946,
                "y": 220.40333639480974,
                "vy": 0.00006301916496347538,
                "vx": -0.000011923442366443683
                },
                {
                "knowl": "y9W5d",
                "title": "Question_x2Fy7rZ3SwYl9jMQkpOD",
                "score": 0,
                "index": 27,
                "x": 578.8453650966497,
                "y": 231.22808063759985,
                "vy": -0.00005712149337100598,
                "vx": 0.0000029326679587927258
                },
                {
                "knowl": "y9W5d",
                "title": "Question_UXqN1F7G3Sbldz02vZne",
                "score": 0,
                "index": 28,
                "x": 604.5567752968274,
                "y": 146.38019867640517,
                "vy": -0.0000414395287790441,
                "vx": 0.00018398077041675734
                },
                {
                "knowl": "y9W5d",
                "title": "Question_Ou3f2Wt9BqExm5DpN7Zk",
                "score": 0,
                "index": 29,
                "x": 645.7255431581275,
                "y": 255.49285211497275,
                "vy": 0.00013698164773903634,
                "vx": -0.00011289752149132694
                },
                {
                "knowl": "y9W5d",
                "title": "Question_Az73sM0rHfWVKuc4X2kL",
                "score": 0,
                "index": 30,
                "x": 630.5549998868297,
                "y": 178.67775821732926,
                "vy": 0.00007301721547825808,
                "vx": 0.00003334552114275054
                },
                {
                "knowl": "y9W5d",
                "title": "Question_EhVPdmlB31M8WKGqL0wc",
                "score": 0,
                "index": 31,
                "x": 660.2251864549087,
                "y": 206.15636614705235,
                "vy": 0.00012616042810775842,
                "vx": -0.00002996027548390376
                },
                {
                "knowl": "y9W5d",
                "title": "Question_pVKXjZn0BkSwYcsa7C31",
                "score": 0,
                "index": 31,
                "x": 606.0739545765028,
                "y": 259.4163321903518,
                "vy": 0.00003437955710474748,
                "vx": -0.0000917929691926957
                },
                {
                "knowl": "t5V9e",
                "title": "Question_s6VmP1G4UbEQWRYHK9Fd",
                "score": 0,
                "index": 33,
                "x": 767.5569689560003,
                "y": 141.42019884441768,
                "vy": -0.0000980095010924115,
                "vx": -0.00008240739873079216
                },
                {
                "knowl": "t5V9e",
                "title": "Question_tgOjrpZLw4RdVzQx85h6",
                "score": 0,
                "index": 34,
                "x": 774.2293413486527,
                "y": 236.79729807423274,
                "vy": 0.00016266351134719433,
                "vx": -0.00025732147597011496
                },
                {
                "knowl": "t5V9e",
                "title": "Question_x2L7AqbMuTjCwPFy6vNr",
                "score": 0,
                "index": 35,
                "x": 747.5025213767166,
                "y": 211.5807048893494,
                "vy": -0.00008291840832414185,
                "vx": 0.00007901407679054492
                },
                {
                "knowl": "t5V9e",
                "title": "Question_3MwAFlmNO8EKrpY5zjUd",
                "score": 0,
                "index": 36,
                "x": 760.50703835412,
                "y": 180.70641702604604,
                "vy": -0.00004576487228237686,
                "vx": 0.00017457857239144874
                },
                {
                "knowl": "t5V9e",
                "title": "Question_3oPyUzDmQtcMfLpGZ0jW",
                "score": 0,
                "index": 37,
                "x": 756.68698515428,
                "y": 265.55597677622507,
                "vy": 0.000040632525885135474,
                "vx": -0.00002057887644478359
                },
                {
                "knowl": "g7R2j",
                "title": "Question_xqlJkmRaP0otZcX4fK3W",
                "score": 0,
                "index": 38,
                "x": 931.8814537685257,
                "y": 175.81846776395517,
                "vy": 0.000020812381074582012,
                "vx": -0.00032780813859299615
                },
                {
                "knowl": "g7R2j",
                "title": "Question_YWXHr4G6Cl7bEm9iF2kQ",
                "score": 0,
                "index": 39,
                "x": 907.5700464345466,
                "y": 295.8214039698457,
                "vy": 0.00021251477132308778,
                "vx": -0.00020911888324437656
                },
                {
                "knowl": "g7R2j",
                "title": "Question_X3wF8QlTyi4mZkDp9Kae",
                "score": 0,
                "index": 40,
                "x": 914.6888154814897,
                "y": 107.21891353680623,
                "vy": -0.000044482826825138194,
                "vx": -0.000044230482014135625
                },
                {
                "knowl": "g7R2j",
                "title": "Question_5fgqjSBwTPG7KUV3it6O",
                "score": 0,
                "index": 41,
                "x": 916.6145834373942,
                "y": 219.74920693322957,
                "vy": 0.00018267756205971289,
                "vx": 0.00010170389398767882
                },
                {
                "knowl": "g7R2j",
                "title": "Question_oCjnFLbIs4Uxwek9rBpu",
                "score": 0,
                "index": 42,
                "x": 891.0390864780807,
                "y": 254.45461550831132,
                "vy": 0.00012002262948087132,
                "vx": 0.000017726289855203915
                },
                {
                "knowl": "s8Y2f",
                "title": "Question_x2Fy7rZ3SwYl9jMQkpOD",
                "score": 0,
                "index": 43,
                "x": 1073.0074648355371,
                "y": 198.46424363199537,
                "vy": 0.00004523342166738415,
                "vx": 0.00020061353072444834
                }
            ]
        # {'student_id': '0088dc183f73c83f763e', 'Question_VgKw8PjY1FR6cm2QI9XW_score': '3.1022438985014604'}
        for data in rawdata:
            title_score = data["title"] + "_score"
            # 调整气泡大小
            data['score'] = round(float(student_titel_score[0][title_score]),2)*100+70
            data['new_title'] = data['title'][9:14] + '...'
        reformatted_data_json = { 'data': rawdata }
        # print(reformatted_data_json)

        return reformatted_data_json
    

    def data_to_json(self, data):
        return json.dumps(data, indent=4)

# 使用示例
if __name__ == "__main__":
    
    # 创建Parallel类的实例，指定本地数据库连接信息
    bubpie = BubPie(
        host='localhost',
        user='root',
        password='qyh443012.',
        database='chinavis2024'
    )
    student_title_score = bubpie.get_students_title_score("0088dc183f73c83f763e")
    reformatted_data_json = bubpie.reformat_student_title_score(student_title_score)
    data_json = bubpie.data_to_json(reformatted_data_json)
    # print(data_json)
    
