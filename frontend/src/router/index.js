import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import Builder from '@/views/Builder'
import Pay from '@/views/Pay'
import Admin from '@/views/Admin'
import Login from '@/views/Login'
import Verify from '@/views/Verify'

import axios from 'axios';


Vue.use(VueRouter)

const routes = [{
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/builder',
    name: "StarmapBuilder",
    component: Builder
  },
  {
    path: '/pay',
    name: "Payment",
    component: Pay,
  },
  {
    path: '/admin',
    name: "Admin",
    component: Admin,
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/verify",
    name: "verify",
    component: Verify,
    props: (route) => ({
      status: route.query.status,
      token: route.query.token
    })
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next)=>{
  let token = Vue.$cookies.get('token');
  if(token === null && to.fullPath === '/admin'){
    return next(to="/login")
  }
  if(to.fullPath === '/admin'){
    axios.get(process.env.VUE_APP_BACKEND + '/token/' + token).then(response=>{
      if(response.status === 200 && response.data.result){
        return next()
      }
      return next(to="/login")
    }).catch((error)=>{
      console.log(error);
      return next(to="/login")
    })
  }
  return next()
})

export default router