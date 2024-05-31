<template>
  <div ref="sceneContainer" class="scene-container" @click="onClick">
    <div class="view-controls">
      <button @click="setTopView">俯视图</button>
      <button @click="setSideView">侧视图</button>
      <button @click="lookCameraPosition">查看相机位置</button>
    </div>

    <div class="menu">
      <div class="menu-item" style="--i:0;">1</div>
      <div class="menu-item" style="--i:1;">2</div>
      <div class="menu-item" style="--i:2;">3</div>
      <div class="menu-item" style="--i:3;">4</div>
      <div class="menu-item" style="--i:4;">5</div>
      <div class="menu-item" style="--i:5;">6</div>
      <div class="menu-item" style="--i:6;">7</div>
      <div class="menu-item" style="--i:7;">8</div>
    </div>
    <!-- ceshi -->

  </div>
</template>

<script>
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import TWEEN from '@tweenjs/tween.js';

export default {
  name: 'ModelViewer',
  components: {

  },

  data() {

    // 初始化student001的坐标
    const basePosition = {
      x: 178.434532168853,
      y: 113.66997527109939,
      z: 164.5923843414466
    };

    // z轴上的间隔
    const zdistances = [
      19.03868865966796,
      35.97814559936524
    ];
    const xdistances = 30.7353286743164
    const studentsPositions = {};
    let xOffsetCounter = 0; // 记录x轴偏移次数
    for (let i = 1; i <= 100; i++) {
      const studentId = `student${String(i).padStart(3, '0')}`;
      let zOffset = 0; // 计算z轴的偏移量
      let xOffset = xOffsetCounter * xdistances; // 计算x轴的偏移量
      if (i % 10 === 0) {
        xOffsetCounter++; // 每加10个学生，xOffsetCounter加1
      }
      for (let j = 1; j < i; j++) {
        if (j % 10 === 0) {
          zOffset = 0;
        } else {
          zOffset += zdistances[(j - 1) % zdistances.length];
        }
      }
      studentsPositions[studentId] = {
        x: basePosition.x - xOffset,
        y: basePosition.y,
        z: basePosition.z - zOffset
      };
    }
    return {
      topValue: 0, // 初始值
      leftValue: 0, // 初始值
      isOpen: false,
      menuLeft: 0,
      menuTop: 0,
      scene: null,
      camera: null,
      renderer: null,
      // controls: null,
      student: null,
      raycaster: new THREE.Raycaster(),
      mouse: new THREE.Vector2(),
      studentsPositions
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

      const axesHelper = new THREE.AxesHelper(20000);
      this.scene.add(axesHelper);


      // 创建渲染器
      this.renderer = new THREE.WebGLRenderer({ antialias: true });
      this.renderer.setSize(this.$refs.sceneContainer.clientWidth, this.$refs.sceneContainer.clientHeight);
      this.renderer.setClearColor(0xffffff);
      this.$refs.sceneContainer.appendChild(this.renderer.domElement);

      // 窗口调整大小处理
      window.addEventListener('resize', this.onWindowResize);

      // 添加光源
      this.addLights();

      // // 添加OrbitControls
      // this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      // this.controls.enableDamping = true;
      // this.controls.dampingFactor = 0.25;
      // this.controls.screenSpacePanning = false;
      // this.controls.maxPolarAngle = Math.PI / 2;

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
      loader.load('/models/student101_4.glb', (gltf) => {
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
      // this.controls.update();
      this.renderer.render(this.scene, this.camera);
    },
    initialView() {
      //原方案
      // this.camera.position.set(0, 400, 0);
      //初始相机看第一个学生
      this.camera.position.set(178.434532168853, 113.66997527109939, 164.5923843414466)
      this.camera.lookAt(97.55521392822266, 32.887508392333984, 75.55369567871094);
    },
    setTopView() {
      const currentPosition = this.camera.position.clone();
      const targetPosition = new THREE.Vector3(0, 400, 0);

      new TWEEN.Tween(currentPosition)
        .to(targetPosition, 1000)
        .easing(TWEEN.Easing.Quadratic.Out)
        .onUpdate(() => {
          this.camera.position.copy(currentPosition);
          // this.camera.lookAt(0, 0, 0);
        })
        .start();
    },
    setSideView() {
      const currentPosition = this.camera.position.clone();
      // const targetPosition = new THREE.Vector3(200, 200, 400);
      const targetPosition = new THREE.Vector3(178.434532168853, 113.66997527109939, 164.5923843414466);

      new TWEEN.Tween(currentPosition)
        .to(targetPosition, 1000)
        .easing(TWEEN.Easing.Quadratic.Out)
        .onUpdate(() => {
          this.camera.position.copy(currentPosition);
          this.camera.lookAt(97.55521392822266, 32.887508392333984, 75.55369567871094);
        })
        .start();
    },
    lookCameraPosition() {
      console.log(this.camera.position.clone());
    },
    calculateItemPosition(index) {
      const angleStep = (2 * Math.PI) / this.items.length;
      const radius = 80;
      const angle = index * angleStep;
      const x = Math.cos(angle) * radius + 100; // 100 是环形菜单中心点的 x 坐标
      const y = Math.sin(angle) * radius + 100; // 100 是环形菜单中心点的 y 坐标
      return {
        left: `${x}px`,
        top: `${y}px`,
      };
    },
    onClick(event) {
      const rect = this.$refs.sceneContainer.getBoundingClientRect();

      this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      this.raycaster.setFromCamera(this.mouse, this.camera);
      const intersects = this.raycaster.intersectObjects(this.scene.children, true);
      console.log(intersects);
      if (intersects.length > 0) {

        this.student = intersects[0].object;
        this.student.material.color.set(0xff0000);
        // 获取学生的ID
        const studentName = this.student.name;

        // 从studentsPositions中获取位置信息
        const targetPosition = new THREE.Vector3(
          this.studentsPositions[studentName].x,
          this.studentsPositions[studentName].y,
          this.studentsPositions[studentName].z
        );

        // const targetPosition = new THREE.Vector3().copy(this.student.position);
        console.log(targetPosition, this.student);

        new TWEEN.Tween(this.camera.position)
          .to({
            x: targetPosition.x,
            y: targetPosition.y,
            z: targetPosition.z
          }, 1000)
          .easing(TWEEN.Easing.Quadratic.Out)
          .start();
        // this.onCameraMoveComplete(targetPosition)
      }
    },
    onCameraMoveComplete(targetPosition) {
      const rect = this.renderer.domElement.getBoundingClientRect(); // 获取渲染器容器的位置信息
      const halfWidth = rect.width / 2; // 容器宽度的一半
      const halfHeight = rect.height / 2; // 容器高度的一半
      const vec2 = new THREE.Vector3(targetPosition.x, targetPosition.y, targetPosition.z).project(this.camera); // 获取相机坐标投影到屏幕坐标系中的位置
      const menuX = vec2.x * halfWidth + halfWidth; // 计算菜单应该显示的x坐标
      const menuY = -vec2.y * halfHeight + halfHeight; // 计算菜单应该显示的y坐标
      // this.showMenu(menuX, menuY); // 调用显示菜单的函数，并传入计算得到的菜单位置信息
    },
    showMenu(x, y) {
      let isAnimating = false;

      const menu = document.querySelector('.menu');
      const isOpen = menu.classList.contains('open');

      if (isOpen) {
        menu.classList.remove('open');
        isAnimating = true;

        setTimeout(() => {
          menu.style.left = `${x}px`;
          menu.style.top = `${y}px`;
          menu.classList.add('open');
          isAnimating = false;
        }, 500);
      } else {
        menu.style.left = `${x}px`;
        menu.style.top = `${y}px`;
        menu.classList.add('open');
      }
    },

  },

}
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

.menu {
  position: absolute;
  width: 200px;
  height: 200px;
  transform: scale(0);
  transition: transform 0.5s;
}

.menu.open {
  transform: scale(1);
}

.menu-item {
  position: absolute;
  width: 50px;
  height: 50px;
  background-color: #ff6347;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.5s, opacity 0.5s;
  transform-origin: 100px 100px;
  opacity: 0;
  transform: rotate(calc(var(--i) * 45deg)) translate(0) rotate(calc(var(--i) * -45deg));
}

.menu.open .menu-item {
  opacity: 1;
  transform: rotate(calc(var(--i) * 45deg)) translate(100px) rotate(calc(var(--i) * -45deg));
}

.menu-item:hover {
  background-color: #ff4500;
}
</style>
