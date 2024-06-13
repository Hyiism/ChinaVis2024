<template>
  <div ref="sceneContainer" class="scene-container" @click="onClick">
    <div class="view-controls">
      <button @click="setTopView">俯视图</button>
      <button @click="setSideView">侧视图</button>
      <button @click="lookCameraPosition">查看相机位置</button>
      <button @click="changeState">Change State</button>
    </div>

    <div class="calendar-container">
      <a-calendar :fullscreen="false" @panelChange="onPanelChange" @select="onSelect" :defaultValue="defaultValue"
        :header-render="headerRender" />
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
  </div>
</template>

<script>
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import TWEEN from '@tweenjs/tween.js';
import PubSub from 'pubsub-js';
import moment from 'moment';
import EventBus from '@/eventBus'; // 导入事件总线

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
      // 状态码
      stateCode: this.getSavedState(),
      topValue: 0, // 初始值
      leftValue: 0, // 初始值
      isOpen: false,
      menuLeft: 0,
      menuTop: 0,
      defaultValue: moment('2023-08-31'),
      model: null,
      container: null,
      scene: null,
      camera: null,
      renderer: null,
      // controls: null,
      student: null,
      raycaster: new THREE.Raycaster(),
      mouse: new THREE.Vector2(),
      studentsPositions,
      allStudent: [],
      appearStudent: [],
      mappedStudents: [],
      receivedStudent: []
    };
  },
  mounted() {
    this.initThreeJS();
    this.subscriptionToken = PubSub.subscribe('studentAppear', (msg, value) => {
      this.handleStudentAppear(value);
    });

  },
  created() {
    EventBus.$on('studentSelected', this.handleStudentSelected);
  },
  beforeDestroy() {
    EventBus.$off('studentSelected', this.handleStudentSelected);
  },
  methods: {
    // TODO: 处理在嵌入中选择学生点的操作
    handleStudentSelected(studentId){
      this.selectedStudentId = studentId;
      // 模拟点击此studentId对应的学生
      console.log("studentId-modelview", studentId);
      
    },

    getSavedState() {
      const savedState = localStorage.getItem('modelViewerStateCode');
      return savedState ? parseInt(savedState) : 0;
    },
    saveState(stateCode) {
      localStorage.setItem('modelViewerStateCode', stateCode);
    },
    changeState() {
      this.stateCode = (this.stateCode + 1) % 3; // Change the stateCode for demonstration
      this.saveState(this.stateCode);
      this.$emit('stateChanged', this.stateCode);
    },

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
      // window.addEventListener('resize', this.onWindowResize);

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
        this.model = gltf.scene;
        this.model.scale.set(1.5, 1.5, 1.5);
        // model.scale.set(1, 1, 1);
        this.scene.add(this.model);

        const objectsToRemove = [];

        for (let i = 1; i <= 100; i++) {
          const studentName = "student" + i.toString().padStart(3, "0"); // 将数字格式化为三位数，例如001
          this.model.traverse((child) => {
            if (child.isMesh && child.name.includes(studentName)) {
              objectsToRemove.push(child);
              this.allStudent.push(child);
            }
          });
        }
        // 从场景中移除这些对象
        objectsToRemove.forEach((child) => {
          if (child.parent) {
            child.parent.remove(child);
          }
        });
        // const mesh = this.allStudent[5]; // 因为appearStudent中的值是1到100的数，需要减1以匹配allStudent的索引
        // if (mesh) { // 确保mesh存在
        //   this.scene.add(mesh);
        // }
      }, undefined, (error) => {
        console.error('An error happened while loading the model', error);
      });
    },
    // onWindowResize() {
    //   const aspect = this.$refs.sceneContainer.clientWidth / this.$refs.sceneContainer.clientHeight;
    //   this.camera.aspect = aspect;
    //   this.camera.updateProjectionMatrix();
    //   this.renderer.setSize(this.$refs.sceneContainer.clientWidth, this.$refs.sceneContainer.clientHeight);
    //   this.camera.aspect = aspect;
    //   this.camera.updateProjectionMatrix();
    // },
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
    onPanelChange(value, mode) {
      console.log(value, mode);
    },
    onSelect(value) {
      // 获取用户选择的时间
      console.log('Selected Date:', value);

      // 转换为日期对象
      const dateObject = new Date(value);

      // 提取星期几，月，日期和年份
      const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun',];
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

      const day = days[dateObject.getUTCDay()];
      const month = months[dateObject.getUTCMonth()];
      const date = dateObject.getUTCDate() + 1; // 加一修正日期
      const year = dateObject.getUTCFullYear();

      const formattedDate = `${day} ${month} ${date} ${year}`;
      console.log('Formatted Date:', formattedDate);

      // 发布事件，将格式化后的日期传递出去
      PubSub.publish('dateSelected', formattedDate);
      // 在这里可以对获取到的时间进行其他处理
    },
    headerRender({ value, type, onChange, onTypeChange }) {
      const start = 0;
      const end = 12;
      const monthOptions = [];

      const current = value.clone();
      const localeData = value.localeData();
      const months = [];
      for (let i = 0; i < 12; i++) {
        current.month(i);
        months.push(localeData.monthsShort(current));
      }

      for (let index = start; index < end; index++) {
        monthOptions.push(
          <a-select-option class="month-item" key={`${index}`}>
            {months[index]}
          </a-select-option>,
        );
      }
      const month = value.month();

      const year = value.year();
      const options = [];
      // 修改这里，只添加2023和2024年份选项
      for (let i = 2023; i <= 2024; i++) {
        options.push(
          <a-select-option key={i} value={i} class="year-item">
            {i}
          </a-select-option>,
        );
      }
      return (
        <div style={{ padding: '10px' }}>
          <a-row type="flex" justify="space-between">
            <a-col>
              <a-radio-group size="small" onChange={e => onTypeChange(e.target.value)} value={type}>
                <a-radio-button value="month">Month</a-radio-button>
                <a-radio-button value="year">Year</a-radio-button>
              </a-radio-group>
            </a-col>
            <a-col>
              <a-select
                size="small"
                dropdownMatchSelectWidth={false}
                class="my-year-select"
                onChange={newYear => {
                  const now = value.clone().year(newYear);
                  onChange(now);
                }}
                value={String(year)}
              >
                {options}
              </a-select>
            </a-col>
            <a-col>
              <a-select
                size="small"
                dropdownMatchSelectWidth={false}
                value={String(month)}
                onChange={selectedMonth => {
                  const newValue = value.clone();
                  newValue.month(parseInt(selectedMonth, 10));
                  onChange(newValue);
                }}
              >
                {monthOptions}
              </a-select>
            </a-col>
          </a-row>
        </div>
      );
    },
    handleStudentAppear(data) {
      if (this.mappedStudents.length === 0) {
        console.log(1111111111111111111111111)
        // 随机放置学生
        let studentNumbers = [];
        for (let i = 1; i <= 100; i++) {
          studentNumbers.push(i);
        }
        studentNumbers = this.shuffleArray(studentNumbers);
        this.receivedStudent = data.students
        // 创建映射
        this.mappedStudents = this.receivedStudent.map((student, index) => {
          return { original: student, mapped: studentNumbers[index] };
        });
        this.appearStudent = this.mappedStudents.map(student => student.mapped);
        console.log("allStudent",this.allStudent)
        console.log("appearStudent",this.appearStudent)
        this.container = new THREE.Object3D();
        this.appearStudent.forEach(index => {
          const mesh = this.allStudent[index - 1]; // 因为appearStudent中的值是1到100的数，需要减1以匹配allStudent的索引
          console.log(mesh)
          if (mesh) { // 确保mesh存在
            this.container.add(mesh);
            // 将容器添加到场景中
            this.scene.add(this.container);
            // 对容器进行放大操作，而不是对模型直接进行放大
            this.container.scale.set(1.5, 1.5, 1.5); // 重新应用缩放设置
          }
        });
        this.animate();
      } else {
        console.log(222222222222222222222222)
        const changedStudent = data.students
        const newMappedStudents = [];
        console.log("旧的mapped：", this.mappedStudents)
        const disappearStudent = [];
        // 遍历 this.mappedStudents 数组
        this.mappedStudents.forEach(student => {
          // 检查 this.changedStudent 中是否存在与当前元素的 original 相同的值
          const existsInChangedStudent = changedStudent.some(changed => changed == student.original);
          // 如果当前元素的 original 值存在于 this.changedStudent 中，则将其保留
          if (existsInChangedStudent) {
            newMappedStudents.push(student);
          } else {
            disappearStudent.push(student.mapped);
          }
        });
        // 更新 this.mappedStudents 数组为新的保留元素数组
        this.mappedStudents = newMappedStudents;
        console.log("新的mapped", this.mappedStudents)
        const objectsToRemove = [];
        const disappearStudentNames = disappearStudent.map(num => {
          const studentNumber = num.toString().padStart(3, "0");
          return "student" + studentNumber;
        });
        console.log("disappear", disappearStudentNames)
        for (let i = 0; i <= disappearStudentNames.length - 1; i++) {
          const studentName = disappearStudentNames[i]
          this.container.traverse((child) => {
            console.log(child.name)
            if (child.name.includes(studentName)) {
              objectsToRemove.push(child);
            }
          });
        }
        console.log(objectsToRemove)
        // 从场景中移除这些对象
        objectsToRemove.forEach((child) => {
          if (child.parent) {
            child.parent.remove(child);
          }
        });
        this.animate();
        this.appearStudent = this.mappedStudents.map(student => student.mapped);
        this.appearStudent.forEach(index => {
          const mesh = this.allStudent[index - 1]; // 因为appearStudent中的值是1到100的数，需要减1以匹配allStudent的索引
          if (mesh) { // 确保mesh存在
            this.container.add(mesh);
            // 将容器添加到场景中
            this.scene.add(this.container);
            // 对容器进行放大操作，而不是对模型直接进行放大
            this.container.scale.set(1.5, 1.5, 1.5); // 重新应用缩放设置
          }
        });
        this.animate();
      }
    },
    shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
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

.calendar-container {
  width: 300px;
  border: none;
  border-radius: 4px;
  position: absolute;
  top: 0;
  right: 0;
  transform: scale(0.75);
  transform-origin: top right;
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
