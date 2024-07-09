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
import { mapGetters } from 'vuex';

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
            selectedDate: "Thu Sep 14 2023",
            stvalue: d3.range(1440).map(Math.random),
            initialLoad: true, // 标识是否是初次加载
        };
    },
    computed: {
        ...mapGetters(['classId'])
    },
    mounted() {
        this.token = PubSub.subscribe('dateSelected', (msg, value) => {
            this.selectedDate = value;
            this.initialLoad = false; // 设置为非初次加载
            this.redrawChart();
        });
        this.token = PubSub.subscribe('showAll', (msg, value) => {
            this.stvalue = d3.range(1440).map(Math.random)
            this.redrawChart();
        });
        this.drawChart();
    },
    methods: {
        initTooltipStyle() {
            return {
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
            };
        },
        formatDate(dateStr) {
            const dateObj = new Date(dateStr);
            const year = dateObj.getFullYear();
            const month = dateObj.getMonth() + 1;
            const day = dateObj.getDate();
            return `${year}.${month}.${day}`;
        },
        fetchStudentData(dayTime, classId) {
            return axios.get(`http://10.12.44.190:8000/getStudentByTime_1/?dayTime=${dayTime}&classId=${classId}`)
                .then(response => {
                    this.stvalue = response.data;
                    this.initialLoad = false; // 设置为非初次加载
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        },
        drawChart() {
            if (!this.initialLoad) {
                const dayTime = this.formatDate(this.selectedDate);
                this.fetchStudentData(dayTime, this.classId).then(() => {
                    this.createSvgChart();
                });
            } else {
                this.createSvgChart();
            }
        },
        createSvgChart() {
            const margin = { top: 0, right: 0, bottom: 0, left: 0 };
            const chartContainerWidth = 1268;
            const width = chartContainerWidth;
            const height = 65;
            const svg = d3.select(this.$refs.chartContainer)
                .append('svg')
                .attr('width', chartContainerWidth)
                .attr('height', height + margin.top + margin.bottom)
                .append('g')
                .attr('transform', `translate(${margin.left},${margin.top})`);

            this.drawBackground(svg, width, height);
            const data = this.prepareChartData();
            this.drawBars(svg, data, width, height);
            this.addBrush(svg, width, height, data);
        },
        drawBackground(svg, width, height) {
            svg.append('rect')
                .attr('class', 'background')
                .style("fill", "#E59C8E")
                .attr('x', 0)
                .attr('y', 0)
                .attr('width', width)
                .attr('height', height);
        },
        prepareChartData() {
            const baseDate = new Date(this.selectedDate);
            return d3.range(1440).map((d, i) => ({
                date: new Date(baseDate.getTime() + i * 60000),
                value: this.stvalue[i]
            }));
        },
        drawBars(svg, data, width, height) {
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

        },
        showTooltip(event, d) {
            this.tooltipVisible = true;
            this.tooltipText = d.date.toLocaleTimeString();
            this.tooltipStyle.left = (event.pageX + 5) + 'px';
            this.tooltipStyle.top = (event.pageY - 28) + 'px';
        },
        hideTooltip() {
            this.tooltipVisible = false;
        },
        addBrush(svg, width, height, data) {
            let startXPosition = null;
            let startYPosition = null;

            const x = d3.scaleTime()
                .domain(d3.extent(data, d => d.date))
                .range([0, width]);

            const brush = d3.brushX()
                .extent([[0, 0], [width, height]])
                .on('start', (event) => {
                    const [mouseXStart, mouseYStart] = d3.pointer(event, window);
                    startXPosition = mouseXStart;
                    startYPosition = mouseYStart;
                })
                .on('brush', (event) => {
                    const selection = event.selection;
                    if (selection) {
                        const [x0, x1] = selection.map(x.invert);
                        const [mouseXEnd, mouseYEnd] = d3.pointer(event, window);
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
                        this.sendDataToBackend(start, end, this.classId);
                        this.tooltipVisibleStart = false;
                        this.tooltipVisibleEnd = false;
                    }
                });

            const brushGroup = svg.append('g')
                .attr('class', 'brush')
                .call(brush);

            d3.select('body').on('click', (event) => {
                const isClickInsideBrush = event.target.closest('.brush');
                if (!isClickInsideBrush) {
                    brushGroup.call(brush.move, null);
                }
            });
        },
        redrawChart() {
            d3.select(this.$refs.chartContainer).select('svg').remove();
            this.drawChart();
        },
        sendDataToBackend(startTime, endTime, classId) {
            axios.get(`http://10.12.44.190:8000/getStudentByTime/?startTime=${startTime}&endTime=${endTime}&className=${classId}`)
                .then(response => {
                    PubSub.publish('studentAppear', JSON.parse(response.data));
                })
                .catch(error => {
                    console.error('Error sending data:', error);
                });
        },
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
