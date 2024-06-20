<template>
  <div ref="chartContainer" class="chart-container-bottomcenter">
    <div class="button-container">
      <button :class="{'selected': selectedDistribution === 'time_distribution'}" @click="selectDistribution('time_distribution')">
        <div>执行用时分布</div>
        <div>用时 {{ time_consume }} 毫秒&nbsp;&nbsp;&nbsp;击败 {{ (time_beat * 100).toFixed(2) }}%</div>
      </button>
      <button :class="{'selected': selectedDistribution === 'memory_distribution'}" @click="selectDistribution('memory_distribution')">
        <div>内存用时分布</div>
        <div>用时 {{ memory_consume }} MB&nbsp;击败 {{ (memory_beat * 100).toFixed(2) }}%</div>
      </button>
    </div>
    <div class="barchart-container"></div>
    <div ref="tooltip" class="tooltip" style="opacity: 0;"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default{
  name:'BarChart',
  data(){
    return{
      student_id: '0088dc183f73c83f763e',
      title_id: 'Question_q7OpB2zCMmW9wS8uNt3H',
      time_consume: 4,
      memory_consume: 327,
      time_beat: 0.67,
      memory_beat: 0.59,
      time_distribution:{
        "1":0.01,
        "2":0.03,
        "3":0.08,
        "4":0.13,
        "5":0.26,
        "6":0.29,
        "7":0.12,
        "8":0.05,
        "9":0.02,
        "10":0.01
      },
      memory_distribution:{
        "1~50":0.005,
        "51~100":0.01,
        "101~150":0.02,
        "151~200":0.03,
        "201~250":0.055,
        "251~300":0.095,
        "301~350":0.15,
        "351~400":0.215,
        "401~450":0.18,
        "451~500":0.11,
        "501~550":0.075,
        "551~600":0.03,
        "601~650":0.015,
        "651~700":0.005,
      },
      selectedDistribution: 'time_distribution'
    }
  },
  mounted() {
    this.drawChart();
  },
  watch: {
    selectedDistribution() {  //选择时间复杂度或者空间复杂度
      this.updateChart();
    }
  },
  methods: {
    selectDistribution(distribution) {
      this.selectedDistribution = distribution;
    },
    findHighlightedColumn(distribution, value) {
      if (distribution === 'time_distribution') {
        return String(value); // time_distribution keys are exact values
      } else if (distribution === 'memory_distribution') {
        // Find the range key that includes the value
        for (const key of Object.keys(this.memory_distribution)) {
          const [min, max] = key.split('~').map(Number);
          if (value >= min && value <= max) {
            return key;
          }
        }
      }
      return null;
    },
    drawChart() {
      const data = this[this.selectedDistribution];
      const container = this.$refs.chartContainer;
      const svgWidth = container.clientWidth;
      const svgHeight = container.clientHeight;
      const margin = { top: 20, right: 30, bottom: 20, left: 40 };
      const width = svgWidth - margin.left - margin.right;
      const height = svgHeight - margin.top - margin.bottom;
      const tooltip = d3.select(this.$refs.tooltip);

      const highlightedColumn = this.findHighlightedColumn(
        this.selectedDistribution,
        this.selectedDistribution === 'time_distribution' ? this.time_consume : this.memory_consume
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
