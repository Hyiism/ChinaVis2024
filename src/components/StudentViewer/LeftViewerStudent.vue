<template>
  <div id="all-card">
    <div id="check-card">
      <div class="grid-container">
        <ul class="days">
          <li class="li-day-label">Sun.</li>
          <li class="li-day-label">Mon.</li>
          <li class="li-day-label">Tue.</li>
          <li class="li-day-label">Wen.</li>
          <li class="li-day-label">Thur.</li>
          <li class="li-day-label">Fri.</li>
          <li class="li-day-label">Sat.</li>
        </ul>

        <ul class="graph">
          <el-tooltip class="item" effect="dark" :content="item.submission_count + ' ' +(item.submission_count > 1 ? 'submissions on ' : 'submission on ') + item.year + '-' + item.month + '-' + item.date"
              placement="top-start" v-for="(item, index) in infos" :key="index" :open-delay="500">
            <li :data-level="item.level" class="li-day" :isToday="item.isToday" @click="handleClick(item)"></li>
          </el-tooltip>
        </ul>
      </div>

      <ul class="months">
        <li class="li-month" :style="{ gridColumnStart: '2' }">Aug</li>
        <li class="li-month" :style="{ gridColumnStart: '3' }">Sep</li>
        <li class="li-month" :style="{ gridColumnStart: '7' }">Oct</li>
        <li class="li-month" :style="{ gridColumnStart: '11' }">Nov</li>
        <li class="li-month" :style="{ gridColumnStart: '15' }">Des</li>
        <li class="li-month" :style="{ gridColumnStart: '19' }">Jau</li>
      </ul>
    </div>
    
    <div id= "detail-card">
      <!-- <p>用来展示所选日期的24小时活跃度情况</p> -->
      <div id="ring-chart"></div> <!-- D3环形饼状图的容器 -->
      <div id="radar-chart"></div> <!-- D3雷达图的容器 -->
    </div>
  </div>
</template>

<script>
import EventBus from '@/eventBus'; // 导入事件总线
import * as d3 from 'd3';
import { mapGetters } from 'vuex';

