<template>
  <div class="bottom-chart">
    <div id="main_student" style="width: 100%; height: 600px;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  mounted() {
    this.initChart();
  },
  methods: {
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
      const T_values = [2, 5, 7, 10];
      const kn_values = [0.47, 0.44, 0.32, 0.25];
      const k0 = 0.5;

      // 生成数据
      function generateData() {
        let data = [];
        for (let T_idx = 0; T_idx < T_values.length; T_idx++) {
          let T = T_values[T_idx];
          let kn = kn_values[T_idx];
          let seriesDataR = [];
          let seriesDataR0 = [];
          for (let t = -20; t <= 20; t += 0.1) {
            let valueR = R(t, T, kn);
            let valueR0 = R0(t, k0);
            if (valueR < 1) {  // 只画出小于1的部分
              seriesDataR.push([t, valueR]);
            }
            if (valueR0 < 1) {  // 只画出小于1的部分
              seriesDataR0.push([t, valueR0]);
            }
          }
          data.push(
            {
              name: `R(t), T=${T}, kn=${kn}`,
              type: 'line',
              smooth: true,
              showSymbol: false,  // 隐藏点
              data: seriesDataR
            },
            {
              name: `R0(t), k0=${k0}`,
              type: 'line',
              smooth: true,
              showSymbol: false,  // 隐藏点
              data: seriesDataR0
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
          name: 'R(t), R0(t)',
          type: 'value',
          min: 0,
          max: 1
        },
        series: generateData()
      };

      myChart.setOption(option);
    },
  }
};
</script>

<style>
.bottom-chart {
  position: relative;
  width: 100%;
  height: 100%;
}

/* #main_student {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
} */
</style>
