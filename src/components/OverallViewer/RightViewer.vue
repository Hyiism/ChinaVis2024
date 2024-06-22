<template>
  <div ref="chart">
    <div class="dropdown-wrapper">
      <a-dropdown class="dropdown">
        <a class="ant-dropdown-link" @click="e => e.preventDefault()">
          Select Feature <a-icon type="down" />
        </a>
        <a-menu slot="overlay" @click="handleMenuClick">
          <a-menu-item key="Group1">学生标签占比</a-menu-item>
          <a-menu-item key="Group2">做题时间段占比</a-menu-item>
          <a-menu-item key="Group3">男女占比</a-menu-item>
          <a-menu-item key="Group4">专业占比</a-menu-item>
          <a-menu-item key="Group5">编程语言使用占比</a-menu-item>
          <a-menu-item key="Group6">做题状态占比</a-menu-item>
         
          <a-menu-item key="Group1">学生标签占比</a-menu-item>
          <a-menu-item key="Group2">做题时间段占比</a-menu-item>
          <a-menu-item key="Group3">男女占比</a-menu-item>
          <a-menu-item key="Group4">专业占比</a-menu-item>
          <a-menu-item key="Group5">编程语言使用占比</a-menu-item>
          <a-menu-item key="Group6">做题状态占比</a-menu-item>
         
        </a-menu>
      </a-dropdown>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import PubSub from 'pubsub-js';