export default {
  name: 'CheckChart',
  data() {
    return {
      infos: [],
      piedata:{
        "state_ae_percentage":20,
        "state_e_percentage":40,
        "state_pc_percentage":25,
        "state_ac_percentage":15,
      },
      timedata:
      {
        "1:00":0.03,
        "2:00":0.08,
        "3:00":0.12,
        "4:00":0.15,
        "5:00":0.22,
        "6:00":0.29,
        "7:00":0.35,
        "8:00":0.51,
        "9:00":0.78,
        "10:00":0.87,
        "11:00":0.93,
        "12:00":0.84,
        "13:00":0.72,
        "14:00":0.86,
        "15:00":0.95,
        "16:00":0.98,
        "17:00":0.92,
        "18:00":0.65,
        "19:00":0.72,
        "20:00":0.63,
        "21:00":0.42,
        "22:00":0.21,
        "23:00":0.11,
        "24:00":0.09,
      }
        
      
      // monthBar: ["Aug", "Sep", "Oct", "Nov", "Des", "Jau"],
      // weekBar: ["Mon", "周二", "周三", "周四", "周五", "周六", "周日"],
    };
  },
  computed: {
    ...mapGetters(['studentId'])
  },
  created() {
    this.fetchStudentScores();
  },
  mounted() {
    this.renderRingChart(); // 绘制环形图
    this.renderRadarChart(); // 绘制雷达图
  },

  methods: {
    fetchStudentScores() {
      this.$axios.get(`http://10.12.44.190:8000/get_check_data/?student_id=${this.studentId}`)
        .then(response => {
          this.infos = JSON.parse(response.data).infos;
          console.log("this.infos");
          console.log(this.infos);
          // this.initializeMonthBar();
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
    },


    handleClick(item) {
      console.log(item.year + "1" + item.month + "1" + item.date);
      点击传数据到modelview执行操作
      EventBus.$emit('checkSelected', {student_id:'r28s9kyo7knrvytyvmt8', 'year':item.year, 'month':item.month, 'date':item.date}); // 触发事件，传递 student_id
    },
    renderRingChart() {
      const ringChartElement = document.getElementById('ring-chart');
      const width = ringChartElement.offsetWidth;
      const height = ringChartElement.offsetHeight;
      const radius = Math.min(width, height) / 2;

      const svg = d3.select(ringChartElement)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);

      const data = Object.entries(this.piedata).map(([key, value]) => ({ key, value }));

      console.log(data); // 用于调试，检查转换后的数据格式

      const pie = d3.pie().value(d => d.value);
      const arc = d3.arc()
        .innerRadius(radius * 0.4)
        .outerRadius(radius * 0.8);

      const color = d3.scaleOrdinal()
        .domain(data.map(d => d.key))
        .range(d3.schemeCategory10);

      const arcs = svg.selectAll(".arc")
        .data(pie(data))
        .enter()
        .append("g")
        .attr("class", "arc");

      arcs.append("path")
        .attr("d", arc)
        .attr("fill", d => color(d.data.key))
        .attr("stroke", "#ffffff") // 添加白色缝隙
        .attr("stroke-width", "2px");

      // 添加文本标签
      arcs.append("text")
        .attr("transform", d => `translate(${arc.centroid(d)})`)
        .attr("text-anchor", "middle")
        .style("font-size", "12px")
        .style("fill", "#000")
        .selectAll("tspan")
        .data(d => [`${d.data.key}`, `${d.data.value}%`])
        .enter()
        .append("tspan")
        .attr("x", 0)
        .attr("dy", (d, i) => (i === 0 ? "-0.5em" : "1em"))
        .style("font-weight", "bold")
        .text(d => d);
    },
    renderRadarChart() {
      const radarChartElement = document.getElementById('radar-chart');
      const width = radarChartElement.offsetWidth;
      const height = radarChartElement.offsetHeight;
      const data = Object.entries(this.timedata).map(([hour, value]) => ({ hour, value }));

      // 使用 D3 绘制雷达图
      const svg = d3.select(radarChartElement)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

      // 设置雷达图的一些参数，如半径、中心点等
      const centerX = width / 2;
      const centerY = height / 2;
      const radius = Math.max(width, height) / 2 * 0.3;

      // 角度比例尺，根据数据点的数量计算角度
      const angleScale = d3.scaleLinear()
        .domain([0, 24])
        .range([0, Math.PI * 2]);

      // 半径比例尺，根据数据点的值计算半径
      const radiusScale = d3.scaleLinear()
        .domain([0, d3.max(Object.values(this.timedata))])
        .range([0, radius]);

      // 创建雷达图的线生成器
      const line = d3.lineRadial()
        .angle(d => angleScale(parseInt(d.hour)))
        .radius(d => radiusScale(d.value))
        .curve(d3.curveCatmullRomClosed); // 使用光滑的 Catmull-Rom 曲线

      // 绘制雷达图的路径
      svg.append('path')
        .datum(data)
        .attr('fill', 'rgba(105, 179, 162, 0.35)') // 设置透明填充颜色
        .attr('stroke', '#69b3a2')
        .attr('stroke-width', 2)
        .attr('transform', `translate(${centerX}, ${centerY})`)
        .attr('d', line);

      // 添加雷达图的数据点标记
      svg.selectAll('.radar-point')
        .data(data)
        .enter()
        .append('circle')
        .attr('class', 'radar-point')
        .attr('cx', d => centerX + radiusScale(d.value) * Math.cos(angleScale(parseInt(d.hour)) - Math.PI / 2))
        .attr('cy', d => centerY + radiusScale(d.value) * Math.sin(angleScale(parseInt(d.hour)) - Math.PI / 2))
        .attr('r', 4)
        .attr('fill', '#69b3a2')
        .on('mouseover', function (event, d) {
          tooltip.style('opacity', 1);
          d3.select(this).attr('r', 7); // 放大点
        })
        .on('mousemove', function (event, d) {
          tooltip.html(`Hour: ${d.hour}<br>Value: ${d.value}`)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 20) + 'px');
        })
        .on('mouseout', function () {
          tooltip.style('opacity', 0);
          d3.select(this).attr('r', 4); // 恢复原大小
        });

      const tooltip = d3.select('body').append('div')
        .attr('class', 'radar-tooltip')
        .style('position', 'absolute')
        .style('background-color', 'white')
        .style('border', '1px solid #ccc')
        .style('padding', '5px')
        .style('border-radius', '5px')
        .style('pointer-events', 'none')
        .style('opacity', 0);
        
        
      // 添加从中心点到外圈的刻度线
      svg.selectAll('.radar-line')
        .data(data)
        .enter()
        .append('line')
        .attr('class', 'radar-line')
        .attr('x1', centerX)
        .attr('y1', centerY)
        .attr('x2', d => centerX + radius * Math.cos(angleScale(parseInt(d.hour)) - Math.PI / 2))
        .attr('y2', d => centerY + radius * Math.sin(angleScale(parseInt(d.hour)) - Math.PI / 2))
        .attr('stroke', '#ccc')
        .attr('stroke-width', 1);

      // 添加多个圆圈，每增加0.2画一个圈
      const circleIntervals = d3.range(0, d3.max(Object.values(this.timedata)), 0.2);
      svg.selectAll('.radar-circle')
        .data(circleIntervals)
        .enter()
        .append('circle')
        .attr('class', 'radar-circle')
        .attr('cx', centerX)
        .attr('cy', centerY)
        .attr('r', d => radiusScale(d))
        .attr('fill', 'none')
        .attr('stroke', '#ccc')
        .attr('stroke-width', 1);

      // 添加外圈
      svg.append('circle')
        .attr('cx', centerX)
        .attr('cy', centerY)
        .attr('r', radius)
        .attr('fill', 'none')
        .attr('stroke', '#ccc')
        .attr('stroke-width', 2);

      const labelRadius = radius + 5 ; // 标签位置在外圈之外
      svg.selectAll('.radar-label')
        .data(data)
        .enter()
        .append('text')
        .attr('class', 'radar-label')
        .attr('x', d => centerX + (labelRadius + 10) * Math.cos(angleScale(parseInt(d.hour)) - Math.PI / 2))
        .attr('y', d => centerY + (labelRadius + 10) * Math.sin(angleScale(parseInt(d.hour)) - Math.PI / 2))
        .attr('text-anchor', d => {
          const angle = angleScale(parseInt(d.hour));
          if (angle >= 0 && angle < Math.PI / 2) return 'middle';
          if (angle >= Math.PI / 2 && angle < Math.PI * 2 / 2) return 'middle';
          return 'middle';
        })
        .attr('dy', d => {
          const angle = angleScale(parseInt(d.hour));
          if (angle >= Math.PI *0 && angle <= Math.PI * 2 / 6) return '0.7em';
          if (angle >= Math.PI * 10 / 6 && angle < Math.PI * 12 / 6) return '0.7em';
          if (angle == Math.PI * 2) return '0.8em';
          return '0em';
        })
        .style('font-size', '8px')
        .text(d => d.hour);

      // 添加雷达图的中心圆点
      svg.append('circle')
        .attr('class', 'radar-center-point')
        .attr('cx', centerX)
        .attr('cy', centerY)
        .attr('r', 3)
        .attr('fill', '#69b3a2');
    }
  }
}
</script>

