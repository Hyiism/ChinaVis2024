<template>
  <div class="bottom-chart">
    <div id="bottom-main"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'BottomViewer',
  mounted() {
    this.initChart();
    window.addEventListener('resize', this.resizeChart);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart);
  },
  methods: {
    initChart() {
      var dataBJ = [
        [1, 55, 9, 56, 0.46, 18, 6, '良'],
        //...（省略部分数据）...
        [31, 46, 5, 49, 0.28, 10, 6, '优']
      ];
      var dataGZ = [
        [1, 26, 37, 27, 1.163, 27, 13, '优'],
        //...（省略部分数据）...
        [31, 118, 50, 0, 1.383, 76, 11, '轻度污染']
      ];
      var dataSH = [
        [1, 91, 45, 125, 0.82, 34, 23, '良'],
        //...（省略部分数据）...
        [31, 187, 143, 201, 1.39, 89, 53, '中度污染']
      ];
      var schema = [
        { name: 'date', index: 0, text: '日期' },
        { name: 'AQIindex', index: 1, text: 'AQI' },
        { name: 'PM25', index: 2, text: 'PM2.5' },
        { name: 'PM10', index: 3, text: 'PM10' },
        { name: 'CO', index: 4, text: ' CO' },
        { name: 'NO2', index: 5, text: 'NO2' },
        { name: 'SO2', index: 6, text: 'SO2' },
        { name: '等级', index: 7, text: '等级' }
      ];
      var lineStyle = {
        width: 1,
        opacity: 0.5
      };
      var option = {
        backgroundColor: '#fff',
        legend: {
          bottom: 30,
          data: ['Beijing', 'Shanghai', 'Guangzhou'],
          itemGap: 20,
          textStyle: {
            color: '#000',
            fontSize: 14
          }
        },
        tooltip: {
          padding: 10,
          backgroundColor: '#fff',
          borderColor: '#777',
          borderWidth: 1
        },
        parallelAxis: [
          {
            dim: 0,
            name: schema[0].text,
            inverse: true,
            max: 31,
            nameLocation: 'start'
          },
          { dim: 1, name: schema[1].text },
          { dim: 2, name: schema[2].text },
          { dim: 3, name: schema[3].text },
          { dim: 4, name: schema[4].text },
          { dim: 5, name: schema[5].text },
          { dim: 6, name: schema[6].text },
          {
            dim: 7,
            name: schema[7].text,
            type: 'category',
            data: ['优', '良', '轻度污染', '中度污染', '重度污染', '严重污染']
          }
        ],
        visualMap: {
          show: true,
          min: 0,
          max: 150,
          dimension: 2,
          inRange: {
            color: ['#d94e5d', '#eac736', '#50a3ba'].reverse()
          }
        },
        parallel: {
          left: '5%',
          right: '18%',
          bottom: 100,
          parallelAxisDefault: {
            type: 'value',
            name: 'AQI指数',
            nameLocation: 'end',
            nameGap: 20,
            nameTextStyle: {
              color: '#fff',
              fontSize: 12
            },
            axisLine: {
              lineStyle: {
                color: '#aaa'
              }
            },
            axisTick: {
              lineStyle: {
                color: '#777'
              }
            },
            splitLine: {
              show: false
            },
            axisLabel: {
              color: '#fff'
            }
          }
        },
        series: [
          {
            name: 'Beijing',
            type: 'parallel',
            lineStyle: lineStyle,
            data: dataBJ
          },
          {
            name: 'Shanghai',
            type: 'parallel',
            lineStyle: lineStyle,
            data: dataSH
          },
          {
            name: 'Guangzhou',
            type: 'parallel',
            lineStyle: lineStyle,
            data: dataGZ
          }
        ]
      };
      var chartDom = document.getElementById('bottom-main');
      var myChart = echarts.init(chartDom);
      myChart.setOption(option);
      this.myChart = myChart;
    },
    resizeChart() {
      if (this.myChart) {
        this.myChart.resize();
      }
    }
  }
};
</script>

<style scoped>
.bottom-chart {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
#bottom-main{
  width: 100%;
  height: 100%;
}
</style>
