import Vue from 'vue'
import App from './App.vue'
import axios from 'axios';
import ElementUI from 'element-ui';
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import 'element-ui/lib/theme-chalk/index.css';
// 贡献图组件库
// import ActivityCalendar from "vue-activity-calendar";
// import "vue-activity-calendar/style.css"; 

Vue.use(ElementUI);
Vue.use(Antd);
// Vue.use(ActivityCalendar);
Vue.prototype.$axios = axios;

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
