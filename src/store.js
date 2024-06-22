import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    classId: '',
    studentId: ''
  },
  mutations: {
    setClassId(state, classId) {
      state.classId = classId;
    },
    setStudentId(state, studentId) {
      state.studentId = studentId;
      console.log("state.studentId",state.studentId)
    }
  },
  actions: {
    updateClassId({ commit }, classId) {
      commit('setClassId', classId);
    },
    updateStudentId({ commit }, studentId) {
      console.log('Payload received:', studentId); // 确保正确接收到数据
      commit('setStudentId', studentId);
    }
  },
  getters: {
    classId: state => state.classId,
    studentId: state => state.studentId,
  }
});
