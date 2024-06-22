<template>
  <div ref="chartContainer1" class="chartContainer-botrig">
    <!-- svg绘制 -->
    <div ref="chartContainer" id="chart-borig"></div>
    <!-- 按钮 -->
    <a-radio-group v-model:value="selectedStack" class="radio-group" @change="onChange">
      <a-radio :value="'stacked'">Stacked</a-radio>
      <a-radio :value="'separated'">Separated</a-radio>
      <a-radio :value="'percentage'">Percentage</a-radio>
    </a-radio-group>
  </div>
</template>

<script>
import * as d3 from 'd3';
import * as aq from 'arquero';

export default {
  name: 'BottomViewer',
  data() {
    return {
      selectedStack: 'stacked', // Initial value for the radio group
      rawData: [
        { "date": "2020-03-01T00:00:00.000", "California": 5, "Florida": 2, "Illinois": 0, "Michigan": 1938, "New Jersey": 3142, "New York": 1, "North Carolina": 3353, "Ohio": 1452, "Pennsylvania": 2397, "Texas": 0 },
        { "date": "2020-03-02T00:00:00.000", "California": 5, "Florida": 0, "Illinois": 1, "Michigan": 1617, "New Jersey": 3289, "New York": 0, "North Carolina": 1776, "Ohio": 1709, "Pennsylvania": 2503, "Texas": 0 },
        { "date": "2020-03-03T00:00:00.000", "California": 7, "Florida": 1, "Illinois": 0, "Michigan": 1789, "New Jersey": 3691, "New York": 1, "North Carolina": 1, "Ohio": 2022, "Pennsylvania": 2637, "Texas": 0 },
        { "date": "2020-03-04T00:00:00.000", "California": 10, "Florida": 0, "Illinois": 0, "Michigan": 1777, "New Jersey": 1, "New York": 9, "North Carolina": 0, "Ohio": 1875, "Pennsylvania": 3007, "Texas": 1 },
        { "date": "2020-03-05T00:00:00.000", "California": 12, "Florida": 1, "Illinois": 1, "Michigan": 1762, "New Jersey": 1, "New York": 11, "North Carolina": 0, "Ohio": 1750, "Pennsylvania": 2768, "Texas": 4 }
        // ... more data here
      ]
    };
  },
  mounted() {
    window.addEventListener('resize', this.drawChart); // Re-draw chart on window resize
    this.drawChart();
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.drawChart);
  },
  methods: {

    createLegend(svg, color, top_10_states, chartContainerWidth, margin) {
      const legend = svg.append("g")
        .attr("transform", `translate(${chartContainerWidth - margin.right}, ${margin.top})`)
        .selectAll("g")
        .data(top_10_states)
        .enter().append("g")
        .attr("transform", (d, i) => `translate(0, ${i * 20})`);

      legend.append("rect")
        .attr("width", 12)
        .attr("height", 12)
        .attr("fill", color);

      legend.append("text")
        .attr("x", 16)
        .attr("y", 6)
        .attr("dy", "0.35em")
        .style("font-size", "10px")
        .text(d => d);
    },

    onChange(e) {
      this.selectedStack = e.target.value;
      this.updateChart();
    },

    drawChart() {
      if (this.svg) {
        this.svg.remove(); // Remove previous chart if it exists
      }

      const rawData = this.rawData;
      const top_10_states = Object.keys(rawData[0]).filter(key => key !== 'date');

      const margin = { top: 10, right: 150, bottom: 20, left: 45 }; // Increase right margin to accommodate legend
      const chartContainerWidth = this.$refs.chartContainer.clientWidth;
      const chartContainerHeight = this.$refs.chartContainer.clientHeight;
      const width = chartContainerWidth - margin.left - margin.right;
      const height = chartContainerHeight - margin.top - margin.bottom;

      const svg = d3.select(this.$refs.chartContainer)
        .append("svg")
        .attr("viewBox", `0 0 ${chartContainerWidth} ${chartContainerHeight}`)
        .attr("preserveAspectRatio", "xMidYMid meet")
        .style("font-family", "sans-serif")
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      this.svg = svg;

      const xAxis = svg.append("g")
        .attr("transform", `translate(0,${height})`);

      const yAxis = svg.append("g");

      const color = d3.scaleOrdinal()
        .domain(top_10_states)
        .range(d3.schemeTableau10)
        .unknown("#ccc");

      this.createLegend(svg, color, top_10_states, chartContainerWidth, margin); // Call createLegend here

      const axisLabel = svg.append("g")
        .attr("transform", `translate(15, ${height / 2})rotate(-90)`)
        .append('text')
        .style("font-size", "12px")
        .style("text-anchor", "middle");

      const cases_per_day = rawData.map(d => {
        const date = new Date(d.date);
        return { ...d, date };
      });

      const by_date = aq
        .from(cases_per_day)
        .groupby('date')
        .pivot("state", "new_cases")
        .objects();

      this.data = { by_date, color, top_10_states, xAxis, yAxis, axisLabel, margin, width, height };
      this.updateChart();
    },

    updateChart() {
      const { by_date, color, top_10_states, xAxis, yAxis, axisLabel, margin, width, height } = this.data;
      const svg = this.svg;

      const stacks = {
        separated: offset,
        stacked: d3.stackOffsetNone,
        percentage: d3.stackOffsetExpand
      };

      const data_series = d3
        .stack()
        .offset(stacks[this.selectedStack])
        .keys(top_10_states)(by_date)
        .map(d => {
          return d.forEach(v => (v.key = d.key)), d;
        });

      const x = d3
        .scaleBand()
        .domain(by_date.map(d => d.date))
        .range([0, width])
        .padding(0.1);

      const y = d3
        .scaleLinear()
        .domain([0, d3.max(data_series, d => d3.max(d, d => d[1]))])
        .rangeRound([height, 0]);

      svg.selectAll("g.series")
        .data(data_series)
        .join(
          enter => enter.append("g")
            .attr("class", "series"),
          update => update,
          exit => exit.remove()
        )
        .attr("fill", d => color(d.key))
        .selectAll("rect")
        .data(d => d)
        .join(
          enter => enter.append("rect"),
          update => update,
          exit => exit.remove()
        )
        .transition()
        .duration(1000)
        .delay((d, i) => x(d.data.date))
        .attr("x", d => x(d.data.date))
        .attr("y", d => y(d[1]))
        .attr("height", d => y(d[0]) - y(d[1]))
        .attr("width", x.bandwidth());

      xAxis
        .call(
          d3.axisBottom(x)
            .tickSizeOuter(0)
            .tickFormat(d => d.toLocaleString('default', { month: 'long' }))
            .tickValues(
              x.domain().filter(d =>
                width > 760
                  ? d.getDate() === 1
                  : d.getDate() === 1 && (d.getMonth() + 1) % 3 === 0
              )
            )
        )
        .call(g => g.selectAll(".domain").remove());

      yAxis
        .call(d3.axisLeft(y).ticks(null, "s"))
        .call(g => g.selectAll(".domain").remove());

      axisLabel.text(
        this.selectedStack === "percentage" ? "Proportion of Cases" : "Cases per Day"
      );
    }
  }
};

function offset(series, order) {
  if (!((n = series.length) > 1)) return;
  for (var i = 1, s0, s1 = series[order[0]], n, m = s1.length; i < n; ++i) {
    (s0 = s1), (s1 = series[order[i]]);
    let base = d3.max(s0, d => d[1]);
    for (var j = 0; j < m; ++j) {
      let diff = s1[j][1] - s1[j][0];
      s1[j][0] = base;
      s1[j][1] = base + diff;
    }
  }
}
</script>

<style scoped>

.chartContainer-botrig {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}
.radio-group {
  width: 100%;
  height: 10%;
  display: flex;
  justify-content: center;
  align-items: center;
  order: 1; /* Ensure the radio buttons appear at the bottom */
}
#chart-borig {
  width: 100%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  order: 0;
  margin: 0 auto; /* Ensure the chart is centered */
}

</style>
