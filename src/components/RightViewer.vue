<template>
  <!-- 桑葚图 展示总体知识点和题目情况 -->
  <div class="chart-container-right">
    <div id="main-right"> </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'EChartsComponent',
  mounted() {
    console.log("!!!!初始化桑吉图前")
    this.initChart();

    window.addEventListener('resize', this.resizeChart);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart);
  },
  methods: {


    initChart() {

      console.log("!!!!初始化")

      var chartDom = document.getElementById('main-right');
      var myChart = echarts.init(chartDom);
      var option;

      const treemapOption = {

        color: [
          "#6AB0CC",  // 浅蓝色
          "#9CB364",  // 浅绿色
          "#CC6464",  // 浅红色
          "#A586CC",  // 浅紫色
          "#CCAC59",  // 浅橙色
          "#7FA6CC",  // 浅蓝色
          "#CC9864",  // 浅珊瑚色
          "#9BCC64"   // 浅橄榄绿
        ],
        title: {
          text: 'Disk Usage',
          left: 'center'
        },


        series: [
          {
            type: 'treemap',
            left: 0,
            top: 40.0,
            right: 0.0,
            bottom: 0.0,

            id: 'knowledge-point-distribution',
            animationDurationUpdate: 1000,
            roam: false,
            nodeClick: undefined,
            data: [{ 'name': 'b3C9s', 'size': 3, 'value': 3, 'children': [{ 'name': 'b3C9s_l4z6od7y', 'size': 2, 'value': 2, 'children': [{ 'name': 'Question_bumGRTJ0c8p4v5D6eHZa', 'size': 1, 'value': 1 }, { 'name': 'Question_hZ5wXofebmTlzKB1jNcP', 'size': 1, 'value': 1 }] }, { 'name': 'b3C9s_j0v1yls8', 'size': 1, 'value': 1, 'children': [{ 'name': 'Question_FNg8X9v5zcbB1tQrxHR3', 'size': 1, 'value': 1 }] }] }, { 'name': 'g7R2j', 'size': 5, 'value': 5, 'children': [{ 'name': 'g7R2j_e0v1yls8', 'size': 4, 'value': 4, 'children': [{ 'name': 'Question_X3wF8QlTyi4mZkDp9Kae', 'size': 1, 'value': 1 }, { 'name': 'Question_oCjnFLbIs4Uxwek9rBpu', 'size': 1, 'value': 1 }, { 'name': 'Question_xqlJkmRaP0otZcX4fK3W', 'size': 1, 'value': 1 }, { 'name': 'Question_5fgqjSBwTPG7KUV3it6O', 'size': 1, 'value': 1 }] }, { 'name': 'g7R2j_j1g8gd3v', 'size': 1, 'value': 1, 'children': [{ 'name': 'Question_YWXHr4G6Cl7bEm9iF2kQ', 'size': 1, 'value': 1 }] }] }, { 'name': 'k4W1c', 'size': 1, 'value': 1, 'children': [{ 'name': 'k4W1c_h5r6nux7', 'size': 1, 'value': 1, 'children': [{ 'name': 'Question_lU2wvHSZq7m43xiVroBc', 'size': 1, 'value': 1 }] }] }, { 'name': 'm3D1v', 'size': 12, 'value': 12, 'children': [{ 'name': 'm3D1v_v3d9is1x', 'size': 2, 'value': 2, 'children': [{ 'name': 'Question_7NJzCXUPcvQF4Mkfh9Wr', 'size': 1, 'value': 1 }, { 'name': 'Question_ZTbD7mxr2OUp8Fz6iNjy', 'size': 1, 'value': 1 }] }, { 'name': 'm3D1v_t0v5ts9h', 'size': 1, 'value': 1, 'children': [{ 'name': 'Question_Jr4Wz5jLqmN01KUwHa7g', 'size': 1, 'value': 1 }] }, { 'name': 'm3D1v_r1d7fr3l', 'size': 9, 'value': 9, 'children': [{ 'name': 'Question_pVKXjZn0BkSwYcsa7C31', 'size': 1, 'value': 1 }, { 'name': 'Question_n2BTxIGw1Mc3Zo6RLdUe', 'size': 1, 'value': 1 }, { 'name': 'Question_NixCn84GdK2tySa5rB1V', 'size': 1, 'value': 1 }, { 'name': 'Question_6RQj2gF3OeK5AmDvThUV', 'size': 1, 'value': 1 }, { 'name': 'Question_oCjnFLbIs4Uxwek9rBpu', 'size': 1, 'value': 1 }, { 'name': 'Question_QRm48lXxzdP7Tn1WgNOf', 'size': 1, 'value': 1 }, { 'name': 'Question_TmKaGvfNoXYq4FZ2JrBu', 'size': 1, 'value': 1 }, { 'name': 'Question_h7pXNg80nJbw1C4kAPRm', 'size': 1, 'value': 1 }, { 'name': 'Question_4nHcauCQ0Y6Pm8DgKlLo', 'size': 1, 'value': 1 }] }] }, { 'name': 'r8S3g', 'size': 6, 'value': 6, 'children': [{ 'name': 'r8S3g_n0m9rsw4', 'size': 4, 'value': 4, 'children': [{ 'name': 'Question_rvB9mVE6Kbd8jAY4NwPx', 'size': 1, 'value': 1 }, { 'name': 'Question_fZrP3FJ4ebUogW9V7taS', 'size': 1, 'value': 1 }, { 'name': 'Question_q7OpB2zCMmW9wS8uNt3H', 'size': 1, 'value': 1 }, { 'name': 'Question_BW0ItEaymH3TkD6S15JF', 'size': 1, 'value': 1 }] }, { 'name': 'r8S3g_l0p5viby', 'size': 2, 'value': 2, 'children': [{ 'name': 'Question_VgKw8PjY1FR6cm2QI9XW', 'size': 1, 'value': 1 }, { 'name': 'Question_q7OpB2zCMmW9wS8uNt3H', 'size': 1, 'value': 1 }] }] }, { 'name': 's8Y2f', 'size': 1, 'value': 1, 'children': [{ 'name': 's8Y2f_v4x8by9j', 'size': 1, 'value': 1, 'children': [{ 'name': 'Question_x2Fy7rZ3SwYl9jMQkpOD', 'size': 1, 'value': 1 }] }] }, { 'name': 't5V9e', 'size': 5, 'value': 5, 'children': [{ 'name': 't5V9e_e1k6cixp', 'size': 5, 'value': 5, 'children': [{ 'name': 'Question_3oPyUzDmQtcMfLpGZ0jW', 'size': 1, 'value': 1 }, { 'name': 'Question_x2L7AqbMuTjCwPFy6vNr', 'size': 1, 'value': 1 }, { 'name': 'Question_s6VmP1G4UbEQWRYHK9Fd', 'size': 1, 'value': 1 }, { 'name': 'Question_tgOjrpZLw4RdVzQx85h6', 'size': 1, 'value': 1 }, { 'name': 'Question_3MwAFlmNO8EKrpY5zjUd', 'size': 1, 'value': 1 }] }] }, { 'name': 'y9W5d', 'size': 11, 'value': 11, 'children': [{ 'name': 'y9W5d_e2j7p95s', 'size': 1, 'value': 1, 'children': [{ 'name': 'Question_EhVPdmlB31M8WKGqL0wc', 'size': 1, 'value': 1 }] }, { 'name': 'y9W5d_p8g6dgtv', 'size': 2, 'value': 2, 'children': [{ 'name': 'Question_Ou3f2Wt9BqExm5DpN7Zk', 'size': 1, 'value': 1 }, { 'name': 'Question_Az73sM0rHfWVKuc4X2kL', 'size': 1, 'value': 1 }] }, { 'name': 'y9W5d_c0w4mj5h', 'size': 8, 'value': 8, 'children': [{ 'name': 'Question_Mh4CZIsrEfxkP1wXtOYV', 'size': 1, 'value': 1 }, { 'name': 'Question_pVKXjZn0BkSwYcsa7C31', 'size': 1, 'value': 1 }, { 'name': 'Question_lU2wvHSZq7m43xiVroBc', 'size': 1, 'value': 1 }, { 'name': 'Question_UXqN1F7G3Sbldz02vZne', 'size': 1, 'value': 1 }, { 'name': 'Question_QRm48lXxzdP7Tn1WgNOf', 'size': 1, 'value': 1 }, { 'name': 'Question_62XbhBvJ8NUSnApgDL94', 'size': 1, 'value': 1 }, { 'name': 'Question_x2Fy7rZ3SwYl9jMQkpOD', 'size': 1, 'value': 1 }, { 'name': 'Question_Ej5mBw9rsOUKkFycGvz2', 'size': 1, 'value': 1 }] }] }],
            universalTransition: true,
            label: {
              show: true,
              formatter: '{b}'
            },
            breadcrumb: {
              show: false
            }
          }
        ]
      };

      const sunburstOption = {
        series: [
          {
            type: 'sunburst',
            id: 'knowledge-point-distribution',
            radius: ['20%', '90%'],
            animationDurationUpdate: 1000,
            nodeClick: undefined,
            data: [{ 'name': 'b3C9s', 'size': 3, 'value': 3, 'children': [{ 'name': 'b3C9s_l4z6od7y', 'size': 2, 'value': 2, 'children': [{ 'name': 'Question_bumGRTJ0c8p4v5D6eHZa', 'size': 1, 'value': 1 }, { 'name': 'Question_hZ5wXofebmTlzKB1jNcP', 'size': 1, 'value': 1 }] }, { 'name': 'b3C9s_j0v1yls8', 'size': 1, 'value': 1, 'children': [{ 'name': 'Question_FNg8X9v5zcbB1tQrxHR3', 'size': 1, 'value': 1 }] }] }, { 'name': 'g7R2j', 'size': 5, 'value': 5, 'children': [{ 'name': 'g7R2j_e0v1yls8', 'size': 4, 'value': 4, 'children': [{ 'name': 'Question_X3wF8QlTyi4mZkDp9Kae', 'size': 1, 'value': 1 }, { 'name': 'Question_oCjnFLbIs4Uxwek9rBpu', 'size': 1, 'value': 1 }, { 'name': 'Question_xqlJkmRaP0otZcX4fK3W', 'size': 1, 'value': 1 }, { 'name': 'Question_5fgqjSBwTPG7KUV3it6O', 'size': 1, 'value': 1 }] }, { 'name': 'g7R2j_j1g8gd3v', 'size': 1, 'value': 1, 'children': [{ 'name': 'Question_YWXHr4G6Cl7bEm9iF2kQ', 'size': 1, 'value': 1 }] }] }, { 'name': 'k4W1c', 'size': 1, 'value': 1, 'children': [{ 'name': 'k4W1c_h5r6nux7', 'size': 1, 'value': 1, 'children': [{ 'name': 'Question_lU2wvHSZq7m43xiVroBc', 'size': 1, 'value': 1 }] }] }, { 'name': 'm3D1v', 'size': 12, 'value': 12, 'children': [{ 'name': 'm3D1v_v3d9is1x', 'size': 2, 'value': 2, 'children': [{ 'name': 'Question_7NJzCXUPcvQF4Mkfh9Wr', 'size': 1, 'value': 1 }, { 'name': 'Question_ZTbD7mxr2OUp8Fz6iNjy', 'size': 1, 'value': 1 }] }, { 'name': 'm3D1v_t0v5ts9h', 'size': 1, 'value': 1, 'children': [{ 'name': 'Question_Jr4Wz5jLqmN01KUwHa7g', 'size': 1, 'value': 1 }] }, { 'name': 'm3D1v_r1d7fr3l', 'size': 9, 'value': 9, 'children': [{ 'name': 'Question_pVKXjZn0BkSwYcsa7C31', 'size': 1, 'value': 1 }, { 'name': 'Question_n2BTxIGw1Mc3Zo6RLdUe', 'size': 1, 'value': 1 }, { 'name': 'Question_NixCn84GdK2tySa5rB1V', 'size': 1, 'value': 1 }, { 'name': 'Question_6RQj2gF3OeK5AmDvThUV', 'size': 1, 'value': 1 }, { 'name': 'Question_oCjnFLbIs4Uxwek9rBpu', 'size': 1, 'value': 1 }, { 'name': 'Question_QRm48lXxzdP7Tn1WgNOf', 'size': 1, 'value': 1 }, { 'name': 'Question_TmKaGvfNoXYq4FZ2JrBu', 'size': 1, 'value': 1 }, { 'name': 'Question_h7pXNg80nJbw1C4kAPRm', 'size': 1, 'value': 1 }, { 'name': 'Question_4nHcauCQ0Y6Pm8DgKlLo', 'size': 1, 'value': 1 }] }] }, { 'name': 'r8S3g', 'size': 6, 'value': 6, 'children': [{ 'name': 'r8S3g_n0m9rsw4', 'size': 4, 'value': 4, 'children': [{ 'name': 'Question_rvB9mVE6Kbd8jAY4NwPx', 'size': 1, 'value': 1 }, { 'name': 'Question_fZrP3FJ4ebUogW9V7taS', 'size': 1, 'value': 1 }, { 'name': 'Question_q7OpB2zCMmW9wS8uNt3H', 'size': 1, 'value': 1 }, { 'name': 'Question_BW0ItEaymH3TkD6S15JF', 'size': 1, 'value': 1 }] }, { 'name': 'r8S3g_l0p5viby', 'size': 2, 'value': 2, 'children': [{ 'name': 'Question_VgKw8PjY1FR6cm2QI9XW', 'size': 1, 'value': 1 }, { 'name': 'Question_q7OpB2zCMmW9wS8uNt3H', 'size': 1, 'value': 1 }] }] }, { 'name': 's8Y2f', 'size': 1, 'value': 1, 'children': [{ 'name': 's8Y2f_v4x8by9j', 'size': 1, 'value': 1, 'children': [{ 'name': 'Question_x2Fy7rZ3SwYl9jMQkpOD', 'size': 1, 'value': 1 }] }] }, { 'name': 't5V9e', 'size': 5, 'value': 5, 'children': [{ 'name': 't5V9e_e1k6cixp', 'size': 5, 'value': 5, 'children': [{ 'name': 'Question_3oPyUzDmQtcMfLpGZ0jW', 'size': 1, 'value': 1 }, { 'name': 'Question_x2L7AqbMuTjCwPFy6vNr', 'size': 1, 'value': 1 }, { 'name': 'Question_s6VmP1G4UbEQWRYHK9Fd', 'size': 1, 'value': 1 }, { 'name': 'Question_tgOjrpZLw4RdVzQx85h6', 'size': 1, 'value': 1 }, { 'name': 'Question_3MwAFlmNO8EKrpY5zjUd', 'size': 1, 'value': 1 }] }] }, { 'name': 'y9W5d', 'size': 11, 'value': 11, 'children': [{ 'name': 'y9W5d_e2j7p95s', 'size': 1, 'value': 1, 'children': [{ 'name': 'Question_EhVPdmlB31M8WKGqL0wc', 'size': 1, 'value': 1 }] }, { 'name': 'y9W5d_p8g6dgtv', 'size': 2, 'value': 2, 'children': [{ 'name': 'Question_Ou3f2Wt9BqExm5DpN7Zk', 'size': 1, 'value': 1 }, { 'name': 'Question_Az73sM0rHfWVKuc4X2kL', 'size': 1, 'value': 1 }] }, { 'name': 'y9W5d_c0w4mj5h', 'size': 8, 'value': 8, 'children': [{ 'name': 'Question_Mh4CZIsrEfxkP1wXtOYV', 'size': 1, 'value': 1 }, { 'name': 'Question_pVKXjZn0BkSwYcsa7C31', 'size': 1, 'value': 1 }, { 'name': 'Question_lU2wvHSZq7m43xiVroBc', 'size': 1, 'value': 1 }, { 'name': 'Question_UXqN1F7G3Sbldz02vZne', 'size': 1, 'value': 1 }, { 'name': 'Question_QRm48lXxzdP7Tn1WgNOf', 'size': 1, 'value': 1 }, { 'name': 'Question_62XbhBvJ8NUSnApgDL94', 'size': 1, 'value': 1 }, { 'name': 'Question_x2Fy7rZ3SwYl9jMQkpOD', 'size': 1, 'value': 1 }, { 'name': 'Question_Ej5mBw9rsOUKkFycGvz2', 'size': 1, 'value': 1 }] }] }],
            universalTransition: true,
            itemStyle: {
              borderWidth: 1,
              borderColor: 'rgba(255,255,255,.5)'
            },
            label: {
              show: true
            }
          }
        ]
      };

      let currentOption = treemapOption;
      myChart.setOption(currentOption);
      setInterval(function () {
        currentOption =
          currentOption === treemapOption ? sunburstOption : treemapOption;
        myChart.setOption(currentOption);
      }, 3000);
    }
  },
};

</script>

<style scoped>
.chart-container-right {
  position: relative;
  width: 90%;
  height: 90%;
}

#main-right {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
}
</style>
