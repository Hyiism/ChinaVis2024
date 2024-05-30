<template>
    <div class="chart-container-right">
      <div id="main-right"> </div>
    </div>
  </template>
  <!-- 这是一个雷达图 -->
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
        var chartDom = document.getElementById('main-right');
        var myChart = echarts.init(chartDom);
        var option = {
  title: {
    text: 'Proportion of Browsers',
    subtext: 'Fake Data',
    top: 10,
    left: 10
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    type: 'scroll',
    bottom: 10,
    data: (function () {
      var list = [];
      for (var i = 1; i <= 28; i++) {
        list.push(i + 2000 + '');
      }
      return list;
    })()
  },
  visualMap: {
    top: 'middle',
    right: 10,
    color: ['red', 'yellow'],
    calculable: true
  },
  radar: {
    indicator: [
      { text: 'IE8-', max: 400 },
      { text: 'IE9+', max: 400 },
      { text: 'Safari', max: 400 },
      { text: 'Firefox', max: 400 },
      { text: 'Chrome', max: 400 }
    ]
  },
  series: (function () {
    var series = [];
    for (var i = 1; i <= 28; i++) {
      series.push({
        type: 'radar',
        symbol: 'none',
        lineStyle: {
          width: 1
        },
        emphasis: {
          areaStyle: {
            color: 'rgba(0,250,0,0.3)'
          }
        },
        data: [
          {
            value: [
              (40 - i) * 10,
              (38 - i) * 4 + 60,
              i * 5 + 10,
              i * 9,
              (i * i) / 2
            ],
            name: i + 2000 + ''
          }
        ]
      });
    }
    return series;
  })()
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
  .chart-container-right {
    position: relative;
    width: 100%;
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
  