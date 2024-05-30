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
  height: 60%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 0px; /* Adjust this value to control the space below */
}

#LeftViewer {
  width: 25%;
  height: 60%;
  position: absolute;
  top: 0;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  /* background-color: #26595f;  */
}

#RightViewer {
  width: 25%;
  height: 60%;
  position: absolute;
  top: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  /* background-color: #26595f; 可以根据需要设置背景颜色 */
}

#BottomViewer {
  width: 100%;
  height: 40%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #07ab8d; /* Adjust as needed */
}

</style>