import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import axios from 'axios'
import VueAxios from 'vue-axios'
import Vuex from 'vuex'
import { v4 as uuidv4 } from 'uuid';

Vue.config.productionTip = false

Vue.use(VueAxios, axios)
Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    path: "",
    starmap:{
      "paint": true,
        "geo": {
            "coordinate": '',
            "date": '',
            "time": '',
        },
        "text": {
            "line1": {
                value: "",
                font: "",
                size: "42",
                color: "#ffffff"
            },
            "line2": {
                value: "",
                font: "",
                size: "42",
                color: "#ffffff"
            },
            "line3": {
                value: "",
                font: "",
                size: "42",
                color: "#ffffff"
            },
        },
        "music": {
          "qr": "",
        },
        "background": {
          "bg":"",
          "x": "",
          "y": "",
        },
        "customize": {
            "size": "A3",
            "frame": "#212121",
            "background": "#000000",
            "dot": true,
            "star": true,
            "constellation": true,
            "constellationText": true,
        },
        "filename": uuidv4() + ".svg"
    }
  },
  mutations: {
    setGeo(state, geo){
      state.starmap.geo = geo
    },
    setText(state, text){
      state.starmap.text = text
    },
    setCustomize(state, customize){
      state.starmap.customize = customize
    },
    setMusic(state, music){
      state.starmap.music = music
    },
    setBg(state, bg){
      state.starmap.background = bg
    },
    setImage(state, path){
      state.path = path
    }
  }
})

new Vue({
  router,
  vuetify,
  store,
  render: h => h(App)
}).$mount('#app')
