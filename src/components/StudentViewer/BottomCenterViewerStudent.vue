<template>
  <div ref="chartContainer" class="chart-container-bottomcenter">
    <div class="button-container">
      <button :class="{'selected': selectedDistribution === 'time_distribution'}" @click="selectDistribution('time_distribution')">
        <div>执行用时分布</div>
        <div>用时 {{ rawData.time_consume }} ms&nbsp;&nbsp;&nbsp;击败 {{ (rawData.time_beat * 100).toFixed(2) }}%</div>
      </button>
      <button :class="{'selected': selectedDistribution === 'memory_distribution'}" @click="selectDistribution('memory_distribution')">
        <div>内存占用分布</div>
        <div>占用 {{ rawData.memory_consume }} MB&nbsp;击败 {{ (rawData.memory_beat * 100).toFixed(2) }}%</div>
      </button>
    </div>
    <div class="barchart-container"></div>
    <div ref="tooltip" class="tooltip" style="opacity: 0;"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import EventBus from '@/eventBus'; // 导入事件总线
import { data } from 'jquery';
import { mapGetters } from 'vuex';

export default{
  name:'BarChart',
  data(){
    return{
      rawData:{},
      selectedDistribution: 'time_distribution',
      title_id_req: 'Question_q7OpB2zCMmW9wS8uNt3H'
    }
  },
  computed: {
    ...mapGetters(['studentId'])
  },
  created(){
    this.fetchStudentScores();
  },
  mounted() {
    // 监听从气泡图传来的题目id
    EventBus.$on('bubTitleIdSelected', this.handleBubSelected);
    this.subscriptionToken = PubSub.subscribe('studentId', (msg, value) => {
      this.fetchStudentScores(value);
    });
    // this.drawChart();
  },
  beforeDestroy() {
    EventBus.$off('bubTitleIdSelected', this.handleBubSelected);
  },
  watch: {
    selectedDistribution() {  //选择时间复杂度或者空间复杂度
      this.updateChart();
    }
  },
  methods: {
    fetchStudentScores() {
      this.$axios.get(`http://10.12.44.190:8000/titleperf/?student_id=${this.studentId}&title_id=${this.title_id_req}`)
        .then(response => {
          this.rawData = JSON.parse(response.data).data;
          this.drawChart();
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
    },
    selectDistribution(distribution) {
      this.selectedDistribution = distribution;
    },
    findHighlightedColumn(distribution, value) {
      if (distribution === 'time_distribution') {
        return String(value); // time_distribution keys are exact values
      } else if (distribution === 'memory_distribution') {
        // Find the range key that includes the value
        for (const key of Object.keys(this.rawData.memory_distribution)) {
          const [min, max] = key.split('~').map(Number);
          if (value >= min && value <= max) {
            return key;
          }
        }
      }
      return null;
    },
    drawChart() {
      // Remove any existing SVG before creating a new one
      d3.select(this.$refs.chartContainer).selectAll('svg').remove();

      const data = this.rawData[this.selectedDistribution];
      const container = this.$refs.chartContainer;
      const svgWidth = container.clientWidth;
      const svgHeight = container.clientHeight;
      const margin = { top: 20, right: 30, bottom: 20, left: 40 };
      const width = svgWidth - margin.left - margin.right;
      const height = svgHeight - margin.top - margin.bottom;
      const tooltip = d3.select(this.$refs.tooltip);

      const highlightedColumn = this.findHighlightedColumn(
        this.selectedDistribution,
        this.selectedDistribution === 'time_distribution' ? this.rawData.time_consume : this.rawData.memory_consume
      );

      const svg = d3.select('.barchart-container')
        .append('svg')
        .attr('width', svgWidth)
        .attr('height', svgHeight)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

      const x = d3.scaleBand()
        .domain(Object.keys(data))
        .range([0, width])
        .padding(0.2);

      const y = d3.scaleLinear()
        .domain([0, d3.max(Object.values(data))])
        .nice()
        .range([height, 0]);

      svg.append('g')
        .selectAll('rect')
        .data(Object.entries(data))
        .enter()
        .append('rect')
        .attr('x', d => x(d[0]))
        .attr('width', x.bandwidth())
        .attr('fill', d => d[0] === highlightedColumn ? 'orange' : 'steelblue')
        .attr('y', height)               //添加直方图生长的动态效果
        .attr('height', 0)
        .attr('rx', 8)               // 设置圆角半径（可以根据需要调整）
        .on('mouseover', (event, d) => {
          tooltip.style('opacity', 1)
                .html(`类别: ${d[0]}<br>占比: ${d[1]}`);
        })
        .on('mousemove', (event) => {
          const containerRect = container.getBoundingClientRect();

          let top = event.clientY - containerRect.top + 60;
          let left = event.clientX - containerRect.left + 6;
          tooltip.style('top', top +  'px')
                 .style('left', left + 'px');
        })
        .on('mouseout', () => {
          tooltip.style('opacity', 0);
        })
        .transition()
        .duration(800)
        .attr('y', d => y(d[1]))
        .attr('height', d => height - y(d[1]))

      svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x));

      svg.append('g')
        .attr('class', 'y-axis')
        .call(d3.axisLeft(y));
    },
    //把原来画的直方图删去，重新根据选择的数据绘制直方图
    updateChart() {
      d3.select('.barchart-container').select('svg').remove();
      this.drawChart();
    },

    // 接收从气泡图传来的题目id 使用此id请求数据
    handleBubSelected(titleId) {
      // console.log('titleId:', titleId);
      // this.rawData.title_id = titleId;
      this.title_id_req = titleId;
      // console.log('this.title_id_req:', this.title_id_req);
      this.fetchStudentScores();
    }
  }
}
</script>

<style scoped>
.chart-container-bottomcenter {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 75%;
  margin-top: 15px;
}

.button-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  width: 100%;
  height: 30%
}

.button-container button {
  flex: 1;
  margin: 0 5px;
  padding: 10px;
  background-color: white;
  color: gray;
  border: 1px solid #ccc;
  font-size: 16px;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
  border-radius: 10px; /* 添加圆角效果 */
}

.button-container button.selected {
  background-color: gray;
  color: white;
}

.button-container button div {
  margin-bottom: 2px;
}

.tooltip {
  position: absolute;
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 10px;
  border-radius: 5px;
  pointer-events: none;
  font-size: 14px;
}
</style>
