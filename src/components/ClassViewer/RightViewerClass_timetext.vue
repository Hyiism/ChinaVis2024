<template>
  <div id="right-all">
    <div id="scatter-button">
      <button @click="setClusterMethod('pca')" class="cluster-button"
        :class="{ 'active': clusterMethod === 'pca' }">PCA</button>
      <button @click="setClusterMethod('tsne')" class="cluster-button"
        :class="{ 'active': clusterMethod === 'tsne' }">T-SNE</button>
      <button @click="setClusterMethod('umap')" class="cluster-button"
        :class="{ 'active': clusterMethod === 'umap' }">UMAP</button>
    </div>
    <div ref="ProjectionView" id="ProjectionView"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';
import EventBus from '@/eventBus'; // 导入事件总线

export default {
  name: 'RightViewerClass',
  data() {
    return {
      nodes: [],
      clusterMethod: 'pca',
    };
  },
  mounted() {
    this.drawView();
    window.addEventListener('resize', this.updateView);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.updateView);
  },
  methods: {
    setClusterMethod(method) {
      this.clusterMethod = method;
      this.drawView(); // Update the view with new data
    },
    async getdata() {
      var _this = this;
      await axios.get(`http://10.12.44.190:8000/get_projection_data/?class_id=Class2&method=${this.clusterMethod}`)
        .then(res => {
          console.log("projection data");
          _this.nodes = JSON.parse(res.data).nodes;
          console.log(_this.nodes, typeof (_this.nodes));
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
      console.log("11111111")
    },
    async drawView() {
      await this.getdata();

      var svgWidth = this.$refs.ProjectionView.offsetWidth;
      var svgHeight = this.$refs.ProjectionView.offsetHeight;
      var margin = { top: 20, right: 20, bottom: 20, left: 20 };
      var width = svgWidth - margin.left - margin.right;
      var height = svgHeight - margin.top - margin.bottom;

      d3.select('#ProjectionView').selectAll('*').remove(); // Clear previous SVG content

      const svg = d3.select('#ProjectionView').append('svg')
        .attr('width', svgWidth)
        .attr('height', svgHeight)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`)
        .call(
          d3.zoom().scaleExtent([1, 10]).on("zoom", (event) => {
            svg.attr("transform", event.transform);
          })
        );

      var colorScale = d3.scaleOrdinal(d3.schemeCategory10);
      const colors = d3.scaleSequential(d3.interpolateMagma);
      const radius = 6;

      var xScale = d3.scaleLinear()
        .domain(d3.extent(this.nodes, (d) => +d.x)).nice()
        .range([0, width]);

      var yScale = d3.scaleLinear()
        .domain(d3.extent(this.nodes, (d) => +d.y)).nice()
        .range([height, 0]);

      const xAxis = d3.axisBottom(xScale);
      const yAxis = d3.axisLeft(yScale);

      svg.append("g")
        .attr("class", "x axis")
        .attr("transform", `translate(0,${height / 2})`)
        .call(xAxis);

      svg.append("g")
        .attr("class", "y axis")
        .attr("transform", `translate(${width / 2},0)`)
        .call(yAxis);

      const glyphs = svg.selectAll('g.glyph')
        .data(this.nodes)
        .enter().append('g')
        .attr('class', 'glyph');

      glyphs.append('circle')
        .attr('cx', d => xScale(d.x))
        .attr('cy', d => yScale(d.y))
        .attr('r', radius)
        .attr('fill', d => colorScale(d.cluster_label))
        .attr("stroke", "grey")
        .attr("class", "eachnode")
        .on('mouseover', (event, d) => {
          d.showRings = true;
          this.updateRings();
        })
        .on('mouseout', (event, d) => {
          d.showRings = false;
          this.updateRings();
        })
        .on('click', (event, d) => {
          const studentId = d.student_id; // 获取 student_id
          console.log("student_id")
          console.log(studentId);
          EventBus.$emit('studentSelected', studentId); // 触发事件，传递 student_id
        });

      this.updateRings = () => {
        glyphs.each(function (node) {
          d3.select(this).selectAll('path').remove();
          d3.select(this).selectAll('line').remove(); // 移除所有分割线
          d3.select(this).selectAll('text').remove(); // 移除所有时间标签

          if (!node.showRings) return;
          const g = d3.select(this);
          const avgScore = node.total_score;
          const startAngle = 0;
          const endAngle = 2 * Math.PI * (avgScore / 150);
          const padding = 4;
          const outer_radius = 13;
          const arcGenerator = d3.arc()
            .innerRadius(radius + padding)
            .outerRadius(outer_radius)
            .startAngle(startAngle)
            .endAngle(endAngle);
          g.append("path")
            .attr("d", arcGenerator)
            .attr("fill", d => colorScale(d.cluster_label))
            .attr("stroke", "grey")
            .attr("transform", `translate(${xScale(node.x)},${yScale(node.y)})`);

          const scoreingData = node.state_data;
          const totalScore = d3.sum(Object.values(scoreingData).map(Number));
          const keyMapping = {
            "state_ae_percentage": 1,
            "state_e_percentage": 2,
            "state_pc_percentage": 3,
            "state_ac_percentage": 4
          };
          const gapAngle = 0.08;
          let startAngle02 = 0;
          for (const [key, value] of Object.entries(scoreingData)) {
            const endAngle02 = startAngle02 + (2 * Math.PI * value / totalScore) - gapAngle;
            const padding = 10;
            const outer_radius = 24;
            const arcGenerator02 = d3.arc()
              .innerRadius(radius + padding)
              .outerRadius(outer_radius)
              .startAngle(startAngle02)
              .endAngle(endAngle02);
            g.append("path")
              .attr("d", arcGenerator02)
              .attr("fill", colors(keyMapping[key] / 8))
              .attr("stroke", "grey")
              .attr("transform", `translate(${xScale(node.x)},${yScale(node.y)})`);
            startAngle02 = endAngle02 + gapAngle;
          }

          const timeData = node.time_data;
          const totalTimeSlots = 24;
          const arcAngle = (2 * Math.PI) / totalTimeSlots;
          let startAngle03 = 0;
          for (const [key, value03] of Object.entries(timeData)) {
            const endAngle03 = startAngle03 + arcAngle;
            const padding = 21;
            const outer_radius = radius + padding + value03 * 33;
            const arcGenerator03 = d3.arc()
              .innerRadius(radius + padding)
              .outerRadius(outer_radius)
              .startAngle(startAngle03)
              .endAngle(endAngle03);
            g.append("path")
              .attr("d", arcGenerator03)
              .attr("fill", colors(value03))
              .attr("stroke", "grey")
              .attr("transform", `translate(${xScale(node.x)},${yScale(node.y)})`);
            startAngle03 = endAngle03;
          }

          // 添加时间标识环
          const outerRadiusTime = radius + 60;
          const arcAngleTime = (2 * Math.PI) / totalTimeSlots;
          let startAngleTime = 0;
          for (let i = 0; i < totalTimeSlots; i++) {
            const endAngleTime = startAngleTime + arcAngleTime;
            const arcGeneratorTime = d3.arc()
              .innerRadius(outerRadiusTime)
              .outerRadius(outerRadiusTime + 1)
              .startAngle(startAngleTime)
              .endAngle(endAngleTime);

            g.append("path")
              .attr("d", arcGeneratorTime)
              .attr("fill", 'lightgrey')
              .attr("transform", `translate(${xScale(node.x)},${yScale(node.y)})`);

            // 添加分割线
            const lineRadius = outerRadiusTime + 1;
            const lineX1 = Math.cos(startAngleTime) * lineRadius;
            const lineY1 = Math.sin(startAngleTime) * lineRadius;
            const lineX2 = Math.cos(startAngleTime) * (lineRadius + 5);
            const lineY2 = Math.sin(startAngleTime) * (lineRadius + 5);

            g.append("line")
              .attr("x1", xScale(node.x) + lineX1)
              .attr("y1", yScale(node.y) + lineY1)
              .attr("x2", xScale(node.x) + lineX2)
              .attr("y2", yScale(node.y) + lineY2)
              .attr("stroke", "lightgrey")
              .attr("stroke-width", 0.5);

            // 添加时间标签
            const labelAngle = startAngleTime + arcAngleTime / 2;
            const labelRadius = outerRadiusTime + 5;
            const labelX = Math.cos(labelAngle) * labelRadius;
            const labelY = Math.sin(labelAngle) * labelRadius;

            g.append("text")
              .attr("x", xScale(node.x) + labelX)
              .attr("y", yScale(node.y) + labelY)
              .attr("dy", "0.35em")
              .attr("text-anchor", "middle")
              .attr("font-size", "5px")
              .attr("fill", "lightgrey")
              .text(`${i}`);

            startAngleTime = endAngleTime;
          }
        });
      };

      // Add legend
      const legend = svg.selectAll(".legend")
        .data(colorScale.domain())
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", (d, i) => `translate(0,${i * 20})`);

      legend.append("rect")
        .attr("x", width - 18)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", colorScale);

      legend.append("text")
        .attr("x", width - 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(d => `cluster ${d}`);

      window.addEventListener('resize', () => {
        const newSvgWidth = this.$refs.ProjectionView.offsetWidth;
        const newSvgHeight = this.$refs.ProjectionView.offsetHeight;
        svg.attr('width', newSvgWidth).attr('height', newSvgHeight);
        const margin_width = newSvgWidth * 0.05;
        const margin_height = newSvgHeight * 0.05;
        xScale.range([margin_width, newSvgWidth - margin_width]);
        yScale.range([margin_height, newSvgHeight - margin_height]);
        glyphs.selectAll('circle').attr('cx', d => xScale(d.x)).attr('cy', d => yScale(d.y));
        this.updateRings();
      });
    },
  },
};
</script>

<style scoped>
#right-all {
  width: 100%;
  height: 100%;
}

#scatter-button {
  width: 100%;
  height: 10%;
  display: flex;
  justify-content: center;
  align-items: center;
}

#ProjectionView {
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
