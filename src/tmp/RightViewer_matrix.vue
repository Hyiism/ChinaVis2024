<template>
  <div id = "scatterplot" ref="scatterplot"></div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "ScatterplotMatrix",
  data() {
    return {
      data: [
        // 有待了解各个属性作用，以及怎么实现元素间联系的目标
        {
          // cluster_label_tsne使用颜色区分属性
          cluster_label_tsne: 0,
          // 下面四个数值属性作为特征
          time_difference_mean: 3,
          time_split_2_percentage: 18.7,
          submit_times_avg: 181,
          total_score: 3750
        },
        {
          cluster_label_tsne: 1,
          time_difference_mean: 35,
          time_split_2_percentage: 17.4,
          submit_times_avg: 186,
          total_score: 3800
        },
        // 可以添加更多的数据对象
      ],
      data: null
    };
  },
  mounted() {
    this.fetchStudentScores();
    // this.createScatterplotMatrix();
  },
  methods: {
    // // 生成随机数据
    // generateData(num) {
    //   const data = [];
    //   for (let i = 0; i < num; i++) {
    //     data.push({
    //       cluster_label_tsne: Math.floor(Math.random() * 4),
    //       time_difference_mean: Math.random() * 50,
    //       time_split_0_percentage: Math.random() * 20,
    //       submit_times_avg: Math.random() * 200 + 100,
    //       total_score: Math.random() * 4000 + 1000
    //     });
    //   }
    //   return data;
    // },
    // 向后端请求top15的详细成绩数据
    fetchStudentScores() {
      this.$axios
        .get('http://10.12.44.190:8000/scatterMatrix/?class_id=all') // 替换为实际的API端点
        .then((response) => {
          this.data = JSON.parse(response.data);
          // 确保在DOM元素完全加载并设置尺寸后再初始化图表
          this.createScatterplotMatrix();
        })
        .catch((error) => {
          console.error('There was an error!', error);
        });
    },    
    createScatterplotMatrix() {
      const data = this.data;

      const width = 928;
      const height = width;
      const padding = 28;
      // const columns = Object.keys(data[0]).filter(key => typeof data[0][key] === "number");
      const columns = ['time_difference_mean', 'time_split_2_percentage', 'submit_times_avg', 'total_score'];
      const size = (width - (columns.length + 1) * padding) / columns.length + padding;

      const x = columns.map(c => d3.scaleLinear()
        .domain(d3.extent(data, d => d[c]))
        .rangeRound([padding / 2, size - padding / 2]));

      const y = x.map(x => x.copy().range([size - padding / 2, padding / 2]));

      // 设置颜色 按照rank_label属性分类
      const color = d3.scaleOrdinal()
        .domain(data.map(d => d.cluster_label_tsne))
        .range(d3.schemeCategory10);

      const axisx = d3.axisBottom()
        .ticks(6)
        .tickSize(size * columns.length);
      const xAxis = g => g.selectAll("g").data(x).join("g")
        .attr("transform", (d, i) => `translate(${i * size},0)`)
        .each(function (d) { return d3.select(this).call(axisx.scale(d)); })
        .call(g => g.select(".domain").remove())
        .call(g => g.selectAll(".tick line").attr("stroke", "#ddd"));

      const axisy = d3.axisLeft()
        .ticks(6)
        .tickSize(-size * columns.length);
      const yAxis = g => g.selectAll("g").data(y).join("g")
        .attr("transform", (d, i) => `translate(0,${i * size})`)
        .each(function (d) { return d3.select(this).call(axisy.scale(d)); })
        .call(g => g.select(".domain").remove())
        .call(g => g.selectAll(".tick line").attr("stroke", "#ddd"));

      const svg = d3.select(this.$refs.scatterplot).append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [-padding, 0, width, height]);

      svg.append("style")
        .text(`circle.hidden { fill: #000; fill-opacity: 1; r: 1px; }`);

      svg.append("g")
        .call(xAxis);

      svg.append("g")
        .call(yAxis);

      const cell = svg.append("g")
        .selectAll("g")
        .data(d3.cross(d3.range(columns.length), d3.range(columns.length)))
        .join("g")
        .attr("transform", ([i, j]) => `translate(${i * size},${j * size})`);

      cell.append("rect")
        .attr("fill", "none")
        .attr("stroke", "#aaa")
        .attr("x", padding / 2 + 0.5)
        .attr("y", padding / 2 + 0.5)
        .attr("width", size - padding)
        .attr("height", size - padding);

      cell.each(function ([i, j]) {
        d3.select(this).selectAll("circle")
          .data(data.filter(d => !isNaN(d[columns[i]]) && !isNaN(d[columns[j]])))
          .join("circle")
          .attr("cx", d => x[i](d[columns[i]]))
          .attr("cy", d => y[j](d[columns[j]]));
      });

      const circle = cell.selectAll("circle")
        .attr("r", 3.5)
        .attr("fill-opacity", 0.7)
        .attr("fill", d => color(d.cluster_label_tsne));

      cell.call(this.brush, circle, svg, { padding, size, x, y, columns, data });

      svg.append("g")
        .style("font", "bold 10px sans-serif")
        .style("pointer-events", "none")
        .selectAll("text")
        .data(columns)
        .join("text")
        .attr("transform", (d, i) => `translate(${i * size},${i * size})`)
        .attr("x", padding)
        .attr("y", padding)
        .attr("dy", ".71em")
        .text(d => d);

      svg.property("value", []);
      return Object.assign(svg.node(), { scales: { color } });
    },
    brush(cell, circle, svg, { padding, size, x, y, columns, data }) {
      const brush = d3.brush()
        .extent([[padding / 2, padding / 2], [size - padding / 2, size - padding / 2]])
        .on("start", brushstarted)
        .on("brush", brushed)
        .on("end", brushended);

      cell.call(brush);

      let brushCell;

      function brushstarted() {
        if (brushCell !== this) {
          d3.select(brushCell).call(brush.move, null);
          brushCell = this;
        }
      }

      function brushed({ selection }, [i, j]) {
        let selected = [];
        if (selection) {
          const [[x0, y0], [x1, y1]] = selection;
          circle.classed("hidden",
            d => x0 > x[i](d[columns[i]])
              || x1 < x[i](d[columns[i]])
              || y0 > y[j](d[columns[j]])
              || y1 < y[j](d[columns[j]]));
          selected = data.filter(
            d => x0 < x[i](d[columns[i]])
              && x1 > x[i](d[columns[i]])
              && y0 < y[j](d[columns[j]])
              && y1 > y[j](d[columns[j]]));
        }
        svg.property("value", selected).dispatch("input");
      }

      function brushended({ selection }) {
        if (selection) return;
        svg.property("value", []).dispatch("input");
        circle.classed("hidden", false);
      }
    }
  }
};
</script>

<style scoped>
#scatterplot {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
