<template>
  <div id="app">
    <div id="titleAll">
      <h2>XXX可视化系统</h2>
    </div>


    <!--                       整体视图组件                            -->
    <div id="LeftViewer" v-if="currentView.LeftViewer">
      <LeftViewer />
    </div>

    <div id="LeftBottomViewer" v-if="currentView.LeftBottomViewer">
      <LeftBottomViewer/>
    </div>

    <div id="ModelViewer">
      <ModelViewer @stateChanged="handleStateChange" :stateCode="initialStateCode""/>
    </div>

    <div id="RightViewer" v-if="currentView.RightViewer">
      <RightViewer/>
    </div>

    <div id="BottomViewer" v-if="currentView.BottomViewer">
      <BottomViewer/>
    </div>

    <div id="BottomCenterViewer" v-if="currentView.BottomCenterViewer">
      <BottomCenterViewer/>
    </div>

    <div id="BottomRightViewer" v-if="currentView.BottomRightViewer">
      <BottomRightViewer/>
    </div>

    <div id="TimeLine">
      <TimeLine/>
    </div>

        <!--                       班级视图组件                            -->
    <div id="LeftViewerClass" v-if="currentView.LeftViewerClass">
      <LeftViewerClass/>
    </div>

    <div id="LeftBottomViewerClass" v-if="currentView.LeftBottomViewerClass">
      <LeftBottomViewerClass/>
    </div>

    <div id="RightViewerClass" v-if="currentView.RightViewerClass">
      <RightViewerClass/>
    </div>

    <div id="BottomViewerClass" v-if="currentView.BottomViewerClass">
      <BottomViewerClass/>
    </div>

    <div id="BottomCenterViewerClass" v-if="currentView.BottomCenterViewerClass">
      <BottomCenterViewerClass/>
    </div>

    <div id="BottomRightViewerClass" v-if="currentView.BottomRightViewerClass">
      <BottomRightViewerClass/>
    </div>

      <!--           学生视图组件              -->
      <div id="LeftViewerStudent" v-if="currentView.LeftViewerStudent">
      <LeftViewerStudent/>
    </div>

    <div id="LeftBottomViewerStudent" v-if="currentView.LeftBottomViewerStudent">
      <LeftBottomViewerStudent/>
    </div>

    <div id="RightViewerStudent" v-if="currentView.RightViewerStudent">
      <RightViewerStudent/>
    </div>

    <div id="BottomViewerStudent" v-if="currentView.BottomViewerStudent">
      <BottomViewerStudent/>
    </div>

    <div id="BottomCenterViewerStudent" v-if="currentView.BottomCenterViewerStudent">
      <BottomCenterViewerStudent/>
    </div>

    <div id="BottomRightViewerStudent" v-if="currentView.BottomRightViewerStudent">
      <BottomRightViewerStudent/>
    </div>

  </div>
</template>

<script>
import ModelViewer from './components/OverallViewer/ModelViewer.vue';
import LeftViewer from './components/OverallViewer/LeftViewer.vue';
import LeftBottomViewer from './components/OverallViewer/LeftBottomViewer.vue';
import RightViewer from './components/OverallViewer/RightViewer.vue';
import BottomViewer from './components/OverallViewer/BottomViewer.vue';
import BottomCenterViewer from './components/OverallViewer/BottomCenterViewer.vue';
import BottomRightViewer from './components/OverallViewer/BottomRightViewer.vue';
import TimeLine from './components/OverallViewer/TimeLine.vue';

import LeftViewerClass from './components/ClassViewer/LeftViewerClass.vue';
import LeftBottomViewerClass from './components/ClassViewer/LeftBottomViewerClass.vue';
import RightViewerClass from './components/ClassViewer/RightViewerClass.vue';
import BottomViewerClass from './components/ClassViewer/BottomViewerClass.vue';
import BottomCenterViewerClass from './components/ClassViewer/BottomCenterViewerClass.vue';
import BottomRightViewerClass from './components/ClassViewer/BottomRightViewerClass.vue';

import LeftViewerStudent from './components/StudentViewer/LeftViewerStudent.vue';
import LeftBottomViewerStudent from './components/StudentViewer/LeftBottomViewerStudent.vue';
import RightViewerStudent from './components/StudentViewer/RightViewerStudent.vue';
import BottomViewerStudent from './components/StudentViewer/BottomViewerStudent.vue';
import BottomCenterViewerStudent from './components/StudentViewer/BottomCenterViewerStudent.vue';
import BottomRightViewerStudent from './components/StudentViewer/BottomRightViewerStudent.vue';


