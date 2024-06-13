<template>
  <!-- 变换图 展示总体知识点和题目情况 -->
  <div>
    <!-- <p>班级视图BottomLeft test</p> -->
    <div ref="chart" class="chart-container"></div>
    <!-- <p>班级视图BottomLeft test</p> -->
    <div ref="chart" class="chart-container"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';

export default {
  name: 'StackedLineChart',
  data() {
    return {
      // data: [
      //   { date: new Date(2020, 0, 1), industry: 'A', unemployed: 100 },
      //   { date: new Date(2020, 0, 1), industry: 'B', unemployed: 200 },
      //   { date: new Date(2020, 0, 1), industry: 'C', unemployed: 300 },
      //   { date: new Date(2020, 1, 1), industry: 'A', unemployed: 150 },
      //   { date: new Date(2020, 1, 1), industry: 'B', unemployed: 250 },
      //   { date: new Date(2020, 1, 1), industry: 'C', unemployed: 350 },
      //   { date: new Date(2020, 2, 1), industry: 'A', unemployed: 200 },
      //   { date: new Date(2020, 2, 1), industry: 'B', unemployed: 100 },
      //   { date: new Date(2020, 2, 1), industry: 'C', unemployed: 250 },
      //   { date: new Date(2020, 3, 1), industry: 'A', unemployed: 50 },
      //   { date: new Date(2020, 3, 1), industry: 'B', unemployed: 350 },
      //   { date: new Date(2020, 3, 1), industry: 'C', unemployed: 450 },
      //   { date: new Date(2020, 4, 1), industry: 'A', unemployed: 300 },
      //   { date: new Date(2020, 4, 1), industry: 'B', unemployed: 400 },
      //   { date: new Date(2020, 4, 1), industry: 'C', unemployed: 540 },
      //   { date: new Date(2020, 5, 1), industry: 'A', unemployed: 300 },
      //   { date: new Date(2020, 5, 1), industry: 'B', unemployed: 450 },
      //   { date: new Date(2020, 5, 1), industry: 'C', unemployed: 100 },
      //   { date: new Date(2020, 6, 1), industry: 'A', unemployed: 400 },
      //   { date: new Date(2020, 6, 1), industry: 'B', unemployed: 50 },
      //   { date: new Date(2020, 6, 1), industry: 'C', unemployed: 80 },
      //   { date: new Date(2020, 7, 1), industry: 'A', unemployed: 450 },
      //   { date: new Date(2020, 7, 1), industry: 'B', unemployed: 120 },
      //   { date: new Date(2020, 7, 1), industry: 'C', unemployed: 650 },
      //   { date: new Date(2020, 8, 1), industry: 'A', unemployed: 500 },
      //   { date: new Date(2020, 8, 1), industry: 'B', unemployed: 200 },
      //   { date: new Date(2020, 8, 1), industry: 'C', unemployed: 700 },
      //   { date: new Date(2020, 9, 1), industry: 'A', unemployed: 50 },
      //   { date: new Date(2020, 9, 1), industry: 'B', unemployed: 650 },
      //   { date: new Date(2020, 9, 1), industry: 'C', unemployed: 750 },
      //   { date: new Date(2020, 10, 1), industry: 'A', unemployed: 500 },
      //   { date: new Date(2020, 10, 1), industry: 'B', unemployed: 700 },
      //   { date: new Date(2020, 10, 1), industry: 'C', unemployed: 800 },
      //   { date: new Date(2020, 11, 1), industry: 'A', unemployed: 320 },
      //   { date: new Date(2020, 11, 1), industry: 'B', unemployed: 750 },
      //   { date: new Date(2020, 11, 1), industry: 'C', unemployed: 200 },
      // ]
      data: []
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://localhost:5000/get_student_scores_data');
        const data = response.data;
        this.processData(data);
        this.createChart();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    processData(data) {
      const formattedData = [];
      data.forEach(row => {
        // 遍历 row 的所有属性
        Object.keys(row).forEach(key => {
            // 检查属性名是否匹配 dateYYYYMMDD 的模式
            const match = key.match(/^date(\d{4})(\d{2})(\d{2})$/);
            if (match) {
                // 提取年份、月份和日期
                const year = parseInt(match[1], 10);
                const month = parseInt(match[2], 10) - 1; // JavaScript 中的月份是从 0 开始的
                const day = parseInt(match[3], 10);
                // 将数据添加到 formattedData 中
                formattedData.push({ 
                    industry: row.knowledge_id, 
                    date: new Date(year, month, day), 
                    unemployed: row[key] 
                });
            }
        });
        // formattedData.push({ industry: row.student_id, date: new Date(2024, 6, 1), unemployed: row.date20240601 });
        // formattedData.push({ industry: row.student_id, date: new Date(2024, 6, 2), unemployed: row.date20240602 });
      });
      this.data = formattedData;
    },
    createChart() {
      const data = this.data;

      const width = 928;
      const height = 550;
      const marginTop = 50;
      const marginRight = 10;
      const marginBottom = 50;
      const marginLeft = 50;

      const series = d3.stack()
        .keys(d3.union(data.map(d => d.industry)))
        .value(([, D], key) => D.get(key)?.unemployed || 0)
        (d3.index(data, d => d.date, d => d.industry));

      const x = d3.scaleUtc()
        .domain(d3.extent(data, d => d.date))
        .range([marginLeft, width - marginRight]);

      const y = d3.scaleLinear()
        .domain([0, d3.max(series, d => d3.max(d, d => d[1]))])
        .rangeRound([height - marginBottom, marginTop]);

      const color = d3.scaleOrdinal()
        .domain(series.map(d => d.key))
        .range(d3.schemeTableau10);

      const area = d3.area()
        .x(d => x(d.data[0]))
        .y0(d => y(d[0]))
        .y1(d => y(d[1]));

      const svg = d3.select(this.$refs.chart)
        .append("svg")
        .attr("id", "stacked-line-chart")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .attr("style", "max-width: 100%; height: 100%;");

      svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y).ticks(height / 80))
        .call(g => g.select(".domain").remove())
        .call(g => g.selectAll(".tick line").clone()
          .attr("x2", width - marginLeft - marginRight)
          .attr("stroke-opacity", 0.1))
          .style("font-size", "20px")
        // .call(g => g.append("text")
        //   .attr("x", -marginLeft)
        //   .attr("y", 10)
        //   .attr("fill", "currentColor")
        //   .attr("text-anchor", "start")
        //   .text("↑ Unemployed persons"));

        const xAxis = d3.axisBottom(x).tickSizeOuter(0).tickFormat(d3.timeFormat("%Y.%m.%d"));
        svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .style("font-size", "16px")
        .call(xAxis)
        .call(g => g.select(".domain").remove())
        .call(g => g.selectAll(".tick line").clone()
          .attr("y2", -height + marginTop + marginBottom)
          .attr("stroke-opacity", 0.1))
        .call(g => g.selectAll(".tick text")
          .style("font-size", "20px"));

        const paths = svg.append("g")
        .selectAll("path")
        .data(series)
        .join("path")
        .attr("fill", d => color(d.key))
        .attr("d", area)
        .attr("class", "area");

      // 添加工具提示框
      const tooltip = svg.append("g")
        .attr("id", "tooltip")
        .style("display", "none");

      tooltip.append("rect")
        .attr("width", 150)
        .attr("height", 40)
        .attr("fill", "white")
        .attr("stroke", "black");

      tooltip.append("text")
        .attr("x", 80)
        .attr("y", 20)
        .attr("dy", ".35em")
        .attr("text-anchor", "middle");

      // 添加交互效果
      paths
        .on("mouseover", function(event, d) {
          d3.selectAll(".area").style("opacity", 0.1);
          d3.select(this).style("opacity", 1);
          tooltip.style("display", null);
        })
        .on("mousemove", function(event, d) {
          const [mouseX, mouseY] = d3.pointer(event, svg.node());
          tooltip.attr("transform", `translate(${mouseX + 10},${mouseY + 20})`);
          tooltip.select("text").text(d.key);
        })
        .on("mouseout", function() {
          d3.selectAll(".area").style("opacity", 1);
          tooltip.style("display", "none");
        });

      // 添加图例
      const legend = svg.append("g")
        .attr("transform", `translate(${marginRight + 70},${marginTop})`)
        .attr("class", "legend");

      // 设置每行显示的图例项数量
      const itemsPerRow = 5;

      // 计算图例项的宽度和高度
      const legendItemWidth = 150;
      const legendItemHeight = 30;
      
      const legendItems = legend.selectAll(".legend-item")
        .data(series)
        .enter()
        .append("g")
        .attr("class", "legend-item")
        // .attr("transform", (d, i) => `translate(0,${i * 20})`);
        .attr("transform", (d, i) => {
          const x = (i % itemsPerRow) * legendItemWidth;
          const y = Math.floor(i / itemsPerRow) * legendItemHeight;
          return `translate(${x},${y})`;
        });

      legendItems.append("rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", 24)
        .attr("height", 24)
        .attr("fill", d => color(d.key));

      legendItems.append("text")
        .attr("x", 30)
        .attr("y", 12)
        .attr("dy", ".35em")
        .text(d => d.key);
    }
  }
};
</script>

<style>
.chart-container {
  width: 100%;
  height: 100%;
}
<style>
.chart-container {
  width: 100%;
  height: 100%;
}
</style>
