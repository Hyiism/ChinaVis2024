<template>
  <div class="bottomright-chart">
    <el-select v-model="selectedcolumns" multiple placeholder="请选择y轴" class="feat-select" v-if="state_all"
      @change="handleSelectChange">
      <el-option v-for="item in allcolumns" :key="item.value" :label="item.label" :value="item.value">
      </el-option>
    </el-select>
    <el-select v-model="selectedcolumns_detail" multiple placeholder="请选择x y轴" class="feat-select" v-if="state_detail" 
      @change="handleSelectChangeDetail">
      <el-option v-for="item in allcolumns" :key="item.value" :label="item.label" :value="item.value">
      </el-option>
    </el-select>
    <div ref="chartContainer" style="display: flex; margin-top: 50px; margin-left: 15px;"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import * as Plot from '@observablehq/plot';
import { data } from 'jquery';
import EventBus from '@/eventBus'; // 导入事件总线
import { mapGetters } from 'vuex';
export default {
  name: 'ClusterPlotChart',
  data() {
    return {
      state_all: true,
      state_detail: false,
      data: [],
      // 默认显示所有类别数据, 根据不同的clusterSelected值向后段请求不同的数据，all 0 1 2 3
      clusterSelected: 'all',
      width: 800,
      height: 500,
      boxWidth: 100,
      allcolumns: [
        { label: "做题数量", value: "title_counts" },
        { label: "平均间隔时间", value: "time_difference_mean" },
        { label: "上午做题比例", value: "time_split_0_percentage" },
        { label: "下午做题比例", value: "time_split_1_percentage" },
        { label: "晚上做题比例", value: "time_split_2_percentage" },
        { label: "平均提交次数", value: "submit_times_avg" },
        { label: "平均空间复杂度", value: "all_memory_avg" },
        { label: "平均时间复杂度", value: "all_timeconsume_avg" },
        { label: "AE状态占比", value: "state_ae_percentage" },
        { label: "AE状态占比", value: "state_e_percentage" },
        { label: "E状态占比", value: "state_pc_percentage" },
        { label: "AC状态占比", value: "state_ac_percentage" }
      ],
      selectedcolumns: ["time_split_2_percentage"],
      selectedcolumns_detail: ["submit_times_avg", "time_split_2_percentage"]
    };
  },
  computed: {
    ...mapGetters(['classId'])
  },
  mounted() {
    // this.renderChart();
    this.fetchStudentScores();
    // 监听clusterSelected事件，当clusterSelected发生变化时，重新获取数据
    EventBus.$on('clusterSelected', (clusterSelected) => {
      // alert('clusterSelected: ' + clusterSelected);
      this.clusterSelected = clusterSelected;
      this.fetchStudentScores();
    });
  },
  beforeDestroy() {
    EventBus.$off('clusterSelected');
  },
  methods: {
    fetchStudentScores() {
      this.$axios.get(`'http://10.12.44.190:8000/scatterMatrix/?class_id=${this.classId}`)
      this.$axios
        .get(`http://10.12.44.190:8000/boxplot/?cluster_id=${this.clusterSelected}&class_id=Class1`) // Replace with actual API endpoint
        .then((response) => {
          this.data = JSON.parse(response.data);
          // 如果是整体视图，就显示每个类别的数据，集中比较用户选的变量的统计情况
          if (this.clusterSelected === 'all') {
            this.state_all = true;
            this.state_detail = false;
            this.renderChart();
            // 如果是类别视图，就细致展示每个类里面的数据，比如用户选择变量1和变量2 就使用变量1和变量2的数据画图；这里暂时以submit_times_avg为横轴 total_score为纵轴
          } else {
            this.state_all = false;
            this.state_detail = true;
            this.renderChartDetail();
          }
        })
        .catch((error) => {
          console.error('There was an error!', error);
        });
    },
    handleSelectChange(val) {
      const maxSelection = 1;
      if (val.length > maxSelection) {
        val.pop();
        this.$message({
          message: `最多只能选择 ${maxSelection} 项`,
          type: 'warning'
        });
      }
      this.selectedcolumns = val;
      this.renderChart();
    },
    handleSelectChangeDetail(val) {
      const maxSelection = 2;
      if (val.length > maxSelection) {
        val.pop();
        this.$message({
          message: `最多只能选择 ${maxSelection} 项`,
          type: 'warning'
        });
      }
      this.selectedcolumns_detail = val;
      this.renderChartDetail();
    },
    renderChart() {
      const colorScale = d3.scaleOrdinal(d3.schemeCategory10).domain(this.clusters);

      const dotPlot = Plot.plot({
        width: this.width - this.boxWidth,
        height: this.height,
        x: {
          label: 'Cluster Label',
          // domain: d3.extent(this.data, d => d.cluster_label_tsne),
          // 到时候嵌入视图分类成1 2 3 4类
          domain: [0, 1, 2, 3],
          tickSize: 6,
          tickPadding: 6,
          tickFormat: d3.format("d"),
          line: true,
          grid: true,
          // labelAnchor: "end",
          labelOffset: 10,
          labelFontSize: 12,
          stroke: "black",
          strokeWidth: 2
        },
        y: {
          label: `${this.selectedcolumns[0]}`,
          domain: this.dataRange,
          tickSize: 6,
          tickPadding: 6,
          tickFormat: d3.format(".2f"),
          line: true,
          grid: true,
          // labelAnchor: "end",
          labelOffset: 10,
          labelFontSize: 12,
          stroke: "black",
          strokeWidth: 2
        },
        color: {
          type: 'ordinal',
          legend: false,
          // TODO: 有待修改为嵌入视图传来的cluster颜色
          range: d3.schemeCategory10,
          domain: this.clusters
        },
        marks: [
          Plot.dot(this.data, { x: 'cluster_label_tsne', y: d => d[this.selectedcolumns[0]], fill: d => colorScale(d.cluster_label_tsne), size: 50, title: d => `Cluster: ${d.cluster_label_tsne}\n ${this.selectedcolumns[0]}: ${d[this.selectedcolumns[0]]}` })
        ]
      });

      const boxPlot = Plot.plot({
        width: this.boxWidth,
        height: this.height,
        x: { type: 'identity' },
        y: { label: null, domain: this.dataRange },
        marks: [
          Plot.ruleX([{ y1: this.st.min, y2: this.st.max }], { x: 12.5, y1: 'y1', y2: 'y2' }),
          Plot.rect([{ y1: this.st.lower, y2: this.st.upper }], { x1: 0, x2: 25, y1: 'y1', y2: 'y2', fill: 'rgba(244,84,30,1)', stroke: 'black', strokeWidth: 1 }),
          Plot.ruleY([this.st.min, this.st.max], { x1: 7, x2: 19 }),
          Plot.ruleY([{ y: this.st.mean }], { x1: 0, x2: 25, y: 'y', strokeWidth: 0.75 }),
          Plot.ruleY([{ y: this.st.median }], { x1: 0, x2: 25, y: 'y', strokeDasharray: '2', strokeWidth: 0.75 }),
          Plot.text(
            [
              { y: this.st.lower, t: `25th Percentile (${this.st.lower.toFixed(2)})` },
              { y: this.st.upper, t: `75th Percentile (${this.st.upper.toFixed(2)})` },
              { y: this.st.min, t: `5th Percentile (${this.st.min.toFixed(2)})` },
              { y: this.st.max, t: `95th Percentile (${this.st.max.toFixed(2)})` },
              { y: this.st.mean, t: `Mean (${this.st.mean.toFixed(2)})` },
              { y: this.st.median, t: `Median (${this.st.median.toFixed(2)})` }
            ],
            { x: 30, y: 'y', text: 't', textAnchor: 'start' }
          ),
          Plot.dotY(
            this.data.filter(d => d[this.selectedcolumns[0]] < this.st.min || d[this.selectedcolumns[0]] > this.st.max),
            { x: 12.5, y: 'submit_times_avg', fill: '#999', fillOpacity: 0.5 }
          )
        ]
      });

      const container = this.$refs.chartContainer;
      container.innerHTML = ''; // 清除之前的图表
      container.appendChild(dotPlot);
      container.appendChild(boxPlot);
      // container.appendChild(dotPlot.node());
      // container.appendChild(boxPlot.node());

      [...boxPlot.querySelectorAll('g.tick')].forEach(d => d.remove());
    },

    renderChartDetail() {
      const colorScale = d3.scaleOrdinal(d3.schemeCategory10).domain(this.clusters);

      const dotPlot = Plot.plot({
        width: this.width - this.boxWidth,
        height: this.height,
        x: {
          label: `${this.selectedcolumns_detail[0]}`,
          domain: d3.extent(this.data, d => d[this.selectedcolumns_detail[0]]),
          tickSize: 6,
          tickPadding: 6,
          tickFormat: d3.format("d"),
          line: true,
          grid: true,
          // labelAnchor: "end",
          labelOffset: 10,
          labelFontSize: 12,
          stroke: "black",
          strokeWidth: 2
        },
        y: {
          label: `${this.selectedcolumns_detail[1]}`,
          domain: this.dataRangeDetail,
          tickSize: 6,
          tickPadding: 6,
          tickFormat: d3.format(".2f"),
          line: true,
          grid: true,
          // labelAnchor: "end",
          labelOffset: 10,
          labelFontSize: 12,
          stroke: "black",
          strokeWidth: 2
        },
        color: {
          type: 'ordinal',
          legend: false,
          // TODO: 有待修改为嵌入视图传来的cluster颜色
          range: d3.schemeCategory10,
          domain: this.clusters
        },
        marks: [
          Plot.dot(this.data, { x: d => d[this.selectedcolumns_detail[0]], y: d => d[this.selectedcolumns_detail[1]], fill: d => colorScale(d.cluster_label_tsne), size: 150, title: d => `${this.selectedcolumns_detail[0]}: ${d[this.selectedcolumns_detail[0]]}\n ${this.selectedcolumns_detail[1]}: ${d[this.selectedcolumns_detail[1]]}` })
        ]
      });

      const boxPlot = Plot.plot({
        width: this.boxWidth,
        height: this.height,
        x: { type: 'identity' },
        y: { label: null, domain: this.dataRangeDetail },
        marks: [
          Plot.ruleX([{ y1: this.stDetail.min, y2: this.stDetail.max }], { x: 12.5, y1: 'y1', y2: 'y2' }),
          Plot.rect([{ y1: this.stDetail.lower, y2: this.stDetail.upper }], { x1: 0, x2: 25, y1: 'y1', y2: 'y2', fill: 'rgba(244,84,30,1)', stroke: 'black', strokeWidth: 1 }),
          Plot.ruleY([this.stDetail.min, this.stDetail.max], { x1: 7, x2: 19 }),
          Plot.ruleY([{ y: this.stDetail.mean }], { x1: 0, x2: 25, y: 'y', strokeWidth: 0.75 }),
          Plot.ruleY([{ y: this.stDetail.median }], { x1: 0, x2: 25, y: 'y', strokeDasharray: '2', strokeWidth: 0.75 }),
          Plot.text(
            [
              { y: this.stDetail.lower, t: `25th Percentile (${this.stDetail.lower.toFixed(2)})` },
              { y: this.stDetail.upper, t: `75th Percentile (${this.stDetail.upper.toFixed(2)})` },
              { y: this.stDetail.min, t: `5th Percentile (${this.stDetail.min.toFixed(2)})` },
              { y: this.stDetail.max, t: `95th Percentile (${this.stDetail.max.toFixed(2)})` },
              { y: this.stDetail.mean, t: `Mean (${this.stDetail.mean.toFixed(2)})` },
              { y: this.stDetail.median, t: `Median (${this.stDetail.median.toFixed(2)})` }
            ],
            { x: 30, y: 'y', text: 't', textAnchor: 'start' }
          ),
          Plot.dotY(
            this.data.filter(d => d.total_score < this.stDetail.min || d.total_score > this.stDetail.max),
            { x: 12.5, y: 'total_score', fill: '#999', fillOpacity: 0.5 }
          )
        ]
      });

      const container = this.$refs.chartContainer;
      container.innerHTML = ''; // 清除之前的图表
      container.appendChild(dotPlot);
      container.appendChild(boxPlot);

      [...boxPlot.querySelectorAll('g.tick')].forEach(d => d.remove());
    }
  },
  watch: {
    selectedcolumns: {
      handler() {
        this.renderChart();
      },
      deep: true
    },
    selectedcolumns_detail: {
      handler() {
        this.renderChartDetail();
      },
      deep: true
    }
  }
};
</script>

<style scoped>
.bottomright-chart {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.feat-select {
  width: 20%;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 10;
  background-color: white;
}
</style>
