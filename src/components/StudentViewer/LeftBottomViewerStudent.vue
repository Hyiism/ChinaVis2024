<template>
  <div style="height:100%;width: 100%;">
    <button v-if="filtered" @click="resetChart" class="reset-button">返回</button>
    <div class="chart-container" ref="chartContainer"></div>
  </div>
  
</template>

<script>
import * as d3 from 'd3';
import EventBus from '@/eventBus'; // 导入事件总线

export default{
  name:'CoordinateGraph',
  data(){
    return{
      originalData: [],
      filtered: false,
      student_id: '0088dc183f73c83f763e',
      // 用来更新请求！
      title_id: 'Question_q7OpB2zCMmW9wS8uNt3H',
      title: [],
    };
  },
  mounted() {
    // 监听从气泡图传来的题目id
    EventBus.$on('bubTitleIdSelected', this.handleBubSelected);
    // this.originalData = this.title.map(t => t.titlestate);
    // this.drawChart(this.originalData);
    this.fetchStudentScores();
  },
  beforeDestroy() {
    EventBus.$off('bubTitleIdSelected', this.handleBubSelected);
    // 监听从气泡图传来的题目id
    EventBus.$on('bubTitleIdSelected', this.handleBubSelected);
    // this.originalData = this.title.map(t => t.titlestate);
    // this.drawChart(this.originalData);
    this.fetchStudentScores();
  },
  beforeDestroy() {
    EventBus.$off('bubTitleIdSelected', this.handleBubSelected);
  },
  methods: {
    fetchStudentScores() {
      this.$axios.get(`http://10.12.44.190:8000/titleprocess/?student_id=${this.student_id}&title_id=${this.title_id}`) // Replace with actual API endpoint
        .then(response => {
            this.title = JSON.parse(response.data);
            // 分数正确显示！！
            // console.log('rawdata!!!', this.score_list);
            // 拿到数据后加载表格
            this.originalData = this.title.map(t => t.titlestate);
            this.drawChart(this.originalData);
          })
          .catch(error => {
            console.error("There was an error!", error);
          });
      },
    fetchStudentScores() {
      this.$axios.get(`http://10.12.44.190:8000/titleprocess/?student_id=${this.student_id}&title_id=${this.title_id}`) // Replace with actual API endpoint
        .then(response => {
            this.title = JSON.parse(response.data);
            // 分数正确显示！！
            // console.log('rawdata!!!', this.score_list);
            // 拿到数据后加载表格
            this.originalData = this.title.map(t => t.titlestate);
            this.drawChart(this.originalData);
          })
          .catch(error => {
            console.error("There was an error!", error);
          });
      },
    drawChart(dataGroups) {
      d3.select(this.$refs.chartContainer).selectAll("*").remove();

      const container = this.$refs.chartContainer;
      const margin = { top: 25, right: 30, bottom: 30, left: 40 };
      const width = container.clientWidth - margin.left - margin.right;
      const height = container.clientHeight - margin.top - margin.bottom;

      const svg = d3.select(this.$refs.chartContainer)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

      const states = this.filtered ? ['error9', 'error8', 'error7', 'error6', 'error5', 'error4', 'error3', 'error2', 'error1', '0'] : ['ac', 'pc', 'e', 'ae', '0'];
      const yScale = d3.scalePoint()
        .domain(states)
        .range([0, height]);

      const parseTime = d3.timeParse("%M:%S");
      const timeData = dataGroups.flat().map(d => parseTime(d.time));
      const xScale = d3.scaleTime()
        .domain(d3.extent(timeData))
        .range([0, width]);

      yScale.domain().forEach(state => {
        svg.append('line')
          .attr('x1', 0)
          .attr('y1', yScale(state))
          .attr('x2', width)
          .attr('y2', yScale(state))
          .attr('stroke', 'lightgray')
          .attr('stroke-dasharray', '4');
      });

      svg.append('g')
        .call(d3.axisLeft(yScale));

      svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d3.timeFormat("%M:%S")).tickValues(timeData));

      svg.append("defs").append("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 0 10 10")
        .attr("refX", "5")
        .attr("refY", "5")
        .attr("markerWidth", "6")
        .attr("markerHeight", "6")
        .attr("orient", "auto-start-reverse")
        .append("path")
        .attr("d", "M 0 0 L 5 5 L 0 10 z")
        .attr("fill", "#bbbdbd");

      const stateColors = {
        'ac': "#038863",
        'pc': "#f0d945",
        'e': "#f38833",
        'ae': "#e82829"
      };

      const methodColors = {
        'Method_m8vwGkEZc3TSW2xqYUoR': "#6090b8",
        'Method_BXr9AIsPQhwNvyGdZL57': "#d19ba9",
        'Method_gj1NLb4Jn7URf9K2kQPd': "#9de1ac",
        'Method_Cj9Ya2R7fZd6xs1q5mNQ': "#003c72",
        'Method_5Q4KoXthUuYz3bvrTDFm': "#c055ac"
      };

      const tooltip = d3.select(this.$refs.chartContainer)
        .append('div')
        .style('position', 'absolute')
        .style('visibility', 'hidden')
        .style('background', '#f9f9f9')
        .style('border', '1px solid #ccc')
        .style('padding', '10px')
        .style('border-radius', '5px')
        .style('box-shadow', '0 0 10px rgba(0,0,0,0.1)');

      dataGroups.forEach((data, groupIndex) => {
        const methodUsage = data.map((d, i) => {
          const usage = {
            'Method_m8vwGkEZc3TSW2xqYUoR': 0,
            'Method_BXr9AIsPQhwNvyGdZL57': 0,
            'Method_gj1NLb4Jn7URf9K2kQPd': 0,
            'Method_Cj9Ya2R7fZd6xs1q5mNQ': 0,
            'Method_5Q4KoXthUuYz3bvrTDFm': 0
          };
          for (let j = 0; j <= i; j++) {
            if (data[j].method in usage) {
              usage[data[j].method]++;
            }
          }
          return usage;
        });

        data.forEach((d, i) => {
          const usage = methodUsage[i];
          const totalUsage = Object.values(usage).reduce((a, b) => a + b, 0);

          const arc = d3.arc()
            .innerRadius(11)
            .outerRadius(16);

          const pie = d3.pie()
            .value(d => d[1]);

          const arcs = pie(Object.entries(usage));

          const g = svg.append('g')
            .attr('transform', `translate(${xScale(parseTime(d.time))},${yScale(this.filtered ? d.errortype : d.state)})`)
            .style("opacity", 0);

          g.selectAll('path')
            .data(arcs)
            .enter()
            .append('path')
            .attr('d', arc)
            .attr('fill', d => methodColors[d.data[0]]);

          g.transition()
            .duration(350)
            .delay(i * 200)
            .style("opacity", 1);

          svg.append('circle')
            .attr('cx', xScale(parseTime(d.time)))
            .attr('cy', yScale(this.filtered ? d.errortype : d.state))
            .attr('r', 9)
            .attr('fill', stateColors[d.state])
            .style("opacity", 0)
            .on('mouseover', (event) => {
              tooltip.html(`Time Consume: ${d.time_consume}<br>Memory Consume: ${d.memory_consume}`)
                .style('visibility', 'visible');
            })
            .on('mousemove', event => {
              const containerRect = container.getBoundingClientRect();
              
              tooltip.style('left', (event.pageX + 10) + 'px')
                .style('top', (event.pageY - containerRect.top) + 'px');
            })
            .on('mouseout', () => {
              tooltip.style('visibility', 'hidden');
            })
            .on('click', () => {
              if (!this.filtered && d.state === 'e') {
                this.filterData(groupIndex);
              }
            })
            .transition()
            .duration(200)
            .delay(i * 200)
            .style("opacity", 1);

          if (i < data.length - 1 && (!this.filtered || (d.state === 'e' && data[i + 1].state === 'e'))) {
            const x1 = xScale(parseTime(d.time));
            const y1 = yScale(this.filtered ? d.errortype : d.state);
            const x2 = xScale(parseTime(data[i + 1].time));
            const y2 = yScale(this.filtered ? data[i + 1].errortype : data[i + 1].state);
            const dx = x2 - x1;
            const dy = y2 - y1;
            const dist = Math.sqrt(dx * dx + dy * dy);
            const offsetX = (dx / dist) * 16;
            const offsetY = (dy / dist) * 16;

            svg.append("line")
              .attr("x1", x1 + offsetX)
              .attr("y1", y1 + offsetY)
              .attr("x2", x2 - offsetX)
              .attr("y2", y2 - offsetY)
              .attr("stroke", "#bbbdbd")
              .attr("stroke-width", 2.5)
              .attr("marker-end", "url(#arrow)")
              .style("opacity", 0)
              .transition()
              .duration(300)
              .delay(i * 250)
              .style("opacity", 1);
          }
        });
      });
    },
    filterData(groupIndex) {
      this.filtered = true;
      // const filteredData = this.originalData.map(group => group.filter(d => d.state === 'e'));
      const filteredData = [this.originalData[groupIndex].filter(d => d.state === 'e')];
      this.drawChart(filteredData);
    },
    resetChart() {
      this.filtered = false;
      this.drawChart(this.originalData);
    },
    // 接收从气泡图传来的题目id 使用此id请求数据
    handleBubSelected(titleId) {
      this.title_id = titleId;
      // console.log('this.title_id_req:', this.title_id_req);
      this.fetchStudentScores();
    }
  }
}
</script>
  
