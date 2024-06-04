<template>
    <svg ref="chart"></svg>
</template>

<script>

import * as d3 from 'd3';

export default {
    name: 'TimeLine',
    components: {

    },

    data() {

        return {

        };
    },
    mounted() {
        this.drawChart();
    },
    methods: {
        drawChart() {
            // Set the dimensions and margins of the graph
            const margin = { top: 10, right: 30, bottom: 30, left: 40 };
            const width = 1000 - margin.left - margin.right;
            const height = 100 - margin.top - margin.bottom;

            // Append the svg object to the body of the page
            const svg = d3.select(this.$refs.chart)
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", `translate(${margin.left},${margin.top})`);

            // Add background rect
            svg.append("rect")
                .attr("class", "background")
                .attr("x", 0)
                .attr("y", 0)
                .attr("width", width)
                .attr("height", height);

            // Create a tooltip
            const tooltip = d3.select(".tooltip");

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
                .attr("x", d => x(d.date))
                .attr("width", width / data.length) // 柱子更细，且无间隙
                .attr("y", d => y(d.value))
                .attr("height", d => height - y(d.value))
                .on("mouseover", function (event, d) {
                    tooltip.transition()
                        .duration(200)
                        .style("opacity", .9);
                    tooltip.html(d.date.toLocaleTimeString())
                        .style("left", (event.pageX + 5) + "px")
                        .style("top", (event.pageY - 28) + "px");
                })
                .on("mouseout", function (d) {
                    tooltip.transition()
                        .duration(500)
                        .style("opacity", 0);
                });

            // Add the area above the bars
            const area = d3.area()
                .x(d => x(d.date))
                .y0(y(0))
                .y1(d => y(d.value));

            svg.append("path")
                .datum(data)
                .attr("class", "area")
                .attr("d", area);

            // Add brushing
            svg.append("g")
                .attr("class", "brush")
                .call(d3.brushX()
                    .extent([[0, 0], [width, height]])
                    .on("end", this.updateChart));
        },

    },

}
</script>

<style scoped></style>