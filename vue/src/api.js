import axios from 'axios'
import store from '@/store'
import router from '@/router'

const apiURL = process.env.API_URL

const apiBase = axios.create({
  baseURL: apiURL,
  timeout: 1000
})

const setToken = () => {
  if (store.getters.getToken) {
    apiBase.defaults.headers['Authorization'] = 'Token ' + store.getters.getToken
  } else if (apiBase.defaults.headers['Authorization']) {
    delete apiBase.defaults.headers['Authorization']
  }
}

const api = {
  apiBase,
  setToken: () => {
    if (store.getters.getToken) {
      setToken()
      apiBase.post('token/valid/').catch(() => {
        store.dispatch('setToken', '').then(() => {
          setToken()
          router.push({ path: '/login' })
        })
      })
    } else {
      setToken()
    }
  },
  login: (username, password) => {
    return new Promise((resolve, reject) => {
      apiBase.post('token/', {
        username: username,
        password: password
      }).then(response => {
        store.dispatch('setToken', response.data.token).then(() => {
          setToken()
          resolve()
        })
      }).catch(() => {
        reject(new Error('Unable to log in with provided credentials.'))
      })
    })
  },
  logout: () => {
    apiBase.post('logout/').then(() => {
      store.dispatch('setToken', '').then(() => {
        setToken()
        router.push({ path: '/login' })
      })
    })
  },
  getTicks: () => apiBase.get('ticks/', {
    params: {
      interval: store.getters.getScale
    }
  }).then(response => {
    store.dispatch('setTicks', response.data)
  })
}

export default api
