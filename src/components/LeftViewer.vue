<template>
    <div class="chart-container">
      <div id="main"> </div>
    </div>
  </template>

  <script>
  import * as echarts from 'echarts';
  
  export default {
    name: 'EChartsComponent',
    mounted() {
      this.initChart();
      window.addEventListener('resize', this.resizeChart);
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.resizeChart);
    },
    methods: {
      initChart() {
        var chartDom = document.getElementById('main');
        var myChart = echarts.init(chartDom);
        var option = {
            title: {
                text: '学生综合成绩排行榜',
                left: 'center',
            },

          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          legend: {
            top: '7%'
          },
          grid: {
            left: '3%',
            right: '4%',
            // bottom: '3%',
            top: '15%',
            containLabel: true
          },
          xAxis: {
            type: 'value'
          },
          yAxis: {
            type: 'category',
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
          },
          series: [
            {
              name: 'subject_1',
              type: 'bar',
              stack: 'total',
              label: {
                show: true
              },
              emphasis: {
                focus: 'series'
              },
              data: [320, 302, 301, 334, 390, 330, 320]
            },
            {
              name: 'subject_2',
              type: 'bar',
              stack: 'total',
              label: {
                show: true
              },
              emphasis: {
                focus: 'series'
              },
              data: [120, 132, 101, 134, 90, 230, 210]
            },
            {
              name: 'subject_3',
              type: 'bar',
              stack: 'total',
              label: {
                show: true
              },
              emphasis: {
                focus: 'series'
              },
              data: [220, 182, 191, 234, 290, 330, 310]
            },
            {
              name: 'subject_4',
              type: 'bar',
              stack: 'total',
              label: {
                show: true
              },
              emphasis: {
                focus: 'series'
              },
              data: [150, 212, 201, 154, 190, 330, 410]
            },
            {
              name: 'subject_5',
              type: 'bar',
              stack: 'total',
              label: {
                show: true
              },
              emphasis: {
                focus: 'series'
              },
              data: [820, 832, 901, 934, 1290, 1330, 1320]
            }
          ]
        };
        option && myChart.setOption(option);
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
  .chart-container {
    position: relative;
    width: 100%;
    height: 90%;
  }

  #main {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
  </style>
  