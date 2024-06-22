<template>
  <div ref="sceneContainer" class="scene-container" @click="onClick" @wheel="onMouseWheel">
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
  </div>
</template>

<script>
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader.js';
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter.js'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import TWEEN from '@tweenjs/tween.js';
import PubSub from 'pubsub-js';
import moment from 'moment';
import EventBus from '@/eventBus'; // 导入事件总线
import { openDB } from 'idb';
import Dexie from 'dexie';


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
    const targetCameraPosition = [
      // 0-9
      {
        "x": 260.9451318010503,
        "y": 121.01175547922786,
        "z": 264.5779856424498
      },
      {
        "x": 256.4460598448812,
        "y": 112.47649131153608,
        "z": 201.24921595617516
      },
      {
        "x": 253.24984916171297,
        "y": 115.33130385468333,
        "z": 103.4213792856595
      },
      {
        "x": 262.6042916397912,
        "y": 115.33130385468343,
        "z": 32.64788755665819
      },
      {
        "x": 256.8089188369539,
        "y": 115.3313038546834,
        "z": -62.013572156377165
      },
      {
        "x": 267.3592589608598,
        "y": 117.27152236292184,
        "z": -141.14634731640814
      },
      {
        "x": 262.7376158609089,
        "y": 117.27152236292184,
        "z": -232.90845042666302
      },
      {
        "x": 264.62503259881066,
        "y": 117.27144298965285,
        "z": -292.7377617354548
      },
      {
        "x": 256.95053856957196,
        "y": 117.27144298965287,
        "z": -379.6126188666117
      },
      {
        "x": 260.9226517313524,
        "y": 117.27144298965287,
        "z": -449.1206805005736
      },
      // 10-19
      {
        "x": 152.98611230951792,
        "y": 118.90037354596092,
        "z": 262.1855245780209
      },
      {
        "x": 154.02540931548788,
        "y": 118.90037354596092,
        "z": 200.40102397278156
      },
      {
        "x": 156.7386338221866,
        "y": 118.90037354596092,
        "z": 94.90402157009014
      },
      {
        "x": 163.4844668753403,
        "y": 123.47967173265597,
        "z": 33.6269263864331
      },
      {
        "x": 160.28630096161305,
        "y": 123.47967173265599,
        "z": -64.66739581278003
      },
      {
        "x": 159.72733166663193,
        "y": 130.65322527551234,
        "z": -134.86999613637897
      },
      {
        "x": 157.14464097499797,
        "y": 130.65322527551234,
        "z": -233.00940471501502
      },
      {
        "x": 158.18272989565392,
        "y": 130.65322527551234,
        "z": -292.91684038728994
      },
      {
        "x": 159.64892049591404,
        "y": 130.65322527551206,
        "z": -398.4906391487441
      },
      {
        "x": 159.08819451329137,
        "y": 130.65322527551206,
        "z": -458.5304688656554
      },
      // 20-29
      {
        "x": 57.27983254750367,
        "y": 115.89866956207285,
        "z": 259.10003942948316
      },
      {
        "x": 59.133682161220634,
        "y": 115.89866956207285,
        "z": 200.82476858987545
      },
      {
        "x": 57.701326946518776,
        "y": 115.89866956207285,
        "z": 96.53327360959247
      },
      {
        "x": 57.04998443610913,
        "y": 115.89866956207285,
        "z": 36.26840865281525
      },
      {
        "x": 58.12285001518501,
        "y": 115.89866956207285,
        "z": -66.03346944120048
      },
      {
        "x": 59.332202120203874,
        "y": 115.89866956207285,
        "z": -129.92722308243125
      },
      {
        "x": 58.9037931748166,
        "y": 115.89866956207285,
        "z": -232.91079503541286
      },
      {
        "x": 58.694508738210914,
        "y": 115.89866956207287,
        "z": -291.8032565775213
      },
      {
        "x": 58.256969695194016,
        "y": 115.89866956207285,
        "z": -397.34733244047027
      },
      {
        "x": 55.80028258138873,
        "y": 115.89866956207285,
        "z": -455.98200256879625
      },
      // 30-39
      {
        "x": -49.88330732925738,
        "y": 110.97626450816873,
        "z": 260.1900896223399
      },
      {
        "x": -49.375862685577204,
        "y": 110.97626450816873,
        "z": 99.83183431072771
      },
      {
        "x": -48.92910941283492,
        "y": 110.97626450816873,
        "z": 96.09646254052126
      },
      {
        "x": -49.66563988389299,
        "y": 110.97626450816873,
        "z": 35.01957684221435
      },
      {
        "x": -50.49513512045729,
        "y": 110.97626450816873,
        "z": -64.69469944555442
      },
      {
        "x": -49.988878345267494,
        "y": 110.97626450816873,
        "z": -125.34576435458206
      },
      {
        "x": -49.547821094837616,
        "y": 110.97626450816873,
        "z": -227.95754030872627
      },
      {
        "x": -47.77803570570586,
        "y": 110.97626450816873,
        "z": -290.6752564417088
      },
      {
        "x": -50.653376881629754,
        "y": 110.97626450816873,
        "z": -394.14559621534545
      },
      {
        "x": -49.74898828091739,
        "y": 110.97626450816873,
        "z": -452.7161526351621
      },
      // 40-49
      {
        "x": -149.31189273631213,
        "y": 110.97602833463263,
        "z": 262.81487265574646
      },
      {
        "x": -149.51520603367408,
        "y": 110.97602833463263,
        "z": 198.8331222912944
      },
      {
        "x": -149.8874345023413,
        "y": 110.97602833463263,
        "z": 98.70675837238971
      },
      {
        "x": -149.6552737899442,
        "y": 110.97602833463263,
        "z": 35.96447972834005
      },
      {
        "x": -149.19668259541254,
        "y": 110.97602833463263,
        "z": -64.1753535424383
      },
      {
        "x": -149.41350183917228,
        "y": 110.97602833463263,
        "z": -128.98783422088735
      },
      {
        "x": -149.4173450220934,
        "y": 110.97602833463263,
        "z": -232.02854995440794
      },
      {
        "x": -149.4173450220934,
        "y": 110.97602833463263,
        "z": -232.02854995440794
      },
      {
        "x": -150.41501738973557,
        "y": 110.97602833463263,
        "z": -396.5452635402859
      },
      {
        "x": -153.96756084843798,
        "y": 110.97602833463263,
        "z": -456.8136039559413
      },
      // 50-59
      {
        "x": -254.75101066309526,
        "y": 110.73892057060502,
        "z": 255.1000557997839
      },
      {
        "x": -253.21716536850045,
        "y": 110.73892057060502,
        "z": 198.99282689743956
      },
      {
        "x": -254.14794738718183,
        "y": 110.73892057060502,
        "z": 90.46149848221205
      },
      {
        "x": -254.57170515155065,
        "y": 110.73892057060502,
        "z": 25.80990441728295
      },
      {
        "x": -253.67099891859584,
        "y": 110.73892057060502,
        "z": -71.10439363169087
      },
      {
        "x": -254.28403775292634,
        "y": 110.73892057060502,
        "z": -131.14691217333052
      },
      {
        "x": -253.93077394686054,
        "y": 110.73892057060502,
        "z": -233.46989034701426
      },
      {
        "x": -253.99631769541486,
        "y": 110.73892057060502,
        "z": -288.1038674935746
      },
      {
        "x": -254.12730757355814,
        "y": 110.73892057060502,
        "z": -397.37191170684287
      },
      {
        "x": -254.12978267843266,
        "y": 110.73892057060502,
        "z": -453.54220925286654
      },
      // 60-69
      {
        "x": -355.3483725861065,
        "y": 114.73892057060502,
        "z": 250.20099705797873
      },
      {
        "x": -354.67729045676776,
        "y": 114.73892057060502,
        "z": 196.36671443299178
      },
      {
        "x": -354.26095800703115,
        "y": 114.73892057060502,
        "z": 92.50741585984065
      },
      {
        "x": -354.87401932140153,
        "y": 114.73892057060502,
        "z": 32.46487291345545
      },
      {
        "x": -355.2572837742689,
        "y": 114.73892057060502,
        "z": -70.6578897019549
      },
      {
        "x": -356.6068733475639,
        "y": 114.73892057060502,
        "z": -131.50021709006398
      },
      {
        "x": -354.8434264293903,
        "y": 114.73892057060502,
        "z": -230.68748582114097
      },
      {
        "x": -356.2560846463705,
        "y": 114.73892057060502,
        "z": -289.9934928097854
      },
      {
        "x": -355.10312631872887,
        "y": 114.73892057060502,
        "z": -393.05309686136525
      },
      {
        "x": -354.7902582052078,
        "y": 114.73892057060502,
        "z": -456.90499640472353
      },
      // 70-79
      {
        "x": -454.240495945044,
        "y": 114.73892057060502,
        "z": 259.99148745761374
      },
      {
        "x": -454.72732235309275,
        "y": 114.73892057060502,
        "z": 196.87621379215182
      },
      {
        "x": -455.29979273699985,
        "y": 114.73892057060502,
        "z": 98.36241237514139
      },
      {
        "x": -454.31341234933745,
        "y": 114.73892057060502,
        "z": 36.84647894334296
      },
      {
        "x": -456.35923210799103,
        "y": 114.73892057060502,
        "z": -63.26662159666148
      },
      {
        "x": -455.92022670710537,
        "y": 114.73892057060502,
        "z": -130.19116193894865
      },
      {
        "x": -454.156779788936,
        "y": 114.73892057060502,
        "z": -229.3784306700203
      },
      {
        "x": -454.5805150732666,
        "y": 114.73892057060502,
        "z": -294.0300003302074
      },
      {
        "x": -455.76347404771,
        "y": 114.73892057060502,
        "z": -396.41613706772114
      },
      {
        "x": -455.63971424626754,
        "y": 114.73892057060502,
        "z": -455.6591653328335
      },
      // 80-89
      {
        "x": -556.2479581424446,
        "y": 94.73892057060502,
        "z": 251.95641740918018
      },
      {
        "x": -557.0502253878516,
        "y": 114.73892057060502,
        "z": 196.52283566119286
      },
      {
        "x": -557.244283909681,
        "y": 114.73892057060502,
        "z": 88.79111184738747
      },
      {
        "x": -557.7311103177248,
        "y": 114.73892057060502,
        "z": 25.675838181924405
      },
      {
        "x": -557.3777938527768,
        "y": 114.73892057060502,
        "z": -76.64727872138826
      },
      {
        "x": -556.0331544892266,
        "y": 114.73892057060502,
        "z": -128.14554642533562
      },
      {
        "x": -557.0270051515832,
        "y": 114.73892057060502,
        "z": -235.14055444109363
      },
      {
        "x": -555.4299935943496,
        "y": 114.73892057060502,
        "z": -292.78419366305764
      },
      {
        "x": -555.876424309855,
        "y": 114.73892057060502,
        "z": -394.3705459588475
      },
      {
        "x": -556.3632507178978,
        "y": 114.73892057060502,
        "z": -457.48581962430853
      },
      // 90-99
      {
        "x": -656.0026494286934,
        "y": 114.73892057060502,
        "z": 264.01967424591106
      },
      {
        "x": -657.710453017805,
        "y": 114.73892057060502,
        "z": 193.15972993943774
      },
      {
        "x": -657.4833264991024,
        "y": 114.73892057060502,
        "z": 93.90939256468357
      },
      {
        "x": -657.170480865614,
        "y": 114.73892057060502,
        "z": 30.057468616590654
      },
      {
        "x": -652.5977226938215,
        "y": 114.73892057060473,
        "z": -71.62283842810973
      },
      {
        "x": -653.3070813669209,
        "y": 114.73892057060473,
        "z": -132.35947175768354
      },
      {
        "x": -652.6274677550392,
        "y": 114.73892057060473,
        "z": -230.8124860448296
      },
      {
        "x": -651.9494279378076,
        "y": 114.73892057060473,
        "z": -297.7350767635012
      },
      {
        "x": -651.9448507106241,
        "y": 114.73892057060473,
        "z": -392.3264847743686
      },
      {
        "x": -652.8413391579687,
        "y": 114.73892057060473,
        "z": -460.7487715255779
      }
    ];
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
      targetCameraPosition,
      rectangleToClassMap,
      allStudent: [],
      appearStudent: [],
      mappedStudents: [],
      receivedStudent: [],
      classId: null,
      db: null,
      modelLoaded: false,
      isClass: false,
      flashing: false,
      flashStartTime: null,
      flashDuration: 1000, // 闪烁持续时间（毫秒）
    };
  },
  async mounted() {
    this.db = await this.openDB();
    this.initThreeJS();
    this.subscriptionToken = PubSub.subscribe('studentAppear', (msg, value) => {
      this.handleStudentAppear(value);
    });
    this.subscriptionTokenClass = PubSub.subscribe('classChange', (msg, value) => {
      this.handleClassClick(value);
    });
  },
  created() {
    EventBus.$on('studentSelected', this.handleStudentSelected);
    EventBus.$on('checkSelected', this.handleCheckSelected);
    EventBus.$on('heatmapStudentIdSelected', this.handleHeatmapSelected);
    
  },
  beforeDestroy() {
    EventBus.$off('studentSelected', this.handleStudentSelected);
    EventBus.$off('checkSelected', this.handleCheckSelected);
    EventBus.$off('heatmapStudentIdSelected', this.handleHeatmapSelected);
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
      console.log("handle foundStudent", foundStudent)
      this.student = this.allStudent[foundStudent.mapped]
      console.log("handleStudentSelected", this.student)

      // this.student.material.color.set(0xff0000);
      const studentName = this.student.name;
      const numberMatch = studentName.match(/\d+/);
      // console.log("this.mappedStudents", this.mappedStudents)
      const number = numberMatch ? parseInt(numberMatch[0], 10) : null; // 将匹配到的数字字符串转换为整数
      // 从studentsPositions中获取位置信息
      const targetPosition = new THREE.Vector3(
        this.targetCameraPosition[number].x,
        this.targetCameraPosition[number].y,
        this.targetCameraPosition[number].z
      );
      new TWEEN.Tween(this.camera.position)
        .to({
          x: targetPosition.x,
          y: targetPosition.y,
          z: targetPosition.z
        }, 1000)
        .easing(TWEEN.Easing.Quadratic.Out)
        .onComplete(() => {
        })
        .start();

    },
    // TODO: 点击github打卡图，主视图跳转日期且显示对应学生，由此可以再拖拽查看其他人情况
    // data:{student_id:" ",year:" ",month:" ",date:" "}
    handleCheckSelected(data) {
      console.log('modelview dataselect:', data)

    },
    // 处理热力图传过来的学生id
    handleHeatmapSelected(student_id){
      this.handleStudentSelected(student_id)

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
      this.camera = new THREE.PerspectiveCamera(50, aspect, 0.1, 3000);

      // const axesHelper = new THREE.AxesHelper(20000);
      // this.scene.add(axesHelper);
      // 创建渲染器
      this.renderer = new THREE.WebGLRenderer({ antialias: true });
      this.renderer.setSize(this.$refs.sceneContainer.clientWidth, this.$refs.sceneContainer.clientHeight);
      this.renderer.setClearColor(0xffffff);
      this.$refs.sceneContainer.appendChild(this.renderer.domElement);
      // 添加光源
      this.addLights();
      // // 添加轨道控制
      // this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      // this.controls.enableDamping = true; // 启用阻尼效果
      // this.controls.dampingFactor = 0.25; // 阻尼系数
      // this.controls.screenSpacePanning = false; // 禁用屏幕空间平移

      this.db = new Dexie('threemodel')
      this.db.version(0.1).stores(
        {
          localVersions: 'matadataid, content, lastversionid, date, time',
          users: '++id, name, &username, *email, address.city',
          relations: '++rid, userId1, userId2, [userId1+userId2], relation',
          books: 'id, author, name, *categories',
          model: 'id, name, type, file'
        }
      )
      this.blobChange()
      const savedState = this.getSavedState()
      if (savedState == 0) {
        this.loadSchoolModel();
      } else {
        this.loadClassModel()
      }
      this.animate();
      this.initialView();
    },
    // 修改model表里的数据
    putDataToIndexDB(blob) {
      // 一定要处理成二进制 this.blobChange()返回的是一个blob对象
      console.log(blob)
      this.db.model.put({
        id: 'classRoom',
        name: '教室模型',
        type: blob.type,
        file: blob
      })
    },
    blobChange() {
      this.$axios({
        method: 'get',
        url: '/models/student101_4.glb',
        responseType: 'blob',
        crossOrigin: true,
        withCredentials: true
      }).then(res => {
        console.log(res.data)
        // 写入indexDB数据库
        this.putDataToIndexDB(res.data)
      })
    },
    addDataDB(obj) {
      this.db.model.add(obj)
    },
    updateDataDB(obj) {
      this.db.model.put(obj)
    },
    delDataDB(key) {
      this.db.model.delete(key)
    },
    getDataDB(key) {
      return this.db.model.get(key)
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
    loadClassModel() {
      const loadModelPromise = () => {
        return new Promise((resolve, reject) => {
          const mtlLoader = new MTLLoader();
          mtlLoader.load(
            '/models/classroom.mtl', // 替换为你的MTL文件路径
            (materials) => {
              materials.preload();
              const objLoader = new OBJLoader();
              objLoader.setMaterials(materials);
              objLoader.load(
                '/models/classroom.obj', // 替换为你的OBJ文件路径
                (object) => {
                  console.log("obj", object)

                  const ambientLight = new THREE.AmbientLight(0xffffff, 1);// 增加环境光强度，可以减少阴影
                  this.scene.add(ambientLight);

                  const directionalLight = new THREE.DirectionalLight(0xffffff, 3);// 平行光，即太阳光，会生成阴影。
                  directionalLight.position.set(5, 10, 7.5);
                  this.scene.add(directionalLight);

                  this.scene.add(object);
                  this.classModel = object
                  this.classModel.scale.set(2, 2, 2);
                  this.classModel.name = 'class'
                  this.currentModelType = 'class'; // 标记当前加载的文件类型
                  this.modelLoaded = true;
                  const currentPosition = this.camera.position.clone();
                  const targetPosition = new THREE.Vector3(608.3748006602943, 246.87681215346672, 507.9700608328807);

                  new TWEEN.Tween(currentPosition)
                    .to(targetPosition, 5000)
                    .easing(TWEEN.Easing.Quadratic.Out)
                    .onUpdate(() => {
                      this.camera.position.copy(currentPosition);
                      // this.camera.lookAt(227.77032470703125, 52.10075378417969, 211.2912139892578);
                      this.camera.lookAt(0, 0, 0)
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
                  resolve();
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
        });
      };

      loadModelPromise().then(() => {
        // 模型加载完成后执行axios.get请求
        this.$axios.get(`http://10.12.44.190:8000/getStudentByClass/?className=${this.classId}`, {
          // params: {
          //   className: this.classId,
          // }
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
    //   const loadModelPromise = () => {
    //     return new Promise((resolve, reject) => {
    //       const modeldata = this.getDataDB('classRoom')
    //       console.log("modeldata", modeldata)
    //       const modelUrl = URL.createObjectURL(new Blob([modeldata.file]))
    //       var loader = new GLTFLoader();
    //       loader.load(modelUrl, (gltf) => {
    //         console.log(gltf)
    //         this.scene.add(gltf.scene)








    //       });
    //         (error) => {
    //           console.log('An error happened', error);
    //         }

    //     });
    //   };

    //   loadModelPromise().then(() => {
    //     // 模型加载完成后执行axios.get请求
    //     this.$axios.get(`http://10.12.44.190:8000/getStudentByClass/?className=${this.classId}`, {
    //       // params: {
    //       //   className: this.classId,
    //       // }
    //     })
    //       .then(response => {
    //         console.error('success sending data:', JSON.parse(response.data));

    //         let studentNumbers = [];
    //         for (let i = 0; i <= 99; i++) {
    //           studentNumbers.push(i);
    //         }
    //         studentNumbers = this.shuffleArray(studentNumbers);
    //         this.receivedStudent = JSON.parse(response.data).students;
    //         // 创建映射
    //         this.mappedStudents = this.receivedStudent.map((student, index) => {
    //           return { original: student, mapped: studentNumbers[index] };
    //         });
    //         this.appearStudent = this.mappedStudents.map(student => student.mapped);
    //         console.log("appearStudent", this.appearStudent);

    //         this.container = new THREE.Object3D();
    //         this.appearStudent.forEach(index => {
    //           const mesh = this.allStudent[index - 1];
    //           if (mesh) { // 确保mesh存在
    //             this.container.add(mesh);
    //             // 将容器添加到场景中
    //             this.scene.add(this.container);
    //             // 对容器进行放大操作，而不是对模型直接进行放大
    //             this.container.scale.set(2, 2, 2); // 重新应用缩放设置
    //           }
    //         });
    //         this.animate();
    //       })
    //       .catch(error => {
    //         console.error('Error sending data:', error);
    //       });
    //   });
    // },
    animate() {
      requestAnimationFrame(this.animate);
      TWEEN.update();
      // this.controls.update();
      // 处理闪烁效果
      if (this.flashing) {
        const elapsed = Date.now() - this.flashStartTime;
        if (elapsed > this.flashDuration) {
          this.flashing = false;
          this.student.material.color.set("#8B8878"); // 恢复到原始颜色
        } else {
          const colorIntensity = (Math.sin(elapsed * 0.01) + 1) / 2; // 0到1之间的值
          const outlineColor = new THREE.Color("#F0FFFF"); // 轮廓颜色
          this.student.material.color.lerp(outlineColor, colorIntensity);
        }
      }

      this.renderer.render(this.scene, this.camera);
    },
    initialView() {
      //原方案
      // this.camera.position.set(0, 400, 0);
      //初始相机看第一个学生
      this.camera.position.set(-1091.4201478569894, -36.93155271255154, 1781.8372416770653)
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
          this.flashing = true;
          this.flashStartTime = Date.now();
          // this.student.material.color.set("#fdb933");
          // 获取学生的ID
          const studentName = this.student.name;
          const numberMatch = studentName.match(/\d+/);
          // console.log("this.mappedStudents", this.mappedStudents)
          const number = numberMatch ? parseInt(numberMatch[0], 10) : null; // 将匹配到的数字字符串转换为整数
          const foundStudent = this.mappedStudents.find(student => student.mapped == number);
          this.stateCode = 2
          this.saveState(this.stateCode);
          this.$emit('stateChanged', this.stateCode);
          console.log(foundStudent.original)
          this.$store.dispatch('updateStudentId', foundStudent.original);
          PubSub.publish('studentId', foundStudent.original);
          // 从studentsPositions中获取位置信息
          const studentPosition = new THREE.Vector3(
            this.student.position.x,
            this.student.position.y,
            this.student.position.z
          );
          const targetPosition = new THREE.Vector3(
            this.targetCameraPosition[number].x,
            this.targetCameraPosition[number].y,
            this.targetCameraPosition[number].z
          );
          console.log('目标学生的', this.student)
          console.log('全部学生的坐标信息', this.studentsPositions)
          console.log('targetPosition', targetPosition)
          new TWEEN.Tween(this.camera.position)
            .to({
              x: targetPosition.x,
              y: targetPosition.y,
              z: targetPosition.z
            }, 1000)
            .easing(TWEEN.Easing.Quadratic.Out)
            // .onUpdate(() => {
            //   // 确保动画完成后相机仍然指向目标位置
            //   this.camera.lookAt(studentPosition);
            // })
            .onComplete(() => {
              // 确保动画完成后相机仍然指向目标位置
              // this.camera.lookAt(studentPosition);
            })
            .start();
        }
      }
    },
    onMouseWheel(event) {
      new TWEEN.Tween(this.camera.position)
        .to({ x: 608.3748006602943, y: 246.87681215346674, z: 507.9700608328807 }, 1000) // 设置相机的新位置和移动时间
        .easing(TWEEN.Easing.Quadratic.Out)
        .start();
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
        // console.log(1111111111111111111111111)
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
    handleClassClick(data) {
      const meshName = Object.keys(this.rectangleToClassMap).find(k => this.rectangleToClassMap[k] === data);
      console.log(meshName)
      this.schoolModel.traverse((child) => {
        if (child.isMesh && child.name.includes(meshName)) {
          console.log(child);

          // 保存原始材质
          const originalMaterial = child.material;

          // 创建一个新的材质来实现闪烁效果
          const flashMaterial = originalMaterial.clone();
          flashMaterial.color.set("BE5454"); // 设置为红色，您可以根据需要调整颜色
          flashMaterial.transparent = true; // 确保新材质是透明的
          flashMaterial.opacity = 0.3; // 设置不透明度为完全不透明

          // 应用新的闪烁材质
          child.material = flashMaterial;

          // 设置闪烁持续时间
          const duration = 500; // 500毫秒，您可以根据需要调整时间

          // 闪烁后恢复原始材质
          setTimeout(() => {
            child.material = originalMaterial;
          }, duration);
        }
      });
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