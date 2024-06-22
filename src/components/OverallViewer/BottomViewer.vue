<template>
  <div class="bottom-chart">
    <div id="bottom-main"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import { min } from 'moment';
import EventBus from '@/eventBus'; // 导入事件总线


export default {
  name: 'BottomViewer',
  // props: {
  //   isVisible: {
  //     type: Boolean,
  //     required: true
  //   },
  // },

  data() {
    return {
      top_students_scores: {},
    };
  },

  mounted() {
    // 执行获取数据的方法
    this.fetchStudentScores();
    window.addEventListener('resize', this.resizeChart);
  },

  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart);
  },

  methods: {
    // 向后端请求top15的详细成绩数据
    fetchStudentScores() {
      this.$axios
        .get('http://10.12.44.190:8000/topstudents') // 替换为实际的API端点
        .then((response) => {
          this.top_students_scores = JSON.parse(response.data);
          // 确保在DOM元素完全加载并设置尺寸后再初始化图表
          this.$nextTick(() => {
            this.initChart();
          });
        })
        .catch((error) => {
          console.error('There was an error!', error);
        });
    },

    // 初始化图表
    initChart() {
      const top5 = this.top_students_scores.top5;
      const top10 = this.top_students_scores.top10;
      const top15 = this.top_students_scores.top15;
      var schema = [
        { name: 'VgKw8PjY1FR6cm2QI9XW', index: 0, text: 't1' ,min: 3, max: 4},
        { name: 'q7OpB2zCMmW9wS8uNt3H', index: 1, text: 't2' ,min: 3, max: 4},
        { name: 'fZrP3FJ4ebUogW9V7taS', index: 2, text: 't3' ,min: 3, max: 4},
        { name: 'BW0ItEaymH3TkD6S15JF', index: 3, text: 't4' ,min: 3, max: 4},
        { name: 'rvB9mVE6Kbd8jAY4NwPx', index: 4, text: 't5' ,min: 3, max: 4},
        { name: '3oPyUzDmQtcMfLpGZ0jW', index: 5, text: 't6' ,min: 3, max: 4},
        { name: '3MwAFlmNO8EKrpY5zjUd', index: 6, text: 't7' ,min: 3, max: 4},
        { name: 'x2L7AqbMuTjCwPFy6vNr', index: 7, text: 't8' ,min: 3, max: 4},
        { name: 'tgOjrpZLw4RdVzQx85h6', index: 8, text: 't9' ,min: 3, max: 4},
        { name: 's6VmP1G4UbEQWRYHK9Fd', index: 9, text: 't10' ,min: 3, max: 4},
        { name: 'h7pXNg80nJbw1C4kAPRm', index: 10, text: 't11' ,min: 3, max: 4},
        { name: '6RQj2gF3OeK5AmDvThUV', index: 11, text: 't12' ,min: 3, max: 4},
        { name: '4nHcauCQ0Y6Pm8DgKlLo', index: 12, text: 't13' ,min: 3, max: 4},
        { name: 'TmKaGvfNoXYq4FZ2JrBu', index: 13, text: 't14' ,min: 3, max: 4},
        { name: 'NixCn84GdK2tySa5rB1V', index: 14, text: 't15' ,min: 3, max: 4},
        { name: 'n2BTxIGw1Mc3Zo6RLdUe', index: 15, text: 't16' ,min: 3, max: 4},
        { name: '7NJzCXUPcvQF4Mkfh9Wr', index: 16, text: 't17' ,min: 3, max: 4},
        { name: 'ZTbD7mxr2OUp8Fz6iNjy', index: 17, text: 't18' ,min: 3, max: 4},
        { name: 'Jr4Wz5jLqmN01KUwHa7g', index: 18, text: 't19' ,min: 3, max: 4},
        { name: 'QRm48lXxzdP7Tn1WgNOf', index: 19, text: 't20' ,min: 3, max: 4},
        { name: 'pVKXjZn0BkSwYcsa7C31', index: 20, text: 't21' ,min: 3, max: 4},
        { name: 'Ej5mBw9rsOUKkFycGvz2', index: 21, text: 't22' ,min: 3, max: 4},
        { name: 'lU2wvHSZq7m43xiVroBc', index: 22, text: 't23' ,min: 3, max: 4},
        { name: 'Mh4CZIsrEfxkP1wXtOYV', index: 23, text: 't24' ,min: 3, max: 4},
        { name: '62XbhBvJ8NUSnApgDL94', index: 24, text: 't25' ,min: 3, max: 4},
        { name: 'x2Fy7rZ3SwYl9jMQkpOD', index: 25, text: 't26' ,min: 3, max: 4},
        { name: 'UXqN1F7G3Sbldz02vZne', index: 26, text: 't27' ,min: 3, max: 4},
        { name: 'Ou3f2Wt9BqExm5DpN7Zk', index: 27, text: 't28' ,min: 3, max: 4},
        { name: 'Az73sM0rHfWVKuc4X2kL', index: 28, text: 't29' ,min: 3, max: 4},
        { name: 'EhVPdmlB31M8WKGqL0wc', index: 29, text: 't30' ,min: 3, max: 4},
        { name: 'oCjnFLbIs4Uxwek9rBpu', index: 30, text: 't31' ,min: 3, max: 4},
        { name: '5fgqjSBwTPG7KUV3it6O', index: 31, text: 't32' ,min: 3, max: 4},
        { name: 'X3wF8QlTyi4mZkDp9Kae', index: 32, text: 't33' ,min: 3, max: 4},
        { name: 'YWXHr4G6Cl7bEm9iF2kQ_', index: 33, text: 't34' ,min: 3, max: 4},
        { name: 'xqlJkmRaP0otZcX4fK3W', index: 34, text: 't35' ,min: 3, max: 4},
        { name: 'bumGRTJ0c8p4v5D6eHZa', index: 35, text: 't36' ,min: 3, max: 4},
        { name: 'hZ5wXofebmTlzKB1jNcP', index: 36, text: 't37' ,min: 3, max: 4},
        { name: 'FNg8X9v5zcbB1tQrxHR3', index: 37, text: 't38' ,min: 3, max: 4},
        { name: 'total_score', index: 38, text: 'Score' ,min: 134, max: 136.3},
      ];

      var lineStyle = {
        width: 1,
        opacity: 0.5,
      };

      var option = {
        title: {
          text: '异常题目检测表',
          left: 'center',
          textStyle: {
            color: '#000',
            fontSize: 20,
          },
          top: '2%',
        },
        backgroundColor: '#fff',
        legend: {
          bottom: '1',
          data: ['0-5', '5-10', '10-15'],
          itemGap: 30,
          textStyle: {
            color: '#000',
            fontSize: 15,
          },
        },
        tooltip: {
          padding: 0,
          backgroundColor: '#fff',
          borderColor: '#777',
          borderWidth: 1,
        },
        parallelAxis: schema.map((item, index) => ({
          dim: index,
          name: item.text,
          min: item.min,
          max: item.max,
          axisLabel: {
            show: false, // 隐藏坐标轴上的标签
            margin: 5, // 调整刻度与轴线之间的距离
          },
          nameLocation: 'end',
          nameTextStyle: {
            color: '#fff', // 隐藏坐标轴上的题目名称
          },
        })),
        parallel: {
          // 此处可调节两坐标轴间间距
          left: '1%',
          right: '1%',
          bottom: '6%',
          parallelAxisDefault: {
            type: 'value',
            name: 'AQI指数',
            nameLocation: 'end',
            nameGap: 5,
            nameTextStyle: {
              color: '#000',
              fontSize: 10,
            },
            axisLine: {
              lineStyle: {
                color: '#aaa',
              },
            },
            axisTick: {
              lineStyle: {
                color: '#000',
              },
            },
            splitLine: {
              show: false,
            },
            axisLabel: {
              color: '#fff',
            },
          },
        },
        series: [
          {
            name: '0-5',
            type: 'parallel',
            lineStyle: lineStyle,
            data: top5,
          },
          {
            name: '5-10',
            type: 'parallel',
            lineStyle: lineStyle,
            data: top10,
          },
          {
            name: '10-15',
            type: 'parallel',
            lineStyle: lineStyle,
            data: top15,
          },
        ],
      };

      var chartDom = document.getElementById('bottom-main');
      var myChart = echarts.init(chartDom);
      myChart.setOption(option);
      this.myChart = myChart;

      // 添加覆盖层
      this.addOverlayLabels(schema);
    },

    // 添加覆盖层方法，bug是切换视图后此html只有刷新才会消失
    addOverlayLabels(schema) {

      // 清除已有的覆盖层
      const existingLabels = document.querySelectorAll('.overlay-label');
      existingLabels.forEach(label => label.remove());
      
      const chartDom = document.getElementById('bottom-main');
      const chartRect = chartDom.getBoundingClientRect();
      schema.forEach((item, index) => {
        const label = document.createElement('div');
        label.className = 'overlay-label';
        label.innerText = item.text;
        // label.innerText.style = 'font-size: 10px';
        label.style.position = 'absolute';
        label.style.top = `${chartRect.top + 40}px`; // 根据需要调整位置
        label.style.left = `${chartRect.left + (index + 1) * (chartRect.width / schema.length) - 20}px`; // 此处调整标签名和坐标轴对齐情况
        label.style.cursor = 'pointer';
        label.addEventListener('click', () => {
          this.handleLabelClick(item);
        });
        document.body.appendChild(label);
      });
    },


    // 处理标签点击事件的方法
    handleLabelClick(item) {
      console.log(`Clicked on label: ${item.name}`);
      // 在这里处理点击事件，例如调用一个函数
      EventBus.$emit('parallelSelected', `${item.name}`); // Emit event
    },

    resizeChart() {
      if (this.myChart) {
        this.myChart.resize();
      }
    },
  },
};
</script>

<style scoped>
.bottom-chart {
  width: 100%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

#bottom-main {
  width: 90%;
  /* height: 600px; */
  height: 100%;
}

.overlay-label {
  font-size: 12px;
  color: #000;
  cursor: pointer;
}
</style>