export default {
  name: 'App',
  components: {
    // 整体视图组件
    ModelViewer,
    LeftViewer,
    LeftBottomViewer,
    RightViewer,
    BottomViewer,
    BottomCenterViewer,
    BottomRightViewer,
    TimeLine,
    // 班级视图组件
    LeftViewerClass,
    LeftBottomViewerClass,
    RightViewerClass,
    BottomViewerClass,
    BottomCenterViewerClass,
    BottomRightViewerClass,
    // 班级视图组件
    LeftViewerStudent,
    LeftBottomViewerStudent,
    RightViewerStudent,
    BottomViewerStudent,
    BottomCenterViewerStudent,
    BottomRightViewerStudent

  },
  data() {
    return {
      initialStateCode: this.getInitialStateCode(),
      currentView: this.getViewState(this.getInitialStateCode())
    }
  },
  methods: {
    getInitialStateCode() {
      const savedState = localStorage.getItem('modelViewerStateCode');
      return savedState ? parseInt(savedState) : 0;
    },
    getViewState(stateCode) {
      console.log(stateCode);
      // stateCode === 0，整体视图
      if (stateCode === 0) {
        // alert("To 整体视图");
        return{
          // 整体视图组件显示控制
          LeftViewer: true,
          LeftBottomViewer: true,
          RightViewer: true,
          BottomViewer: true,
          BottomCenterViewer: true,
          BottomRightViewer: true,
          TimeLine: true,
          // 班级视图组件显示控制
          LeftViewerClass: false,
          LeftBottomViewerClass: false,
          RightViewerClass: false,
          BottomViewerClass: false,
          BottomCenterViewerClass: false,
          BottomRightViewerClass: false,
          // 学生视图组件显示控制
          LeftViewerStudent: false,
          LeftBottomViewerStudent: false,
          RightViewerStudent: false,
          BottomViewerStudent: false,
          BottomCenterViewerStudent: false,
          BottomRightViewerStudent: false
        };
        // stateCode === 1，class视图
      } else if (stateCode === 1) {
        // alert("To 班级视图");
        return{
          // 整体视图组件显示控制
          LeftViewer: false,
          LeftBottomViewer: false,
          RightViewer: false,
          BottomViewer: false,
          BottomCenterViewer: false,
          BottomRightViewer: false,
          TimeLine: false,
          // 班级视图组件显示控制
          LeftViewerClass: true,
          LeftBottomViewerClass: true,
          RightViewerClass: true,
          BottomViewerClass: true,
          BottomCenterViewerClass: true,
          BottomRightViewerClass: true,
          // 学生视图组件显示控制
          LeftViewerStudent: false,
          LeftBottomViewerStudent: false,
          RightViewerStudent: false,
          BottomViewerStudent: false,
          BottomCenterViewerStudent: false,
          BottomRightViewerStudent: false
        };
        // stateCode === 2，student视图
      } else if (stateCode === 2) {
          // alert("To 学生视图");
          return{
          // 整体视图组件显示控制
          LeftViewer: false,
          LeftBottomViewer: false,
          RightViewer: false,
          BottomViewer: false,
          BottomCenterViewer: false,
          BottomRightViewer: false,
          TimeLine: false,
          // 班级视图组件显示控制
          LeftViewerClass: false,
          LeftBottomViewerClass: false,
          RightViewerClass: false,
          BottomViewerClass: false,
          BottomCenterViewerClass: false,
          BottomRightViewerClass: false,
          // 学生视图组件显示控制
          LeftViewerStudent: true,
          LeftBottomViewerStudent: true,
          RightViewerStudent: true,
          BottomViewerStudent: true,
          BottomCenterViewerStudent: true,
          BottomRightViewerStudent: true
        };
      }else{
        console.error("stateCode error!", error);
      }
    },
    handleStateChange(stateCode) {
      this.currentView = this.getViewState(stateCode);
    }
  }
}
</script>


<style>

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box; /* Ensure padding and border are included in the element's total width and height */
}

#app {
  display: flex;
  flex-direction: column; /* Arrange children in a column */
  align-items: center; /* Center align horizontally */
  height: 100vh;
  margin: 0;
  box-sizing: border-box; /* Ensure padding is included in the height */
}

#titleAll {
  width: 100%;
  height: 3%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f0f0;
  border-bottom: 1px solid #e0e0e0;
}
                                                 /*                     整体视图样式控制         */

#ModelViewer {
  width: 50%;
  height: 55%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 0px; 
  /* 添加阴影效果 */
  /* box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.1);  */
  border-radius: 10px; 
  top: 3%;
}

/*  */
#TimeLine {
  width: 50%;
  height: 5%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 0px; 
  top: 58%;
  left: 25%;
}

#LeftViewer {
  width: calc(25% - 4px);
  height: calc(30% - 4px);
  position: absolute;
  top: 3%;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 添加阴影效果 */
  box-shadow: 2px 0px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
}

#LeftBottomViewer {
  width: calc(25% - 4px);
  height: calc(30% - 4px);
  position: absolute;
  top: 33%;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 添加阴影效果 */
  box-shadow: 2px 0px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
}

