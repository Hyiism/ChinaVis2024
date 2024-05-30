<template>
  <div id="app">

    <div id="LeftViewer">
      <LeftViewer/>
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

  </div>

</template>

<script>
import ModelViewer from './components/ModelViewer.vue';
import LeftViewer from './components/LeftViewer.vue';
import RightViewer from './components/RightViewer.vue';
import BottomViewer from './components/BottomViewer.vue';

export default {
  name: 'App',
  components: {
    ModelViewer,
    LeftViewer,
    RightViewer,
    BottomViewer
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
  height: calc(60% - 4px);
  position: absolute;
  top: 0;
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
  top: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 添加阴影效果 */
  box-shadow: -2px 0px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
}

#BottomViewer {
  width: calc(100% - 4px);
  height: calc(40% - 1px);
  display: flex;
  justify-content: center;
  align-items: center;

  /* 添加阴影效果 */
  box-shadow: 0px -2px 8px rgba(0, 0, 0, 0.1); 
  border-radius: 10px; 
  position: absolute;
  bottom: 0; /* Stick to the bottom */
}



</style>