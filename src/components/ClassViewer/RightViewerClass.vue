<template>
  <div id="right-all">
    <div id="scatter-button">
      <button @click="setClusterMethod('pca')" class="cluster-button" :class="{ 'active': clusterMethod === 'pca' }">PCA</button>
      <button @click="setClusterMethod('tsne')" class="cluster-button" :class="{ 'active': clusterMethod === 'tsne' }">T-SNE</button>
      <button @click="setClusterMethod('umap')" class="cluster-button" :class="{ 'active': clusterMethod === 'umap' }">UMAP</button>
    </div>
    <div ref="ProjectionView" id="ProjectionView"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';
import EventBus from '@/eventBus'; // 导入事件总线

export default {
  name: 'ProjectionView',
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
          console.log(_this.nodes, typeof(_this.nodes));
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
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
      // var colorScale = d3.scaleOrdinal()
      //   .domain([0, 1, 2, 3])  // Ensure the domain covers all four clusters
      //   .range(d3.schemeCategory10);
      const radius = 6;
      const padding = 2;
      const outer_radius = 50;

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
        });;

      this.updateRings = () => {
        glyphs.each(function(node) {
          d3.select(this).selectAll('path').remove();
          if (!node.showRings) return;
          const g = d3.select(this);
          const ringData = node.ring_data;
          const total = d3.sum(Object.values(ringData).map(Number));
          let startAngle = 0;
          for (const [key, value] of Object.entries(ringData)) {
            const endAngle = startAngle + (2 * Math.PI * value / total);
            const arcGenerator = d3.arc()
              .innerRadius(radius + padding)
              .outerRadius(outer_radius)
              .startAngle(startAngle)
              .endAngle(endAngle);
            g.append("path")
              .attr("d", arcGenerator)
              .attr("fill", colorScale(key))
              .attr("stroke", "grey")
              .attr("transform", `translate(${xScale(node.x)},${yScale(node.y)})`);
            startAngle = endAngle;
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
