<template>
  <div id="scatter-all">
    <div id="scatter-button">
      <button @click="setClusterMethod('pca')" class="cluster-button" :class="{ 'active': clusterMethod === 'pca' }">PCA</button>
      <button @click="setClusterMethod('tsne')" class="cluster-button" :class="{ 'active': clusterMethod === 'tsne' }">T-SNE</button>
      <button @click="setClusterMethod('umap')" class="cluster-button" :class="{ 'active': clusterMethod === 'umap' }">UMAP</button>
    </div>
    <div ref="chart" id="scatter-chart"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import ecStat from 'echarts-stat'; // 正确引入 echarts-stat

export default {
  name: 'ScatterChart',
  data() {
    return {
      myChart: null,
      rawData: [],
      data: [],
      clusterLabels: [],
      clusterMethod: 'pca',
      CLUSTER_COUNT: 4,
      DIENSIION_CLUSTER_INDEX: 2,
      COLOR_ALL: [
        '#37A2DA',
        '#e06343',
        '#37a354',
        '#b55dba',
        '#b5bd48'
      ],
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
      this.$axios.get(`http://10.12.44.190:8000/scaterVis_2d/?class_id=Class2&method=${this.clusterMethod}`) // 替换为实际的API端点
        .then(response => {
          this.rawData = JSON.parse(response.data).data;
          console.log("###2d scatter start###");
          console.log(this.rawData);
          this.processData();
          this.initChart();
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
    },
    processData() {
      this.data = this.rawData.map(item => [item[1], item[2]]); // 提取 x 和 y
      this.clusterLabels = this.rawData.map(item => item[3]); // 提取 cluster_label
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
          encode: { tooltip: [0, 1] },
          symbolSize: 10, // 调整点的大小
          itemStyle: {
            borderColor: '#555'
          }
        }
      };

      this.myChart.setOption(option);
    }
  }
};
</script>

<style scoped>

#scatter-all {
  width: 100%;
  height: 100%;
}
#scatter-button {
  /* margin-top: 10px; */
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
