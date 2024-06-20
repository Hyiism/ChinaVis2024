<template>
  <div id="right-all">
    <div id="controls">
      <select v-model="selectedEmbedding" @change="setEmbedding(selectedEmbedding)">
          <option value="features_vis_seq">SeqData</option>
          <option value="features_vis_concat">ConcatData</option>
          <option value="features_vis_all">AllData</option>
      </select>
      <div id="scatter-button">
        <button @click="setClusterMethod('pca')" class="cluster-button" :class="{ 'active': clusterMethod === 'pca' }">PCA</button>
        <button @click="setClusterMethod('tsne')" class="cluster-button" :class="{ 'active': clusterMethod === 'tsne' }">T-SNE</button>
        <button @click="setClusterMethod('umap')" class="cluster-button" :class="{ 'active': clusterMethod === 'umap' }">UMAP</button>
      </div>
    </div>
    <div ref="ProjectionView" id="ProjectionView"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';
import EventBus from '@/eventBus'; // 导入事件总线
import { mapGetters } from 'vuex';

export default {
  name: 'RightViewerClass',
  data() {
    return {
      nodes: [],
      clusterMethod: 'pca',
      selectedEmbedding: 'features_vis_seq',
    };
  },
  computed: {
    ...mapGetters(['classId'])
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
    setEmbedding(embedding) {
      this.selectedEmbedding = embedding;
      this.drawView(); // Update the view with new data
    },
    async getdata() {
      var _this = this;
      await axios.get(`http://10.12.44.190:8000/get_projection_data/?class_id=${this.classId}&method=${this.clusterMethod}&embedding=${this.selectedEmbedding}`)
        .then(res => {
          console.log("projection data");
          _this.nodes = JSON.parse(res.data).nodes;
          console.log(_this.nodes, typeof(_this.nodes));
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
      // console.log("11111111")
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
          const avgScore = node.total_score;    //平均分，分数越高圆弧越长
          const startAngle = 0;
          const endAngle = 2 * Math.PI * (avgScore / 150);     //4是随便取的,暂时设置满分150分，按比例画圈
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
          
          
          const scoreingData = node.state_data;     //做题正确程度的占比，按顺时针依次是全错、基本错、基本对、全对
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
        .style("fill", colorScale)
        .on('click', (event, d) => {
          console.log("click legend");
          console.log(d);
          EventBus.$emit('clusterSelected', d); // Emit event
        });

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

/* #scatter-button {
  width: 100%;
  height: 10%;
  display: flex;
  justify-content: center;
  align-items: center;
} */
#controls {
  width: 100%;
  height: 10%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

#scatter-button {
  width: 86%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
select {
  margin-left: 10px;
  width: 14%;
  height: 40%;
  font-size: 12px;
  border-radius: 5px; /* 添加圆角 */
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
