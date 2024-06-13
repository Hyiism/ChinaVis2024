<template>
  <div id="scatter-all">
    <div id="scatter-button">
      <button @click="setClusterMethod('pca')" class="cluster-button" :class="{ 'active': clusterMethod === 'pca' }">PCA</button>
      <button @click="setClusterMethod('tsne')" class="cluster-button" :class="{ 'active': clusterMethod === 'tsne' }">T-SNE</button>
      <button @click="setClusterMethod('umap')" class="cluster-button" :class="{ 'active': clusterMethod === 'umap' }">UMAP</button>
    </div>
    <div ref="chart" id="scatter-chart">
      <!-- <div ref="d3Container" id="d3-container"></div> -->
    </div>
    <div ref="d3Container" id="d3-container"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import * as d3 from 'd3';
import axios from 'axios';
import ecStat from 'echarts-stat'; // 正确引入 echarts-stat

export default {
  name: 'ScatterChart',
  data() {
    return {
      myChart: null,
      rawData: [],
      data: [],
      clusterLabels: [],
      studentIds: [],
      clusterMethod: 'pca',
      CLUSTER_COUNT: 4,
      DIENSIION_CLUSTER_INDEX: 3,
      COLOR_ALL: ['#37A2DA', '#e06343', '#37a354', '#b55dba', '#b5bd48'],
      pieces: []
    };
  },
  mounted() {
    this.fetchScatterData();
  },
  methods: {
    setClusterMethod(method) {
      this.clusterMethod = method;
      this.fetchScatterData();
    },
    fetchScatterData() {
      axios.get(`http://10.12.44.190:8000/scaterVis_2d/?class_id=Class2&method=${this.clusterMethod}`)
        .then(response => {
          this.rawData = JSON.parse(response.data).data;
          this.processData();
          this.initChart();
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
    },
    processData() {
      this.data = this.rawData.map(item => [item[1], item[2], item[0]]); // 现在data为[x,y,student_id]
      this.clusterLabels = this.rawData.map(item => item[3]); // 提取 cluster_label
      this.studentIds = this.rawData.map(item => item[0]); // 提取 student_id
    },
    initChart() {
      this.$nextTick(() => {
        if (this.myChart) {
          this.myChart.dispose();
        }
        this.myChart = echarts.init(this.$refs.chart);
        this.generatePieces();
        echarts.registerTransform(ecStat.transform.clustering);
        this.updateChart();

        this.myChart.on('click', (params) => {
          const studentId = params.data[2]; // 获取 student_id
          const { offsetX, offsetY } = params.event.event; // 获取点击的X和Y坐标
          this.drawRings(studentId, offsetX, offsetY); // 绘制环状图
        });
      });
    },
    generatePieces() {
      this.pieces = [];
      for (let i = 0; i < this.CLUSTER_COUNT; i++) {
        this.pieces.push({
          value: i,
          label: 'cluster ' + i,
          color: this.COLOR_ALL[i]
        });
      }
    },
    updateChart() {
      const option = {
        dataset: [
          {
            source: this.data.map((item, index) => [...item, this.clusterLabels[index]])
          }
        ],
        tooltip: {
          position: 'top'
        },
        visualMap: {
          type: 'piecewise',
          top: 'middle',
          min: 0,
          max: this.CLUSTER_COUNT,
          left: 10,
          splitNumber: this.CLUSTER_COUNT,
          dimension: this.DIENSIION_CLUSTER_INDEX,
          pieces: this.pieces
        },
        grid: {
          left: 120
        },
        xAxis: {},
        yAxis: {},
        series: {
          type: 'scatter',
          encode: { tooltip: [2] },
          symbolSize: 12, // 调整点的大小
          itemStyle: {
            borderColor: '#555'
          }
        }
      };

      this.myChart.setOption(option);
    },
    drawRings(studentId, x, y) {
      // 查找选定的学生节点数据
      const studentData = this.rawData.find(d => d[0] === studentId);
      console.log(studentData)

      if (!studentData) return;

      // 模拟环状图数据（此部分需根据实际数据结构进行调整）
      const ringData = {
        "mor": 0.5,
        "afte": 0.4,
        "night": 0.1
      };

      // 清除之前的D3图表
      d3.select(this.$refs.d3Container).selectAll("*").remove();

      const svg = d3.select(this.$refs.d3Container).append("svg")
        .attr("width", 200) // 固定宽度
        .attr("height", 200) // 固定高度
        .style("position", "absolute")
        .style("left", `${x - 102}px`) // 确保环状图中心对齐点击位置
        .style("top", `${y - 796}px`); // 确保环状图中心对齐点击位置
        // .style("top", `${y - 100}px`); // 确保环状图中心对齐点击位置

      const radius = 5;
      const padding = 2;
      const outer_radius = 50;

      const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

      const total = d3.sum(Object.values(ringData).map(Number));
      let startAngle = 0;

      for (const [key, value] of Object.entries(ringData)) {
        const endAngle = startAngle + (2 * Math.PI * value / total);
        const arcGenerator = d3.arc()
          .innerRadius(radius + padding)
          .outerRadius(outer_radius)
          .startAngle(startAngle)
          .endAngle(endAngle);

        svg.append("path")
          .attr("d", arcGenerator)
          .attr("fill", colorScale(key))
          .attr("stroke", "grey")
          .attr("transform", `translate(100, 100)`); // 将环状图移动到中心

        startAngle = endAngle;
      }
    }
  }
};
</script>

<style scoped>
#scatter-all {
  width: 100%;
  height: 100%;
  position: relative;
}
#scatter-button {
  width: 100%;
  height: 10%;
  display: flex;
  justify-content: center;
  align-items: center;
}
#scatter-chart {
  width: 100%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
}
#d3-container {
  position: absolute;
  pointer-events: none;
}
.cluster-button {
  margin-right: 10px;
  width: 100px;
  height: 30px;
  font-size: 16px;
  background-color: #409EFF;
  color: #fff;
  border: none;
  border-radius: 5px;
}
.active {
  background-color: #45a049 !important;
}
</style>