<style scoped>
.chart-container {
  width: 100%;
  height: 90%;
  top:35px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}
.reset-button {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 5px 10px;
  background-color: #038863;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}
.reset-button:hover {
  background-color: #026648;
}
</style>







<!-- <script>
import * as d3 from 'd3';

export default{
  name:'CoordinateGraph',
  data(){
    return{
      originalData: [],
      filtered: false,
      student_id: '0088dc183f73c83f763e',
      title:[
        {
          title_id: 'Question_q7OpB2zCMmW9wS8uNt3H',
          titlestate:[
            {
              state: 'e',
              time: '0:00',
              time_consume: 4,
              memory_consume: 327,
              errortype:'error1',
              method:'Method_m8vwGkEZc3TSW2xqYUoR',
            },
            {
              state: 'e',
              time: '0:12',
              time_consume: 4,
              memory_consume: 327,
              errortype: 'error5',
              method: 'Method_BXr9AIsPQhwNvyGdZL57',
            },
            {
              state: 'ae',
              time: '0:50',
              time_consume: 4,
              memory_consume: 327,
              errortype: null,
              method: 'Method_gj1NLb4Jn7URf9K2kQPd',
            },
            {
              state: 'e',
              time: '1:08',
              time_consume: 4,
              memory_consume: 327,
              errortype: 'error3',
              method: 'Method_BXr9AIsPQhwNvyGdZL57',
            },
            {
              state: 'pc',
              time: '1:32',
              time_consume: 4,
              memory_consume: 327,
              errortype: null,
              method:'Method_Cj9Ya2R7fZd6xs1q5mNQ',
            },
            {
              state: 'e',
              time: '1:45',
              time_consume: 4,
              memory_consume: 327,
              errortype: 'error9',
              method: 'Method_5Q4KoXthUuYz3bvrTDFm',
            },
            {
              state: 'ac',
              time: '2:20',
              time_consume: 4,
              memory_consume: 327,
              errortype: null,
              method:'Method_5Q4KoXthUuYz3bvrTDFm',
            },
            {
              state: 'ac',
              time: '2:42',
              time_consume: 4,
              memory_consume: 268,
              errortype: null,
              method:'Method_5Q4KoXthUuYz3bvrTDFm',
            },
          ]
        },
        {
          title_id: 'Question_q7OpB2zCMmW9wS8uNt3b',
          titlestate:[
            {
              state: 'e',
              time: '0:00',
              time_consume: 4,
              memory_consume: 327,
              errortype:'error1',
              method:'Method_m8vwGkEZc3TSW2xqYUoR',
            },
            {
              state: 'e',
              time: '0:38',
              time_consume: 4,
              memory_consume: 327,
              errortype: 'error3',
              method: 'Method_BXr9AIsPQhwNvyGdZL57',
            },
            {
              state: 'e',
              time: '0:52',
              time_consume: 4,
              memory_consume: 327,
              errortype: 'error5',
              method: 'Method_BXr9AIsPQhwNvyGdZL57',
            },
            {
              state: 'ae',
              time: '1:00',
              time_consume: 4,
              memory_consume: 327,
              errortype: null,
              method: 'Method_gj1NLb4Jn7URf9K2kQPd',
            },
            {
              state: 'pc',
              time: '1:32',
              time_consume: 4,
              memory_consume: 327,
              errortype: null,
              method:'Method_Cj9Ya2R7fZd6xs1q5mNQ',
            },
            {
              state: 'e',
              time: '1:45',
              time_consume: 4,
              memory_consume: 327,
              errortype: 'error9',
              method: 'Method_5Q4KoXthUuYz3bvrTDFm',
            },
            {
              state: 'ac',
              time: '2:20',
              time_consume: 4,
              memory_consume: 327,
              errortype: null,
              method:'Method_5Q4KoXthUuYz3bvrTDFm',
            },
            {
              state: 'ac',
              time: '2:42',
              time_consume: 4,
              memory_consume: 268,
              errortype: null,
              method:'Method_5Q4KoXthUuYz3bvrTDFm',
            },
          ]
        }
        
      ],
      
    };
  },
  mounted() {
    this.originalData = this.title[0].titlestate;
    this.drawChart(this.originalData);
  },
  methods: {
    drawChart(data) {
      d3.select(this.$refs.chartContainer).selectAll("*").remove();

      const container = this.$refs.chartContainer;
      const margin = { top: 25, right: 30, bottom: 30, left: 40 };
      const width = container.clientWidth - margin.left - margin.right;
      const height = container.clientHeight - margin.top - margin.bottom;

      const svg = d3.select(this.$refs.chartContainer)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

      const states = this.filtered ? ['error9', 'error8', 'error7', 'error6', 'error5', 'error4', 'error3', 'error2', 'error1','0'] : ['ac', 'pc', 'e', 'ae', '0'];
      const yScale = d3.scalePoint()
        .domain(states)
        .range([0, height]);

      // 将时间转换为分钟数
      const parseTime = d3.timeParse("%M:%S");
      const timeData = data.map(d => parseTime(d.time));
      const xScale = d3.scaleTime()
        .domain(d3.extent(timeData))
        .range([0, width]);

      // 为纵坐标绘制四条横线
      yScale.domain().forEach(state => {
        svg.append('line')
          .attr('x1', 0)
          .attr('y1', yScale(state))
          .attr('x2', width)
          .attr('y2', yScale(state))
          .attr('stroke', 'lightgray')
          .attr('stroke-dasharray', '4');
      });

      svg.append('g')
        .call(d3.axisLeft(yScale));

      svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d3.timeFormat("%M:%S")).tickValues(timeData));

      // 添加箭头定义
      svg.append("defs").append("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 0 10 10")
        .attr("refX", "8")
        .attr("refY", "5")
        .attr("markerWidth", "6")
        .attr("markerHeight", "6")
        .attr("orient", "auto-start-reverse")
        .append("path")
        .attr("d", "M 0 0 L 8 5 L 0 10 z")
        .attr("fill", "#5a5a5a");

      // 定义状态颜色
      const stateColors = {
        'ac': "#038863",
        'pc': "#f0d945",
        'e': "#f38833",
        'ae': "#e82829"
      };

      // 定义编程语言颜色
      const methodColors = {
        'Method_m8vwGkEZc3TSW2xqYUoR': "#6090b8",
        'Method_BXr9AIsPQhwNvyGdZL57': "#d19ba9",
        'Method_gj1NLb4Jn7URf9K2kQPd': "#9de1ac",
        'Method_Cj9Ya2R7fZd6xs1q5mNQ': "#003c72",
        'Method_5Q4KoXthUuYz3bvrTDFm': "#c055ac"
      };

      // 计算每个数据点之前编程语言使用情况
      const methodUsage = data.map((d, i) => {
        const usage = {
          'Method_m8vwGkEZc3TSW2xqYUoR': 0,
          'Method_BXr9AIsPQhwNvyGdZL57': 0,
          'Method_gj1NLb4Jn7URf9K2kQPd': 0,
          'Method_Cj9Ya2R7fZd6xs1q5mNQ': 0,
          'Method_5Q4KoXthUuYz3bvrTDFm': 0
        };
        for (let j = 0; j <= i; j++) {
          if (data[j].method in usage) {
            usage[data[j].method]++;
          }
        }
        return usage;
      });

      // 定义提示框
      const tooltip = d3.select(this.$refs.chartContainer)
        .append('div')
        .style('position', 'absolute')
        .style('visibility', 'hidden')
        .style('background', '#f9f9f9')
        .style('border', '1px solid #ccc')
        .style('padding', '10px')
        .style('border-radius', '5px')
        .style('box-shadow', '0 0 10px rgba(0,0,0,0.1)');

      // 绘制数据点和箭头
      data.forEach((d, i) => {
        const usage = methodUsage[i];
        const totalUsage = Object.values(usage).reduce((a, b) => a + b, 0);

        // 绘制外环
        const arc = d3.arc()
          .innerRadius(11)
          .outerRadius(16);

        const pie = d3.pie()
          .value(d => d[1]);

        const arcs = pie(Object.entries(usage));

        const g = svg.append('g')
          .attr('transform', `translate(${xScale(timeData[i])},${yScale(this.filtered ? d.errortype : d.state)})`)
          .style("opacity", 0);

        g.selectAll('path')
          .data(arcs)
          .enter()
          .append('path')
          .attr('d', arc)
          .attr('fill', d => methodColors[d.data[0]]);

        g.transition()
          .duration(350)
          .delay(i * 200)
          .style("opacity", 1);
        
        svg.append('circle')
          .attr('cx', xScale(timeData[i]))
          .attr('cy', yScale(this.filtered ? d.errortype : d.state))
          .attr('r', 9)
          .attr('fill', stateColors[d.state])
          .style("opacity", 0)
          .on('mouseover', (event) => {
            tooltip.html(`Time Consume: ${d.time_consume}<br>Memory Consume: ${d.memory_consume}`)
              .style('visibility', 'visible');
          })
          .on('mousemove', event => {
            const containerRect = container.getBoundingClientRect();
            
            tooltip.style('left', (event.pageX + 10) + 'px')
              .style('top', (event.pageY - containerRect.top) + 'px');
          })
          .on('mouseout', () => {
            tooltip.style('visibility', 'hidden');
          })
          .on('click', () => {
            if (!this.filtered && d.state === 'e') {
              this.filterData();
            }
          })
          .transition()
          .duration(200)
          .delay(i * 200)
          .style("opacity", 1);

        if (i < data.length - 1 && (!this.filtered || (d.state === 'e' && data[i + 1].state === 'e'))) {
          const x1 = xScale(timeData[i]);
          const y1 = yScale(this.filtered ? d.errortype : d.state);
          const x2 = xScale(timeData[i + 1]);
          const y2 = yScale(this.filtered ? data[i + 1].errortype : data[i + 1].state);
          const dx = x2 - x1;
          const dy = y2 - y1;
          const dist = Math.sqrt(dx * dx + dy * dy);
          const offsetX = (dx / dist) * 16; // 16 is the outer radius of the arc
          const offsetY = (dy / dist) * 16;

          svg.append("line")
            .attr("x1", x1 + offsetX)
            .attr("y1", y1 + offsetY)
            .attr("x2", x2 - offsetX)
            .attr("y2", y2 - offsetY)
            .attr("stroke", "#5a5a5a")
            .attr("stroke-width", 2.5)
            .attr("marker-end", "url(#arrow)")
            .style("opacity", 0)  // 初始透明度为 0
            .transition()
            .duration(300)
            .delay(i * 250)
            .style("opacity", 1);
        }
      }); 
    },
    filterData() {
      this.filtered = true;
      const filteredData = this.originalData.filter(d => d.state === 'e');
      this.drawChart(filteredData);
    },
    resetChart() {
      this.filtered = false;
      this.drawChart(this.originalData);
    },
  }
}
</script> -->