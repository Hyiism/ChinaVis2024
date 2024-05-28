<template>
  <div id="app">
    <ModelViewer/>
  </div>
</template>

<script>
import ModelViewer from './components/ModelViewer.vue';

export default {
  name: 'App',
  components: {
    ModelViewer,
  }
};
</script>

<style>
#app {
  width: 100%;
  height: 100vh;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