#RightViewer {
  width: calc(25% - 4px); /* Adjust this value to control the space between the two viewers */
  height: calc(60% - 4px);
  position: absolute;
  top: 3%;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 添加阴影效果 */
  box-shadow: -2px 0px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
}

#BottomViewer {
  width: calc(55% - 4px);
  height: calc(37% - 1px);
  display: flex;
  justify-content: center;
  align-items: center;

  /* 添加阴影效果 */
  box-shadow: 0px -2px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
  position: absolute;
  bottom: 0; /* Stick to the bottom */
  left: 0;
}

#BottomCenterViewer {
  width: calc(20% - 4px);
  height: calc(37% - 1px);
  display: flex;
  justify-content: center;
  align-items: center;

  /* 添加阴影效果 */
  box-shadow: 0px -2px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
  position: absolute;
  bottom: 0; /* Stick to the bottom */
  left: 55%;
}

#BottomRightViewer {
  width: calc(25% - 4px);
  height: calc(37% - 1px);
  display: flex;
  justify-content: center;
  align-items: center;

  /* 添加阴影效果 */
  box-shadow: 0px -2px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 5px; 
  position: absolute;
  bottom: 0; /* Stick to the bottom */
  right: 0;
}

                                         /*                     班级视图样式控制         */
#LeftViewerClass {
  width: calc(25% - 4px);
  height: calc(30% - 4px);
  position: absolute;
  top: 3%;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 添加阴影效果 */
  box-shadow: 2px 0px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
}

#LeftBottomViewerClass {
  width: calc(25% - 4px);
  height: calc(30% - 4px);
  position: absolute;
  top: 33%;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 添加阴影效果 */
  box-shadow: 2px 0px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
}

#RightViewerClass {
  width: calc(25% - 4px); /* Adjust this value to control the space between the two viewers */
  height: calc(60% - 4px);
  position: absolute;
  top: 3%;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 添加阴影效果 */
  box-shadow: -2px 0px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
}

#BottomViewerClass {
  width: calc(55% - 4px);
  height: calc(37% - 1px);
  display: flex;
  justify-content: center;
  align-items: center;

  /* 添加阴影效果 */
  box-shadow: 0px -2px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
  position: absolute;
  bottom: 0; /* Stick to the bottom */
  left: 0;
}

#BottomCenterViewerClass {
  width: calc(20% - 4px);
  height: calc(37% - 1px);
  display: flex;
  justify-content: center;
  align-items: center;

  /* 添加阴影效果 */
  box-shadow: 0px -2px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
  position: absolute;
  bottom: 0; /* Stick to the bottom */
  left: 55%;
}

#BottomRightViewerClass {
  width: calc(25% - 4px);
  height: calc(37% - 1px);
  display: flex;
  justify-content: center;
  align-items: center;

  /* 添加阴影效果 */
  box-shadow: 0px -2px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 5px; 
  position: absolute;
  bottom: 0; /* Stick to the bottom */
  right: 0;
}

                                        /*                     学生视图样式控制         */
  #LeftViewerStudent {
  width: calc(25% - 4px);
  height: calc(30% - 4px);
  position: absolute;
  top: 3%;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 添加阴影效果 */
  box-shadow: 2px 0px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
}

#LeftBottomViewerStudent {
  width: calc(25% - 4px);
  height: calc(30% - 4px);
  position: absolute;
  top: 33%;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 添加阴影效果 */
  box-shadow: 2px 0px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
}

#RightViewerStudent {
  width: calc(25% - 4px); /* Adjust this value to control the space between the two viewers */
  height: calc(60% - 4px);
  position: absolute;
  top: 3%;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 添加阴影效果 */
  box-shadow: -2px 0px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
}

#BottomViewerStudent {
  width: calc(55% - 4px);
  height: calc(37% - 1px);
  display: flex;
  justify-content: center;
  align-items: center;

  /* 添加阴影效果 */
  box-shadow: 0px -2px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
  position: absolute;
  bottom: 0; /* Stick to the bottom */
  left: 0;
}

#BottomCenterViewerStudent {
  width: calc(20% - 4px);
  height: calc(37% - 1px);
  display: flex;
  justify-content: center;
  align-items: center;

  /* 添加阴影效果 */
  box-shadow: 0px -2px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
  position: absolute;
  bottom: 0; /* Stick to the bottom */
  left: 55%;
}

#BottomRightViewerStudent {
  width: calc(25% - 4px);
  height: calc(37% - 1px);
  display: flex;
  justify-content: center;
  align-items: center;

  /* 添加阴影效果 */
  box-shadow: 0px -2px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 5px; 
  position: absolute;
  bottom: 0; /* Stick to the bottom */
  right: 0;
}

</style>