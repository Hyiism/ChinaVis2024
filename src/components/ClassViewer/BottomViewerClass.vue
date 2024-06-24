<template>
  <div class="bottom-chart">
    <!-- <p>班级视图BottomViewer test</p> -->
    <div ref="chart" class="bottom-chart"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';
import { mapGetters } from 'vuex';
import EventBus from '@/eventBus'; // 导入事件总线


export default {
  name: 'BottomChart',
  data() {
    return {
      heatmapData: [],
    };
  },
  computed: {
    ...mapGetters(['classId'])
  },
  mounted() {
    this.fetchHeatmapData();
  },
  methods: {
    async fetchHeatmapData() {
      try {
        const response = await axios.get(`http://10.12.44.190:8000/heatmap/?class_id=${this.classId}`);
        const jsondata = JSON.parse(response.data);
        // 在processData中处理后 赋值给heatmapData绘图
        this.processData(jsondata);
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

      const myGroups = Array.from(new Set(this.heatmapData.map(d => d.group)));
      const myVars = Array.from(new Set(this.heatmapData.map(d => d.variable)));

      // Build X scales and axis
      const x = d3.scaleBand()
        .range([0, width])
        .domain(myGroups)
        .padding(0.05);

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
      const myColor = d3.scaleLinear()
        .domain([valueExtent[0], valueExtent[1]])
        .interpolate(d3.interpolateRgb)
        .range(["#e0eaf3", "#306ab4"]);
      // const myColor = d3.scaleSequential()
      //   .interpolator(d3.interpolateBlues) //颜色从浅蓝色到深蓝色
      //   // .interpolator(d3.interpolateRdBu)

      //   .domain([valueExtent[0], valueExtent[1]]); //把颜色反一下，让较深的颜色来代表较大的数据

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
        tooltip.html(`Student_id: ${d.group}<br>Knowledge: ${d.variable}<br>Timeconsume: ${d.value}`)
          .style("left",`${event.pageX + 5}px`)
          .style("top", `${event.pageY - 800}px`);
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
        .on("mouseleave", mouseleave)
        .on("click", (event, d) => {
          // d.group为学生id
          console.log(d.group);
          EventBus.$emit('heatmapStudentIdSelected', d.group); // 发送学生id 主视图响应动画
        })

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
  overflow: visible;
}
</style>