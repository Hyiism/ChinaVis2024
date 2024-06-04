<template>
  <div ref="chart" id="scater"></div>
</template>

<script>
import * as echarts from 'echarts';
import 'echarts-gl';  // 引入 ECharts 3D 扩展

export default {
  name: 'ChartViewer',
  data() {
    return {
      myChart: null,
      // data: [
      //   [1, 10, 20, 30, 85, 'A'],
      //   [2, 20, 30, 40, 90, 'B'],
      //   [3, 30, 40, 50, 95, 'A'],
      //   [4, 40, 50, 60, 80, 'C'],
      //   [5, 50, 60, 70, 70, 'B']
      // ],

      // 这个用来接受后段传来的json数据
      data: [],

      
      fieldIndices: {
        student_id: 0,
        x: 1,
        y: 2,
        z: 3,
        cluster_label: 4,
        total_score: 5
      },

      labels: [0, 1, 2, 3 ],
      labelColors: ['#00fea8', '#000', '#fe0300', '#ffbd67']
    };
  },
  mounted() {
    this.fetchScaterData();
    // this.myChart = echarts.init(this.$refs.chart);
    // this.updateChart();
  },

  methods: {
    // 向后端请求top15的详细成绩数据
    fetchScaterData() {
      this.$axios.get('http://10.12.44.190:8000/scaterVis') // 替换为实际的API端点
        .then(response => {
          this.data = JSON.parse(response.data).data;
          console.log("###scater start###")
          console.log(this.data)
          // 数据获取成功后再初始化图表，不然图表获取不到数据
          this.myChart = echarts.init(this.$refs.chart);
          this.updateChart();
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
    },

    getMaxScore(data) {
      return Math.max(...data.map(item => item[this.fieldIndices.total_score]));
    },
    updateChart() {
      const maxScore = this.getMaxScore(this.data);
      const labelIndexMap = this.labels.reduce((obj, label, index) => {
        obj[label] = index;
        return obj;
      }, {});

      this.myChart.setOption({
        title: {
          text: '学生做题情况嵌入展示',
          left: 'center',
          textStyle: {
            color: '#000',
            fontSize: 20
        },
          top: 40
        },

        tooltip: {},
        visualMap: {
          show: true, // 不显示视觉映射控件
          dimension: this.fieldIndices.cluster_label,
          categories: this.labels,
          inRange: {
            color: this.labelColors
          }
        },
        xAxis3D: {
          name: 'x',
          type: 'value',
          axisLine: {
            lineStyle: {
              color: '#c0c0c0' // 坐标轴线颜色
            }
          },
          axisLabel: {
            color: '#c0c0c0' // 坐标轴标签颜色
          }
        },
        yAxis3D: {
          name: 'y',
          type: 'value',
          axisLine: {
            lineStyle: {
              color: '#c0c0c0' // 坐标轴线颜色
            }
          },
          axisLabel: {
            color: '#c0c0c0' // 坐标轴标签颜色
          }
        },
        zAxis3D: {
          name: 'z',
          type: 'value',
          min: 6,  // 指定 z 轴的最小值
          max: 12,  // 指定 z 轴的最大值
          axisLine: {
            lineStyle: {
              color: '#c0c0c0' // 坐标轴线颜色
            }
          },
          axisLabel: {
            color: '#000' // 坐标轴标签颜色
          }
        },
        grid3D: {
          axisLine: {
            lineStyle: {
              color: '#000' // 三维网格轴线颜色
            }
          },
          axisPointer: {
            lineStyle: {
              color: '#ffbd67'
            }
          },
          viewControl: {}
        },
        series: [
          {
            type: 'scatter3D',
            dimensions: ['x', 'y', 'z', 'cluster_label', 'total_score', 'student_id'],
            data: this.data.map(item => {
              return {
                value: [
                  item[this.fieldIndices.x],
                  item[this.fieldIndices.y],
                  item[this.fieldIndices.z],
                  item[this.fieldIndices.cluster_label],
                  item[this.fieldIndices.total_score],
                  item[this.fieldIndices.student_id],
                ],
                itemStyle: {
                  color: this.labelColors[labelIndexMap[item[this.fieldIndices.cluster_label]]]
                }
              };
            }),
            symbolSize: val => {
              // 根据total_score的值来调整点的大小
              // return (val[4] / (maxScore)) * 10; // Scale symbol size based on score
              return ((val[4] - 30) / (maxScore - 30)) * 8 + 5
            },
            itemStyle: {
              borderWidth: 1,
              borderColor: 'rgba(255,255,255,0.8)'
            },
            emphasis: {
              itemStyle: {
                color: '#fff'
              }
            }
          }
        ]
      });
    }
  }
};
</script>

<style scoped>
#scater{
  width: 100%;
  height: 100%;
}
</style>
