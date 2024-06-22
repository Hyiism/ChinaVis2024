<template>
    <div ref="chartContainer" style="width: 100%; height: 100%;">
        <div class="tooltip" v-show="tooltipVisible" :style="tooltipStyle">{{ tooltipText }}</div>
        <div class="tooltipStart" v-show="tooltipVisibleStart" :style="tooltipStyleStart">{{ tooltipTextStart }}</div>
        <div class="tooltipEnd" v-show="tooltipVisibleEnd" :style="tooltipStyleEnd">{{ tooltipTextEnd }}</div>
    </div>
</template>

<script>
import * as d3 from 'd3';
import axios from 'axios';
import PubSub from 'pubsub-js';

export default {
    name: 'TimeSelectionChart',
    data() {
        return {
            tooltipVisible: false,
            tooltipText: '',
            tooltipStyle: {
                position: 'absolute',
                textAlign: 'center',
                width: '50px',
                height: '27px',
                padding: '2px',
                font: '12px sans-serif',
                background: 'white',
                border: '0px',
                borderRadius: '8px',
                pointerEvents: 'none',
                opacity: 1,
                left: '0px',
                top: '0px'
            },
            tooltipVisibleStart: false,
            tooltipTextStart: '',
            tooltipStyleStart: {
                position: 'absolute',
                textAlign: 'center',
                width: '50px',
                height: '27px',
                padding: '2px',
                font: '12px sans-serif',
                background: 'white',
                border: '0px',
                borderRadius: '8px',
                left: '0px',
                top: '0px',
            },
            tooltipVisibleEnd: false,
            tooltipTextEnd: '',
            tooltipStyleEnd: {
                position: 'absolute',
                textAlign: 'center',
                width: '50px',
                height: '27px',
                padding: '2px',
                font: '12px sans-serif',
                background: 'white',
                border: '0px',
                borderRadius: '8px',
                zIndex: 1
            },
            selectedDate: "Thu Aug 31 2023",
            className : 'Class1'
        };
    },
    mounted() {
        this.drawChart();
        this.token = PubSub.subscribe('dateSelected', (msg, value) => {
            this.selectedDate = value;
            console.log(this.selectedDate);
            this.redrawChart();
        });
    },
    methods: {
        drawChart() {
            const margin = { top: 0, right: 0, bottom: 0, left: 0 };
            // const chartContainerWidth = this.$refs.chartContainer.clientWidth;
            const chartContainerWidth = 1268;
            console.log('chartContainerWidth', chartContainerWidth)
            const width = chartContainerWidth;
            const height = 65;
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

            const baseDate = new Date(this.selectedDate);
            const data = d3.range(1440).map((d, i) => ({
                date: new Date(baseDate.getTime() + i * 60000), // 每分钟增加一次
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
                .style("fill", "#BBE3A5")
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
            let startXPosition = null;
            let startYPosition = null;

            // 添加刷子
            const brush = d3.brushX()
                .extent([[0, 0], [width, height]])
                .on('start', (event) => {
                    // 获取刷子的起始位置
                    const [mouseXStart, mouseYStart] = d3.pointer(event, window);
                    startXPosition = mouseXStart;
                    startYPosition = mouseYStart;
                })
                .on('brush', (event) => {
                    const selection = event.selection;
                    if (selection) {
                        const [x0, x1] = selection.map(x.invert);
                        const [mouseXEnd, mouseYEnd] = d3.pointer(event, window);
                        // 显示悬浮时间
                        this.tooltipVisibleStart = true;
                        this.tooltipVisibleEnd = true;
                        this.tooltipStyleStart.left = startXPosition + 'px';
                        this.tooltipStyleStart.top = startYPosition + 'px';

                        this.tooltipStyleEnd.left = mouseXEnd + 'px';
                        this.tooltipStyleEnd.top = mouseYEnd + 'px';
                        this.tooltipTextStart = `${x0.toLocaleTimeString()}`;
                        this.tooltipTextEnd = `${x1.toLocaleTimeString()}`;
                    }
                })
                .on('end', (event) => {
                    const selection = event.selection;
                    if (selection) {
                        const [x0, x1] = selection.map(x.invert);
                        const start = this.selectedDate + ' ' + x0.toLocaleTimeString();
                        const end = this.selectedDate + ' ' + x1.toLocaleTimeString();
                        // 调用发送数据到后端的方法
                        this.sendDataToBackend(start,end,this.className);
                        console.log("发送",x0, x1)
                        this.tooltipVisibleStart = false;
                        this.tooltipVisibleEnd = false;
                    }
                });
            const brushGroup = svg.append('g')
                .attr('class', 'brush')
                .call(brush);

            // 添加全局点击事件监听器，点击时清除刷子
            d3.select('body').on('click', (event) => {
                const isClickInsideBrush = event.target.closest('.brush');
                if (!isClickInsideBrush) {
                    brushGroup.call(brush.move, null);
                }
            });
        },
        redrawChart() {
            // 在这里重新绘制图表
            d3.select(this.$refs.chartContainer).select('svg').remove(); // 移除旧的图表
            this.drawChart(); // 重新调用绘图方法
        },
        sendDataToBackend(startTime, endTime, className) {
            // 使用axios发送数据到后端
            this.$axios.get(`http://10.12.44.190:8000/getStudentByTime/?startTime=${startTime}&endTime=${endTime}&className=${className}`, {
                // params: {
                //     startTime: startTime, // 使用toISOString()将日期转换为ISO格式
                //     endTime: endTime,
                //     className: className
                // }
            })
                .then(response => {
                    PubSub.publish('studentAppear', JSON.parse(response.data));

                })
                .catch(error => {
                    console.error('Error sending data:', error);
                });
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

.brush .selection {
    fill: #8884d8;
    fill-opacity: 0.5;
}

.bar {
    fill: #AAFAAA;
}


.background {
    fill: #F29897;
}
</style>