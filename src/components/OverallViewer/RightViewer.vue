<template>
  <div ref="chart"></div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "BubblePieChart",
  data() {
    return {
      chartData: [
        { year: "2015", Far_West: 638204.73, Great_Lakes: 773652.1, Mideast: 901256.45, Plains: 563472.8, Southwest: 677852.5 },
        { year: "2016", Far_West: 834239.75, Great_Lakes: 528526.45, Mideast: 790321.8, Plains: 702123.55, Southwest: 743201.45 },
        { year: "2017", Far_West: 706713.65, Great_Lakes: 680840.1, Mideast: 852513.1, Plains: 784705.65, Southwest: 758358.55 },
        { year: "2018", Far_West: 794760.85, Great_Lakes: 810682.75, Mideast: 1115504.4, Plains: 864321.8, Southwest: 1046147.4 },
        { year: "2019", Far_West: 662596.75, Great_Lakes: 681682.75, Mideast: 857757.85, Plains: 717995.5, Southwest: 806509.45 },
        { year: "2020", Far_West: 743987.1, Great_Lakes: 719003.35, Mideast: 983205.7, Plains: 929722.4, Southwest: 1062684.3 },
      ],
      territories: ["Far West", "Great Lakes", "Mideast", "Plains", "Southwest"],
      width: 700,
      height: 650,
      // 多出来的margin 放legend
      margin: { left: 40, bottom: 50, top: 60, right: 20 },
      color: d3.scaleOrdinal(d3.schemeTableau10).domain(["Far West", "Great Lakes", "Mideast", "Plains", "Southwest"])
    };
  },
  mounted() {
    this.drawChart();
  },
  methods: {
    drawChart() {
      const { chartData, territories, width, height, margin, color } = this;

      console.log("Chart Data:", chartData);
      console.log("Territories:", territories);

      const svg = d3.select(this.$refs.chart)
        .append("svg")
        .attr("font-size", "10pt")
        .attr("cursor", "default")
        .attr("viewBox", [0, 0, width, height])
        .attr("width", width)  
        .attr("height", height);   


      console.log("SVG element created:", svg.node());

      const x = d3.scaleBand()
        .domain(chartData.map(d => d.year))
        .range([margin.left, width - margin.left - margin.right]);
      const hx = x.bandwidth() / 2;

      const y = d3.scaleLinear()
        .domain(d3.extent(chartData.flatMap(d => territories.map(t => d[t]))))
        .range([height - margin.top - margin.bottom, margin.top]);

      const r = d3.scaleLinear()
        .domain(d3.extent(chartData.flatMap(d => territories.map(t => d[t]))))
        .range([hx / 2, hx]);

      const drawGuidelines = (g, data, line) => {
        g.selectAll("path")
          .data(data)
          .join("path")
          .attr("stroke", "#ddd")
          .attr("stroke-dasharray", "5,5")
          .attr("d", line);
      };

      svg.append("g").call(g => drawGuidelines(g, chartData.map(d => d.year),
        d => d3.line()([[x(d) + hx, margin.top], [x(d) + hx, height - margin.bottom]])
      ));

      svg.append("g").call(g => drawGuidelines(g, y.ticks().reverse().slice(1),
        d => d3.line()([[margin.left, y(d)], [width - margin.left - margin.right, y(d)]])
      ));

      const g = svg.selectAll(".pie")
        .data(chartData)
        .join("g")
        .attr("class", "pie")
        .attr("transform", d => `translate(${x(d.year) + hx},${y(d3.sum(territories.map(t => d[t])))})`)
        .call(g => g.append("text")
          .attr("dy", "1em")
          .attr("text-anchor", "middle")
          .attr("transform", d => `translate(0,${r(d3.sum(territories.map(t => d[t])))})`)
          .text(d => this.toCurrency(d3.sum(territories.map(t => d[t]))))
        );

      const pg = g.selectAll("g")
        .data(d => d3.pie().value(d => d.value)(territories.map(t => ({ key: t, value: d[t] }))).map(p => ({ pie: p, total: d3.sum(territories.map(t => d[t])) })))
        .join("g")
        .call(g => g.append("title")
          .text((d, i) => `${territories[i]}\n${this.toCurrency(d.pie.value)} (${(d.pie.value / d.total * 100).toFixed(1)}%)`)
        );

      const pie = d => d3.arc()
        .innerRadius(0)
        .outerRadius(r(d.total))
        .startAngle(d.pie.startAngle)
        .endAngle(d.pie.endAngle);

      const slice = pg.append("path")
        .attr("d", d => pie(d)())
        .attr("opacity", 1)
        .attr("fill", (d, i) => color(territories[i]));

      const pct = pg.append("text")
        .attr("text-anchor", "middle")
        .attr("fill", "white")
        .attr("transform", (d, i) => {
          const c = pie(d).centroid(d.pie.value);
          return `translate(${c[0]},${c[1]})`;
        })
        .attr("opacity", "0")
        .text(d => (d.pie.value / d.total * 100).toFixed(1) + "%");

      svg.append("g").call(g => this.drawAxis(g, margin.left, 0, d3.axisLeft(y).ticks(height / 100, "s")));
      svg.append("g").call(g => this.drawAxis(g, 0, height - margin.bottom, d3.axisBottom(x)));
      // 先不去绘制legend
      svg.append("g").call(this.drawLegend);

      console.log("Chart drawn successfully.");

      return svg.node();
    },

    drawAxis(g, x, y, axis) {
      g.attr("transform", `translate(${x},${y})`)
        .call(axis)
        .selectAll(".tick text")
        .attr("font-size", "9pt");
    },

    drawLegend(g) {
      const { territories, color, margin, width } = this;
      const legend = g.attr("transform", `translate(${margin.left}, ${margin.top})`)
        .selectAll("g")
        .data(territories)
        .join("g")
        .attr("transform", (d, i) => `translate(${i * 120}, 0)`)  // 每个图例项水平排列
        .call(g => g.append("rect")
          .attr("rx", 3).attr("ry", 3)
          .attr("width", 20).attr("height", 15)
          .attr("fill", d => color(d)))
        .call(g => g.append("text").attr("dx", 25).attr("alignment-baseline", "hanging").text(d => d))
        .on("mouseover", this.highlight)
        .on("mouseout", () => this.highlight());
    },
    highlight(e) {
      const { color } = this;
      const legend = d3.selectAll("g");
      const i = e ? legend.nodes().indexOf(e.currentTarget) : -1;
      d3.selectAll("path").transition().duration(500).attr("opacity", (d, j) => i === -1 || j === i ? 1 : 0.3);
      d3.selectAll("text").transition().duration(500)
        .attr("opacity", function (d, j) {
          if (j === i) {
            this.parentNode.parentNode.appendChild(this.parentNode);
            return 1;
          }
          else return 0;
        });
    },
    toCurrency(num) {
      return d3.format("$,.2f")(num);
    }
  }
};
</script>

<style scoped>
svg {
  font-family: sans-serif;
}
</style>
