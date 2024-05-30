<template>
  <div ref="sceneContainer" class="scene-container" @click="onClick">
    <div class="view-controls">
      <button @click="setTopView">俯视图</button>
      <button @click="setSideView">侧视图</button>
      <button @click="lookCameraPosition">查看相机位置</button>
    </div>
  </div>
</template>

<script>
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import TWEEN from '@tweenjs/tween.js';

export default {
  name: 'ModelViewer',
  data() {
    return {
      scene: null,
      camera: null,
      renderer: null,
      controls: null,
      raycaster: new THREE.Raycaster(),
      mouse: new THREE.Vector2(),
    };
  },
  mounted() {
    this.initThreeJS();
    window.addEventListener('resize', this.onWindowResize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onWindowResize);
  },
  methods: {
    initThreeJS() {
      // 创建场景
      this.scene = new THREE.Scene();
      this.scene.background = new THREE.Color(0xffffff);

      // 初始化透视相机
      const aspect = this.$refs.sceneContainer.clientWidth / this.$refs.sceneContainer.clientHeight;
      this.camera = new THREE.PerspectiveCamera(80, aspect, 0.1, 1000);
      this.camera.position.set(0, 400, 0);
      this.camera.lookAt(0, 0, 0);

      // 创建渲染器
      this.renderer = new THREE.WebGLRenderer({ antialias: true });
      this.renderer.setSize(this.$refs.sceneContainer.clientWidth, this.$refs.sceneContainer.clientHeight);
      this.$refs.sceneContainer.appendChild(this.renderer.domElement);

      // 添加光源
      this.addLights();

      // 添加OrbitControls
      this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      this.controls.enableDamping = true;
      this.controls.dampingFactor = 0.25;
      this.controls.screenSpacePanning = false;
      this.controls.maxPolarAngle = Math.PI / 2;

      // 加载模型
      this.loadModel();

      // 动画循环
      this.animate();
    },
    addLights() {
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
      this.scene.add(ambientLight);

      const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
      directionalLight.position.set(10, 10, 10).normalize();
      this.scene.add(directionalLight);

      const pointLight = new THREE.PointLight(0xffffff, 1, 500);
      pointLight.position.set(0, 50, 100);
      this.scene.add(pointLight);
    },
    loadModel() {
      const loader = new GLTFLoader();
      loader.load('/models/student101_2.glb', (gltf) => {
        const model = gltf.scene;
        model.scale.set(1.5, 1.5, 1.5);
        this.scene.add(model);
        model.traverse((child) => {
          if (child.isMesh && child.name.includes("student019")) {
            child.material.color.set(0xff0000);
          }
        });
      }, undefined, (error) => {
        console.error('An error happened while loading the model', error);
      });
    },
    onWindowResize() {
      if (this.$refs.sceneContainer) {
        const aspect = this.$refs.sceneContainer.clientWidth / this.$refs.sceneContainer.clientHeight;
        this.camera.aspect = aspect;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.$refs.sceneContainer.clientWidth, this.$refs.sceneContainer.clientHeight);
      }
    },
    animate() {
      requestAnimationFrame(this.animate);
      TWEEN.update();
      this.controls.update();
      this.renderer.render(this.scene, this.camera);
    },
    setTopView() {
      const currentPosition = this.camera.position.clone();
      const targetPosition = new THREE.Vector3(0, 400, 0);

      new TWEEN.Tween(currentPosition)
        .to(targetPosition, 1000)
        .easing(TWEEN.Easing.Quadratic.Out)
        .onUpdate(() => {
          this.camera.position.copy(currentPosition);
          this.camera.lookAt(0, 0, 0);
        })
        .start();
    },
    setSideView() {
      const currentPosition = this.camera.position.clone();
      const targetPosition = new THREE.Vector3(200, 200, 400);

      new TWEEN.Tween(currentPosition)
        .to(targetPosition, 1000)
        .easing(TWEEN.Easing.Quadratic.Out)
        .onUpdate(() => {
          this.camera.position.copy(currentPosition);
          this.camera.lookAt(0, 0, 0);
        })
        .start();
    },
    lookCameraPosition() {
      console.log(this.camera.position.clone());
    },
    onClick(event) {
      const rect = this.$refs.sceneContainer.getBoundingClientRect();
      this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      this.raycaster.setFromCamera(this.mouse, this.camera);
      const intersects = this.raycaster.intersectObjects(this.scene.children, true);

      if (intersects.length > 0) {
        const target = intersects[0].object;
        const targetPosition = target.position.clone();

        new TWEEN.Tween(this.camera.position)
          .to({
            x: targetPosition.x + 40,
            y: targetPosition.y + 40,
            z: targetPosition.z + 80
          }, 1000)
          .easing(TWEEN.Easing.Quadratic.Out)
          .onStart(() => console.log('Animation started'))
          .onComplete(() => console.log('Animation completed'))
          .start();
      } else {
        console.log('No intersected objects');
      }
    },
  },
};
</script>

<style scoped>
.scene-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

canvas {
  width: 100%;
  height: 100%;
}

.view-controls {
  position: absolute;
  top: 10px;
  left: 10px;
}

.view-controls button {
  margin: 10px;
  padding: 10px 20px;
  font-size: 10px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
  background-color: #4CAF50;
  color: white;
}

.view-controls button:hover {
  background-color: #45a049;
}
</style>
