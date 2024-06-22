<template>
  <div class="chart-container-right">
    <div id="main"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import PubSub from 'pubsub-js';
import EventBus from '@/eventBus'; // 导入事件总线

export default {
  name: 'SimpleEChartsComponent',
  data() {
    return {
      chart: null,
      initialData: [], // 用于存储初始数据
      initialOption: null,
      mousemoveData: null, // 用于存储鼠标事件
      timeoutId: null, // 用于存储定时器ID
      latestTimestamp: 0,

      treemapOption: {
        tooltip: {
          formatter: function (info) {
            var treePathInfo = info.treePathInfo;
            var treePath = [];
            for (var i = 1; i < treePathInfo.length; i++) {
              treePath.push(treePathInfo[i].name);
            }
            // 此处可以分情况输出:
            // 可能的情况:
            //  1. 知识点 > 子知识点 > 题目id
            //  2. 知识点 > 子知识点
            //  3. 知识点

            return [
              '<div class="tooltip-title">' +
              echarts.format.encodeHTML(treePath.join(' ➤ ')) +
              '</div>',
            ].join('');
          },
        },

        series: [{
          breadcrumb: { show: false },
          // name: 'knowledge-point',
          type: 'treemap',
          left: 0,
          top: 0,
          right: 0,
          bottom: 0,
          data: [
            {
              name: 'b3C9s', size: 3, value: 3,
              itemStyle: { color: '#d75254' }, // 第一个知识点颜色
              children: [
                { name: 'j0v1yls8', size: 1, value: 1, children: [{ name: 'FNg8X9v5zcbB1tQrxHR3', size: 1, value: 1 }] },
                { name: 'l4z6od7y', size: 2, value: 2, children: [{ name: 'hZ5wXofebmTlzKB1jNcP', size: 1, value: 1 }, { name: 'bumGRTJ0c8p4v5D6eHZa', size: 1, value: 1 }] }
              ]
            },
            {
              name: 'g7R2j', size: 5, value: 5,
              itemStyle: { color: '#Ef7a47' }, // 第二个知识点颜色
              children: [
                { name: 'j1g8gd3v', size: 1, value: 1, children: [{ name: 'YWXHr4G6Cl7bEm9iF2kQ', size: 1, value: 1 }] },
                { name: 'e0v1yls8', size: 4, value: 4, children: [{ name: 'xqlJkmRaP0otZcX4fK3W', size: 1, value: 1 }, { name: 'oCjnFLbIs4Uxwek9rBpu', size: 1, value: 1 }, { name: 'X3wF8QlTyi4mZkDp9Kae', size: 1, value: 1 }, { name: '5fgqjSBwTPG7KUV3it6O', size: 1, value: 1 }] }
              ]
            },
            {
              name: 'k4W1c', size: 1, value: 1,
              itemStyle: { color: '#62acd5' }, // 第三个知识点颜色
              children: [{ name: 'h5r6nux7', size: 1, value: 1, children: [{ name: 'lU2wvHSZq7m43xiVroBc', size: 1, value: 1 }] }]
            },
            {
              name: 'm3D1v', size: 12, value: 12,
              itemStyle: { color: '#efd05f' }, // 第四个知识点颜色
              children: [
                { name: 'v3d9is1x', size: 2, value: 2, children: [{ name: '7NJzCXUPcvQF4Mkfh9Wr', size: 1, value: 1 }, { name: 'ZTbD7mxr2OUp8Fz6iNjy', size: 1, value: 1 }] },
                { name: 't0v5ts9h', size: 1, value: 1, children: [{ name: 'Jr4Wz5jLqmN01KUwHa7g', size: 1, value: 1 }] },
                { name: 'r1d7fr3l', size: 9, value: 9, children: [{ name: 'QRm48lXxzdP7Tn1WgNOf', size: 1, value: 1 }, { name: 'h7pXNg80nJbw1C4kAPRm', size: 1, value: 1 }, { name: 'NixCn84GdK2tySa5rB1V', size: 1, value: 1 }, { name: '6RQj2gF3OeK5AmDvThUV', size: 1, value: 1 }, { name: 'pVKXjZn0BkSwYcsa7C31', size: 1, value: 1 }, { name: '4nHcauCQ0Y6Pm8DgKlLo', size: 1, value: 1 }, { name: 'TmKaGvfNoXYq4FZ2JrBu', size: 1, value: 1 }, { name: 'n2BTxIGw1Mc3Zo6RLdUe', size: 1, value: 1 }, { name: 'oCjnFLbIs4Uxwek9rBpu', size: 1, value: 1 }] }
              ]
            },
            {
              name: 'r8S3g', size: 6, value: 6,
              itemStyle: { color: '#9acce0' }, // 第五个知识点颜色
              children: [
                { name: 'n0m9rsw4', size: 4, value: 4, children: [{ name: 'rvB9mVE6Kbd8jAY4NwPx', size: 1, value: 1 }, { name: 'BW0ItEaymH3TkD6S15JF', size: 1, value: 1 }, { name: 'q7OpB2zCMmW9wS8uNt3H', size: 1, value: 1 }, { name: 'fZrP3FJ4ebUogW9V7taS', size: 1, value: 1 }] },
                { name: 'l0p5viby', size: 2, value: 2, children: [{ name: 'q7OpB2zCMmW9wS8uNt3H', size: 1, value: 1 }, { name: 'VgKw8PjY1FR6cm2QI9XW', size: 1, value: 1 }] }
              ]
            },
            {
              name: 's8Y2f', size: 1, value: 1,
              itemStyle: { color: '#0d365e' }, // 第六个知识点颜色
              children: [{ name: 'v4x8by9j', size: 1, value: 1, children: [{ name: 'x2Fy7rZ3SwYl9jMQkpOD', size: 1, value: 1 }] }]
            },
            {
              name: 't5V9e', size: 5, value: 5,
              itemStyle: { color: '#427fad' }, // 第七个知识点颜色
              children: [{ name: 'e1k6cixp', size: 5, value: 5, children: [{ name: '3MwAFlmNO8EKrpY5zjUd', size: 1, value: 1 }, { name: '3oPyUzDmQtcMfLpGZ0jW', size: 1, value: 1 }, { name: 'tgOjrpZLw4RdVzQx85h6', size: 1, value: 1 }, { name: 's6VmP1G4UbEQWRYHK9Fd', size: 1, value: 1 }, { name: 'x2L7AqbMuTjCwPFy6vNr', size: 1, value: 1 }] }]
            },
            {
              name: 'y9W5d', size: 11, value: 11,
              itemStyle: { color: '#f3aa58' }, // 第八个知识点颜色
              children: [
                { name: 'p8g6dgtv', size: 2, value: 2, children: [{ name: 'Az73sM0rHfWVKuc4X2kL', size: 1, value: 1 }, { name: 'Ou3f2Wt9BqExm5DpN7Zk', size: 1, value: 1 }] },
                { name: 'c0w4mj5h', size: 8, value: 8, children: [{ name: 'QRm48lXxzdP7Tn1WgNOf', size: 1, value: 1 }, { name: 'Mh4CZIsrEfxkP1wXtOYV', size: 1, value: 1 }, { name: '62XbhBvJ8NUSnApgDL94', size: 1, value: 1 }, { name: 'Ej5mBw9rsOUKkFycGvz2', size: 1, value: 1 }, { name: 'pVKXjZn0BkSwYcsa7C31', size: 1, value: 1 }, { name: '4nHcauCQ0Y6Pm8DgKlLo', size: 1, value: 1 }, { name: 'TmKaGvfNoXYq4FZ2JrBu', size: 1, value: 1 }, { name: 'n2BTxIGw1Mc3Zo6RLdUe', size: 1, value: 1 }] },
                { name: 'q0v6gy3r', size: 1, value: 1, children: [{ name: 'RQm4fJ6N0Orx7PkGvL8W', size: 1, value: 1 }] }
              ]
            }
          ],
          // 您的数据在这里
          universalTransition: true, // 启用过渡效果
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
          textStyle: {
            textShadow: false, // 关闭阴影
            textBorderColor: 'transparent', // 设置文字描边颜色为透明，相当于关闭描边
          },
        }]
      }
    };
  },
  mounted() {
    this.initChart();
    // 订阅消息
    PubSub.subscribe('title_ID', (msg, data) => {

      if (data.timestamp > this.latestTimestamp) {
        this.latestTimestamp = data.timestamp;
        console.log("PubSub 订阅了 title_ID!!!");
        console.log(data.title_ID);
        this.triggerDispatchAction(data.title_ID);

      }

    });
    
    // 监听从stack传来的知识点id
    EventBus.$on('stackSelected', this.handleStackSelected);
    // 监听从parallel传来的题目id parallelSelected
    EventBus.$on('parallelSelected', this.handleParallelSelected);
    window.addEventListener('resize', this.resizeChart);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart);
    // 关闭监听从stack传来的知识点id
    EventBus.$off('stackSelected', this.handleStackSelected);
    // 关闭监听从parallel传来的题目id parallelSelected
    EventBus.$off('parallelSelected', this.handleParallelSelected);
  },
  methods: {
    initChart() {
      var chartDom = document.getElementById('main');
      this.chart = echarts.init(chartDom);

      this.initialData = this.treemapOption.series[0].data; // 存储初始数据
      this.initialOption = JSON.parse(JSON.stringify(this.treemapOption)); // 存储初始配置
      this.chart.setOption(this.treemapOption);

      this.chart.on('mouseover', this.handleMouseOver);
      this.chart.on('mouseout', this.handleMouseOut);
    },

    // 处理从stack传来的知识点id,
    handleStackSelected(knowledge_id) {
      // console.log("leftbottom: stack传来的知识点id", knowledge_id.substr(0,5));
      // 通过知识点id找到对应的知识点
      this.triggerDispatchAction(knowledge_id.substr(0,5));
    },

    // 处理从stack传来的知识点id,
    handleParallelSelected(title_id) {
      // console.log("leftbottom: stack传来的知识点id", knowledge_id.substr(0,5));
      // 通过知识点id找到对应的知识点
      this.triggerDispatchAction(title_id);
    },

    // 处理传来的title_ID
    triggerDispatchAction(nodeName) {
      const path = this.findNodeByName(this.initialData, nodeName);
      // console.log("题目的名字！！！！")
      // console.log(path[path.length - 1].name)

      console.log(path);
      if (path.length > 0) {
        const targetNode = path[0];
        // 通过设置根节点模拟点击效果
        this.chart.setOption({
          series: [{
            left: 10,
            top: 10,
            right: 10,
            bottom: 10,
            data: [targetNode]
          }]
        });

        // 显示目标节点的提示
        this.chart.dispatchAction({
          type: 'highlight',
          seriesIndex: 0,
          name: path[path.length - 1].name
        });

        if (this.timeoutId) {
          clearTimeout(this.timeoutId);
          this.timeoutId = null; // 重置 timeoutId
        }

        // 启动复原定时器
        this.startRestoreTimer();
      }
    },
    handleMouseOver(params) {
      if (params.seriesType === 'treemap') {
        // 鼠标悬停在 treemap 内部时，清除定时器
        if (this.timeoutId) {
          clearTimeout(this.timeoutId);
          this.timeoutId = null;
        }
      }
    },
    handleMouseOut(params) {
      if (params.seriesType === 'treemap') {
        // 鼠标移出 treemap 后，启动定时器
        this.startRestoreTimer();
      }
    },
    startRestoreTimer() {
      this.timeoutId = setTimeout(() => {
        this.chart.setOption(this.initialOption); // 恢复初始状态
        this.chart.dispatchAction({
          type: 'downplay',
          seriesIndex: 0,
          name: null
        });
      }, 3000); // 3000 毫秒后复原，可根据需要调整时间
    },
    findNodeByName(data, name) {
      for (let node of data) {
        if (node.name === name) {
          return [node]; // 找到目标节点
        } else if (node.children) {
          const result = this.findNodeByName(node.children, name);
          if (result.length > 0) {
            return [node].concat(result); // 返回包括父节点在内的路径
          }
        }
      }
      return []; // 没找到返回空数组
    },
    resizeChart() {
      if (this.chart) {
        this.chart.resize();
      }
    }
  }




};
</script>

<style>
.chart-container-right {
  position: relative;
  width: 90%;
  height: 90%;
}

#main {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
}
</style>
