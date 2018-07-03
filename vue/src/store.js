import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'

Vue.use(Vuex)

const vuexLocal = new VuexPersistence({
  storage: window.localStorage,
  reducer: (state) => ({
    token: state.token,
    scale: state.scale
  })
})

const state = {
  token: '',
  ticks: [],
  scale: '6h',
  colors: {
    $blue: '#1e88e5',
    $red: '#c62828',
    $yellow: '#ffc107',
    $green: '#26a69a',
    $cyan: '#00acc1'
  }
}

const mutations = {
  setToken (state, token) {
    state.token = token
  },
  setTicks (state, ticks) {
    state.ticks = ticks
  },
  setScale (state, scale) {
    state.scale = scale
  }
}

const actions = {
  setToken: ({ commit }, token) => commit('setToken', token),
  setTicks: ({ commit }, ticks) => commit('setTicks', ticks),
  setScale: ({ commit }, scale) => commit('setScale', scale)
}

const getters = {
  getToken: state => state.token,
  getTicks: state => state.ticks,
  getScale: state => state.scale,
  getColors: state => state.colors
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
  plugins: [vuexLocal.plugin]
})
