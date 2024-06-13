<template>
  <div class="bottom-chart">
    <!-- <p>班级视图BottomViewer test</p> -->
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
        const response = await axios.get('http://localhost:5000/get_class_knowledge_data');
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
        formattedData.push({ group: row.student_id, variable: 'b3C9s_score', value: row.b3C9s_score });
        formattedData.push({ group: row.student_id, variable: 'g7R2j_score', value: row.g7R2j_score });
        formattedData.push({ group: row.student_id, variable: 'k4W1c_score', value: row.k4W1c_score });
        formattedData.push({ group: row.student_id, variable: 'm3D1v_score', value: row.m3D1v_score });
        formattedData.push({ group: row.student_id, variable: 'r8S3g_score', value: row.r8S3g_score });
        formattedData.push({ group: row.student_id, variable: 's8Y2f_score', value: row.s8Y2f_score });
        formattedData.push({ group: row.student_id, variable: 't5V9e_score', value: row.t5V9e_score });
        formattedData.push({ group: row.student_id, variable: 'y9W5d_score', value: row.y9W5d_score });
        // formattedData.push({ group: row.class_id, variable: 'class_average_score', value: row.class_average_score });
      });
      this.heatmapData = formattedData;
    },
    createChart() {
      const margin = {top: 60, right: 60, bottom: 30, left: 105};
      // const width = 1050 - margin.left - margin.right;
      // const height = 300 - margin.top - margin.bottom;
      const width = this.$refs.chart.clientWidth - margin.left - margin.right - 0;
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
        .attr("id", "heatmap-svg"); // 给 SVG 元素添加一个 ID，以便其他视图中可以通过此 ID 定位该元素

      // Sample data
      // const data = [
      //   {group: 'A', variable: 'v1', value: 30},
      //   {group: 'A', variable: 'v2', value: 70},
      //   {group: 'B', variable: 'v1', value: 50},
      //   {group: 'B', variable: 'v2', value: 90},
      //   {group: 'C', variable: 'v1', value: 20},
      //   {group: 'C', variable: 'v2', value: 10},
      //   {group: 'D', variable: 'v1', value: 60},
      //   {group: 'D', variable: 'v2', value: 80},
      // ];

      // const myGroups = Array.from(new Set(data.map(d => d.group)));
      // const myVars = Array.from(new Set(data.map(d => d.variable)));
      const myGroups = Array.from(new Set(this.heatmapData.map(d => d.group)));
      const myVars = Array.from(new Set(this.heatmapData.map(d => d.variable)));

      // Build X scales and axis
      const x = d3.scaleBand()
        .range([0, width])
        .domain(myGroups)
        .padding(0.05);
      // svg.append("g")
      //   .style("font-size", 15)
      //   .attr("transform", `translate(0, ${height})`)
      //   .call(d3.axisBottom(x).tickSize(0))
      //   .select(".domain").remove();

      // Build Y scales and axis
      const y = d3.scaleBand()
        .range([height, 0])
        .domain(myVars)
        .padding(0.05);
      svg.append("g")
        .style("font-size", 15)
        .call(d3.axisLeft(y).tickSize(0))
        .select(".domain").remove();

      // Build color scale
      // const myColor = d3.scaleSequential()
      //   .interpolator(d3.interpolateInferno)
      //   .domain([50, 1]);
      // Compute color scale domain
      const valueExtent = d3.extent(this.heatmapData, d => d.value);
      const myColor = d3.scaleSequential()
        // .interpolator(d3.interpolateInferno) //颜色从黄到紫
        // .interpolator(d3.interpolateViridis) //颜色从深紫色到黄绿色
        .interpolator(d3.interpolateMagma)  //颜色从深紫色到黄色
        // .interpolator(d3.interpolatePlasma) //颜色从紫色到黄色，过渡较为平滑
        // .interpolator(d3.interpolateCividis) //颜色从蓝色到黄色，适合色盲人士
        // .interpolator(d3.interpolateWarm) //颜色从红色到黄色，模拟温暖的颜色渐变
        // .interpolator(d3.interpolateCool) //颜色从蓝色到红色，模拟凉爽的颜色渐变
        // .interpolator(d3.interpolateCubehelixDefault) //基于立方螺旋算法的颜色渐变，默认从黑色到白色
        // .interpolator(d3.interpolateRainbow) //颜色从红色到紫色的彩虹渐变
        // .interpolator(d3.interpolateSinebow) //类似于d3.interpolateRainbow，但使用正弦波生成渐变
        // .interpolator(d3.interpolateBlues) //颜色从浅蓝色到深蓝色
        // .interpolator(d3.interpolateGreens) //颜色从浅绿色到深绿色
        // .interpolator(d3.interpolateGreys) //颜色从白色到黑色
        // .interpolator(d3.interpolateBuGn) //颜色从浅蓝绿色到深蓝绿色
        // .interpolator(d3.interpolateBuPu) //颜色从浅蓝色到深紫色
        // .interpolator(d3.interpolateOrRd) //颜色从浅橙色到深红色
        // .interpolator(d3.interpolatePuRd) //颜色从浅紫色到深红色
        // .interpolator(d3.interpolateYlOrBr) //颜色从浅黄色到深橙棕色
        .domain([valueExtent[1], valueExtent[0]]); //把颜色反一下，让较深的颜色来代表较大的数据

      // Create a tooltip
      const tooltip = d3.select(this.$refs.chart)
        .append("div")
        .style("opacity", 0)  //设置工具提示的初始透明度为 0
        .attr("class", "tooltip")
        .style("background-color", "white")  //设置展示数据的小框为白色
        .style("border", "solid")  //设置工具提示的边框为实线
        .style("border-width", "2px")  //设置工具提示的边框宽度为 2 像素
        .style("border-radius", "5px")  //设置工具提示的边框圆角半径为 5 像素,，给它一个圆角外观
        .style("padding", "5px")  //设置工具提示内容的内边距为 5 像素，确保内容不紧贴边框
        .style("pointer-events", "none")
        .style("position", "absolute");

      // Tooltip functions
      const mouseover = function(event, d) {
        tooltip.style("opacity", 1);
        d3.select(this).style("stroke", "black").style("opacity", 1);
      };
      const mousemove = function(event, d) {
        tooltip.html(`Group: ${d.group}<br>Variable: ${d.variable}<br>Value: ${d.value}`)
          .style("left",`${event.pageX + 5}px`)
          .style("top", `${event.pageY - 570}px`);
      };
      const mouseleave = function(event, d) {
        tooltip.style("opacity", 0);
        d3.select(this).style("stroke", "none").style("opacity", 0.8);
      };

      // Add the squares
      svg.selectAll()
        .data(this.heatmapData, function(d) {return d.group + ':' + d.variable;})
        .join("rect")
        .attr("x", function(d) { return x(d.group); })
        .attr("y", function(d) { return y(d.variable); })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("width", x.bandwidth())
        .attr("height", y.bandwidth())
        .style("fill", function(d) { return myColor(d.value); })
        .style("stroke-width", 4)
        .style("stroke", "none")
        .style("opacity", 0.8)
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave);

      // Add title to graph
      // svg.append("text")
      //   .attr("x", 0)
      //   .attr("y", -50)
      //   .attr("text-anchor", "left")
      //   .style("font-size", "22px")
      //   .text("A d3.js heatmap");

      // Add subtitle to graph
      // svg.append("text")
      //   .attr("x", 0)
      //   .attr("y", -20)
      //   .attr("text-anchor", "left")
      //   .style("font-size", "14px")
      //   .style("fill", "grey")
      //   .style("max-width", 400)
      //   .text("A short description of the take-away message of this chart.");

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

      // Create color stops for the gradient based on the color scale
      // const colorRange = d3.range(1, 101, 1); // Range of values from 1 to 100
      // colorRange.forEach(value => {
      //   gradient.append("stop")
      //     .attr("offset", `${(value - 1) / 99 * 100}%`)
      //     .attr("stop-color", myColor(value));
      // });
      const colorRange = d3.range(valueExtent[0], valueExtent[1], (valueExtent[1] - valueExtent[0]) / 100);
      colorRange.forEach((value, index) => {
        gradient.append("stop")
          .attr("offset", `${index / (colorRange.length - 1) * 100}%`)
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
  overflow: visible; /* 确保容器能显示超出的部分 */
  /* position: relative; */
}
</style>


