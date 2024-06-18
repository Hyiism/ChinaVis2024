<template>
  <!-- 变换图 展示总体知识点和题目情况 -->
  <div class="chart-container-right">
    <div id="main-right"> </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import PubSub from 'pubsub-js';

export default {
  name: 'EChartsComponent',
  data() {

    return {
      treemapOption: {
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
          // textStyle: {
          //   fontSize: 13 // 设置字体大小
          // },
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
            },
            upperLabel: {
              show: true,
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
            levels: [
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
            ],
            data: [{ 'name': 'b3C9s', 'size': 3, 'value': 3, 'children': [{ 'name': 'j0v1yls8', 'size': 1, 'value': 1, 'children': [{ 'name': 'FNg8X9v5zcbB1tQrxHR3', 'size': 1, 'value': 1 }] }, { 'name': 'l4z6od7y', 'size': 2, 'value': 2, 'children': [{ 'name': 'hZ5wXofebmTlzKB1jNcP', 'size': 1, 'value': 1 }, { 'name': 'bumGRTJ0c8p4v5D6eHZa', 'size': 1, 'value': 1 }] }] }, { 'name': 'g7R2j', 'size': 5, 'value': 5, 'children': [{ 'name': 'j1g8gd3v', 'size': 1, 'value': 1, 'children': [{ 'name': 'YWXHr4G6Cl7bEm9iF2kQ', 'size': 1, 'value': 1 }] }, { 'name': 'e0v1yls8', 'size': 4, 'value': 4, 'children': [{ 'name': 'xqlJkmRaP0otZcX4fK3W', 'size': 1, 'value': 1 }, { 'name': 'oCjnFLbIs4Uxwek9rBpu', 'size': 1, 'value': 1 }, { 'name': 'X3wF8QlTyi4mZkDp9Kae', 'size': 1, 'value': 1 }, { 'name': '5fgqjSBwTPG7KUV3it6O', 'size': 1, 'value': 1 }] }] }, { 'name': 'k4W1c', 'size': 1, 'value': 1, 'children': [{ 'name': 'h5r6nux7', 'size': 1, 'value': 1, 'children': [{ 'name': 'lU2wvHSZq7m43xiVroBc', 'size': 1, 'value': 1 }] }] }, { 'name': 'm3D1v', 'size': 12, 'value': 12, 'children': [{ 'name': 'v3d9is1x', 'size': 2, 'value': 2, 'children': [{ 'name': '7NJzCXUPcvQF4Mkfh9Wr', 'size': 1, 'value': 1 }, { 'name': 'ZTbD7mxr2OUp8Fz6iNjy', 'size': 1, 'value': 1 }] }, { 'name': 't0v5ts9h', 'size': 1, 'value': 1, 'children': [{ 'name': 'Jr4Wz5jLqmN01KUwHa7g', 'size': 1, 'value': 1 }] }, { 'name': 'r1d7fr3l', 'size': 9, 'value': 9, 'children': [{ 'name': 'QRm48lXxzdP7Tn1WgNOf', 'size': 1, 'value': 1 }, { 'name': 'h7pXNg80nJbw1C4kAPRm', 'size': 1, 'value': 1 }, { 'name': 'NixCn84GdK2tySa5rB1V', 'size': 1, 'value': 1 }, { 'name': '6RQj2gF3OeK5AmDvThUV', 'size': 1, 'value': 1 }, { 'name': 'pVKXjZn0BkSwYcsa7C31', 'size': 1, 'value': 1 }, { 'name': '4nHcauCQ0Y6Pm8DgKlLo', 'size': 1, 'value': 1 }, { 'name': 'TmKaGvfNoXYq4FZ2JrBu', 'size': 1, 'value': 1 }, { 'name': 'n2BTxIGw1Mc3Zo6RLdUe', 'size': 1, 'value': 1 }, { 'name': 'oCjnFLbIs4Uxwek9rBpu', 'size': 1, 'value': 1 }] }] }, { 'name': 'r8S3g', 'size': 6, 'value': 6, 'children': [{ 'name': 'n0m9rsw4', 'size': 4, 'value': 4, 'children': [{ 'name': 'rvB9mVE6Kbd8jAY4NwPx', 'size': 1, 'value': 1 }, { 'name': 'BW0ItEaymH3TkD6S15JF', 'size': 1, 'value': 1 }, { 'name': 'q7OpB2zCMmW9wS8uNt3H', 'size': 1, 'value': 1 }, { 'name': 'fZrP3FJ4ebUogW9V7taS', 'size': 1, 'value': 1 }] }, { 'name': 'l0p5viby', 'size': 2, 'value': 2, 'children': [{ 'name': 'q7OpB2zCMmW9wS8uNt3H', 'size': 1, 'value': 1 }, { 'name': 'VgKw8PjY1FR6cm2QI9XW', 'size': 1, 'value': 1 }] }] }, { 'name': 's8Y2f', 'size': 1, 'value': 1, 'children': [{ 'name': 'v4x8by9j', 'size': 1, 'value': 1, 'children': [{ 'name': 'x2Fy7rZ3SwYl9jMQkpOD', 'size': 1, 'value': 1 }] }] }, { 'name': 't5V9e', 'size': 5, 'value': 5, 'children': [{ 'name': 'e1k6cixp', 'size': 5, 'value': 5, 'children': [{ 'name': '3MwAFlmNO8EKrpY5zjUd', 'size': 1, 'value': 1 }, { 'name': '3oPyUzDmQtcMfLpGZ0jW', 'size': 1, 'value': 1 }, { 'name': 'tgOjrpZLw4RdVzQx85h6', 'size': 1, 'value': 1 }, { 'name': 's6VmP1G4UbEQWRYHK9Fd', 'size': 1, 'value': 1 }, { 'name': 'x2L7AqbMuTjCwPFy6vNr', 'size': 1, 'value': 1 }] }] }, { 'name': 'y9W5d', 'size': 11, 'value': 11, 'children': [{ 'name': 'p8g6dgtv', 'size': 2, 'value': 2, 'children': [{ 'name': 'Az73sM0rHfWVKuc4X2kL', 'size': 1, 'value': 1 }, { 'name': 'Ou3f2Wt9BqExm5DpN7Zk', 'size': 1, 'value': 1 }] }, { 'name': 'c0w4mj5h', 'size': 8, 'value': 8, 'children': [{ 'name': 'QRm48lXxzdP7Tn1WgNOf', 'size': 1, 'value': 1 }, { 'name': 'Mh4CZIsrEfxkP1wXtOYV', 'size': 1, 'value': 1 }, { 'name': '62XbhBvJ8NUSnApgDL94', 'size': 1, 'value': 1 }, { 'name': 'Ej5mBw9rsOUKkFycGvz2', 'size': 1, 'value': 1 }, { 'name': 'pVKXjZn0BkSwYcsa7C31', 'size': 1, 'value': 1 }, { 'name': 'UXqN1F7G3Sbldz02vZne', 'size': 1, 'value': 1 }, { 'name': 'x2Fy7rZ3SwYl9jMQkpOD', 'size': 1, 'value': 1 }, { 'name': 'lU2wvHSZq7m43xiVroBc', 'size': 1, 'value': 1 }] }, { 'name': 'e2j7p95s', 'size': 1, 'value': 1, 'children': [{ 'name': 'EhVPdmlB31M8WKGqL0wc', 'size': 1, 'value': 1 }] }] }]
          }
        ]
      }


    };
  },
  mounted() {

    this.initChart();
    // 订阅消息
    PubSub.subscribe('title_ID', (msg, data) => {
      console.log("PubSub订阅的title_ID!!!")
      console.log(data)
      // 通了
      this.handleMessage(data);
    });


    window.addEventListener('resize', this.resizeChart);

  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart);
  },
  methods: {

    initChart() {
      console.log("!!!!treemap初始化initChart()内部")
      var chartDom = document.getElementById('main-right');
      this.chart = echarts.init(chartDom);
      this.chart.setOption(this.treemapOption);

      
      this.chart.dispatchAction({
          type: 'showTip',
          name: 'b3C9s'
        });
    },

    handleMessage(title_ID) {

      this.chart.dispatchAction({
          type: 'showTip',
          name: 'b3C9s'
        });
      // 查找对应节点的数据路径
      // console.log("treemapOption中的数据")
      // console.log(this.treemapOption.series[0].data)
      // const targetNode = this.findNodeById(this.treemapOption.series[0].data, title_ID);
      // console.log("targetNode的值:  ")
      // console.log(targetNode)
      // if (true) {
      //   console.log("targetNode.dataIndex的值")
      //   console.log(targetNode.dataIndex)
      //   // 触发点击效果
      //   this.chart.dispatchAction({
      //     type: 'highlight',
      //     name: 'b3C9s'
      //   });
      //   //显示 tooltip
      //   this.chart.dispatchAction({
      //     type: 'showTip',
      //     name: 'b3C9s'
      //   });
      // }
    },
    findNodeById(data, id) {
      for (let node of data) {
        console.log("findNodeById中的node")
        console.log(node)
        if (node.name === id) {
          return node;
        } else if (node.children) {
          const result = this.findNodeById(node.children, id);
          if (result) {
            return result;
          }
        }
      }
      return null;
    },
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
