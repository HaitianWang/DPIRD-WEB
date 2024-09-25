import Vue from 'vue'
import Router from 'vue-router'
import frontPage from "../components/frontPage";
import mainPage from "../components/mainPage";
import regiPage from "../components/regiPage";
import uploadPage from "../components/uploadPage";
import timeCapsule from "../components/timeCapsule";
import store from '../store'
import userPage from "../components/userPage";

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'frontPage',
      component: frontPage
    },
    {
      path: '/mainPage',
      name: 'mainPage',
      component: mainPage,
      meta: { requiresAuth: true }
    },
    {
      path: '/regiPage',
      name: 'regiPage',
      component: regiPage
    },
    {
      path: '/uploadPage',
      name: 'uploadPage',
      component: uploadPage,
      meta: { requiresAuth: true }
    },
    {
      path: '/timeCapsule',
      name: 'timeCapsule',
      component: timeCapsule,
      meta: { requiresAuth: true }
    },
    {
      path: '/userPage',
      name: 'userPage',
      component: userPage,
      meta: { requiresAuth: true }
    },
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // Check if user is authenticated using Vuex store
    if (!store.getters.isLoggedIn) {
      next({
        path: '/',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
