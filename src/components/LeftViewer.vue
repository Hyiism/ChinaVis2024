<template>
  <div class="chart-container">
    <div id="main"> </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  name: 'EChartsComponent',
  data() {
    return {
      chartData: null,
    };
  },
  mounted() {
    this.fetchChartData();
    window.addEventListener('resize', this.resizeChart);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart);
  },
  methods: {
    fetchChartData() {
      axios.post('http://localhost:5000/get_data')
        .then(response => {
          this.chartData = response.data;
          this.initChart();
        })
        .catch(error => {
          console.error("There was an error fetching the chart data:", error);
        });
    },
    initChart() {
      if (!this.chartData) return;

      const chartDom = document.getElementById('main');
      const myChart = echarts.init(chartDom);

      const yAxisData = this.chartData.student_id; 
      const seriesData = this.chartData.x.map(scores => scores.map(score => parseFloat(score.toFixed(2)))); // 保留两位小数

      const option = {
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
          top: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'value'
        },
        yAxis: {
          type: 'category',
          data: ['St01', 'St02', 'St03', 'St04', 'St05', 'St06', 'St07','St08', 'St09', 'St10']
          // data: yAxisData
        },
        series: [
          {
            name: 'Question_VgKw8PjY1FR6cm2QI9XW_score',
            type: 'bar',
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: seriesData.map(d => d[0])
          },
          {
            name: 'Question_q7OpB2zCMmW9wS8uNt3H_score',
            type: 'bar',
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: seriesData.map(d => d[1])
          },
          {
            name: 'Question_fZrP3FJ4ebUogW9V7taS_score',
            type: 'bar',
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: seriesData.map(d => d[2])
          },
          {
            name: 'Question_BW0ItEaymH3TkD6S15JF_score',
            type: 'bar',
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: seriesData.map(d => d[3])
          },
          {
            name: 'Question_rvB9mVE6Kbd8jAY4NwPx_score',
            type: 'bar',
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: seriesData.map(d => d[4])
          },
          {
            name: 'Question_3oPyUzDmQtcMfLpGZ0jW_score',
            type: 'bar',
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: seriesData.map(d => d[4])
          }
          ,
          {
            name: 'Question_3MwAFlmNO8EKrpY5zjUd_score',
            type: 'bar',
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: seriesData.map(d => d[4])
          },
          {
            name: 'Question_x2L7AqbMuTjCwPFy6vNr_score',
            type: 'bar',
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: seriesData.map(d => d[4])
          },
          {
            name: 'Question_tgOjrpZLw4RdVzQx85h6_score',
            type: 'bar',
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: seriesData.map(d => d[4])
          },
          {
            name: 'Question_s6VmP1G4UbEQWRYHK9Fd_score',
            type: 'bar',
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: seriesData.map(d => d[4])
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










<!-- <template>
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
   -->