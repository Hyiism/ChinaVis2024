<template>
  <div ref="chart">
    <div class="dropdown-wrapper">
      <a-dropdown class="dropdown">
        <a class="ant-dropdown-link" @click="e => e.preventDefault()">
          Select Territory Group <a-icon type="down" />
        </a>
        <a-menu slot="overlay" @click="handleMenuClick">
          <a-menu-item key="Group1">Group 1</a-menu-item>
          <a-menu-item key="Group2">Group 2</a-menu-item>
        </a-menu>
      </a-dropdown>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "BubblePieChart",
  data() {
    return {
      chartData: [
        {
          "class": "Class1",
          "values": [638204.73, 773652.1, 901256.45, 563472.8, 677852.5],
          "total": 3554438.58
        },
        {
          "class": "Class2",
          "values": [834239.75, 528526.45, 790321.8, 702123.55, 743201.45],
          "total": 3598413
        },
        {
          "class": "Class3",
          "values": [706713.65, 680840.1, 852513.1, 784705.65, 758358.55],
          "total": 3783131.05
        },
        {
          "class": "Class4",
          "values": [794760.85, 810682.75, 1115504.4, 864321.8, 1046147.4],
          "total": 4631417.2
        },
        {
          "class": "Class5",
          "values": [662596.75, 681682.75, 857757.85, 717995.5, 806509.45],
          "total": 3726542.3
        },
        {
          "class": "Class6",
          "values": [743987.1, 719003.35, 983205.7, 929722.4, 1062684.3],
          "total": 4438602.85
        },
        {
          "class": "Class7",
          "values": [638204.73, 773652.1, 901256.45, 563472.8, 677852.5],
          "total": 3554438.58
        },
        {
          "class": "Class8",
          "values": [638204.73, 773652.1, 901256.45, 563472.8, 677852.5],
          "total": 3554438.58
        },
        {
          "class": "Class9",
          "values": [638204.73, 773652.1, 901256.45, 563472.8, 677852.5],
          "total": 3554438.58
        },
        {
          "class": "Class10",
          "values": [638204.73, 773652.1, 901256.45, 563472.8, 677852.5],
          "total": 3554438.58
        },
        {
          "class": "Class11",
          "values": [638204.73, 773652.1, 901256.45, 563472.8, 677852.5],
          "total": 3554438.58
        },
        {
          "class": "Class12",
          "values": [638204.73, 773652.1, 901256.45, 563472.8, 677852.5],
          "total": 3554438.58
        },
        {
          "class": "Class13",
          "values": [638204.73, 773652.1, 901256.45, 563472.8, 677852.5],
          "total": 3554438.58
        },
        {
          "class": "Class14",
          "values": [638204.73, 773652.1, 901256.45, 563472.8, 677852.5],
          "total": 3554438.58
        },
        {
          "class": "Class15",
          "values": [638204.73, 773652.1, 901256.45, 563472.8, 677852.5],
          "total": 3554438.58
        }
      ],
      territoryGroups: {
        Group1: ["Far West", "Great Lakes", "Mideast", "Plains", "Southwest"],
        Group2: ["Northeast", "Southeast", "Central", "Mountain", "Pacific"]
      },
      selectedTerritoryGroup: "Group1",
      classes: [
        "Class1", "Class2", "Class3", "Class4", "Class5", "Class6",
        "Class7", "Class8", "Class9", "Class10", "Class11", "Class12",
        "Class13", "Class14", "Class15"
      ],
      width: 700,
      height: 650,
      margin: { left: 40, bottom: 50, top: 60, right: 20 },
      color: d3.scaleOrdinal(d3.schemeTableau10).domain([
        "Class1", "Class2", "Class3", "Class4", "Class5", "Class6",
        "Class7", "Class8", "Class9", "Class10", "Class11", "Class12",
        "Class13", "Class14", "Class15"
      ]),
      legend: null,
      slice: null,
      pct: null
    };
  },
  mounted() {
    this.drawChart();
  },
  methods: {
    handleMenuClick({ key }) {
      this.selectedTerritoryGroup = key;
      this.updateChart();
    },
    drawChart() {
      const { chartData, territoryGroups, selectedTerritoryGroup, classes, width, height, margin, color } = this;
      const territories = territoryGroups[selectedTerritoryGroup];
      const svg = d3.select(this.$refs.chart)
        .append("svg")
        .attr("font-size", "10pt")
        .attr("cursor", "default")
        .attr("viewBox", [0, 0, width, height])
        .attr("width", width)
        .attr("height", height);

      const x = d3.scaleBand()
        .domain(classes)
        .range([margin.left, width - margin.left - margin.right]);

      const hx = x.bandwidth() / 2;

      const y = d3.scaleLinear()
        .domain(d3.extent(chartData.map(d => d.total)))
        .range([height - margin.top - margin.bottom, margin.top]);

      const r = d3.scaleLinear()
        .domain(d3.extent(chartData.map(d => d.total)))
        .range([hx / 2, hx]);

      const toCurrency = num => d3.format("$,.2f")(num);

      const drawGuidelines = (g, data, line) => {
        g.selectAll("path")
          .data(data)
          .join("path")
          .attr("stroke", "#ddd")
          .attr("stroke-dasharray", "5,5")
          .attr("d", line);
      };

      svg.append("g").call(g => drawGuidelines(g, classes,
        d => d3.line()([[x(d) + hx, margin.top], [x(d) + hx, height - margin.bottom]])
      ));

      svg.append("g").call(g => drawGuidelines(g, y.ticks().reverse().slice(1),
        d => d3.line()([[margin.left, y(d)], [width - margin.left - margin.right, y(d)]])
      ));

      const g = svg.selectAll(".pie")
        .data(chartData)
        .join("g")
        .attr("class", "pie")
        .attr("transform", d => `translate(${x(d.class) + hx},${y(d.total)})`)
        .call(g => g.append("text")
          .attr("dy", "1em")
          .attr("text-anchor", "middle")
          .attr("transform", d => `translate(0,${r(d.total)})`)
          .text(d => toCurrency(d.total))
        );

      const pg = g.selectAll("g")
        .data(d => d3.pie()(d.values).map(p => ({ pie: p, total: d.total })))
        .join("g")
        .call(g => g.append("title")
          .text((d, i) => `${territories[i]}\n${toCurrency(d.pie.value)} (${(d.pie.value / d.total * 100).toFixed(1)}%)`)
        );

      const pie = d => d3.arc()
        .innerRadius(0)
        .outerRadius(r(d.total))
        .startAngle(d.pie.startAngle)
        .endAngle(d.pie.endAngle);

      this.slice = pg.append("path")
        .attr("d", d => pie(d)())
        .attr("opacity", 0.8)
        .attr("fill", (d, i) => color(territories[i]));

      const legend = svg.append("g")
        .attr("transform", `translate(0,${height - margin.bottom})`);

      this.legend = legend.selectAll("g")
        .data(territories)
        .join("g")
        .attr("transform", (d, i) => `translate(${x(classes[i]) + hx},0)`);

      this.legend.append("rect")
        .attr("width", hx)
        .attr("height", 20)
        .attr("fill", (d, i) => color(d));

      this.legend.append("text")
        .attr("dy", "1em")
        .attr("dx", hx / 2)
        .attr("text-anchor", "middle")
        .attr("fill", "#fff")
        .text(d => d);
    },
    updateChart() {
      const { territoryGroups, selectedTerritoryGroup, chartData, color } = this;
      const territories = territoryGroups[selectedTerritoryGroup];

      this.legend.data(territories)
        .select("rect")
        .attr("fill", (d, i) => color(d));

      this.legend.data(territories)
        .select("text")
        .text(d => d);

      this.slice.data(d => d3.pie()(d.values).map(p => ({ pie: p, total: d.total })))
        .attr("fill", (d, i) => color(territories[i]));
    }
  }
};
</script>

<style scoped>
.pie text {
  font: 10px sans-serif;
}
.ant-dropdown-link {
  cursor: pointer;
  color: #1890ff;
  user-select: none;
}
.dropdown-wrapper {
  margin-bottom: 20px;
}
</style>
