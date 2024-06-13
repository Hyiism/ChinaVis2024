<template>
  <div class="chart-container-bottomcenter">
    <!-- 使用 radio 组件 -->
    <radio :options="options" v-model="selectedOption" />
    <p>Selected Option: {{ selectedOption }}</p>
  </div>
</template>

<script>
import { radio } from "@jashkenas/inputs"

export default {
  components: {
    radio
  },
  data() {
    return {
      // 定义选项
      options: ["Lust", "Gluttony", "Greed", "Sloth", "Wrath", "Envy", "Pride"],
      // 绑定选择的值
      selectedOption: null
    };
  },

}

</script>

<style scoped>
.chart-container-bottomcenter {
  width: 100%;
  height: 100%;
}
.radio input[type=radio] {
  width: 100%;
  height: 100%;
}

</style>
