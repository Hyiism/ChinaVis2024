<!-- <template>
    <div id="timeline" ref="timeLine" class="time-line">
        <svg ref="svgElement"></svg>
    </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'TimeLine',
    data() {
        return {};
    },
    mounted() {
        this.drawChart();
    },
    methods: {
        drawChart() {
            const margin = { top: 0, right: 30, bottom: 30, left: 0 };
            const width = this.$refs.timeLine.clientWidth;
            const height = this.$refs.timeLine.clientHeight;

            const svg = d3.select(this.$refs.svgElement)
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", `translate(${margin.left},${margin.top})`);

            // Add background rect
            svg.append("rect")
                .attr("class", "background")
                .style("fill", "#F29897")
                .attr("x", 0)
                .attr("y", 0)
                .attr("width", width)
                .attr("height", height);

            const tooltip = d3.select("#timeline").append("div")
                .attr("class", "tooltip")
                .style("opacity", 0);

            // Generate more random data
            const data = d3.range(500).map((d, i) => ({
                date: new Date(2023, 3, 13, 0, i * 1, 0),
                value: Math.random()
            }));

            // X axis
            const x = d3.scaleTime()
                .domain(d3.extent(data, d => d.date))
                .range([0, width]);

            // Y axis
            const y = d3.scaleLinear()
                .domain([0, 1])
                .range([height, 0]);

            // Add the bars
            svg.selectAll(".bar")
                .data(data)
                .enter().append("rect")
                .attr("class", "bar")
                .style("fill", "#AAFAAA")
                .attr("x", d => x(d.date))
                .attr("width", width / data.length) // 柱子更细，且无间隙
                .attr("y", d => y(d.value))
                .attr("height", d => height - y(d.value))
                .on("mouseover", function(event, d) {
                    tooltip.transition()
                        .duration(200)
                        .style("opacity", .9);
                    tooltip.html(d.date.toLocaleTimeString())
                        .style("left", (event.pageX + 5) + "px")
                        .style("top", (event.pageY - 28) + "px");
                })
                .on("mouseout", function() {
                    tooltip.transition()
                        .duration(500)
                        .style("opacity", 0);
                });

            // Add brushing (uncomment if needed)
            // svg.append("g")
            //     .attr("class", "brush")
            //     .call(d3.brushX()
            //         .extent([[0, 0], [width, height]])
            //         .on("end", this.updateChart))
            //     .on("mouseover", function(event, d) {
            //         console.log("Mouse over:", d);
            //     })
            //     .on("click", function(event, d) {
            //         console.log("Mouse out:", d);
            //     });
        },
        updateChart() {
            // Brushing functionality (if needed)
        }
    }
};
</script>

<style scoped>
.time-line {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}

#timeline .tooltip {
    position: absolute;
    text-align: center;
    width: 60px;
    height: 18px;
    padding: 2px;
    font: 12px sans-serif;
    background: white;
    border: 0px;
    border-radius: 8px;
    pointer-events: none;
    opacity: 0;
}
</style> -->

<template>
    <div ref="chartContainer" style="width: 100%">
      <div class="tooltip" v-show="tooltipVisible" :style="tooltipStyle">{{ tooltipText }}</div>
    </div>
  </template>
  
  <script>
  import * as d3 from 'd3';
  
  export default {
    name: 'TimeSelectionChart',
    data() {
      return {
        tooltipVisible: false,
        tooltipText: '',
        tooltipStyle: {
          position: 'absolute',
          textAlign: 'center',
          width: '60px',
          height: '18px',
          padding: '2px',
          font: '12px sans-serif',
          background: 'white',
          border: '0px',
          borderRadius: '8px',
          pointerEvents: 'none',
          opacity: 1,
          left: '0px',
          top: '0px'
        }
      };
    },
    mounted() {
      this.drawChart();
    },
    methods: {
      drawChart() {
        const margin = { top: 28, right: 30, bottom: 30, left: 0 };
        const chartContainerWidth = this.$refs.chartContainer.clientWidth;
        const width = chartContainerWidth - margin.left - margin.right;
        const height = 100 - margin.top - margin.bottom;
        // console.log(this.$refs.chartContainer.clientWidth)
  
        const svg = d3.select(this.$refs.chartContainer)
          .append('svg')
          .attr('width', chartContainerWidth)
          .attr('height', height + margin.top + margin.bottom)
          .append('g')
          .attr('transform', `translate(${margin.left},${margin.top})`);
  
        svg.append('rect')
          .attr('class', 'background')
          .style("fill", "#F29897")
          .attr('x', 0)
          .attr('y', 0)
          .attr('width', chartContainerWidth)
          .attr('height', height);
  
        const data = d3.range(500).map((d, i) => ({
          date: new Date(2023, 3, 13, 0, i * 1, 0),
          value: Math.random()
        }));
  
        const x = d3.scaleTime()
          .domain(d3.extent(data, d => d.date))
          .range([0, width]);
  
        const y = d3.scaleLinear()
          .domain([0, 1])
          .range([height, 0]);
  
        svg.selectAll('.bar')
          .data(data)
          .enter().append('rect')
          .attr('class', 'bar')
          .style("fill", "#AAFAAA")
          .attr('x', d => x(d.date))
          .attr('width', width / data.length)
          .attr('y', d => y(d.value))
          .attr('height', d => height - y(d.value))
          .on('mouseover', (event, d) => {
            this.tooltipVisible = true;
            this.tooltipText = d.date.toLocaleTimeString();
            this.tooltipStyle.left = (event.pageX + 5) + 'px';
            this.tooltipStyle.top = (event.pageY - 28) + 'px';
          })
          .on('mouseout', () => {
            this.tooltipVisible = false;
          });
  
        // const brush = d3.brushX()
        //   .extent([[0, 0], [width, height]])
        //   .on('end', this.updateChart);
  
        // svg.append('g')
        //   .attr('class', 'brush')
        //   .call(brush);
      },
      updateChart(event) {
        const extent = event.selection;
        if (!extent) return;
  
        const x = d3.scaleTime().domain(d3.extent(data, d => d.date)).range([0, width]);
        const selectedTimeRange = [
          x.invert(extent[0]),
          x.invert(extent[1])
        ];
  
        console.log("Selected time range:", selectedTimeRange);
      }
    }
  };
  </script>
  
  <style scoped>

.chartContainer {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}

  .tooltip {
    opacity: 0;
  }
  
  .brush .selection {
    fill: #8884d8;
    fill-opacity: 0.5;
  }
  
  .bar {
    fill: #AAFAAA;
  }
/*   
  .border {
    stroke: #000;
    stroke-width: 1px;
    fill: #f8f8f8;
  } */
  
  .background {
    fill: #F29897;
  }
  </style>
  