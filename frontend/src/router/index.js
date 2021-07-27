import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Builder from '@/views/Builder'
import Pay from '@/views/Pay'
import Admin from '@/views/Admin'

Vue.use(VueRouter)

const routes = [
  {
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
  },{
    path: '/admin',
    name: "Admin",
    component: Admin,
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
