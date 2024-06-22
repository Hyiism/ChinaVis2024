<template>
  <div id="bottom-main">
    <el-select v-model="selectedcolumns" multiple placeholder="请选择" class="custom-select">
      <el-option
        v-for="item in allcolumns"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>

    <div ref="scatterplot" id="scattermatrix"></div>
    <!-- <el-select v-model="selectedcolumns" multiple placeholder="请选择" class="custom-select1">
      <el-option
        v-for="item in allcolumns"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select> -->
  </div>
</template>

<script>
import * as d3 from "d3";
import { mapGetters } from 'vuex';

export default {
  name: "ScatterplotMatrix",
  data() {
    return {
      selectedcolumns: ["submit_times_avg", "time_split_2_percentage"],
      allcolumns: [
        { label: "做题数量", value: "title_counts" },
        { label: "平均间隔时间", value: "time_difference_mean" },
        { label: "上午做题比例", value: "time_split_0_percentage" },
        { label: "下午做题比例", value: "time_split_1_percentage" },
        { label: "晚上做题比例", value: "time_split_2_percentage" },
        { label: "平均提交次数", value: "submit_times_avg" },
        { label: "平均空间复杂度", value: "all_memory_avg" },
        { label: "平均时间复杂度", value: "all_timeconsume_avg" },
        { label: "AE状态占比", value: "state_ae_percentage" },
        { label: "AE状态占比", value: "state_e_percentage" },
        { label: "E状态占比", value: "state_pc_percentage" },
        { label: "AC状态占比", value: "state_ac_percentage" }
      ],
      data: []
    };
  },
    computed: {
    ...mapGetters(['classId'])
  },
  mounted() {
    this.fetchStudentScores();
  },
  methods: {
    fetchStudentScores() {
      console.log("仓库中的班级", this.classId)
      this.$axios.get(`http://10.12.44.190:8000/scatterMatrix/?class_id=${this.classId}`) // Replace with actual API endpoint
        .then((response) => {
          this.data = JSON.parse(response.data);
          this.createScatterplotMatrix();
        })
        .catch((error) => {
          console.error('There was an error!', error);
        });
    },
    createScatterplotMatrix() {
      if (!this.selectedcolumns.length) {
        return;
      }

      const data = this.data;
      const columns = this.selectedcolumns.concat('total_score');

      const clusterColors = {
        0: "#1e466e",
        1: "#72bcd5",
        2: "#Ffd06f",
        3: "#E76254",
      };

      const width = 470;
      const height = width;
      const padding = 28;
      const size = (width - (columns.length + 1) * padding) / columns.length + padding;

      const x = columns.map(c => d3.scaleLinear()
        .domain(d3.extent(data, d => d[c]))
        .rangeRound([padding / 2, size - padding / 2]));

      const y = x.map(x => x.copy().range([size - padding / 2, padding / 2]));

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

      d3.select(this.$refs.scatterplot).selectAll("*").remove(); // Clear previous plot

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
        .attr("fill", d => clusterColors[d.cluster_label_tsne]);

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
  },
  watch: {
    selectedcolumns(newVal) {
      this.createScatterplotMatrix(); // Redraw the plot when selected columns change
    }
  }
};
</script>

<style scoped>
#bottom-main {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.custom-select {
  width: 20%;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 10;
  background-color: white;
}
/* .custom-select1 {
  width: 15%;
  position: absolute;
  top: 0;
  right: 0;
  z-index: 10;
  background-color: white;
} */

#scattermatrix {
  width: 80%;
  height: 100%;
  position: absolute;
  right: 0;
  bottom: 0;
}
</style>
