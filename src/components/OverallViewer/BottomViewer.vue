<template>
  <div class="bottom-chart">
    <div id="bottom-main"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import PubSub from 'pubsub-js';

export default {
  name: 'ParallelCoordinates',
  mounted() {
    this.initChart();
  },
  methods: {
    initChart() {
      var chartDom = document.getElementById('bottom-main');
      var myChart = echarts.init(chartDom);

      const option = {
        parallelAxis: [
          { dim: 0, name: 'Price' },
          { dim: 1, name: 'Net Weight' },
          { dim: 2, name: 'Amount' },
          { dim: 3, name: 'Score' }
        ],
        series: {
          type: 'parallel',
          lineStyle: {
            width: 4
          },
          data: [
            [12, 43.3, 23.4, 23],
            [23, 43.3, 55.4, 34],
            [12, 13.3, 13.4, 13],
            [33, 43.3, 44.4, 44]
          ]
        }
      };

      myChart.setOption(option);

      // 监听鼠标靠近坐标轴的事件
      myChart.on('mouseover', params => {

        console.log(params)
        if (params.componentType === 'parallelAxis') {
          const axisName = option.parallelAxis[params.parallelAxisIndex].name;
          PubSub.publish('axisHovered', axisName);
          console.log(axisName)
        }
      });

      // 在鼠标移开时取消高亮
      myChart.on('mouseout', params => {
        if (params.componentType === 'parallelAxis') {
          PubSub.publish('axisHovered', null);
        }
      });
    }
  }
};
</script>

<style scoped>
.bottom-chart {
  width: 100%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
}

#bottom-main {
  width: 100%;
  height: 100%;
}
</style>
