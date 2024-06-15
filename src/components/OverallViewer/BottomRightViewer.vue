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
import EventBus from '@/eventBus'; // 导入事件总线

export default {
  name: 'BottomViewer',
  data() {
    return {
      selectedStack: 'stacked', // Initial value for the radio group
      //   rawData: [
      //   { "student_ID": "2020-03-01T00:00:00.000", "b3C9s_score": 5, "g7R2j_score": 2, "k4W1c_score": 0, "m3D1v_score": 19, "r8S3g_score": 31, "s8Y2f_score": 1, "t5V9e_score": 33, "y9W5d_score": 14 },
      //   { "student_ID": "2020-03-02T00:00:00.000", "b3C9s_score": 5, "g7R2j_score": 0, "k4W1c_score": 1, "m3D1v_score": 16, "r8S3g_score": 32, "s8Y2f_score": 0, "t5V9e_score": 18, "y9W5d_score": 17 },
      //   { "student_ID": "2020-03-03T00:00:00.000", "b3C9s_score": 7, "g7R2j_score": 1, "k4W1c_score": 0, "m3D1v_score": 17, "r8S3g_score": 36, "s8Y2f_score": 1, "t5V9e_score": 0, "y9W5d_score": 20},
      //   { "student_ID": "2020-03-04T00:00:00.000", "b3C9s_score": 10, "g7R2j_score": 0, "k4W1c_score": 0, "m3D1v_score": 17, "r8S3g_score": 0, "s8Y2f_score": 9, "t5V9e_score": 0, "y9W5d_score": 18 },
      //   { "student_ID": "2020-03-05T00:00:00.000", "b3C9s_score": 12, "g7R2j_score": 1, "k4W1c_score": 1, "m3D1v_score": 17, "r8S3g_score": 0, "s8Y2f_score": 11, "t5V9e_score": 0, "y9W5d_score": 17 },
      // ],
      rawData: [],
      top_10_states: ["b3C9s_score", "g7R2j_score", "k4W1c_score", "m3D1v_score", "r8S3g_score", "s8Y2f_score", "t5V9e_score", "y9W5d_score"]

    };
  },
  mounted() {

    window.addEventListener('resize', this.drawChart); // Re-draw chart on window resize
    this.fetchStudentScores();
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.drawChart);
  },
  methods: {

    fetchStudentScores() {
      this.$axios.get('http://10.12.44.190:8000/get_stack_data')
        .then(response => {
          this.rawData = JSON.parse(response.data).data;
          // console.log("#####this.rawData#######:", this.rawData)
          // 请求数据完成后 画图
          this.drawChart();
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
    },

    createLegend(svg, color, top_10_states, chartContainerWidth, margin) {
      const legend = svg.append("g")
        .attr("transform", `translate(${chartContainerWidth - margin.right}, ${margin.top})`)
        .selectAll("g")
        .data(top_10_states)
        .enter().append("g")
        .attr("transform", (d, i) => `translate(0, ${i * 20})`)
        .on("click", (event, d) => {
          // 点击知识点legend,将知识点id传到知识点视图
          EventBus.$emit('stackSelected', d); // Emit event
          // console.log("点击知识点legend:", d)
        });;

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

      const margin = { top: 10, right: 150, bottom: 20, left: 50 }; // Increase right margin to accommodate legend
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

      // 不计算而是直接定义数据
      const by_date = this.rawData;
      const top_10_states = this.top_10_states;

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

      this.data = { by_date, color, top_10_states, xAxis, yAxis, axisLabel, margin, width, height };
      // console.log("this.data:", by_date, color, top_10_states, xAxis, yAxis, axisLabel, margin, width, height)

      this.updateChart();
    },

    updateChart() {

      const { by_date, color, top_10_states, xAxis, yAxis, axisLabel, margin, width, height } = this.data;
      // const { by_date, color, top_10_states, xAxis, yAxis, axisLabel, margin, width, height } = this.data;
      // console.log("this.data:", this.data.by_date)
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
        .domain(by_date.map(d => d.student_ID))
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
        .delay((d, i) => x(d.data.student_ID))
        .attr("x", d => x(d.data.student_ID))
        .attr("y", d => y(d[1]))
        .attr("height", d => y(d[0]) - y(d[1]))
        .attr("width", x.bandwidth());

      // xAxis
      //   .call(
      //     d3.axisBottom(x)
      //       .tickSizeOuter(0)
      //       .tickFormat(d => d.toLocaleString('default', { month: 'long' }))
      //       .tickValues(
      //         x.domain().filter(d =>
      //           width > 760
      //             ? d.getDate() === 1
      //             : d.getDate() === 1 && (d.getMonth() + 1) % 3 === 0
      //         )
      //       )
      //   )
      // .call(g => g.selectAll(".domain").remove());
      xAxis
        .call(
          d3.axisBottom(x)
            .tickSizeOuter(0)
            .tickFormat((d, i) => i % 10 === 0 ? d : "") // 每隔10个 student_id 显示一个
            .tickValues(
              x.domain().filter((d, i) => i % 10 === 0) // 选取每隔10个 student_id
            )
        );

      yAxis
        .call(d3.axisLeft(y).ticks(null, "s"))
        .call(g => g.selectAll(".domain").remove());

      // axisLabel.text(
      //   this.selectedStack === "percentage" ? "Proportion of Cases" : "Cases per Day"
      // );
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
  order: 1;
  /* Ensure the radio buttons appear at the bottom */
}

#chart-borig {
  width: 100%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  order: 0;
  margin: 0 auto;
  /* Ensure the chart is centered */
}
</style>
