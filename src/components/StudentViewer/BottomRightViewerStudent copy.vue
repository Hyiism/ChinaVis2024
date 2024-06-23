<template>
  <div class="bottom-chart">
    <div id="main_student"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import EventBus from '@/eventBus'; // 导入事件总线

export default {
  // bubKnowledgeIdSelected
  mounted() {
    this.fetchStudentScores();
    EventBus.$on('bubKnowledgeIdSelected', this.handleBubKnowledgeSelected);
    // this.initChart();
  },
  data(){
    return {
      T_values: [],
      kn_values: [],
      knowledge_id: 't5V9e'
    }
  },
  methods: {
    fetchStudentScores() {
    this.$axios.get(`http://10.12.44.190:8000/forget/?student_id=0088dc183f73c83f763e&knowledge_id=${this.knowledge_id}`) // Replace with actual API endpoint
      .then(response => {
          let rawdata = JSON.parse(response.data);
          console.log('rawdata', rawdata);
          this.T_values = rawdata.T_list;
          this.kn_values = rawdata.K_list;
          // 分数正确显示！！
          console.log('T_values', this.T_value);
          console.log('kn_values', this.kn_values);
          // 拿到数据后加载表格
          this.initChart();
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
    },
    initChart() {
      var chartDom = document.getElementById('main_student');
      var myChart = echarts.init(chartDom);

      // 定义指数衰减函数
      function R(t, T, kn) {
        return Math.exp(-kn * (t - T));
      }

      function R0(t, k0) {
        return Math.exp(-k0 * t);
      }

      // 参数设置
      // const T_values = [2, 5, 7, 10];
      // const kn_values = [0.47, 0.44, 0.32, 0.25];
      // const k0 = 0.5;
      const T_values = this.T_values.slice(1);
      const kn_values = this.kn_values.slice(1);
      const k0 = 0.5;
      // 颜色设置，每条线对应的实线和虚线颜色
      const colors = ['#ff0000', '#00ff00', '#0000ff', '#ff00ff'];

      // 生成数据
      function generateData() {
        let data = [];
        
        // R0 数据生成
        let seriesDataR0_solid = [];
        let seriesDataR0_dashed = [];
        // for (let t = -20; t <= 30; t += 0.1) {
        for (let t = -20; t <= T_values[T_values.length-1]+5; t += 0.1) {
          let valueR0 = R0(t, k0);
          if (valueR0 < 1) {
            if (t >= 0 && t <= 2) {
              seriesDataR0_solid.push([t, valueR0]);
            } else {
              seriesDataR0_dashed.push([t, valueR0]);
            }
          }
        }
        data.push(
          {
            name: `R0(t), k0=${k0} (solid)`,
            type: 'line',
            smooth: true,
            showSymbol: false,
            lineStyle: {
              normal: {
                color: '#000000', // 设置实线和虚线颜色
                type: 'solid'
              }
            },
            data: seriesDataR0_solid
          },
          {
            name: `R0(t), k0=${k0} (dashed)`,
            type: 'line',
            smooth: true,
            showSymbol: false,
            lineStyle: {
              normal: {
                color: '#000000', // 设置实线和虚线颜色
                type: 'dashed'
              }
            },
            data: seriesDataR0_dashed
          }
        );

        // R 数据生成
        for (let T_idx = 0; T_idx < T_values.length; T_idx++) {
          let T = T_values[T_idx];
          let kn = kn_values[T_idx];
          let seriesDataR_solid = [];
          let seriesDataR_dashed = [];
          
          // for (let t = -20; t <= 20; t += 0.1) {
          for (let t = -20; t <= T_values[T_values.length-1]+5; t += 0.1) {
            let valueR = R(t, T, kn);
            if (valueR < 1) {
              if ((t >= 2 && t <= 5 && T === 2) ||
                  (t >= 5 && t <= 7 && T === 5) ||
                  (t >= 7 && t <= 10 && T === 7)||
                  (t >= 10 && T === 10)) {
                seriesDataR_solid.push([t, valueR]);
              } else {
                seriesDataR_dashed.push([t, valueR]);
              }
            }
          }
          data.push(
            {
              name: `R(t), T=${T}, kn=${kn} (solid)`,
              type: 'line',
              smooth: true,
              showSymbol: false,
              lineStyle: {
                normal: {
                  color: `${colors[T_idx]}`, // 设置实线颜色
                  type: 'solid'
                }
              },
              data: seriesDataR_solid
            },
            {
              name: `R(t), T=${T}, kn=${kn} (dashed)`,
              type: 'line',
              smooth: true,
              showSymbol: false,
              lineStyle: {
                normal: {
                  type: 'dashed',
                  color: `${colors[T_idx]}`, // 设置实线颜色
                }
              },
              data: seriesDataR_dashed
            }
          );
        }
        
        return data;
      }

      var option = {
        title: {
          text: 'Exponential Decay Functions'
        },
        xAxis: {
          name: 't',
          type: 'value',
          min: 0,
          interval: 1
        },
        yAxis: {
          name: '记忆剩余',
          type: 'value',
          min: 0,
          max: 1,
          axisLabel: {
            formatter: function (value) {
              return (value * 100).toFixed(0) + '%';
            }
          }
        },
        series: generateData()
      };

      myChart.setOption(option);
      window.addEventListener('resize', () => {
        myChart.resize();
      });
    },
    // 处理气泡点击事件 接收知识点id
    handleBubKnowledgeSelected(bubKnow) {
      console.log('Bubble selected:', bubKnow);
      this.knowledge_id = bubKnow;
      this.fetchStudentScores();
    }
  }
};
</script>

<style>
.bottom-chart {
  position: relative;
  width: 100%;
  height: 100%;
}

#main_student {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>