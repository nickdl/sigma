import Vue from 'vue'
import VueRouter from 'vue-router'
import Overview from '@/components/Overview'
import Login from '@/components/Login'
import store from '@/store'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Overview',
      component: Overview,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.length === 0) {
    next({ path: '/' })
  } else if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.getToken) {
      next({ path: '/login' })
    } else {
      next()
    }
  } else {
    if (store.getters.getToken && to.name === 'Login') {
      next({ path: '/' })
    } else {
      next()
    }
  }
})

export default router