<style>
#all-card {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  /* border: 1px solid #ccc; 添加边框
  border-radius: 10px; 添加圆角
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 添加阴影
  padding: 20px; 添加内边距 */
}
/* 上面的提交次数打卡表 */
#check-card {
  width: 100%;
  height: 60%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid #ccc; /* 添加边框 */
  border-radius: 10px; /* 添加圆角 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  /* border: #D0D7DE solid 1px;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px; */
}
/* 下面的24小时详细活跃度表 */
#detail-card {
  width: 100%;
  height: 40%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  /* border-bottom: #D0D7DE solid 1px;
  border-left: #D0D7DE solid 1px;
  border-right: #D0D7DE solid 1px;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px; */
}

#ring-chart {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 50%;
  height: 40%;
  border: 1px solid #ccc; /* 添加边框 */
  border-radius: 10px; /* 添加圆角 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}
#radar-chart {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 50%;
  height: 40%;
  border: 1px solid #ccc; /* 添加边框 */
  border-radius: 10px; /* 添加圆角 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}

.grid-container {
  display: flex;
}
.days {
  display: grid;
  grid-template-columns: 21px;
  grid-template-rows: repeat(7, 21px);
  font-size: 10px;
  color: #aaa;
  padding-inline-start: 0px;
  margin: 20px 0 5px 0; /* 改变 margin */
  margin-left: 20px;
  margin-right: 10px; /* 增加右侧间距 */
  font-size: 10px; /* 增大字体 */
}

.graph {
  display: grid;
  grid-template-columns: 21px repeat(22, 21px); /* 添加一列给周标签 */
  grid-template-rows: repeat(7, 21px);
  padding-inline-start: 0px;
  grid-auto-flow: column;          
  margin: 20px 20px 5px 0; /* 调整 margin 以适应左侧的周标签 */
}

.months {
  display: grid;
  grid-template-columns: repeat(22, 23px);
  grid-template-rows: 23px;
  font-size: 10px;
  color: #aaa;
  padding-inline-start: 0px;
  margin: 5px 20px 5px 20px;
}

.li-month {
  display: inline-block;
}

.li-day {
  background-color: #eaeaea;
  list-style: none;
  margin: 1.5px;
  border-radius: 3px;
}

.li-day:hover {
  box-shadow: 0px 0px 5px rgb(57, 120, 255);
}

.graph li[data-level="0"] {
  background-color: #EBEDF0;
}

.graph li[data-level="1"] {
  background-color: #9BE9A8;
}

.graph li[data-level="2"] {
  background-color: #40C463;
}

.graph li[data-level="3"] {
  background-color: #30A14F;
}

.graph li[data-level="4"] {
  background-color: #216E39;
}

.li-day-label {
  display: inline-block;
  text-align: center;
  margin: 1.5px;
}
</style>
