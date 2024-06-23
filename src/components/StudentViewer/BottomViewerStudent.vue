<template>
  <div ref="bubbleChartContainer" class="bubble-chart-container">
    <div ref="bubbleChart"></div>
  </div>
</template>

<script>
import * as d3v5 from 'd3v5';
import { mapGetters } from 'vuex';
import EventBus from '@/eventBus'; // 导入事件总线
export default {
  data() {
    return {
      rawdata: [],
    };
  },
  computed: {
    ...mapGetters(['studentId'])
  },
  created() {
    this.fetchStudentScores();
  },
  mounted() {
    this.subscriptionToken = PubSub.subscribe('studentId', (msg, value) => {
      this.fetchStudentScores(value);
    });
    window.addEventListener('resize', this.createBubbleChart); // Recreate chart on window resize
    // this.$nextTick(() => {
    //   this.createBubbleChart();
    //   window.addEventListener('resize', this.createBubbleChart); // Recreate chart on window resize
    // });
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.createBubbleChart);
  },
  methods: {
    fetchStudentScores() {
      this.$axios.get(`http://10.12.44.190:8000/bubpie/?student_id=${this.studentId}`) // Replace with actual API endpoint
        .then(response => {
          this.rawdata = JSON.parse(response.data).data;
          // 分数正确显示！！
          // console.log('rawdata!!!', this.score_list);
          // 拿到数据后加载表格
          this.createBubbleChart();
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
    },
    createBubbleChart() {
      // Remove any existing SVG before creating a new one
      d3v5.select(this.$refs.bubbleChart).selectAll('*').remove();

      const bubbleData = this.rawdata;
      const word = 'new_title';
      const frequency = 'score';
      const maxSize = 22;
      const xAxis = 'knowl';

      const container = this.$refs.bubbleChartContainer;
      const containerWidth = container.clientWidth;
      const containerHeight = container.clientHeight;
      const width = containerWidth;
      const height = containerHeight;
      console.log('height', height);
      console.log('width', width);
      const margin = { t: 0, l: 50, r: 20, b: 0 };
      const padding = 2;
      const knowledge_list = ['k4W1c', 'b3C9s', 'r8S3g', 'm3D1v', 'y9W5d', 't5V9e', 'g7R2j', 's8Y2f']

      if (xAxis === undefined) {
        bubbleData.map(d => (d.xAxis = 0));
      }

      const time = d3v5.set(bubbleData.map(d => d[xAxis])).values();

      let x = d3v5
        .scalePoint()
        .domain(time)
        .range([margin.l, width - margin.l - margin.r]);

      let svg = d3v5
        .select(this.$refs.bubbleChart)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

      const xaxis = svg
        .append("g")
        .attr("transform", `translate(0,${height - 50})`)
        .call(d3v5.axisBottom(x)).selectAll(".tick")
        .on('click', (event, d) => {
          // 这里的d是index值
          console.log('X Axis Tick Clicked:', knowledge_list[d]);
          // 在这里可以处理点击事件的逻辑，例如发送事件或者执行其他操作
          EventBus.$emit('bubKnowledgeIdSelected', knowledge_list[d]);
        });

      const colorScale = d3v5.scaleOrdinal(d3v5.schemeCategory10);

      const luminance = 50;
      const textColor = d3v5
        .scaleQuantile()
        .range(["#fff", "#000"])
        .domain([0, luminance, 100]);

      // 设置圆圈大小
      const r = d3v5
        .scaleSqrt()
        .domain([0, d3v5.max(bubbleData, d => d[frequency])])
        .range([0, maxSize]);

      const simulation = d3v5
        .forceSimulation(bubbleData)
        .force("x", d3v5.forceX(d => x(d[xAxis])).strength(1))
        .force("y", d3v5.forceY(height / 2).strength(0.2))
        .force(
          "collide",
          d3v5
            .forceCollide()
            .radius(d => r(d[frequency]) + padding)
            .iterations(10)
        )
        .alpha(0.2);

      let gBubble = svg.selectAll('gBubble').data(bubbleData);
      gBubble.exit().remove();

      let bubble = gBubble
        .enter()
        .append('g')
        .classed('gBubble', true)
        .attr('id', d => d[word]);

      bubble
        .append('circle')
        .attr('r', d => r(d[frequency]))
        .attr('fill', d => colorScale(d[word]))
        .attr('fill-opacity', 0.4)
        .attr('stroke', d => d3v5.rgb(colorScale(d[word])).darker(1))
        .attr('stroke-width', 1)
        .on('click', function (event, d) { // 添加点击事件监听器
          // 这里的d是当前点击的气泡的数据 有问题 d是index值
          // 点击气泡 传出去当前气泡的title名称 为隔壁的做题视图提供数据
          console.log('Bubble clicked:', bubbleData[d]['title']);
          EventBus.$emit('bubTitleIdSelected', bubbleData[d]['title']);
        });

      const textLabels = bubble
        .append('text')
        .text(d => d[word])
        .style('text-anchor', 'middle')
        .attr("dominant-baseline", "central")
        .attr('font-family', 'sans-serif')
        .attr('font-size', '8px')
        .attr('font-weight', 'normal')
        .style('stroke', 'white')
        .style('stroke-width', 2);
      // .on('click', function(event, d) { // 添加点击事件监听器
      //   // 这里的d是当前点击的气泡的数据 有问题 d是index值
      //   // 点击气泡 传出去当前气泡的title名称 为隔壁的做题视图提供数据
      //   console.log('Bubble clicked:', d);
      //   // EventBus.$emit('bubTitleIdSelected', bubbleData[d]['title']);
      // });

      const textBck = bubble
        .append('text')
        .text(d => d[word])
        .style('text-anchor', 'middle')
        .attr("dominant-baseline", "central")
        .attr('font-family', 'sans-serif')
        .attr('font-size', '8px')
        .attr('font-weight', 'normal');

      gBubble = gBubble.merge(bubble);

      gBubble.call(this.drag(simulation));

      simulation.nodes(bubbleData).on('tick', () => {
        gBubble.attr('transform', d => 'translate(' + d.x + ',' + d.y + ')');
      });
    },
    drag(simulation) {
      function dragstarted(d) {
        if (!d3v5.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(d) {
        d.fx = d3v5.event.x;
        d.fy = d3v5.event.y;
      }

      function dragended(d) {
        if (!d3v5.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }

      return d3v5
        .drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
    }
  }
};
</script>

<style scoped>
.bubble-chart-container {
  width: 100%;
  height: 100%;
}
</style>