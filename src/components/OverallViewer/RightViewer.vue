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
import * as d3 from "d3";

export default {
  name: "BubblePieChart",
  name: "BubblePieChart",
  data() {
    return {
      chartData: [
        {
          "class": "Class1",
          "values": [
            638204.73,
            773652.1,
            901256.45,
            563472.8,
            677852.5
          ],
          "total": 3554438.58
        },
        {
          "class": "Class2",
          "values": [
            834239.75,
            528526.45,
            790321.8,
            702123.55,
            743201.45
          ],
          "total": 3598413
        },
        {
          "class": "Class3",
          "values": [
            706713.65,
            680840.1,
            852513.1,
            784705.65,
            758358.55
          ],
          "total": 3783131.05
        },
        {
          "class": "Class4",
          "values": [
            794760.85,
            810682.75,
            1115504.4,
            864321.8,
            1046147.4
          ],
          "total": 4631417.2
        },
        {
          "class": "Class5",
          "values": [
            662596.75,
            681682.75,
            857757.85,
            717995.5,
            806509.45
          ],
          "total": 3726542.3
        },
        {
          "class": "Class6",
          "values": [
            743987.1,
            719003.35,
            983205.7,
            929722.4,
            1062684.3
          ],
          "total": 4438602.85
        },
        {
          "class": "Class7",
          "values": [
            638204.73,
            773652.1,
            901256.45,
            563472.8,
            677852.5
          ],
          "total": 3554438.58
        },
        {
          "class": "Class8",
          "values": [
            638204.73,
            773652.1,
            901256.45,
            563472.8,
            677852.5
          ],
          "total": 3554438.58
        },
        {
          "class": "Class9",
          "values": [
            638204.73,
            773652.1,
            901256.45,
            563472.8,
            677852.5
          ],
          "total": 3554438.58
        },
        {
          "class": "Class10",
          "values": [
            638204.73,
            773652.1,
            901256.45,
            563472.8,
            677852.5
          ],
          "total": 3554438.58
        },
        {
          "class": "Class11",
          "values": [
            638204.73,
            773652.1,
            901256.45,
            563472.8,
            677852.5
          ],
          "total": 3554438.58
        },
        {
          "class": "Class12",
          "values": [
            638204.73,
            773652.1,
            901256.45,
            563472.8,
            677852.5
          ],
          "total": 3554438.58
        },
        {
          "class": "Class13",
          "values": [
            638204.73,
            773652.1,
            901256.45,
            563472.8,
            677852.5
          ],
          "total": 3554438.58
        },
        {
          "class": "Class14",
          "values": [
            638204.73,
            773652.1,
            901256.45,
            563472.8,
            677852.5
          ],
          "total": 3554438.58
        },
        {
          "class": "Class15",
          "values": [
            638204.73,
            773652.1,
            901256.45,
            563472.8,
            677852.5
          ],
          "total": 3554438.58
        }
      ],
      territoryGroups: {
        Group1: ["Far West", "Great Lakes", "Mideast", "Plains", "Southwest"],
        Group2: ["Northeast", "Southeast", "Central", "Mountain", "Pacific"]
      },
      selectedTerritoryGroup: "Group1",
      classes: ["Class1", "Class2", "Class3", "Class4", "Class5", "Class6", "Class7", "Class8", "Class9", "Class10", "Class11", "Class12", "Class13", "Class14", "Class15"],
      width: 700,
      height: 650,
      margin: { left: 40, bottom: 50, top: 60, right: 20 },
      color: d3.scaleOrdinal(d3.schemeTableau10).domain(["Class1", "Class2", "Class3", "Class4", "Class5", "Class6", "Class7", "Class8", "Class9", "Class10", "Class11", "Class12", "Class13", "Class14", "Class15"]),
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
        d => d3.line()([[x(d) + hx, margin.top], [x(d) + hx, height - margin.bottom]]))
      );

      svg.append("g").call(g => drawGuidelines(g, y.ticks().reverse().slice(1),
        d => d3.line()([[margin.left, y(d)], [width - margin.left - margin.right, y(d)]]))
      );

      const g = svg.selectAll(".pie")
        .data(chartData)
        .join("g")
        .attr("class", "pie")
        .attr("transform", d => `translate(${x(d.class) + hx},${y(d.total)})`)
        .call(g => g.append("text")
          .attr("dy", "1em")
          .attr("text-anchor", "middle")
          .attr("transform", d => `translate(0,${r(d.total)})`)
          .text(d => toCurrency(d.total)));

      const pg = g.selectAll("g")
        .data(d => d3.pie()(d.values).map(p => ({ pie: p, total: d.total })))
        .join("g")
        .call(g => g.append("title")
          .text((d, i) => `${territories[i]}\n${toCurrency(d.pie.value)} (${(d.pie.value / d.total * 100).toFixed(1)}%)`));

      const pie = d => d3.arc()
        .innerRadius(0)
        .outerRadius(r(d.total))
        .startAngle(d.pie.startAngle)
        .endAngle(d.pie.endAngle);

      this.slice = pg.append("path")
        .attr("d", d => pie(d)())
        .attr("opacity", 1)
        .attr("fill", (d, i) => color(territories[i]));

      this.pct = pg.append("text")
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
      svg.append("g").call(this.drawLegend);
      return svg.node();
    },

    drawAxis(g, x, y, axis) {
      g.attr("transform", `translate(${x},${y})`)
        .call(axis)
        .selectAll(".tick text")
        .attr("font-size", "9pt");
    },

    drawLegend(g) {
      const { territoryGroups, selectedTerritoryGroup, color, margin, width } = this;
      const territories = territoryGroups[selectedTerritoryGroup];
      this.legend = g.attr("transform", `translate(${margin.left + 20}, ${margin.top - 60})`)
        .selectAll("g")
        .data(territories)
        .join("g")
        .attr("transform", (d, i) => `translate(0,${i * 20})`)
        .call(g => g.append("rect")
          .attr("rx", 3).attr("ry", 3)
          .attr("width", 20).attr("height", 15)
          .attr("fill", d => color(d)))
        .call(g => g.append("text").attr("dx", 25).attr("alignment-baseline", "hanging").text(d => d))
        .on("mouseover", this.highlight)
        .on("mouseout", () => this.highlight());
    },
    highlight(e) {
      const i = e ? this.legend.nodes().indexOf(e.currentTarget) : -1;
      this.slice.transition().duration(500).attr("opacity", (d, j) => i === -1 || j === i ? 1 : 0.3);
      this.pct.transition().duration(500)
        .attr("opacity", function (d, j) {
          if (j === i) {
            this.parentNode.parentNode.appendChild(this.parentNode);
            return 1;
          }
          else return 0;
        });
    },
    updateChart() {
      // 清除之前的画布
      d3.select(this.$refs.chart).selectAll("svg").remove();
      // 重新绘制图表
      this.drawChart();
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

.dropdown-wrapper {
  position: absolute;
  top: 30px;
  right: 40px;
}
</style>
