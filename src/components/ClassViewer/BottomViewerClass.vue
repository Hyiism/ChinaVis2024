<template>
  <div class="bottom-chart">
    <div ref="chart" class="bottom-chart"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';

export default {
  name: 'BottomChart',
  data() {
    return {
      heatmapData: [],
    };
  },
  mounted() {
    this.fetchHeatmapData();
  },
  methods: {
    async fetchHeatmapData() {
      try {
        const response = await axios.get('http://10.12.44.190:8000/get_class_knowledge_data');
        const data = response.data;
        this.processData(data);
        this.createChart();
      } catch (error) {
        console.error('Error fetching heatmap data:', error);
      }
    },
    processData(data) {
      const formattedData = [];
      data.forEach(row => {
        formattedData.push({ group: row.class_id, variable: 'b3C9s_score', value: row.b3C9s_score });
        formattedData.push({ group: row.class_id, variable: 'g7R2j_score', value: row.g7R2j_score });
        formattedData.push({ group: row.class_id, variable: 'k4W1c_score', value: row.k4W1c_score });
        formattedData.push({ group: row.class_id, variable: 'm3D1v_score', value: row.m3D1v_score });
        formattedData.push({ group: row.class_id, variable: 'r8S3g_score', value: row.r8S3g_score });
        formattedData.push({ group: row.class_id, variable: 's8Y2f_score', value: row.s8Y2f_score });
        formattedData.push({ group: row.class_id, variable: 't5V9e_score', value: row.t5V9e_score });
        formattedData.push({ group: row.class_id, variable: 'y9W5d_score', value: row.y9W5d_score });
      });
      this.heatmapData = formattedData;
    },
    createChart() {
      const margin = { top: 60, right: 50, bottom: 30, left: 100 };
      const width = this.$refs.chart.clientWidth - margin.left - margin.right;
      const height = this.$refs.chart.clientHeight - margin.top - margin.bottom;

      // Remove any existing SVG
      d3.select(this.$refs.chart).selectAll("*").remove();

      // Append the svg object to the ref div
      const svg = d3.select(this.$refs.chart)
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`)
        .attr("id", "heatmap-svg");

      const myGroups = Array.from(new Set(this.heatmapData.map(d => d.group)));
      const myVars = Array.from(new Set(this.heatmapData.map(d => d.variable)));

      // Build X scales and axis
      const x = d3.scaleBand()
        .range([0, width])
        .domain(myGroups)
        .padding(0.05);
      svg.append("g")
        .style("font-size", 15)
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(x).tickSize(0))
        .select(".domain").remove();

      // Build Y scales and axis
      const y = d3.scaleBand()
        .range([height, 0])
        .domain(myVars)
        .padding(0.05);
      svg.append("g")
        .style("font-size", 15)
        .call(d3.axisLeft(y).tickSize(0))
        .select(".domain").remove();

      // Compute color scale domain
      const valueExtent = d3.extent(this.heatmapData, d => d.value);
      const myColor = d3.scaleSequential()
        .interpolator(d3.interpolateYlGnBu)
        .domain([valueExtent[0], valueExtent[1]]);

      // Create a tooltip
      const tooltip = d3.select(this.$refs.chart)
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "2px")
        .style("border-radius", "5px")
        .style("padding", "5px")
        .style("pointer-events", "none")
        .style("position", "absolute");

      // Tooltip functions
      const mouseover = function (event, d) {
        tooltip.style("opacity", 1);
        d3.select(this).style("stroke", "black").style("opacity", 1);
      };
      const mousemove = function (event, d) {
        tooltip.html(`Group: ${d.group}<br>Variable: ${d.variable}<br>Value: ${d.value}`)
          .style("left", `${event.pageX + 5}px`)
          .style("top", `${event.pageY - 570}px`);
      };
      const mouseleave = function (event, d) {
        tooltip.style("opacity", 0);
        d3.select(this).style("stroke", "none").style("opacity", 0.8);
      };

      // Add the squares
      svg.selectAll()
        .data(this.heatmapData, function (d) { return d.group + ':' + d.variable; })
        .join("rect")
        .attr("x", function (d) { return x(d.group); })
        .attr("y", function (d) { return y(d.variable); })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("width", x.bandwidth())
        .attr("height", y.bandwidth())
        .style("fill", function (d) { return myColor(d.value); })
        .style("stroke-width", 4)
        .style("stroke", "none")
        .style("opacity", 0.8)
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave);

      // Add legend
      const legendHeight = height;
      const legendWidth = 20;
      const legendMargin = 10;
      const legend = svg.append("g")
        .attr("class", "legend")
        .attr("transform", `translate(${width + legendMargin}, 0)`);

      const legendScale = d3.scaleLinear()
        .domain(valueExtent)
        .range([legendHeight, 0]);

      const legendAxis = d3.axisRight(legendScale)
        .ticks(5);

      legend.append("g")
        .attr("class", "axis")
        .attr("transform", `translate(${legendWidth}, 0)`)
        .call(legendAxis);

      const gradient = svg.append("defs")
        .append("linearGradient")
        .attr("id", "gradient")
        .attr("x1", "0%")
        .attr("y1", "100%")
        .attr("x2", "0%")
        .attr("y2", "0%");

      const colorRange = d3.range(1, 101, 1);
      colorRange.forEach(value => {
        gradient.append("stop")
          .attr("offset", `${(value - 1) / 99 * 100}%`)
          .attr("stop-color", myColor(value));
      });

      legend.append("rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", legendWidth)
        .attr("height", legendHeight)
        .style("fill", "url(#gradient)");
    }
  }
}
</script>

<style scoped>
.bottom-chart {
  width: 100%;
  height: 100%;
  overflow: visible;
}
</style>
