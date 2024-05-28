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
  name: 'ModelViewer1',
  components: {
    
  },
  data() {
    return {
      scene: null,
      camera: null,
      perspectiveCamera: null,
      renderer: null,
      controls: null,
      student: null,
      raycaster: new THREE.Raycaster(),
      mouse: new THREE.Vector2(),
      viewMode: 'ortho',
      showMenu: false,
      menuItems: [
        { label: 'Home', value: 'home' },
        { label: 'About', value: 'about' },
        { label: 'Services', value: 'services' },
        { label: 'Contact', value: 'contact' }
      ]
    };
  },
  mounted() {
    this.initThreeJS();
  },
  methods: {
    initThreeJS() {
      // 创建场景
      this.scene = new THREE.Scene();
      this.scene.background = new THREE.Color(0xffffff);

      const aspect = this.$refs.sceneContainer.clientWidth / this.$refs.sceneContainer.clientHeight;

      // 初始化透视相机
      this.camera = new THREE.PerspectiveCamera(80, aspect, 0.1, 1000);

      // 创建渲染器
      this.renderer = new THREE.WebGLRenderer({ antialias: true });
      this.renderer.setSize(this.$refs.sceneContainer.clientWidth, this.$refs.sceneContainer.clientHeight);
      this.renderer.setClearColor(0xffffff);
      this.$refs.sceneContainer.appendChild(this.renderer.domElement);

      // 窗口调整大小处理
      window.addEventListener('resize', this.onWindowResize);

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
      this.initialView();
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
      const aspect = this.$refs.sceneContainer.clientWidth / this.$refs.sceneContainer.clientHeight;
      this.camera.aspect = aspect;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(this.$refs.sceneContainer.clientWidth, this.$refs.sceneContainer.clientHeight);
      this.camera.aspect = aspect;
      this.camera.updateProjectionMatrix();
    },
    animate() {
      requestAnimationFrame(this.animate);
      TWEEN.update();
      this.controls.update();
      this.renderer.render(this.scene, this.camera);
    },
    initialView() {
      this.camera.position.set(0, 400, 0);
      this.camera.lookAt(0, 0, 0);
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

      console.log('Mouse coordinates:', this.mouse.x, this.mouse.y);

      this.raycaster.setFromCamera(this.mouse, this.camera);
      const intersects = this.raycaster.intersectObjects(this.scene.children, true);

      if (intersects.length > 0) {
        this.student = intersects[0].object;
        const targetPosition = new THREE.Vector3().copy(this.student.position);

        console.log('Target position:', targetPosition);

        // 取消之前的动画
        TWEEN.removeAll();

        new TWEEN.Tween(this.camera.position)
          .to({
            x: targetPosition.x + 40,
            y: targetPosition.y + 40,
            z: targetPosition.z + 80
          }, 1000)
          .easing(TWEEN.Easing.Quadratic.Out)
          .onStart(() => {
            console.log('Animation started');
          })
          .onComplete(() => {
            console.log('Animation completed');
          })
          .start();

        console.log('Moving camera to:', {
          x: targetPosition.x ,
          y: targetPosition.y ,
          z: targetPosition.z ,
        });
      } else {
        console.log('No intersected objects');
      }
    },
    focusOnObject(object) {
      const point3d = getPointRay(this.sence, this.camera).point;
      const time = 5000;
      // 克隆相机用户计算点击后相机聚焦的位置
      const cloneCamera = this.camera.clone();
      // this.camera.lookAt(point3d);
      cloneCamera.lookAt(point3d);

      new TWEEN.Tween(this.camera.position)
        .to({ x: cloneCamera.position.x, y: cloneCamera.position.y, z: cloneCamera.position.z }, 1000)
        .easing(TWEEN.Easing.Back.Out).start();

      new TWEEN.Tween(this.camera.rotation)
        .to({ x: cloneCamera.rotation.x, y: cloneCamera.rotation.y, z: cloneCamera.rotation.z }, 1000)
        .easing(TWEEN.Easing.Back.Out).start();
    },

    showRadialMenu(x, y) {
      const menu = document.createElement('div');
      menu.className = 'radial-menu';
      menu.style.position = 'absolute';
      menu.style.left = `${x}px`;
      menu.style.top = `${y}px`;

      // 创建环形菜单的选项
      const options = ['Option 1', 'Option 2', 'Option 3'];
      options.forEach(option => {
        const menuItem = document.createElement('div');
        menuItem.className = 'menu-item';
        menuItem.innerText = option;
        menuItem.onclick = () => {
          console.log(`${option} clicked`);
          document.body.removeChild(menu);
        };
        menu.appendChild(menuItem);
      });

      document.body.appendChild(menu);

      // 设置环形菜单样式
      const radius = 50; // 半径
      const angleStep = (2 * Math.PI) / options.length;
      for (let i = 0; i < options.length; i++) {
        const angle = i * angleStep;
        const item = menu.children[i];
        item.style.position = 'absolute';
        item.style.transform = `translate(${radius * Math.cos(angle)}px, ${radius * Math.sin(angle)}px)`;
      }
    }

  }
};
</script>

<style scoped>
.scene-container {
  width: 45%;
  height: 50vh;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 0;
  position: absolute;
  top: 0;
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
