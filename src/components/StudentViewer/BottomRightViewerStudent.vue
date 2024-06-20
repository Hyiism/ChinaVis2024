<template>
  <div ref="chartContainer" class="chart-container">
    <svg ref="chart"></svg>
  </div>
</template>

<script>
import * as d3 from 'd3';
import { mapGetters } from 'vuex';

export default {
  name: 'SunburstChart',
  data() {
    return {
      preferdata: {
        name: "root",
        knowledge: [
          {
            name: "r8S3g",
            subknowledge: [
              {
                name: "r8S3g_l0p5viby",
                title: [
                  { name: "Question_VgKw8PjY1FR6cm2QI9XW", value: 12 },
                  { name: "Question_q7OpB2zCMmW9wS8uNt3H", value: 12 },
                ]
              },
              {
                name: "r8S3g_n0m9rsw4",
                title: [
                  { name: "Question_q7OpB2zCMmW9wS8uNt3H", value: 12 },
                  { name: "Question_fZrP3FJ4ebUogW9V7taS", value: 12 },
                  { name: "Question_BW0ItEaymH3TkD6S15JF", value: 12 },
                  { name: "Question_rvB9mVE6Kbd8jAY4NwPx", value: 12 },
                ]
              },
            ]
          },
          {
            name: "t5V9e",
            subknowledge: [
              {
                name: "t5V9e_e1k6cixp",
                title: [
                  { name: "Question_3oPyUzDmQtcMfLpGZ0jW", value: 12 },
                  { name: "Question_3MwAFlmNO8EKrpY5zjUd", value: 12 },
                  { name: "Question_x2L7AqbMuTjCwPFy6vNr", value: 12 },
                  { name: "Question_tgOjrpZLw4RdVzQx85h6", value: 12 },
                  { name: "Question_s6VmP1G4UbEQWRYHK9Fd", value: 12 },
                ]
              },
            ]
          },
          {
            name: "m3D1v",
            subknowledge: [
              {
                name: "m3D1v_r1d7fr3l",
                title: [
                  { name: "Question_h7pXNg80nJbw1C4kAPRm", value: 12 },
                  { name: "Question_6RQj2gF3OeK5AmDvThUV", value: 12 },
                  { name: "Question_4nHcauCQ0Y6Pm8DgKlLo", value: 12 },
                  { name: "Question_TmKaGvfNoXYq4FZ2JrBu", value: 12 },
                  { name: "Question_NixCn84GdK2tySa5rB1V", value: 12 },
                  { name: "Question_n2BTxIGw1Mc3Zo6RLdUe", value: 12 },
                  { name: "Question_QRm48lXxzdP7Tn1WgNOf", value: 12 },
                  { name: "Question_pVKXjZn0BkSwYcsa7C31", value: 12 },
                  { name: "Question_oCjnFLbIs4Uxwek9rBpu", value: 12 },
                ]
              },
              {
                name: "m3D1v_v3d9is1x",
                title: [
                  { name: "Question_7NJzCXUPcvQF4Mkfh9Wr", value: 12 },
                  { name: "Question_ZTbD7mxr2OUp8Fz6iNjy", value: 12 },
                  { name: "Question_x2L7AqbMuTjCwPFy6vNr", value: 12 },
                  { name: "Question_tgOjrpZLw4RdVzQx85h6", value: 12 },
                  { name: "Question_s6VmP1G4UbEQWRYHK9Fd", value: 12 },
                ]
              },
              {
                name: "m3D1v_t0v5ts9h",
                title: [
                  { name: "Question_Jr4Wz5jLqmN01KUwHa7g", value: 12 },
                ]
              },
            ]
          },
          {
            name: "y9W5d",
            subknowledge: [
              {
                name: "y9W5d_c0w4mj5h",
                title: [
                  { name: "Question_QRm48lXxzdP7Tn1WgNOf", value: 12 },
                  { name: "Question_pVKXjZn0BkSwYcsa7C31", value: 12 },
                  { name: "Question_Ej5mBw9rsOUKkFycGvz2", value: 12 },
                  { name: "Question_lU2wvHSZq7m43xiVroBc", value: 12 },
                  { name: "Question_Mh4CZIsrEfxkP1wXtOYV", value: 12 },
                  { name: "Question_62XbhBvJ8NUSnApgDL94", value: 12 },
                  { name: "Question_x2Fy7rZ3SwYl9jMQkpOD", value: 12 },
                  { name: "Question_UXqN1F7G3Sbldz02vZne", value: 12 },
                ]
              },
              {
                name: "y9W5d_p8g6dgtv",
                title: [
                  { name: "Question_Ou3f2Wt9BqExm5DpN7Zk", value: 12 },
                  { name: "Question_Az73sM0rHfWVKuc4X2kL", value: 12 },
                ]
              },
              {
                name: "y9W5d_e2j7p95s",
                title: [
                  { name: "Question_EhVPdmlB31M8WKGqL0wc", value: 12 },
                ]
              },
            ]
          },
          {
            name: "k4W1c",
            subknowledge: [
              {
                name: "k4W1c_h5r6nux7",
                title: [
                  { name: "Question_lU2wvHSZq7m43xiVroBc", value: 12 },
                ]
              },
            ]
          },
          {
            name: "s8Y2f",
            subknowledge: [
              {
                name: "s8Y2f_v4x8by9j",
                title: [
                  { name: "Question_x2Fy7rZ3SwYl9jMQkpOD", value: 12 },
                ]
              },
            ]
          },
          {
            name: "g7R2j",
            subknowledge: [
              {
                name: "g7R2j_e0v1yls8",
                title: [
                  { name: "Question_oCjnFLbIs4Uxwek9rBpu", value: 12 },
                  { name: "Question_5fgqjSBwTPG7KUV3it6O", value: 12 },
                  { name: "Question_X3wF8QlTyi4mZkDp9Kae", value: 12 },
                  { name: "Question_xqlJkmRaP0otZcX4fK3W", value: 12 },
                  { name: "", value: 12 },
                ]
              },
              {
                name: "g7R2j_j1g8gd3v",
                title: [
                  { name: "Question_YWXHr4G6Cl7bEm9iF2kQ", value: 12 },
                ]
              },
            ]
          },
          {
            name: "b3C9s",
            subknowledge: [
              {
                name: "b3C9s_l4z6od7y",
                title: [
                  { name: "Question_bumGRTJ0c8p4v5D6eHZa", value: 12 },
                  { name: "Question_hZ5wXofebmTlzKB1jNcP", value: 12 },
                ]
              },
              {
                name: "b3C9s_j0v1yls8",
                title: [
                  { name: "Question_FNg8X9v5zcbB1tQrxHR3", value: 12 },
                ]
              },
            ]
          },
        ]
      }
    };
  },
  computed: {
    ...mapGetters(['studentId'])
  },
  mounted() {
    this.drawChart();
    window.addEventListener('resize', this.drawChart);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.drawChart);
  },
  methods: {
    drawChart() {
      const container = this.$refs.chartContainer;
      const svg = d3.select(this.$refs.chart);

      const width = container.clientWidth;
      const height = container.clientHeight;
      const radius = Math.min(width, height) / 2.2;

      svg.selectAll("*").remove();

      const processData = (data) => {
        const convert = (node) => {
          if (node.title) {
            // return { 
            //   name: node.name, 
            //   value: node.title.reduce((sum, t) => sum + t.value, 0) 
            // };
            return {
              name: node.name,
              children: node.title.map(titleNode => ({
                name: titleNode.name,
                value: titleNode.value
              }))
            };
          }
          const children = node.knowledge || node.subknowledge;
          return { 
            name: node.name, 
            children: children.map(convert) 
          };
        };
        return convert(data);
      };

      const rootData = processData(this.preferdata);
      const root = d3.hierarchy(rootData).sum(d => d.value);

      const partition = d3.partition().size([2 * Math.PI, radius]);

      partition(root);

      const color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, root.children.length + 1));

      const arc = d3.arc()
        .startAngle(d => d.x0)
        .endAngle(d => d.x1)
        .innerRadius(d => d.y0)
        .outerRadius(d => d.y1);

      svg
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${width / 2},${height / 2})`)
        .selectAll('path')
        .data(root.descendants())
        .enter().append('path')
        .attr('d', arc)
        .style('fill', d => color(d.data.name))
        .append('title')
        .text(d => `${d.data.name}\n${d.value}`);
    },
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
