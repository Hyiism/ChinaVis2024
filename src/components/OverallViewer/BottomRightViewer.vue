<template>
  <!-- 变换图 展示总体知识点和题目情况 -->
  <div class="chart-container-right">
    <div id="main-right"> </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'EChartsComponent',
  mounted() {
    console.log("!!!!初始化treemap前")
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
      function getLevelOption() {
        return [
          {
            itemStyle: {
              borderColor: '	#FFFFFF',
              borderWidth: 0,
              gapWidth: 0
            },
            upperLabel: {
              show: false
            }
          },
          {
            itemStyle: {
              borderColor: '#FFFFFF',
              borderWidth: 2,
              gapWidth: .5
            },
            emphasis: {
              itemStyle: {
                borderColor: '#EEE5DE'
              }
            }
          },
          {
            colorSaturation: [0.6, 0.9],
            itemStyle: {
              borderWidth: 0,
              gapWidth: .5,
              borderColorSaturation: 0.9
            }
          }
        ];
      }



      const treemapOption = {
        tooltip: {
          formatter: function (info) {
            console.info("!!!!!!!!!@@@@@@@TREEMAP")
            console.info(info)
            var value = info.value;
            var treePathInfo = info.treePathInfo;
            var treePath = [];
            for (var i = 1; i < treePathInfo.length; i++) {
              treePath.push(treePathInfo[i].name);
            }
            return [
              '<div class="tooltip-title">' +
              echarts.format.encodeHTML(treePath.join(' ➤ ')) +
              '</div>',
            ].join('');

          },
          textStyle: {
            fontSize: 15 // 设置字体大小zcg
          },
        },
        series: [
          {
            name: 'knowledge-point',
            type: 'treemap',
            id: 'knowledge-point-distribution',
            left: 0,
            top: 0.0,
            right: 0.0,
            bottom: 0.0,
            label: {
              show: true,
              // left: 'center'
              // formatter: '{b}'
            },
            upperLabel: {
              show: true,
              //  left: 'center'
              // fontSize: 14,
              // textBorderWidth: 0

              textStyle: {
                color: '#1C1C1C',
                fontWeight: 540,
                fontSize: 13,
              },
              height: 20
            },
            itemStyle: {
              borderColor: '#FFFFFF'
            },
            textStyle: {
              textShadow: false, // 关闭阴影
              textBorderColor: 'transparent', // 设置文字描边颜色为透明，相当于关闭描边
            },
            levels: getLevelOption(),
            data: [{ 'name': 'b3C9s', 'size': 3, 'value': 3, 'children': [{ 'name': 'j0v1yls8', 'size': 1, 'value': 1, 'children': [{ 'name': 'FNg8X9v5zcbB1tQrxHR3', 'size': 1, 'value': 1 }] }, { 'name': 'l4z6od7y', 'size': 2, 'value': 2, 'children': [{ 'name': 'hZ5wXofebmTlzKB1jNcP', 'size': 1, 'value': 1 }, { 'name': 'bumGRTJ0c8p4v5D6eHZa', 'size': 1, 'value': 1 }] }] }, { 'name': 'g7R2j', 'size': 5, 'value': 5, 'children': [{ 'name': 'j1g8gd3v', 'size': 1, 'value': 1, 'children': [{ 'name': 'YWXHr4G6Cl7bEm9iF2kQ', 'size': 1, 'value': 1 }] }, { 'name': 'e0v1yls8', 'size': 4, 'value': 4, 'children': [{ 'name': 'xqlJkmRaP0otZcX4fK3W', 'size': 1, 'value': 1 }, { 'name': 'oCjnFLbIs4Uxwek9rBpu', 'size': 1, 'value': 1 }, { 'name': 'X3wF8QlTyi4mZkDp9Kae', 'size': 1, 'value': 1 }, { 'name': '5fgqjSBwTPG7KUV3it6O', 'size': 1, 'value': 1 }] }] }, { 'name': 'k4W1c', 'size': 1, 'value': 1, 'children': [{ 'name': 'h5r6nux7', 'size': 1, 'value': 1, 'children': [{ 'name': 'lU2wvHSZq7m43xiVroBc', 'size': 1, 'value': 1 }] }] }, { 'name': 'm3D1v', 'size': 12, 'value': 12, 'children': [{ 'name': 'v3d9is1x', 'size': 2, 'value': 2, 'children': [{ 'name': '7NJzCXUPcvQF4Mkfh9Wr', 'size': 1, 'value': 1 }, { 'name': 'ZTbD7mxr2OUp8Fz6iNjy', 'size': 1, 'value': 1 }] }, { 'name': 't0v5ts9h', 'size': 1, 'value': 1, 'children': [{ 'name': 'Jr4Wz5jLqmN01KUwHa7g', 'size': 1, 'value': 1 }] }, { 'name': 'r1d7fr3l', 'size': 9, 'value': 9, 'children': [{ 'name': 'QRm48lXxzdP7Tn1WgNOf', 'size': 1, 'value': 1 }, { 'name': 'h7pXNg80nJbw1C4kAPRm', 'size': 1, 'value': 1 }, { 'name': 'NixCn84GdK2tySa5rB1V', 'size': 1, 'value': 1 }, { 'name': '6RQj2gF3OeK5AmDvThUV', 'size': 1, 'value': 1 }, { 'name': 'pVKXjZn0BkSwYcsa7C31', 'size': 1, 'value': 1 }, { 'name': '4nHcauCQ0Y6Pm8DgKlLo', 'size': 1, 'value': 1 }, { 'name': 'TmKaGvfNoXYq4FZ2JrBu', 'size': 1, 'value': 1 }, { 'name': 'n2BTxIGw1Mc3Zo6RLdUe', 'size': 1, 'value': 1 }, { 'name': 'oCjnFLbIs4Uxwek9rBpu', 'size': 1, 'value': 1 }] }] }, { 'name': 'r8S3g', 'size': 6, 'value': 6, 'children': [{ 'name': 'n0m9rsw4', 'size': 4, 'value': 4, 'children': [{ 'name': 'rvB9mVE6Kbd8jAY4NwPx', 'size': 1, 'value': 1 }, { 'name': 'BW0ItEaymH3TkD6S15JF', 'size': 1, 'value': 1 }, { 'name': 'q7OpB2zCMmW9wS8uNt3H', 'size': 1, 'value': 1 }, { 'name': 'fZrP3FJ4ebUogW9V7taS', 'size': 1, 'value': 1 }] }, { 'name': 'l0p5viby', 'size': 2, 'value': 2, 'children': [{ 'name': 'q7OpB2zCMmW9wS8uNt3H', 'size': 1, 'value': 1 }, { 'name': 'VgKw8PjY1FR6cm2QI9XW', 'size': 1, 'value': 1 }] }] }, { 'name': 's8Y2f', 'size': 1, 'value': 1, 'children': [{ 'name': 'v4x8by9j', 'size': 1, 'value': 1, 'children': [{ 'name': 'x2Fy7rZ3SwYl9jMQkpOD', 'size': 1, 'value': 1 }] }] }, { 'name': 't5V9e', 'size': 5, 'value': 5, 'children': [{ 'name': 'e1k6cixp', 'size': 5, 'value': 5, 'children': [{ 'name': '3MwAFlmNO8EKrpY5zjUd', 'size': 1, 'value': 1 }, { 'name': '3oPyUzDmQtcMfLpGZ0jW', 'size': 1, 'value': 1 }, { 'name': 'tgOjrpZLw4RdVzQx85h6', 'size': 1, 'value': 1 }, { 'name': 's6VmP1G4UbEQWRYHK9Fd', 'size': 1, 'value': 1 }, { 'name': 'x2L7AqbMuTjCwPFy6vNr', 'size': 1, 'value': 1 }] }] }, { 'name': 'y9W5d', 'size': 11, 'value': 11, 'children': [{ 'name': 'p8g6dgtv', 'size': 2, 'value': 2, 'children': [{ 'name': 'Az73sM0rHfWVKuc4X2kL', 'size': 1, 'value': 1 }, { 'name': 'Ou3f2Wt9BqExm5DpN7Zk', 'size': 1, 'value': 1 }] }, { 'name': 'c0w4mj5h', 'size': 8, 'value': 8, 'children': [{ 'name': 'QRm48lXxzdP7Tn1WgNOf', 'size': 1, 'value': 1 }, { 'name': 'Mh4CZIsrEfxkP1wXtOYV', 'size': 1, 'value': 1 }, { 'name': '62XbhBvJ8NUSnApgDL94', 'size': 1, 'value': 1 }, { 'name': 'Ej5mBw9rsOUKkFycGvz2', 'size': 1, 'value': 1 }, { 'name': 'pVKXjZn0BkSwYcsa7C31', 'size': 1, 'value': 1 }, { 'name': 'UXqN1F7G3Sbldz02vZne', 'size': 1, 'value': 1 }, { 'name': 'x2Fy7rZ3SwYl9jMQkpOD', 'size': 1, 'value': 1 }, { 'name': 'lU2wvHSZq7m43xiVroBc', 'size': 1, 'value': 1 }] }, { 'name': 'e2j7p95s', 'size': 1, 'value': 1, 'children': [{ 'name': 'EhVPdmlB31M8WKGqL0wc', 'size': 1, 'value': 1 }] }] }]
          }
        ]
      };

      const sunburstOption = {
        tooltip: {
          formatter: function (info) {
            var value = info.value;
            var treePathInfo = info.treePathInfo;
            var treePath = [];
            for (var i = 1; i < treePathInfo.length; i++) {
              treePath.push(treePathInfo[i].name);
            }
            return [
              '<div class="tooltip-title">' +
              echarts.format.encodeHTML(treePath.join(' ➤ ')) +
              '</div>',
            ].join('');
          },
          textStyle: {
            fontSize: 20 // 设置字体大小
          },

        },
        series: [
          {
            type: 'sunburst',
            id: 'knowledge-point-distribution',

            left: 0,
            top: 0.0,
            right: 0.0,
            bottom: 0.0,
            radius: ["15%", '98%'],
            sort: undefined,
            emphasis: {
              focus: 'ancestor',
              label: {
                show: false // 鼠标移到系列上时，仍然不显示标签
              }
            },


            itemStyle: {
              borderRadius: 10,
            },
            data: [{ 'name': 'b3C9s', 'size': 3, 'value': 3, 'children': [{ 'name': 'j0v1yls8', 'size': 1, 'value': 1, 'children': [{ 'name': 'FNg8X9v5zcbB1tQrxHR3', 'size': 1, 'value': 1 }] }, { 'name': 'l4z6od7y', 'size': 2, 'value': 2, 'children': [{ 'name': 'hZ5wXofebmTlzKB1jNcP', 'size': 1, 'value': 1 }, { 'name': 'bumGRTJ0c8p4v5D6eHZa', 'size': 1, 'value': 1 }] }] }, { 'name': 'g7R2j', 'size': 5, 'value': 5, 'children': [{ 'name': 'j1g8gd3v', 'size': 1, 'value': 1, 'children': [{ 'name': 'YWXHr4G6Cl7bEm9iF2kQ', 'size': 1, 'value': 1 }] }, { 'name': 'e0v1yls8', 'size': 4, 'value': 4, 'children': [{ 'name': 'xqlJkmRaP0otZcX4fK3W', 'size': 1, 'value': 1 }, { 'name': 'oCjnFLbIs4Uxwek9rBpu', 'size': 1, 'value': 1 }, { 'name': 'X3wF8QlTyi4mZkDp9Kae', 'size': 1, 'value': 1 }, { 'name': '5fgqjSBwTPG7KUV3it6O', 'size': 1, 'value': 1 }] }] }, { 'name': 'k4W1c', 'size': 1, 'value': 1, 'children': [{ 'name': 'h5r6nux7', 'size': 1, 'value': 1, 'children': [{ 'name': 'lU2wvHSZq7m43xiVroBc', 'size': 1, 'value': 1 }] }] }, { 'name': 'm3D1v', 'size': 12, 'value': 12, 'children': [{ 'name': 'v3d9is1x', 'size': 2, 'value': 2, 'children': [{ 'name': '7NJzCXUPcvQF4Mkfh9Wr', 'size': 1, 'value': 1 }, { 'name': 'ZTbD7mxr2OUp8Fz6iNjy', 'size': 1, 'value': 1 }] }, { 'name': 't0v5ts9h', 'size': 1, 'value': 1, 'children': [{ 'name': 'Jr4Wz5jLqmN01KUwHa7g', 'size': 1, 'value': 1 }] }, { 'name': 'r1d7fr3l', 'size': 9, 'value': 9, 'children': [{ 'name': 'QRm48lXxzdP7Tn1WgNOf', 'size': 1, 'value': 1 }, { 'name': 'h7pXNg80nJbw1C4kAPRm', 'size': 1, 'value': 1 }, { 'name': 'NixCn84GdK2tySa5rB1V', 'size': 1, 'value': 1 }, { 'name': '6RQj2gF3OeK5AmDvThUV', 'size': 1, 'value': 1 }, { 'name': 'pVKXjZn0BkSwYcsa7C31', 'size': 1, 'value': 1 }, { 'name': '4nHcauCQ0Y6Pm8DgKlLo', 'size': 1, 'value': 1 }, { 'name': 'TmKaGvfNoXYq4FZ2JrBu', 'size': 1, 'value': 1 }, { 'name': 'n2BTxIGw1Mc3Zo6RLdUe', 'size': 1, 'value': 1 }, { 'name': 'oCjnFLbIs4Uxwek9rBpu', 'size': 1, 'value': 1 }] }] }, { 'name': 'r8S3g', 'size': 6, 'value': 6, 'children': [{ 'name': 'n0m9rsw4', 'size': 4, 'value': 4, 'children': [{ 'name': 'rvB9mVE6Kbd8jAY4NwPx', 'size': 1, 'value': 1 }, { 'name': 'BW0ItEaymH3TkD6S15JF', 'size': 1, 'value': 1 }, { 'name': 'q7OpB2zCMmW9wS8uNt3H', 'size': 1, 'value': 1 }, { 'name': 'fZrP3FJ4ebUogW9V7taS', 'size': 1, 'value': 1 }] }, { 'name': 'l0p5viby', 'size': 2, 'value': 2, 'children': [{ 'name': 'q7OpB2zCMmW9wS8uNt3H', 'size': 1, 'value': 1 }, { 'name': 'VgKw8PjY1FR6cm2QI9XW', 'size': 1, 'value': 1 }] }] }, { 'name': 's8Y2f', 'size': 1, 'value': 1, 'children': [{ 'name': 'v4x8by9j', 'size': 1, 'value': 1, 'children': [{ 'name': 'x2Fy7rZ3SwYl9jMQkpOD', 'size': 1, 'value': 1 }] }] }, { 'name': 't5V9e', 'size': 5, 'value': 5, 'children': [{ 'name': 'e1k6cixp', 'size': 5, 'value': 5, 'children': [{ 'name': '3MwAFlmNO8EKrpY5zjUd', 'size': 1, 'value': 1 }, { 'name': '3oPyUzDmQtcMfLpGZ0jW', 'size': 1, 'value': 1 }, { 'name': 'tgOjrpZLw4RdVzQx85h6', 'size': 1, 'value': 1 }, { 'name': 's6VmP1G4UbEQWRYHK9Fd', 'size': 1, 'value': 1 }, { 'name': 'x2L7AqbMuTjCwPFy6vNr', 'size': 1, 'value': 1 }] }] }, { 'name': 'y9W5d', 'size': 11, 'value': 11, 'children': [{ 'name': 'p8g6dgtv', 'size': 2, 'value': 2, 'children': [{ 'name': 'Az73sM0rHfWVKuc4X2kL', 'size': 1, 'value': 1 }, { 'name': 'Ou3f2Wt9BqExm5DpN7Zk', 'size': 1, 'value': 1 }] }, { 'name': 'c0w4mj5h', 'size': 8, 'value': 8, 'children': [{ 'name': 'QRm48lXxzdP7Tn1WgNOf', 'size': 1, 'value': 1 }, { 'name': 'Mh4CZIsrEfxkP1wXtOYV', 'size': 1, 'value': 1 }, { 'name': '62XbhBvJ8NUSnApgDL94', 'size': 1, 'value': 1 }, { 'name': 'Ej5mBw9rsOUKkFycGvz2', 'size': 1, 'value': 1 }, { 'name': 'pVKXjZn0BkSwYcsa7C31', 'size': 1, 'value': 1 }, { 'name': 'UXqN1F7G3Sbldz02vZne', 'size': 1, 'value': 1 }, { 'name': 'x2Fy7rZ3SwYl9jMQkpOD', 'size': 1, 'value': 1 }, { 'name': 'lU2wvHSZq7m43xiVroBc', 'size': 1, 'value': 1 }] }, { 'name': 'e2j7p95s', 'size': 1, 'value': 1, 'children': [{ 'name': 'EhVPdmlB31M8WKGqL0wc', 'size': 1, 'value': 1 }] }] }],
            levels: [
              {},
              {
                r0: '25%',
                r: '45%',
                itemStyle: {
                  borderWidth: 3
                },
                label: {
                  rotate: 'tangential',
                }
              },
              {
                r0: '50%',
                r: '85%',
                label: {
                  align: 'right'
                }
              },
              {
                r0: '90%',
                r: '95%',
                label: {
                  show: false,
                  // position: 'outside',
                  // padding: 3,
                  // silent: false
                },
                itemStyle: {
                  borderWidth: 3
                }
              }
            ],

          }
        ]
      };

      let currentOption = treemapOption;
      myChart.setOption(currentOption);
      // setInterval(function () {
      //   currentOption =
      //     currentOption === treemapOption ? sunburstOption : treemapOption;
      //   myChart.setOption(currentOption);
      // }, 3000);
    }
  },
};

</script>

<style scoped>
.chart-container-right {
  position: relative;
  width: 98%;
  height: 98%;
}

#main-right {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
}
</style>
