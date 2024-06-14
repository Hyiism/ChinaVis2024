<template>
  <div id="right-all">
    <div id="scatter-button">
      <button @click="setClusterMethod('pca')" class="cluster-button" :class="{ 'active': clusterMethod === 'pca' }">PCA</button>
      <button @click="setClusterMethod('tsne')" class="cluster-button" :class="{ 'active': clusterMethod === 'tsne' }">T-SNE</button>
      <button @click="setClusterMethod('umap')" class="cluster-button" :class="{ 'active': clusterMethod === 'umap' }">UMAP</button>
    </div>
    <div ref="ProjectionView" id="ProjectionView"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';
import EventBus from '@/eventBus'; // 导入事件总线

export default {
  name: 'ProjectionView',
  data() {
    return {
      // nodes: [],
      nodes:[
        {
          "student_id":"0088dc183f73c83f763e",
          "x":3.05165,
          "y":15.4957,
          "cluster_label":0,
          // 没有使用
          "ring_data":
          {
            "b3C9s_score":0.1255671184572454,
            "g7R2j_score":0.1320208532929779,
            "k4W1c_score":0.12582324426716812,
            "m3D1v_score":0.12834082246696263,
            "r8S3g_score":0.1025220247849365,
            "s8Y2f_score":0.13844086448198067,
            "t5V9e_score":0.11675804797941387,
            "y9W5d_score":0.13052702426931498
          },
          // 学生综合评分，满分4分，第一个圈
          "total_syth_score_avg":2.56,
          // 做题状态占比， 第二个圈
          "score_data":
          {
            "state_ae_percentage":0.18627450980392157,
            "state_e_percentage":0.5294117647058824,
            "state_pc_percentage":0.08823529411764706,
            "state_ac_percentage":0.19607843137254902
          },
          // 最外面柱状图，最大是1（可以计算该时间点所有的平均提交次数）
          "time_data":
          {
            "01:00":0.02,
            "02:00":0.05,
            "03:00":0.09,
            "04:00":0.11,
            "05:00":0.19,
            "06:00":0.23,
            "07:00":0.36,
            "08:00":0.58,
            "09:00":0.75,
            "10:00":0.87,
            "11:00":0.97,
            "12:00":0.82,
            "13:00":0.74,
            "14:00":0.79,
            "15:00":0.96,
            "16:00":0.93,
            "17:00":0.95,
            "18:00":0.77,
            "19:00":0.54,
            "20:00":0.68,
            "21:00":0.35,
            "22:00":0.24,
            "23:00":0.07,
            "24:00":0.04
          }
        }
      ],
      clusterMethod: 'pca',
    };
  },
  mounted() {
    this.drawView();
    window.addEventListener('resize', this.updateView);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.updateView);
  },
  methods: {
    setClusterMethod(method) {
      this.clusterMethod = method;
      this.drawView(); // Update the view with new data
    },
    async getdata() {
      // var _this = this;
      // await axios.get(`http://10.12.44.190:8000/get_projection_data/?class_id=Class2&method=${this.clusterMethod}`)
      //   .then(res => {
      //     console.log("projection data");
      //     _this.nodes = JSON.parse(res.data).nodes;
      //     console.log(_this.nodes, typeof(_this.nodes));
      //   })
      //   .catch(error => {
      //     console.error("There was an error!", error);
      //   });
      console.log("1111")
    },
    async drawView() {
      await this.getdata();

      var svgWidth = this.$refs.ProjectionView.offsetWidth;
      var svgHeight = this.$refs.ProjectionView.offsetHeight;
      var margin = { top: 20, right: 20, bottom: 20, left: 20 };
      var width = svgWidth - margin.left - margin.right;
      var height = svgHeight - margin.top - margin.bottom;

      d3.select('#ProjectionView').selectAll('*').remove(); // Clear previous SVG content

      const svg = d3.select('#ProjectionView').append('svg')
        .attr('width', svgWidth)
        .attr('height', svgHeight)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`)
        .call(
          d3.zoom().scaleExtent([1, 10]).on("zoom", (event) => {
            svg.attr("transform", event.transform);
          })
        );

      var colorScale = d3.scaleOrdinal(d3.schemeCategory10);
      // 创建渐变颜色比例
      const colors = d3.scaleSequential(d3.interpolateMagma);
      
      // var colorScale = d3.scaleOrdinal()
      //   .domain([0, 1, 2, 3])  // Ensure the domain covers all four clusters
      //   .range(d3.schemeCategory10);
      const radius = 6;

      var xScale = d3.scaleLinear()
        .domain(d3.extent(this.nodes, (d) => +d.x)).nice()
        .range([0, width]);

      var yScale = d3.scaleLinear()
        .domain(d3.extent(this.nodes, (d) => +d.y)).nice()
        .range([height, 0]);

      const xAxis = d3.axisBottom(xScale);
      const yAxis = d3.axisLeft(yScale);

      svg.append("g")
        .attr("class", "x axis")
        .attr("transform", `translate(0,${height / 2})`)
        .call(xAxis);

      svg.append("g")
        .attr("class", "y axis")
        .attr("transform", `translate(${width / 2},0)`)
        .call(yAxis);

      const glyphs = svg.selectAll('g.glyph')
        .data(this.nodes)
        .enter().append('g')
        .attr('class', 'glyph');

      glyphs.append('circle')
        .attr('cx', d => xScale(d.x))
        .attr('cy', d => yScale(d.y))
        .attr('r', radius)
        .attr('fill', d => colorScale(d.cluster_label))
        .attr("stroke", "grey")
        .attr("class", "eachnode")
        .on('mouseover', (event, d) => {
          d.showRings = true;
          this.updateRings();
        })
        .on('mouseout', (event, d) => {
          d.showRings = false;
          this.updateRings();
        })
        .on('click', (event, d) => {
          const studentId = d.student_id; // 获取 student_id
          console.log("student_id")
          console.log(studentId);
          EventBus.$emit('studentSelected', studentId); // 触发事件，传递 student_id
        });;

      this.updateRings = () => {
        glyphs.each(function(node) {
          d3.select(this).selectAll('path').remove();
          if (!node.showRings) return;
          const g = d3.select(this);
          const avgScore = node.total_syth_score_avg;    //平均分，分数越高圆弧越长
          const startAngle = 0;
          const endAngle = 2 * Math.PI * (avgScore / 4);     //4是随便取的
          // const padding = 4;
          // const outer_radius = 13;
          const padding = 4;
          const outer_radius = 13;
          const arcGenerator = d3.arc()
            .innerRadius(radius + padding)
            .outerRadius(outer_radius)
            .startAngle(startAngle)
            .endAngle(endAngle);
          g.append("path")
            .attr("d", arcGenerator)
            .attr("fill", d => colorScale(d.cluster_label))
            .attr("stroke", "grey")
            .attr("transform", `translate(${xScale(node.x)},${yScale(node.y)})`);
          
          
          const scoreingData = node.score_data;     //做题正确程度的占比，按顺时针依次是全错、基本错、基本对、全对
          const totalScore = d3.sum(Object.values(scoreingData).map(Number));
          const keyMapping = {
            "state_ae_percentage": 1,
            "state_e_percentage": 2,
            "state_pc_percentage": 3,
            "state_ac_percentage": 4
          };
          const gapAngle = 0.08; // 间隔角度，给每个扇形之间留一条小白缝
          let startAngle02 = 0;
          for (const [key, value] of Object.entries(scoreingData)) {
            const endAngle02 = startAngle02 + (2 * Math.PI * value / totalScore) - gapAngle;
            const padding = 10;
            const outer_radius = 24;
            // const padding = 36;
            // const outer_radius = 48;
            const arcGenerator02 = d3.arc()
              .innerRadius(radius + padding)
              .outerRadius(outer_radius)
              .startAngle(startAngle02)
              .endAngle(endAngle02);
            g.append("path")
              .attr("d", arcGenerator02)
              // .attr("fill", colorScale(key))
              // .attr("fill", colors(value / totalScore*1.5))
              .attr("fill", colors(keyMapping[key]/8))
              .attr("stroke", "grey")
              .attr("transform", `translate(${xScale(node.x)},${yScale(node.y)})`);
            startAngle02 = endAngle02 + gapAngle;
          }

          const timeData = node.time_data;    //每个小时的出勤率或做题量，平分成24个扇形，扇形半径越大，颜色越浅，说明出勤率越高
          const totalTimeSlots = 24
          const arcAngle = (2 * Math.PI) / totalTimeSlots;
          let startAngle03 = 0;
          for (const [key, value03] of Object.entries(timeData)) {
            const endAngle03 = startAngle03 + arcAngle;
            const padding = 21;
            // const padding = 10;
            const outer_radius = radius + padding + value03*33;
            // const outer_radius = radius + padding + value03*24;
            const arcGenerator03 = d3.arc()
              .innerRadius(radius + padding)  //27
              .outerRadius(outer_radius)    //最大60
              .startAngle(startAngle03)
              .endAngle(endAngle03);
            g.append("path")
              .attr("d", arcGenerator03)
              // .attr("fill", colorScale(key))
              .attr("fill", colors(value03))
              .attr("stroke", "grey")
              .attr("transform", `translate(${xScale(node.x)},${yScale(node.y)})`);
            startAngle03 = endAngle03;
          }
        });
      };









      // Add legend
      const legend = svg.selectAll(".legend")
        .data(colorScale.domain())
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", (d, i) => `translate(0,${i * 20})`);

      legend.append("rect")
        .attr("x", width - 18)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", colorScale);

      legend.append("text")
        .attr("x", width - 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(d => `cluster ${d}`);

      window.addEventListener('resize', () => {
        const newSvgWidth = this.$refs.ProjectionView.offsetWidth;
        const newSvgHeight = this.$refs.ProjectionView.offsetHeight;
        svg.attr('width', newSvgWidth).attr('height', newSvgHeight);
        const margin_width = newSvgWidth * 0.05;
        const margin_height = newSvgHeight * 0.05;
        xScale.range([margin_width, newSvgWidth - margin_width]);
        yScale.range([margin_height, newSvgHeight - margin_height]);
        glyphs.selectAll('circle').attr('cx', d => xScale(d.x)).attr('cy', d => yScale(d.y));
        this.updateRings();
      });
    },
  },
};
</script>

<style scoped>
#right-all {
  width: 100%;
  height: 100%;
}

#scatter-button {
  width: 100%;
  height: 10%;
  display: flex;
  justify-content: center;
  align-items: center;
}

#ProjectionView {
  width: 100%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cluster-button {
  margin-right: 10px;
  width: 100px;
  height: 30px;
  font-size: 16px;
  background-color: #409EFF;
  color: #fff;
  border: none;
  border-radius: 5px;
}

.active {
  background-color: #45a049 !important;
}
</style>
