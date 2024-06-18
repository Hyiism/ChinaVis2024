<template>
  <div class="bottom-chart">
    <div id="bottom-main"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'BottomViewer',

  data() {
    return {
      top_students_scores: {}
    };
  },

  mounted() {
    // 执行获取数据的方法
    this.fetchStudentScores();
    // 初始化图表
    // this.initChart();
    window.addEventListener('resize', this.resizeChart);
  },

  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart);
  },

  methods: {
    // 向后端请求top15的详细成绩数据
    fetchStudentScores() {
      this.$axios.get('http://10.12.44.190:8000/topstudents') // 替换为实际的API端点
        .then(response => {
          this.top_students_scores = JSON.parse(response.data);
          // 数据获取成功后再初始化图表，不然图表获取不到数据
          this.initChart();

        })
        .catch(error => {
          console.error("There was an error!", error);
        });
    },

    // 初始化图表
    initChart() {

      console.log("###start###")
      // console.log(this.top_students_scores['top5'])
      console.log(this.top_students_scores.top5)
      const top5 = this.top_students_scores.top5;
      const top10 = this.top_students_scores.top10;
      const top15 = this.top_students_scores.top15;

      var schema = [
        { name: 'title_1', index: 0, text: 't1' },
        { name: 'title_2', index: 1, text: 't2' },
        { name: 'title_3', index: 2, text: 't3' },
        { name: 'title_4', index: 3, text: 't4' },
        { name: 'title_5', index: 4, text: 't5' },
        { name: 'title_6', index: 5, text: 't6' },
        { name: 'title_7', index: 6, text: 't7' },
        { name: 'title_8', index: 7, text: 't8' },
        { name: 'title_9', index: 8, text: 't9' },
        { name: 'title_10', index: 9, text: 't10' },
        { name: 'title_11', index: 10, text: 't11' },
        { name: 'title_12', index: 11, text: 't12' },
        { name: 'title_13', index: 12, text: 't13' },
        { name: 'title_14', index: 13, text: 't14' },
        { name: 'title_15', index: 14, text: 't15' },
        { name: 'title_16', index: 15, text: 't16' },
        { name: 'title_17', index: 16, text: 't17' },
        { name: 'title_18', index: 17, text: 't18' },
        { name: 'title_19', index: 18, text: 't19' },
        { name: 'title_20', index: 19, text: 't20' },
        { name: 'title_21', index: 20, text: ' t21' },
        { name: 'title_22', index: 21, text: 't22' },
        { name: 'title_23', index: 22, text: 't23' },
        { name: 'title_24', index: 23, text: 't24' },
        { name: 'title_25', index: 24, text: 't25' },
        { name: 'title_26', index: 25, text: 't26' },
        { name: 'title_27', index: 26, text: 't27' },
        { name: 'title_28', index: 27, text: 't28' },
        { name: 'title_29', index: 28, text: 't29' },
        { name: 'title_30', index: 29, text: 't30' },
        { name: 'title_31', index: 30, text: 't31' },
        { name: 'title_32', index: 31, text: 't32' },
        { name: 'title_33', index: 32, text: 't33' },
        { name: 'title_34', index: 33, text: 't34' },
        { name: 'title_35', index: 34, text: 't35' },
        { name: 'title_36', index: 35, text: 't36' },
        { name: 'title_37', index: 36, text: 't37' },
        { name: 'title_38', index: 37, text: 't38' },
        { name: 'score', index: 38, text: 'Score' },

      ];
      var lineStyle = {
        width: 1,
        opacity: 0.5
      };

      var option = {
        title: {
          text: '异常题目检测表',
          left: 'center',
          textStyle: {
            color: '#000',
            fontSize: 20
          },
          top: '2%'
        },

        backgroundColor: '#fff',
        legend: {
          bottom: "1",
          data: ['0-5', '5-10', '10-15'],
          itemGap: 30,
          textStyle: {
            color: '#000',
            fontSize: 15
          }
        },
        tooltip: {
          padding: 10,
          backgroundColor: '#fff',
          borderColor: '#777',
          borderWidth: 1
        },

        parallelAxis: [
          { dim: 0, name: schema[0].text, min: 3, max: 4 },
          { dim: 1, name: schema[1].text, min: 3, max: 4 },
          { dim: 2, name: schema[2].text, min: 3, max: 4 },
          { dim: 3, name: schema[3].text, min: 3, max: 4 },
          { dim: 4, name: schema[4].text, min: 3, max: 4 },
          { dim: 5, name: schema[5].text, min: 3, max: 4 },
          { dim: 6, name: schema[6].text, min: 3, max: 4 },
          { dim: 7, name: schema[7].text, min: 3, max: 4 },
          { dim: 8, name: schema[8].text, min: 3, max: 4 },
          { dim: 9, name: schema[9].text, min: 3, max: 4 },
          { dim: 10, name: schema[10].text, min: 3, max: 4 },
          { dim: 11, name: schema[11].text, min: 3, max: 4 },
          { dim: 12, name: schema[12].text, min: 3, max: 4 },
          { dim: 13, name: schema[13].text, min: 3, max: 4 },
          { dim: 14, name: schema[14].text, min: 3, max: 4 },
          { dim: 15, name: schema[15].text, min: 3, max: 4 },
          { dim: 16, name: schema[16].text, min: 3, max: 4 },
          { dim: 17, name: schema[17].text, min: 3, max: 4 },
          { dim: 18, name: schema[18].text, min: 3, max: 4 },
          { dim: 19, name: schema[19].text, min: 3, max: 4 },
          { dim: 20, name: schema[20].text, min: 3, max: 4 },
          { dim: 21, name: schema[21].text, min: 3, max: 4 },
          { dim: 22, name: schema[22].text, min: 3, max: 4 },
          { dim: 23, name: schema[23].text, min: 3, max: 4 },
          { dim: 24, name: schema[24].text, min: 3, max: 4 },
          { dim: 25, name: schema[25].text, min: 3, max: 4 },
          { dim: 26, name: schema[26].text, min: 3, max: 4 },
          { dim: 27, name: schema[27].text, min: 3, max: 4 },
          { dim: 28, name: schema[28].text, min: 3, max: 4 },
          { dim: 29, name: schema[29].text, min: 3, max: 4 },
          { dim: 30, name: schema[30].text, min: 3, max: 4 },
          { dim: 31, name: schema[31].text, min: 3, max: 4 },
          { dim: 32, name: schema[32].text, min: 3, max: 4 },
          { dim: 33, name: schema[33].text, min: 3, max: 4 },
          { dim: 34, name: schema[34].text, min: 3, max: 4 },
          { dim: 35, name: schema[35].text, min: 3, max: 4 },
          { dim: 36, name: schema[36].text, min: 3, max: 4 },
          { dim: 37, name: schema[37].text, min: 3, max: 4 },
          { dim: 38, name: schema[38].text, min: 130, max: 137 },

        ],

        visualMap: {
          show: false,
          min: 134,
          max: 136.3,
          dimension: 38,
          inRange: {
            color: ['#d94e5d', '#eac736', '#50a3ba'].reverse()
          }
        },

        parallel: {
          left: '5%',
          right: '5%',
          bottom: '6%',
          parallelAxisDefault: {
            type: 'value',
            name: 'AQI指数',
            nameLocation: 'end',
            nameGap: 5,
            nameTextStyle: {
              color: '#000',
              fontSize: 11
            },
            axisLine: {
              lineStyle: {
                color: '#aaa'
              }
            },
            axisTick: {
              // 坐标轴上横线，同样设为白色为不显示
              lineStyle: {
                color: '#000'
              }
            },
            splitLine: {
              show: false
            },
            // 坐标轴数字颜色配置，show配置无效，这里颜色设为白色代替
            axisLabel: {
              color: '#fff'
              // show: false
            }
          }
        },

        series: [
          {
            name: '0-5',
            type: 'parallel',
            // lineStyle: lineStyle,
            // 针对top5 的第6条平均数据加粗显示
            // lineStyle: (params) => {
            //   return {
            //     color: params.data[0] === top5[0][0] ? '#000' : lineStyle.color,
            //     width: params.data[0] === top5[0][0] ? 10 : lineStyle.width, // 加粗
            //   };
            // },
            data: top5
          },
          {
            name: '5-10',
            type: 'parallel',
            lineStyle: lineStyle,
            data: top10
          },
          {
            name: '10-15',
            type: 'parallel',
            lineStyle: lineStyle,
            data: top15
          }
        ]
      };
      var chartDom = document.getElementById('bottom-main');
      var myChart = echarts.init(chartDom);
      myChart.setOption(option);
      this.myChart = myChart;
      this.myChart.on('mouseover', function (params) {

        console.log("!!!!!平行图鼠标事件");
        // 控制台打印数据的名称
        console.log(params.name);
        console.log(params);

      });

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