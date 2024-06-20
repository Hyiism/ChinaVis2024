<template>
  <div ref="sceneContainer" class="scene-container" @click="onClick">
    <div class="view-controls">
      <!-- <button @click="setTopView">俯视图</button>
      <button @click="setSideView">侧视图</button> -->
      <!-- <button @click="lookCameraPosition">查看相机位置</button>
      <button @click="changeState">Change State</button>
      <button @click="changeToOverview">返回主视图</button> -->
      <a-button type="dashed" @click="lookCameraPosition">Look Camera Position</a-button>
      <a-button type="dashed" @click="changeToOverview">Switch OverView</a-button>
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
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader.js';
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter.js'
// import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import TWEEN from '@tweenjs/tween.js';
import PubSub from 'pubsub-js';
import moment from 'moment';
import EventBus from '@/eventBus'; // 导入事件总线
import { openDB } from 'idb';

export default {
  name: 'ModelViewer',
  components: {

  },

  data() {

    // 初始化student001的坐标
    const basePosition = {
      x: 227.77032470703125,
      y: 52.10075378417969,
      z: 211.2912139892578
    };

    // z轴上的间隔
    const zdistances = [
      30.671859741211,
      50.9932708740234
    ];
    const xdistances = 50.4543222900391;
    const studentsPositions = {};

    for (let i = 0; i < 100; i++) {
      const studentId = `student${String(i).padStart(3, '0')}`;

      let xOffset = Math.floor(i / 10) * xdistances; // 每10个学生x轴偏移一次
      let zOffset = 0;

      for (let j = 1; j <= i % 10; j++) { // 处理当前这组10个学生的z轴偏移
        zOffset += zdistances[(j - 1) % zdistances.length];
      }

      studentsPositions[studentId] = {
        x: basePosition.x - xOffset,
        y: basePosition.y,
        z: basePosition.z - zOffset
      };
    }
    // 添加字典，key为Rectangle001，value为Class1
    const rectangleToClassMap = {
      'Rectangle001': 'Class1',
      'Rectangle002': 'Class2',
      'Rectangle003': 'Class3',
      'Rectangle004': 'Class4',
      'Rectangle005': 'Class5',
      'Rectangle006': 'Class6',
      'Rectangle007': 'Class7',
      'Rectangle008': 'Class8',
      'Rectangle009': 'Class9',
      'Rectangle010': 'Class10',
      'Rectangle011': 'Class11',
      'Rectangle012': 'Class12',
      'Rectangle013': 'Class13',
      'Rectangle014': 'Class14',
      'Rectangle015': 'Class15',
    };
    return {
      // 状态码
      stateCode: this.getSavedState(),
      topValue: 0, // 初始值
      leftValue: 0, // 初始值
      isOpen: false,
      menuLeft: 0,
      menuTop: 0,
      defaultValue: moment('2023-08-31'),
      schoolModel: null,
      classModel: null,
      currentModelType: null,
      container: null,
      scene: null,
      camera: null,
      renderer: null,
      // controls: null,
      student: null,
      classRoom: null,
      raycaster: new THREE.Raycaster(),
      mouse: new THREE.Vector2(),
      studentsPositions,
      rectangleToClassMap,
      allStudent: [],
      appearStudent: [],
      mappedStudents: [],
      receivedStudent: [],
      classId: null,
      db: null,
      modelLoaded: false,
      isClass: false
    };
  },
  async mounted() {
    this.db = await this.openDB();
    this.initThreeJS();
    this.subscriptionToken = PubSub.subscribe('studentAppear', (msg, value) => {
      this.handleStudentAppear(value);
    });

  },
  created() {
    EventBus.$on('studentSelected', this.handleStudentSelected);
    EventBus.$on('checkSelected', this.handleCheckSelected);
  },
  beforeDestroy() {
    EventBus.$off('studentSelected', this.handleStudentSelected);
    EventBus.$off('checkSelected', this.handleCheckSelected);
    this.controls.dispose(); // 清理轨道控制
  },
  methods: {
    async openDB() {
      return openDB('threejs-models', 1, {
        upgrade(db) {
          if (!db.objectStoreNames.contains('models')) {
            db.createObjectStore('models');
          }
        }
      });
    },
    async saveModel(key, data) {
      const tx = this.db.transaction('models', 'readwrite');
      const store = tx.objectStore('models');
      await store.put(data, key);
      await tx.done;
    },
    async getModel(key) {
      const tx = this.db.transaction('models', 'readonly');
      const store = tx.objectStore('models');
      const data = await store.get(key);
      await tx.done;
      return data;
    },
    // TODO: 处理在嵌入中选择学生点的操作
    handleStudentSelected(studentId) {
      this.selectedStudentId = studentId;
      this.appearStudent = this.mappedStudents.map(student => student.original);
      const foundStudent = this.mappedStudents.find(student => student.original == this.selectedStudentId);
      console.log(foundStudent.mapped)
      this.student = this.allStudent[foundStudent.mapped - 1]

      this.student.material.color.set(0xff0000);
      // // 获取学生的ID
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
      console.log("studentId-modelview", studentId);

    },
    // TODO: 点击github打卡图，主视图跳转日期且显示对应学生，由此可以再拖拽查看其他人情况
    // data:{student_id:" ",year:" ",month:" ",date:" "}
    handleCheckSelected(data) {
      console.log('modelview dataselect:', data)

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

    async initThreeJS() {
      // 创建场景
      this.scene = new THREE.Scene();
      this.scene.background = new THREE.Color(0xffffff);

      const aspect = this.$refs.sceneContainer.clientWidth / this.$refs.sceneContainer.clientHeight;

      // 初始化透视相机
      this.camera = new THREE.PerspectiveCamera(80, aspect, 0.1, 3000);
      // this.camera = new THREE.PerspectiveCamera(80, aspect, 10, 1000);

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

      // 添加轨道控制
      // this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      // this.controls.enableDamping = true; // 启用阻尼效果
      // this.controls.dampingFactor = 0.25; // 阻尼系数
      // this.controls.screenSpacePanning = false; // 禁用屏幕空间平移
      // const click = await this.getModelDataFromIndexedDB('schoolModel');
      // if (savedModelData) {
      //   console.log("Loading model from IndexedDB...");
      //   this.loadModelFromBuffer(savedModelData, 'school');
      //   this.modelLoaded = true;
      // } else {
      //   console.log("Loading model from network...");
      //   this.loadSchoolModel();
      // }
      const savedState = this.getSavedState()
      if (savedState == 0) {
        this.loadSchoolModel();
      } else {
        this.loadClassModel()
      }

      this.animate();
      this.initialView();
    },
    async getModelDataFromIndexedDB(modelName) {
      const db = await this.openDB();
      const tx = db.transaction('models', 'readonly');
      const store = tx.objectStore('models');
      const modelData = await store.get(modelName);
      await tx.done;
      return modelData;
    },
    loadModelFromBuffer(modelData, modelName) {
      const loader = new GLTFLoader();
      loader.parse(modelData, '', (gltf) => {
        this.scene.add(gltf.scene);
        this[`${modelName}Model`] = gltf.scene;
        this.currentModelType = modelName;
        console.log('Model loaded from buffer');
      });
    },
    addLights() {
      // 添加光源
      const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);// 增加环境光强度，可以减少阴影
      this.scene.add(ambientLight);

      const directionalLight = new THREE.DirectionalLight(0xffffff, 1);// 平行光，即太阳光，会生成阴影。
      directionalLight.position.set(5, 10, 7.5);
      this.scene.add(directionalLight);

      const pointLight = new THREE.PointLight(0xffffff, 1.5, 100); // 单点发光，照射所有方向的光源（需要设置光源位置），它也不会生成阴影。
      pointLight.position.set(0, 2, 5);
      this.scene.add(pointLight);
    },
    loadSchoolModel() {
      // 使用MTLLoader加载材质文件
      const mtlLoader = new MTLLoader();
      mtlLoader.load(
        '/models/school.mtl', // 替换为你的MTL文件路径
        (materials) => {
          materials.preload();
          // 使用OBJLoader加载OBJ文件
          const objLoader = new OBJLoader();
          objLoader.setMaterials(materials);
          objLoader.load(
            '/models/school.obj', // 替换为你的OBJ文件路径
            (object) => {
              console.log("obj", object)
              this.scene.add(object);
              this.schoolModel = object
              this.schoolModel.name = 'school'
              this.currentModelType = 'school'; // 标记当前加载的文件类型

              this.modelLoaded = true;
              // Save model to IndexedDB
              // this.saveModelToIndexedDB('schoolModel', object);

            },
            (xhr) => {
              console.log((xhr.loaded / xhr.total * 100) + '% loaded');
            },
            (error) => {
              console.log('An error happened', error);
            }
          );
        },
        (xhr) => {
          console.log((xhr.loaded / xhr.total * 100) + '% loaded');
        },
        (error) => {
          console.log('An error happened', error);
        }
      );
    },
    // async saveModelToIndexedDB(modelName, modelObject) {
    //   const gltfExporter = new GLTFExporter();
    //   gltfExporter.parse(
    //     modelObject,
    //     async (gltf) => {
    //       const db = await this.openDB();
    //       const tx = db.transaction('models', 'readwrite');
    //       const store = tx.objectStore('models');
    //       await store.put(gltf, modelName);
    //       await tx.done;
    //       console.log('Model saved to IndexedDB');
    //     },
    //     { binary: true }
    //   );
    // },
    loadClassModel() {
      const loadModelPromise = () => {
        return new Promise((resolve, reject) => {
          const loader = new GLTFLoader();
          loader.load('/models/classroom.glb', (gltf) => {
            this.classModel = gltf.scene;
            this.classModel.scale.set(2, 2, 2);
            // const currentPosition = this.camera.position.clone();
            // const targetPosition = new THREE.Vector3(251.0974656502318, 153.83576291656343, 247.37127012156563);

            // new TWEEN.Tween(currentPosition)
            //   .to(targetPosition, 1000)
            //   .easing(TWEEN.Easing.Quadratic.Out)
            //   .onUpdate(() => {
            //     this.camera.position.copy(currentPosition);
            //     this.camera.lookAt(0, 0, 0);
            //   })
            //   .start();
            this.scene.add(this.classModel);
            console.log("classModel", this.classModel)
            // // Set initial opacity to 0
            // this.classModel.traverse((child) => {
            //   if (child.isMesh) {
            //     child.material.transparent = true;
            //     child.material.opacity = 0;
            //   }
            // });

            // // Fade-in effect
            // const fadeInDuration = 2000;
            // new TWEEN.Tween({ opacity: 0 })
            //   .to({ opacity: 1 }, fadeInDuration)
            //   .easing(TWEEN.Easing.Linear.None)
            //   .onUpdate((tween) => {
            //     this.classModel.traverse((child) => {
            //       if (child.isMesh) {
            //         child.material.opacity = tween.opacity;
            //       }
            //     });
            //   })
            //   .start();

            // Camera position animation
            const currentPosition = this.camera.position.clone();
            const targetPosition = new THREE.Vector3(608.3748006602943, 246.87681215346672, 507.9700608328807);

            new TWEEN.Tween(currentPosition)
              .to(targetPosition, 1000)
              .easing(TWEEN.Easing.Linear.None)
              .onUpdate(() => {
                this.camera.position.copy(currentPosition);
                this.camera.lookAt(227.77032470703125, 52.10075378417969, 211.2912139892578);
              })
              .start();

            const objectsToRemove = [];

            for (let i = 0; i <= 99; i++) {
              const studentName = "student" + i.toString().padStart(3, "0");
              this.classModel.traverse((child) => {
                if (child.isMesh && child.name.includes(studentName)) {
                  objectsToRemove.push(child);
                  this.allStudent.push(child);
                }
              });
            }
            console.log("初始化视图allStudent", this.allStudent);
            objectsToRemove.forEach((child) => {
              if (child.parent) {
                child.parent.remove(child);
              }
            });
            resolve(); // 模型加载完成后，resolve Promise
          }, undefined, (error) => {
            console.error('An error happened while loading the model', error);
            reject(error); // 如果模型加载失败，reject Promise
          });
        });
      };

      loadModelPromise().then(() => {
        // 模型加载完成后执行axios.get请求
        this.$axios.get('http://10.12.44.205:8000/getStudent4Class', {
          params: {
            className: this.classId,
          }
        })
          .then(response => {
            console.error('success sending data:', JSON.parse(response.data));

            let studentNumbers = [];
            for (let i = 0; i <= 99; i++) {
              studentNumbers.push(i);
            }
            studentNumbers = this.shuffleArray(studentNumbers);
            this.receivedStudent = JSON.parse(response.data).students;
            // 创建映射
            this.mappedStudents = this.receivedStudent.map((student, index) => {
              return { original: student, mapped: studentNumbers[index] };
            });
            this.appearStudent = this.mappedStudents.map(student => student.mapped);
            console.log("appearStudent", this.appearStudent);

            this.container = new THREE.Object3D();
            this.appearStudent.forEach(index => {
              const mesh = this.allStudent[index - 1];
              if (mesh) { // 确保mesh存在
                this.container.add(mesh);
                // 将容器添加到场景中
                this.scene.add(this.container);
                // 对容器进行放大操作，而不是对模型直接进行放大
                this.container.scale.set(2, 2, 2); // 重新应用缩放设置
              }
            });
            this.animate();
          })
          .catch(error => {
            console.error('Error sending data:', error);
          });
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
      this.camera.position.set(-434.0740788423603, 601.6679527037107, 1345.2141853240598)
      this.camera.lookAt(227.77032470703125, 52.10075378417969, 211.2912139892578);
    },
    // initialView() {
    //   //原方案
    //   // this.camera.position.set(0, 400, 0);
    //   //初始相机看第一个学生
    //   this.camera.position.set(178.434532168853, 113.66997527109939, 164.5923843414466)
    //   this.camera.lookAt(97.55521392822266, 32.887508392333984, 75.55369567871094);
    // },
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
    changeToOverview() {
      this.stateCode = 0
      this.saveState(this.stateCode);
      this.currentModelType = 'school'
      window.location.reload();
      // this.stateCode = 0
      // this.saveState(this.stateCode);
      // this.currentModelType = 'school'
      // this.scene.remove(this.container);
      // this.hideCurrentModel(this.classModel, () => {
      //   this.loadSchoolModel();
      // });
      // this.$emit('stateChanged', this.stateCode);
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
    hideCurrentModel(model, callback) {
      new TWEEN.Tween({ opacity: 1 }) // 初始透明度为1
        .to({ opacity: 0 }, 1000) // 目标透明度为0，持续时间为1秒
        .easing(TWEEN.Easing.Linear.None)
        .onUpdate(function (obj) {
          model.children.forEach(child => {
            if (child.isMesh) { // 如果子节点是mesh
              child.material.transparent = true;
              child.material.opacity = obj.opacity; // 调整透明度
            } else if (child.children.length > 0) {
              child.children.forEach(grandchild => {
                if (grandchild.isMesh) { // 如果孙节点是mesh
                  grandchild.material.transparent = true;
                  grandchild.material.opacity = obj.opacity; // 调整透明度
                }
              });
            }
          });
        })
        .onComplete(() => {
          this.scene.remove(model); // 动画结束后移除模型
          new TWEEN.Tween(this.camera.position)
            .to({ x: -434.0740788423603, y: 601.6679527037107, z: 1345.2141853240598 }, 1000) // 设置相机的新位置和移动时间
            .easing(TWEEN.Easing.Quadratic.Out)
            .onUpdate(() => {
              this.camera.lookAt(new THREE.Vector3(0, 0, 0)); // 每次更新时让相机指向目标位置
            })
            .start();
          if (this.currentModelType === 'school') {
            // 移动相机的逻辑
            // this.camera.lookAt(227.77032470703125, 52.10075378417969, 211.2912139892578);
            new TWEEN.Tween(this.camera.position)
              .to({ x: -434.0740788423603, y: 601.6679527037107, z: 1345.2141853240598 }, 1000) // 设置相机的新位置和移动时间
              .easing(TWEEN.Easing.Quadratic.Out)
              .onUpdate(() => {
                this.camera.lookAt(new THREE.Vector3(0, 0, 0)); // 每次更新时让相机指向目标位置
              })
              .start();
          }
          if (callback) callback(); // 调用回调函数加载新模型
        })
        .start();
    },
    // const vm = this,
    onClick(event) {
      const rect = this.$refs.sceneContainer.getBoundingClientRect();

      this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      if (this.currentModelType == 'school') {
        console.log('Currently loaded model: school');
        this.raycaster.setFromCamera(this.mouse, this.camera);
        const intersects = this.raycaster.intersectObjects(this.scene.children, true);
        console.log(intersects);
        if (intersects.length > 0) {
          this.classRoom = intersects[0].object;
          const ckey = this.classRoom.name
          this.classId = this.rectangleToClassMap[ckey]
          this.stateCode = 1
          this.saveState(this.stateCode);
          this.$emit('stateChanged', this.stateCode);
          this.$store.dispatch('updateClassId', this.classId);
          this.hideCurrentModel(this.schoolModel, () => {
            this.currentModelType = 'class'
            this.loadClassModel();
          });
        }
      } else if (this.currentModelType == 'class') {
        console.log('Currently loaded model: class');
        this.raycaster.setFromCamera(this.mouse, this.camera);
        const intersects = this.raycaster.intersectObjects(this.scene.children, true);
        console.log(intersects);
        if (intersects.length > 0) {
          this.student = intersects[0].object;
          this.student.material.color.set(0xff0000);
          // 获取学生的ID
          const studentName = this.student.name;
          const numberMatch = studentName.match(/\d+/);
          // console.log("this.mappedStudents", this.mappedStudents)
          const number = numberMatch ? parseInt(numberMatch[0], 10) : null; // 将匹配到的数字字符串转换为整数
          const foundStudent = this.mappedStudents.find(student => student.mapped == number);
          this.stateCode = 2
          this.saveState(this.stateCode);
          this.$emit('stateChanged', this.stateCode);
          this.$store.dispatch('updateStudentId', foundStudent.original);
          // 从studentsPositions中获取位置信息
          const targetPosition = new THREE.Vector3(
            this.studentsPositions[studentName].x,
            this.studentsPositions[studentName].y,
            this.studentsPositions[studentName].z
          );
          console.log('目标学生的', this.student)
          console.log('全部学生的坐标信息', this.studentsPositions)
          console.log('targetPosition', targetPosition)
          new TWEEN.Tween(this.camera.position)
            .to({
              x: targetPosition.x + 301,
              y: targetPosition.y + 89,
              z: targetPosition.z + 279
            }, 1000)
            .easing(TWEEN.Easing.Quadratic.Out)
            .onComplete(() => {
              // 确保动画完成后相机仍然指向目标位置
              // this.camera.lookAt(targetPosition);
            })
            .start();
        }
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
        for (let i = 0; i <= 99; i++) {
          studentNumbers.push(i);
        }
        studentNumbers = this.shuffleArray(studentNumbers);
        this.receivedStudent = data.students
        // 创建映射
        this.mappedStudents = this.receivedStudent.map((student, index) => {
          return { original: student, mapped: studentNumbers[index] };
        });
        this.appearStudent = this.mappedStudents.map(student => student.mapped);
        // console.log("allStudent", this.allStudent)
        this.container = new THREE.Object3D();
        this.appearStudent.forEach(index => {
          const mesh = this.allStudent[index]; // 因为appearStudent中的值是1到100的数，需要减1以匹配allStudent的索引
          console.log(mesh)
          if (mesh) { // 确保mesh存在
            this.container.add(mesh);
            // 将容器添加到场景中
            this.scene.add(this.container);
            // 对容器进行放大操作，而不是对模型直接进行放大
            this.container.scale.set(2, 2, 2); // 重新应用缩放设置
          }
        });
        this.animate();
      } else {
        console.log(222222222222222222222222)
        // console.log("allStudent", this.allStudent)
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
            this.container.scale.set(2, 2, 2); // 重新应用缩放设置
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

/* .view-controls button {
  margin: 10px;
  padding: 10px 20px;
  font-size: 10px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
  background-color: #4CAF50;
  color: white;
} */

/* .view-controls button:hover {
  background-color: #45a049;
} */

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