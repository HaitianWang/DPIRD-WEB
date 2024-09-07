import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    username: null
  },
  mutations: {
    setUsername(state, username) {
      state.username = username
    }
  },
  actions: {
    login({ commit }, username) {
      commit('setUsername', username)
    },
    logout({ commit }) {
      commit('setUsername', null)
    }
  },
  getters: {
    isLoggedIn: state => !!state.username,
    getUsername: state => state.username
  }
})