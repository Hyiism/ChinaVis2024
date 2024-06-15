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
      <p>用来展示所选日期的24小时活跃度情况</p>
    </div>
  </div>
</template>

<script>
import EventBus from '@/eventBus'; // 导入事件总线

export default {
  name: 'CheckChart',
  data() {
    return {
      infos: [],
      // monthBar: ["Aug", "Sep", "Oct", "Nov", "Des", "Jau"],
      // weekBar: ["Mon", "周二", "周三", "周四", "周五", "周六", "周日"],
    };
  },

  created() {
    this.fetchStudentScores();
  },

  methods: {
    fetchStudentScores() {
      this.$axios.get('http://10.12.44.190:8000/get_check_data/?student_id=r28s9kyo7knrvytyvmt8')
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
      // console.log(item.year + "1" + item.month + "1" + item.date);
      // 点击传数据到modelview执行操作
      EventBus.$emit('checkSelected', {student_id:'r28s9kyo7knrvytyvmt8', 'year':item.year, 'month':item.month, 'date':item.date}); // 触发事件，传递 student_id
    }
  }
}
</script>

<style>
#all-card {
  width: 90%;
  height: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
/* 上面的提交次数打卡表 */
#check-card {
  width: 100%;
  height: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  /* border: #D0D7DE solid 1px;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px; */
}
/* 下面的24小时详细活跃度表 */
#detail-card {
  width: 100%;
  height: 50%;
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