export default {
  name: "BubblePieChart",
  data() {

    // 将最开始的状态设置为 学生标签占比
    const chartData  = [{ 'class': 'Class1', 'values': [31, 31, 34], 'total': 96 }, { 'class': 'Class10', 'values': [32, 20, 32], 'total': 84 }, { 'class': 'Class11', 'values': [27, 41, 28], 'total': 96 }, { 'class': 'Class12', 'values': [38, 33, 24], 'total': 95 }, { 'class': 'Class13', 'values': [17, 41, 33], 'total': 91 }, { 'class': 'Class14', 'values': [23, 24, 33], 'total': 80 }, { 'class': 'Class15', 'values': [31, 22, 28], 'total': 81 }, { 'class': 'Class2', 'values': [47, 27, 18], 'total': 92 }, { 'class': 'Class3', 'values': [47, 36, 26], 'total': 109 }, { 'class': 'Class4', 'values': [32, 27, 27], 'total': 86 }, { 'class': 'Class5', 'values': [32, 16, 36], 'total': 84 }, { 'class': 'Class6', 'values': [14, 42, 42], 'total': 98 }, { 'class': 'Class7', 'values': [37, 32, 29], 'total': 98 }, { 'class': 'Class8', 'values': [25, 40, 35], 'total': 100 }, { 'class': 'Class9', 'values': [22, 23, 29], 'total': 74 }]
    
    // 男女占比数据
    const chartData_gender = [
      { 'class': 'Class1', 'values': [48.0, 48.0], 'total': 96.0 },
      { 'class': 'Class2', 'values': [41.0, 51.0], 'total': 92.0 },
      { 'class': 'Class3', 'values': [51.0, 58.0], 'total': 109.0 },
      { 'class': 'Class4', 'values': [42.0, 44.0], 'total': 86.0 },
      { 'class': 'Class5', 'values': [49.0, 35.0], 'total': 84.0 },
      { 'class': 'Class6', 'values': [44.0, 54.0], 'total': 98.0 },
      { 'class': 'Class7', 'values': [57.0, 41.0], 'total': 98.0 },
      { 'class': 'Class8', 'values': [47.0, 53.0], 'total': 100.0 },
      { 'class': 'Class9', 'values': [38.0, 36.0], 'total': 74.0 },
      { 'class': 'Class10', 'values': [48.0, 36.0], 'total': 84.0 },
      { 'class': 'Class11', 'values': [47.0, 49.0], 'total': 96.0 },
      { 'class': 'Class12', 'values': [42.0, 53.0], 'total': 95.0 },
      { 'class': 'Class13', 'values': [54.0, 37.0], 'total': 91.0 },
      { 'class': 'Class14', 'values': [44.0, 36.0], 'total': 80.0 },
      { 'class': 'Class15', 'values': [31.0, 50.0], 'total': 81.0 }
    ]
    
    // 学习时间段与总分
    const chartData_time = [{ 'class': 'Class2', 'values': [50.5092125972618, 40.416048834183606, 1.0747385685545796], 'total': 117.37276660541328 },
    { 'class': 'Class10', 'values': [49.63848867871629, 33.584480848102025, 0.7770304731816867], 'total': 109.36225103008965 },
    { 'class': 'Class14', 'values': [43.3472744423269, 36.577692024848055, 0.07503353282502903], 'total': 107.76076696942259 },
    { 'class': 'Class5', 'values': [46.46940193635793, 37.027791903645976, 0.5028061599960593], 'total': 107.42989181358148 },
    { 'class': 'Class3', 'values': [64.1162975713662, 44.34719672212225, 0.5365057065115487], 'total': 115.66433047580146 },
    { 'class': 'Class15', 'values': [43.31760256533903, 36.79864195560382, 0.8837554790571253], 'total': 111.14506949773266 },
    { 'class': 'Class4', 'values': [48.68388258256469, 37.15917951729767, 0.15693790013763373], 'total': 112.29337309706447 },
    { 'class': 'Class13', 'values': [53.39647554866193, 37.130520027666925, 0.4730044236711488], 'total': 107.17844379546719 },
    { 'class': 'Class1', 'values': [59.77841446397387, 35.40263009773567, 0.8189554382904619], 'total': 110.16180021557204 },
    { 'class': 'Class6', 'values': [56.86713668583801, 40.72473027447213, 0.40813303968984377], 'total': 100.33066852293989 },
    { 'class': 'Class11', 'values': [57.786200426817075, 37.1861907567761, 1.0276088164068502], 'total': 111.48708467019877 },
    { 'class': 'Class9', 'values': [44.21980233043908, 28.520653997981036, 1.2595436715798602], 'total': 109.22016824892405 },
    { 'class': 'Class7', 'values': [55.30878566577731, 41.12611131190798, 1.5651030223147082], 'total': 112.90257982235623 },
    { 'class': 'Class8', 'values': [65.84829522056421, 32.80805515736088, 1.3436496220748886], 'total': 107.43093319298745 },
    { 'class': 'Class12', 'values': [51.15072065526562, 42.677268047275795, 1.172011297458573], 'total': 114.56477952341316 }]
   
    // 标签
    const chartData_label = chartData
    
    // 专业
    const chartData_major = [{ 'class': 'Class1', 'values': [16, 18, 26, 17, 19], 'total': 96 }, { 'class': 'Class10', 'values': [15, 22, 12, 19, 16], 'total': 84 }, { 'class': 'Class11', 'values': [22, 18, 20, 18, 18], 'total': 96 }, { 'class': 'Class12', 'values': [18, 14, 20, 23, 20], 'total': 95 }, { 'class': 'Class13', 'values': [19, 15, 23, 15, 19], 'total': 91 }, { 'class': 'Class14', 'values': [14, 16, 13, 16, 21], 'total': 80 }, { 'class': 'Class15', 'values': [3, 23, 21, 20, 14], 'total': 81 }, { 'class': 'Class2', 'values': [21, 13, 26, 20, 12], 'total': 92 }, { 'class': 'Class3', 'values': [16, 27, 22, 22, 22], 'total': 109 }, { 'class': 'Class4', 'values': [17, 19, 21, 15, 14], 'total': 86 }, { 'class': 'Class5', 'values': [25, 17, 9, 17, 16], 'total': 84 }, { 'class': 'Class6', 'values': [18, 16, 19, 22, 23], 'total': 98 }, { 'class': 'Class7', 'values': [14, 23, 21, 21, 19], 'total': 98 }, { 'class': 'Class8', 'values': [24, 19, 22, 24, 11], 'total': 100 }, { 'class': 'Class9', 'values': [16, 17, 16, 11, 14], 'total': 74 }]
    
    // 编程语言使用
    const chartData_method = [{'class': 'Class1', 'values': [3854, 4059, 3814, 3899, 3887], 'total': 110.16180021557204}, {'class': 'Class10', 'values': [2702, 2801, 2575, 2675, 2692], 'total': 109.36225103008965}, {'class': 'Class11', 'values': [2960, 3042, 3140, 2943, 2857], 'total': 111.48708467019877}, {'class': 'Class12', 'values': [2707, 2923, 2776, 2767, 2827], 'total': 114.56477952341316}, {'class': 'Class13', 'values': [3221, 3082, 3309, 3248, 3243], 'total': 107.17844379546719}, {'class': 'Class14', 'values': [2405, 2492, 2299, 2418, 2516], 'total': 107.76076696942259}, {'class': 'Class15', 'values': [2519, 2401, 2449, 2550, 2492], 'total': 111.14506949773266}, {'class': 'Class2', 'values': [2803, 2721, 2697, 2797, 2827], 'total': 117.37276660541328}, {'class': 'Class3', 'values': [3443, 3236, 3252, 3333, 3451], 'total': 115.66433047580146}, {'class': 'Class4', 'values': [2951, 2710, 2815, 2958, 2849], 'total': 112.29337309706447}, {'class': 'Class5', 'values': [2780, 2948, 2795, 2840, 2715], 'total': 107.42989181358148}, {'class': 'Class6', 'values': [4146, 4011, 4011, 4003, 4031], 'total': 100.33066852293989}, {'class': 'Class7', 'values': [3490, 3388, 3447, 3516, 3432], 'total': 112.90257982235623}, {'class': 'Class8', 'values': [4018, 3968, 3962, 3958, 3779], 'total': 107.43093319298745}, {'class': 'Class9', 'values': [2848, 2799, 2852, 2857, 2825], 'total': 109.22016824892405}]
    
    // 四中状态占比
    const chartData_state = [{'class': 'Class1', 'values': [4248.0, 7771.0, 3197.0, 4297.0], 'total': 110.16180021557204}, {'class': 'Class10', 'values': [2853.0, 4690.0, 2532.0, 3370.0], 'total': 109.36225103008965}, {'class': 'Class11', 'values': [2649.0, 5826.0, 2247.0, 4220.0], 'total': 111.48708467019877}, {'class': 'Class12', 'values': [2547.0, 4304.0, 2760.0, 4389.0], 'total': 114.56477952341316}, {'class': 'Class13', 'values': [3154.0, 6323.0, 2848.0, 3778.0], 'total': 107.17844379546719}, {'class': 'Class14', 'values': [2225.0, 4619.0, 2146.0, 3140.0], 'total': 107.76076696942259}, {'class': 'Class15', 'values': [2422.0, 4572.0, 1972.0, 3445.0], 'total': 111.14506949773266}, {'class': 'Class2', 'values': [2519.0, 4093.0, 3134.0, 4099.0], 'total': 117.37276660541328}, {'class': 'Class3', 'values': [3374.0, 6256.0, 2464.0, 4621.0], 'total': 115.66433047580146}, {'class': 'Class4', 'values': [3198.0, 5276.0, 2185.0, 3624.0], 'total': 112.29337309706447}, {'class': 'Class5', 'values': [2954.0, 5366.0, 2590.0, 3168.0], 'total': 107.42989181358148}, {'class': 'Class6', 'values': [4423.0, 8780.0, 3143.0, 3856.0], 'total': 100.33066852293989}, {'class': 'Class7', 'values': [3535.0, 5987.0, 3337.0, 4414.0], 'total': 112.90257982235623}, {'class': 'Class8', 'values': [3818.0, 8621.0, 3192.0, 4054.0], 'total': 107.43093319298745}, {'class': 'Class9', 'values': [2590.0, 5634.0, 2192.0, 3765.0], 'total': 109.22016824892405}]



    // 将最开始的状态设置为 学生标签占比
    const chartData  = [{ 'class': 'Class1', 'values': [31, 31, 34], 'total': 96 }, { 'class': 'Class10', 'values': [32, 20, 32], 'total': 84 }, { 'class': 'Class11', 'values': [27, 41, 28], 'total': 96 }, { 'class': 'Class12', 'values': [38, 33, 24], 'total': 95 }, { 'class': 'Class13', 'values': [17, 41, 33], 'total': 91 }, { 'class': 'Class14', 'values': [23, 24, 33], 'total': 80 }, { 'class': 'Class15', 'values': [31, 22, 28], 'total': 81 }, { 'class': 'Class2', 'values': [47, 27, 18], 'total': 92 }, { 'class': 'Class3', 'values': [47, 36, 26], 'total': 109 }, { 'class': 'Class4', 'values': [32, 27, 27], 'total': 86 }, { 'class': 'Class5', 'values': [32, 16, 36], 'total': 84 }, { 'class': 'Class6', 'values': [14, 42, 42], 'total': 98 }, { 'class': 'Class7', 'values': [37, 32, 29], 'total': 98 }, { 'class': 'Class8', 'values': [25, 40, 35], 'total': 100 }, { 'class': 'Class9', 'values': [22, 23, 29], 'total': 74 }]
    
    // 男女占比数据
    const chartData_gender = [
      { 'class': 'Class1', 'values': [48.0, 48.0], 'total': 96.0 },
      { 'class': 'Class2', 'values': [41.0, 51.0], 'total': 92.0 },
      { 'class': 'Class3', 'values': [51.0, 58.0], 'total': 109.0 },
      { 'class': 'Class4', 'values': [42.0, 44.0], 'total': 86.0 },
      { 'class': 'Class5', 'values': [49.0, 35.0], 'total': 84.0 },
      { 'class': 'Class6', 'values': [44.0, 54.0], 'total': 98.0 },
      { 'class': 'Class7', 'values': [57.0, 41.0], 'total': 98.0 },
      { 'class': 'Class8', 'values': [47.0, 53.0], 'total': 100.0 },
      { 'class': 'Class9', 'values': [38.0, 36.0], 'total': 74.0 },
      { 'class': 'Class10', 'values': [48.0, 36.0], 'total': 84.0 },
      { 'class': 'Class11', 'values': [47.0, 49.0], 'total': 96.0 },
      { 'class': 'Class12', 'values': [42.0, 53.0], 'total': 95.0 },
      { 'class': 'Class13', 'values': [54.0, 37.0], 'total': 91.0 },
      { 'class': 'Class14', 'values': [44.0, 36.0], 'total': 80.0 },
      { 'class': 'Class15', 'values': [31.0, 50.0], 'total': 81.0 }
    ]
    
    // 学习时间段与总分
    const chartData_time = [{ 'class': 'Class2', 'values': [50.5092125972618, 40.416048834183606, 1.0747385685545796], 'total': 117.37276660541328 },
    { 'class': 'Class10', 'values': [49.63848867871629, 33.584480848102025, 0.7770304731816867], 'total': 109.36225103008965 },
    { 'class': 'Class14', 'values': [43.3472744423269, 36.577692024848055, 0.07503353282502903], 'total': 107.76076696942259 },
    { 'class': 'Class5', 'values': [46.46940193635793, 37.027791903645976, 0.5028061599960593], 'total': 107.42989181358148 },
    { 'class': 'Class3', 'values': [64.1162975713662, 44.34719672212225, 0.5365057065115487], 'total': 115.66433047580146 },
    { 'class': 'Class15', 'values': [43.31760256533903, 36.79864195560382, 0.8837554790571253], 'total': 111.14506949773266 },
    { 'class': 'Class4', 'values': [48.68388258256469, 37.15917951729767, 0.15693790013763373], 'total': 112.29337309706447 },
    { 'class': 'Class13', 'values': [53.39647554866193, 37.130520027666925, 0.4730044236711488], 'total': 107.17844379546719 },
    { 'class': 'Class1', 'values': [59.77841446397387, 35.40263009773567, 0.8189554382904619], 'total': 110.16180021557204 },
    { 'class': 'Class6', 'values': [56.86713668583801, 40.72473027447213, 0.40813303968984377], 'total': 100.33066852293989 },
    { 'class': 'Class11', 'values': [57.786200426817075, 37.1861907567761, 1.0276088164068502], 'total': 111.48708467019877 },
    { 'class': 'Class9', 'values': [44.21980233043908, 28.520653997981036, 1.2595436715798602], 'total': 109.22016824892405 },
    { 'class': 'Class7', 'values': [55.30878566577731, 41.12611131190798, 1.5651030223147082], 'total': 112.90257982235623 },
    { 'class': 'Class8', 'values': [65.84829522056421, 32.80805515736088, 1.3436496220748886], 'total': 107.43093319298745 },
    { 'class': 'Class12', 'values': [51.15072065526562, 42.677268047275795, 1.172011297458573], 'total': 114.56477952341316 }]
   
    // 标签
    const chartData_label = chartData
    
    // 专业
    const chartData_major = [{ 'class': 'Class1', 'values': [16, 18, 26, 17, 19], 'total': 96 }, { 'class': 'Class10', 'values': [15, 22, 12, 19, 16], 'total': 84 }, { 'class': 'Class11', 'values': [22, 18, 20, 18, 18], 'total': 96 }, { 'class': 'Class12', 'values': [18, 14, 20, 23, 20], 'total': 95 }, { 'class': 'Class13', 'values': [19, 15, 23, 15, 19], 'total': 91 }, { 'class': 'Class14', 'values': [14, 16, 13, 16, 21], 'total': 80 }, { 'class': 'Class15', 'values': [3, 23, 21, 20, 14], 'total': 81 }, { 'class': 'Class2', 'values': [21, 13, 26, 20, 12], 'total': 92 }, { 'class': 'Class3', 'values': [16, 27, 22, 22, 22], 'total': 109 }, { 'class': 'Class4', 'values': [17, 19, 21, 15, 14], 'total': 86 }, { 'class': 'Class5', 'values': [25, 17, 9, 17, 16], 'total': 84 }, { 'class': 'Class6', 'values': [18, 16, 19, 22, 23], 'total': 98 }, { 'class': 'Class7', 'values': [14, 23, 21, 21, 19], 'total': 98 }, { 'class': 'Class8', 'values': [24, 19, 22, 24, 11], 'total': 100 }, { 'class': 'Class9', 'values': [16, 17, 16, 11, 14], 'total': 74 }]
    
    // 编程语言使用
    const chartData_method = [{'class': 'Class1', 'values': [3854, 4059, 3814, 3899, 3887], 'total': 110.16180021557204}, {'class': 'Class10', 'values': [2702, 2801, 2575, 2675, 2692], 'total': 109.36225103008965}, {'class': 'Class11', 'values': [2960, 3042, 3140, 2943, 2857], 'total': 111.48708467019877}, {'class': 'Class12', 'values': [2707, 2923, 2776, 2767, 2827], 'total': 114.56477952341316}, {'class': 'Class13', 'values': [3221, 3082, 3309, 3248, 3243], 'total': 107.17844379546719}, {'class': 'Class14', 'values': [2405, 2492, 2299, 2418, 2516], 'total': 107.76076696942259}, {'class': 'Class15', 'values': [2519, 2401, 2449, 2550, 2492], 'total': 111.14506949773266}, {'class': 'Class2', 'values': [2803, 2721, 2697, 2797, 2827], 'total': 117.37276660541328}, {'class': 'Class3', 'values': [3443, 3236, 3252, 3333, 3451], 'total': 115.66433047580146}, {'class': 'Class4', 'values': [2951, 2710, 2815, 2958, 2849], 'total': 112.29337309706447}, {'class': 'Class5', 'values': [2780, 2948, 2795, 2840, 2715], 'total': 107.42989181358148}, {'class': 'Class6', 'values': [4146, 4011, 4011, 4003, 4031], 'total': 100.33066852293989}, {'class': 'Class7', 'values': [3490, 3388, 3447, 3516, 3432], 'total': 112.90257982235623}, {'class': 'Class8', 'values': [4018, 3968, 3962, 3958, 3779], 'total': 107.43093319298745}, {'class': 'Class9', 'values': [2848, 2799, 2852, 2857, 2825], 'total': 109.22016824892405}]
    
    // 四中状态占比
    const chartData_state = [{'class': 'Class1', 'values': [4248.0, 7771.0, 3197.0, 4297.0], 'total': 110.16180021557204}, {'class': 'Class10', 'values': [2853.0, 4690.0, 2532.0, 3370.0], 'total': 109.36225103008965}, {'class': 'Class11', 'values': [2649.0, 5826.0, 2247.0, 4220.0], 'total': 111.48708467019877}, {'class': 'Class12', 'values': [2547.0, 4304.0, 2760.0, 4389.0], 'total': 114.56477952341316}, {'class': 'Class13', 'values': [3154.0, 6323.0, 2848.0, 3778.0], 'total': 107.17844379546719}, {'class': 'Class14', 'values': [2225.0, 4619.0, 2146.0, 3140.0], 'total': 107.76076696942259}, {'class': 'Class15', 'values': [2422.0, 4572.0, 1972.0, 3445.0], 'total': 111.14506949773266}, {'class': 'Class2', 'values': [2519.0, 4093.0, 3134.0, 4099.0], 'total': 117.37276660541328}, {'class': 'Class3', 'values': [3374.0, 6256.0, 2464.0, 4621.0], 'total': 115.66433047580146}, {'class': 'Class4', 'values': [3198.0, 5276.0, 2185.0, 3624.0], 'total': 112.29337309706447}, {'class': 'Class5', 'values': [2954.0, 5366.0, 2590.0, 3168.0], 'total': 107.42989181358148}, {'class': 'Class6', 'values': [4423.0, 8780.0, 3143.0, 3856.0], 'total': 100.33066852293989}, {'class': 'Class7', 'values': [3535.0, 5987.0, 3337.0, 4414.0], 'total': 112.90257982235623}, {'class': 'Class8', 'values': [3818.0, 8621.0, 3192.0, 4054.0], 'total': 107.43093319298745}, {'class': 'Class9', 'values': [2590.0, 5634.0, 2192.0, 3765.0], 'total': 109.22016824892405}]


    return {

      chartData,
      chartData_gender,
      chartData_time,
      chartData_label,
      chartData_major,
      chartData_method,
      chartData_state,
      // 字典用于映射Group --> Data
      data_dic: {
        Group1: chartData_label, Group2: chartData_time, Group3: chartData_gender
        , Group4: chartData_major, Group5: chartData_method,Group6: chartData_state
      },



      chartData,
      chartData_gender,
      chartData_time,
      chartData_label,
      chartData_major,
      chartData_method,
      chartData_state,
      // 字典用于映射Group --> Data
      data_dic: {
        Group1: chartData_label, Group2: chartData_time, Group3: chartData_gender
        , Group4: chartData_major, Group5: chartData_method,Group6: chartData_state
      },


      territoryGroups: {
        Group1: ["top1/3", "top2/3", "top3/3"],       
        Group2: ['morning', 'afternoon', 'evening'],
        Group3: ["male", "female"],
        Group4: ['J23517', 'J87654', 'J78901', 'J40192', 'J57489'],
        Group5: ['Method_Cj9Ya2R7fZd6xs1q5mNQ', 'Method_m8vwGkEZc3TSW2xqYUoR', 'Method_BXr9AIsPQhwNvyGdZL57', 'Method_gj1NLb4Jn7URf9K2kQPd', 'Method_5Q4KoXthUuYz3bvrTDFm'],
        Group6: ['Absolutely_Error', 'Error', 'Partially_Correct', 'Absolutely_Correct']
        Group1: ["top1/3", "top2/3", "top3/3"],       
        Group2: ['morning', 'afternoon', 'evening'],
        Group3: ["male", "female"],
        Group4: ['J23517', 'J87654', 'J78901', 'J40192', 'J57489'],
        Group5: ['Method_Cj9Ya2R7fZd6xs1q5mNQ', 'Method_m8vwGkEZc3TSW2xqYUoR', 'Method_BXr9AIsPQhwNvyGdZL57', 'Method_gj1NLb4Jn7URf9K2kQPd', 'Method_5Q4KoXthUuYz3bvrTDFm'],
        Group6: ['Absolutely_Error', 'Error', 'Partially_Correct', 'Absolutely_Correct']
      },
      selectedTerritoryGroup: "Group1",
      classes: ["Class1", "Class2", "Class3", "Class4", "Class5", "Class6", "Class7", "Class8", "Class9", "Class10", "Class11", "Class12", "Class13", "Class14", "Class15"],
      width: 680,
      height: 730,
      margin: { left: 43, bottom: 20, top: 90, right: 0 },
      color: d3.scaleOrdinal(d3.schemeTableau10).domain(["Class1", "Class2", "Class3", "Class4", "Class5", "Class6", "Class7", "Class8", "Class9", "Class10", "Class11", "Class12", "Class13", "Class14", "Class15"]),
      classes: ["Class1", "Class2", "Class3", "Class4", "Class5", "Class6", "Class7", "Class8", "Class9", "Class10", "Class11", "Class12", "Class13", "Class14", "Class15"],
      width: 680,
      height: 730,
      margin: { left: 43, bottom: 20, top: 90, right: 0 },
      color: d3.scaleOrdinal(d3.schemeTableau10).domain(["Class1", "Class2", "Class3", "Class4", "Class5", "Class6", "Class7", "Class8", "Class9", "Class10", "Class11", "Class12", "Class13", "Class14", "Class15"]),
      legend: null,
      slice: null,
      pct: null
    };
  },
  mounted() {
    this.drawChart();
  },
  methods: {
    handleMenuClick({ key }) {
      this.selectedTerritoryGroup = key;

      // 替换数据
      console.log('data_dic', this.data_dic)
      this.chartData = this.data_dic[key]
      console.log('chartData', this.chartData)


      // 替换数据
      console.log('data_dic', this.data_dic)
      this.chartData = this.data_dic[key]
      console.log('chartData', this.chartData)

      this.updateChart();
    },
    handlePieClick(event, d) {
      PubSub.publish('classChange', d.class);
    },
    drawChart() {

      console.log('data_dic_drawChart', this.data_dic)

      console.log('data_dic_drawChart', this.data_dic)
      const { chartData, territoryGroups, selectedTerritoryGroup, classes, width, height, margin, color } = this;
      const territories = territoryGroups[selectedTerritoryGroup];


      const svg = d3.select(this.$refs.chart)
        .append("svg")
        .attr("font-size", "10pt")
        .attr("cursor", "default")
        .attr("viewBox", [0, 0, width, height])
        .attr("width", width)
        .attr("height", height);

      const x = d3.scaleBand()
        .domain(classes)
        .range([margin.left, width - margin.left - margin.right]);

      const hx = x.bandwidth() / 2;

      const y = d3.scaleLinear()
        .domain(d3.extent(chartData.map(d => d.total)))
        .range([height - margin.top - margin.bottom, margin.top]);

      const r = d3.scaleLinear()
        .domain(d3.extent(chartData.map(d => d.total)))
        .range([hx / 2, hx]);

      const toCurrency = num => d3.format(".2f")(num);
      const toCurrency = num => d3.format(".2f")(num);

      const drawGuidelines = (g, data, line) => {
        g.selectAll("path")
          .data(data)
          .join("path")
          .attr("stroke", "#ddd")
          .attr("stroke-dasharray", "5,5")
          .attr("d", line);
      };

      svg.append("g").call(g => drawGuidelines(g, classes,
        d => d3.line()([[x(d) + hx, margin.top], [x(d) + hx, height - margin.bottom]]))
      );
        d => d3.line()([[x(d) + hx, margin.top], [x(d) + hx, height - margin.bottom]]))
      );

      svg.append("g").call(g => drawGuidelines(g, y.ticks().reverse().slice(1),
        d => d3.line()([[margin.left, y(d)], [width - margin.left - margin.right, y(d)]]))
      );
        d => d3.line()([[margin.left, y(d)], [width - margin.left - margin.right, y(d)]]))
      );

      const g = svg.selectAll(".pie")
        .data(chartData)
        .join("g")
        .attr("class", "pie")
        .attr("transform", d => `translate(${x(d.class) + hx},${y(d.total)})`)
        .call(g => g.append("text")
          .attr("dy", "1em")
          .attr("text-anchor", "middle")
          .attr("transform", d => `translate(0,${r(d.total)})`)
          .text(d => toCurrency(d.total)));
          .text(d => toCurrency(d.total)));

      const pg = g.selectAll("g")
        .data(d => d3.pie()(d.values).map(p => ({ pie: p, total: d.total ,class: d.class})))
        .join("g")
        .call(g => g.append("title")
          .text((d, i) => `${territories[i]}\n${toCurrency(d.pie.value)} (${(d.pie.value / d.total * 100).toFixed(1)}%)`));
          .text((d, i) => `${territories[i]}\n${toCurrency(d.pie.value)} (${(d.pie.value / d.total * 100).toFixed(1)}%)`));

      const pie = d => d3.arc()
        .innerRadius(0)
        .outerRadius(r(d.total))
        .startAngle(d.pie.startAngle)
        .endAngle(d.pie.endAngle);

      this.slice = pg.append("path")
        .attr("d", d => pie(d)())
        .attr("opacity", 1)
        .attr("fill", (d, i) => color(territories[i]));
        .attr("opacity", 1)
        .attr("fill", (d, i) => color(territories[i]))

      this.pct = pg.append("text")
        .attr("text-anchor", "middle")
        .attr("fill", "white")
        .attr("transform", (d, i) => {
          const c = pie(d).centroid(d.pie.value);
          return `translate(${c[0]},${c[1]})`;
        })
        .attr("opacity", "0")
        .text(d => (d.pie.value / d.total * 100).toFixed(1) + "%");

      svg.append("g").call(g => this.drawAxis(g, margin.left, 0, d3.axisLeft(y).ticks(height / 100, "s")));
      svg.append("g").call(g => this.drawAxis(g, 0, height - margin.bottom, d3.axisBottom(x)));
      svg.append("g").call(this.drawLegend);
      return svg.node();
    },

    drawAxis(g, x, y, axis) {
      g.attr("transform", `translate(${x},${y})`)
        .call(axis)
        .selectAll(".tick text")
        .attr("font-size", "8pt");
    },

    drawLegend(g) {
      const { territoryGroups, selectedTerritoryGroup, color, margin, width } = this;
      const territories = territoryGroups[selectedTerritoryGroup];
      pg.on('click', this.handlePieClick);

      this.pct = pg.append("text")
        .attr("text-anchor", "middle")
        .attr("fill", "white")
        .attr("transform", (d, i) => {
          const c = pie(d).centroid(d.pie.value);
          return `translate(${c[0]},${c[1]})`;
        })
        .attr("opacity", "0")
        .text(d => (d.pie.value / d.total * 100).toFixed(1) + "%");

      svg.append("g").call(g => this.drawAxis(g, margin.left, 0, d3.axisLeft(y).ticks(height / 100, "s")));
      svg.append("g").call(g => this.drawAxis(g, 0, height - margin.bottom, d3.axisBottom(x)));
      svg.append("g").call(this.drawLegend);
      return svg.node();
    },

    drawAxis(g, x, y, axis) {
      g.attr("transform", `translate(${x},${y})`)
        .call(axis)
        .selectAll(".tick text")
        .attr("font-size", "8pt");
    },

      this.legend = g.attr("transform", `translate(${margin.left + 20}, ${margin.top - 60})`)
        .selectAll("g")
    drawLegend(g) {
      const { territoryGroups, selectedTerritoryGroup, color, margin, width } = this;
      const territories = territoryGroups[selectedTerritoryGroup];

      this.legend = g.attr("transform", `translate(${margin.left + 20}, ${margin.top - 60})`)
        .selectAll("g")
        .data(territories)
        .join("g")
        .attr("transform", (d, i) => `translate(0,${i * 20})`)
        .call(g => g.append("rect")
          .attr("rx", 3).attr("ry", 3)
          .attr("width", 20).attr("height", 15)
          .attr("fill", d => color(d)))
        .call(g => g.append("text").attr("dx", 25).attr("alignment-baseline", "hanging").text(d => d))
        .on("mouseover", this.highlight)
        .on("mouseout", () => this.highlight());
    },
    highlight(e) {
      const i = e ? this.legend.nodes().indexOf(e.currentTarget) : -1;
      this.slice.transition().duration(500).attr("opacity", (d, j) => i === -1 || j === i ? 1 : 0.3);
      this.pct.transition().duration(500)
        .attr("opacity", function (d, j) {
          if (j === i) {
            this.parentNode.parentNode.appendChild(this.parentNode);
            return 1;
          }
          else return 0;
        });
        .attr("transform", (d, i) => `translate(0,${i * 20})`)
        .call(g => g.append("rect")
          .attr("rx", 3).attr("ry", 3)
          .attr("width", 20).attr("height", 15)
          .attr("fill", d => color(d)))
        .call(g => g.append("text").attr("dx", 25).attr("alignment-baseline", "hanging").text(d => d))
        .on("mouseover", this.highlight)
        .on("mouseout", () => this.highlight());
    },
    highlight(e) {
      const i = e ? this.legend.nodes().indexOf(e.currentTarget) : -1;
      this.slice.transition().duration(500).attr("opacity", (d, j) => i === -1 || j === i ? 1 : 0.3);
      this.pct.transition().duration(500)
        .attr("opacity", function (d, j) {
          if (j === i) {
            this.parentNode.parentNode.appendChild(this.parentNode);
            return 1;
          }
          else return 0;
        });
    },
    updateChart() {
      // 清除之前的画布
      d3.select(this.$refs.chart).selectAll("svg").remove();


      // 重新绘制图表
      this.drawChart();
    },
    toCurrency(num) {
      return d3.format(".2f")(num);
      // 清除之前的画布
      d3.select(this.$refs.chart).selectAll("svg").remove();


      // 重新绘制图表
      this.drawChart();
    },
    toCurrency(num) {
      return d3.format(".2f")(num);
    }
  }
};
</script>

<style scoped>
svg {
  font-family: sans-serif;
svg {
  font-family: sans-serif;
}


.dropdown-wrapper {
  position: absolute;
  top: 30px;
  right: 40px;
  /* left: 10px; */
  position: absolute;
  top: 30px;
  right: 40px;
  /* left: 10px; */
}
</style>
