<template>
    <div class="chart-container">
      <div id="main"> </div>
    </div>
  </template>

  <script>
  import * as echarts from 'echarts';
  
  export default {
    name: 'EChartsComponent',

    data() {
      return {
        top_students: {}
      };
    },
    mounted() {
      this.fetchStudentScores();
      // this.initChart();
      window.addEventListener('resize', this.resizeChart);
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.resizeChart);
    },
    methods: {
      // 向后端请求top15的详细成绩数据
      fetchStudentScores() {
        this.$axios.get('http://10.12.44.190:8000/ranking') // 替换为实际的API端点
          .then(response => {
            this.top_students = JSON.parse(response.data);
            console.log("###left start###")
            console.log(this.top_students)
            // 数据获取成功后再初始化图表，不然图表获取不到数据
            this.initChart();
          })
          .catch(error => {
            console.error("There was an error!", error);
          });
      },
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
            // top: '15%',
            show: false
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            // top: '35%',
            containLabel: true
          },
          xAxis: {
            type: 'value',
            min: 0,
            max: 160
          },
          yAxis: {
            type: 'category',
            // data: ['1', '2', '3', '4', '5', '6', '7']
            data: this.top_students.student_id.reverse()
          },
          series: [
            {
              name: 'subject_1',
              type: 'bar',
              stack: 'total',
              label: {
                show: false
              },
              emphasis: {
                focus: 'series'
              },
              barWidth: 15, // 调整柱状图的宽度
              barGap: '30%', // 调整柱状图之间的间隔
              // data: [320, 302, 301, 334, 390, 330, 320]
              data: this.top_students.subject_3.reverse()
            },
            {
              name: 'subject_2',
              type: 'bar',
              stack: 'total',
              label: {
                show: false
              },
              emphasis: {
                focus: 'series'
              },
              // data: [120, 132, 101, 134, 90, 230, 210]
              data: this.top_students.subject_6.reverse()
            },
            {
              name: 'subject_3',
              type: 'bar',
              stack: 'total',
              label: {
                show: false
              },
              emphasis: {
                focus: 'series'
              },
              // data: [220, 182, 191, 234, 290, 330, 310]
              data: this.top_students.subject_1.reverse()
            },
            {
              name: 'subject_4',
              type: 'bar',
              stack: 'total',
              label: {
                show: false
              },
              emphasis: {
                focus: 'series'
              },
              // data: [150, 212, 201, 154, 190, 330, 410]
              data: this.top_students.subject_5.reverse()
            },
            {
              name: 'subject_5',
              type: 'bar',
              stack: 'total',
              label: {
                show: false
              },
              emphasis: {
                focus: 'series'
              },
              // data: [820, 832, 901, 934, 1290, 1330, 1320]
              data: this.top_students.subject_7.reverse()
            },
            {
              name: 'subject_6',
              type: 'bar',
              stack: 'total',
              label: {
                show: false
              },
              emphasis: {
                focus: 'series'
              },
              // data: [820, 832, 901, 934, 1290, 1330, 1320]
              data: this.top_students.subject_2.reverse()
            },
            {
              name: 'subject_7',
              type: 'bar',
              stack: 'total',
              label: {
                show: false
              },
              emphasis: {
                focus: 'series'
              },
              // data: [820, 832, 901, 934, 1290, 1330, 1320]
              data: this.top_students.subject_8.reverse()
            },
            {
              name: 'subject_8',
              type: 'bar',
              stack: 'total',
              label: {
                show: false
              },
              emphasis: {
                focus: 'series'
              },
              // data: [820, 832, 901, 934, 1290, 1330, 1320]
              data: this.top_students.subject_4.reverse()
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
  