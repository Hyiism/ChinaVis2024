<template>
  <!-- 个人知识点雷达图 -->
  <div class="chart-container-bottomcenter">
    <div id="main-bottomcenter"> </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'EChartsComponent',
  mounted() {
    this.fetchStudentScores()
    // this.initChart();
    window.addEventListener('resize', this.resizeChart);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart);
  },
  methods: {

    // 向后端请求数据
    fetchStudentScores() {
      this.$axios.get('http://10.12.44.205:8000/radarchart/?student_ID=8b6d1125760bd3939b6e') // 替换为实际的API端点
        .then(response => {
          this.know_scores = JSON.parse(response.data);

          console.log("#########################################!!!!")
          console.log(this.know_scores)
          console.log(this.know_scores['know_IDs'])
          // 数据获取成功后再初始化图表，不然图表获取不到数据
          this.initChart();
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
    },


    initChart() {
      var chartDom = document.getElementById('main-bottomcenter');
      var myChart = echarts.init(chartDom);
      // 包含名称的数组
      var know_IDs = this.know_scores['know_IDs'];
      // 创建一个空数组，用于存储生成的对象
      var indicator = [];
      // 循环遍历namelist数组
      for (var i = 0; i < know_IDs.length; i++) {
        // 创建一个包含名称和最大值的对象，并添加到indicator数组中
        var obj = { name: know_IDs[i], max:4 };
        indicator.push(obj);
      }

      var option = {
        title: {
          text: 'XX学生知识点掌握情况'
        },

        radar: {
          // shape: 'circle',
          indicator: indicator
        },
        series: [
          {
            name: 'Budget vs spending',
            type: 'radar',
            data: [
              {
                value: [2, 1, 2, 2, 2, 2, 2, 2],
              }
            ]
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
.chart-container-bottomcenter {
  position: relative;
  width: 100%;
  height: 90%;
}

#main-bottomcenter {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
}
</style>
