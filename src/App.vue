<template>
  <div id="app">

    <div id="titleAll">
      <h2>XXX可视化系统</h2>
    </div>

    <div id="LeftViewer">
      <LeftViewer/>
    </div>

    <div id="LeftBottomViewer">
      <LeftBottomViewer/>
    </div>

    <div id="ModelViewer">
      <ModelViewer/>
    </div>

    <div id="RightViewer">
      <RightViewer/>
    </div>

    <div id="BottomViewer">
      <BottomViewer/>
    </div>

    <div id="BottomCenterViewer">
      <BottomCenterViewer/>
    </div>

    <div id="BottomRightViewer">
      <BottomRightViewer/>
    </div>

  </div>

</template>

<script>
import ModelViewer from './components/ModelViewer.vue';
import LeftViewer from './components/LeftViewer.vue';
import LeftBottomViewer from './components/LeftBottomViewer.vue';
import RightViewer from './components/RightViewer.vue';
import BottomViewer from './components/BottomViewer.vue';
import BottomCenterViewer from './components/BottomCenterViewer.vue';
import BottomRightViewer from './components/BottomRightViewer.vue';

export default {
  name: 'App',
  components: {
    ModelViewer,
    LeftViewer,
    LeftBottomViewer,
    RightViewer,
    BottomViewer,
    BottomCenterViewer,
    BottomRightViewer
  }
};
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

#ModelViewer {
  width: 50%;
  height: calc(60% - 4px);
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 0px; 
  /* 添加阴影效果 */
  box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  border-radius: 10px; 
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



</style>