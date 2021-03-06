import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import axios from "axios";
import VueAxios from "vue-axios";
import Vuex from "vuex";
import {
  v4 as uuidv4
} from "uuid";
import VueCookies from 'vue-cookies'
import Vuelidate from 'vuelidate'
import VuePersianDatetimePicker from 'vue-persian-datetime-picker';

Vue.config.productionTip = false;

Vue.use(VueCookies)
Vue.use(VueAxios, axios);
Vue.use(Vuex);
Vue.use(Vuelidate);

Vue.use(VuePersianDatetimePicker, {
  name: 'custom-date-picker',
  props: {
    inputFormat: 'YYYY-MM-DD',
    format: 'jYYYY-jMM-jDD',
    editable: false,
    inputClass: 'v-input v-input--dense',
    placeholder: 'تاریخ',
    altFormat: 'YYYY-MM-DD',
    color: '#1976d2',
    autoSubmit: false,
  }
});
Vue.$cookies.config('7d')


const store = new Vuex.Store({
  state: {
    loading: false,
    path: "",
    starmap: {
      roban: false,
      paint: true,
      shape: false,
      geo: {
        location: "",
        date: "",
        time: "",
        province: "",
        city: "",
      },
      text: {
        line1: {
          value: "",
          font: "",
          size: "42",
          color: "#ffffff",
        },
        line2: {
          value: "",
          font: "",
          size: "42",
          color: "#ffffff",
        },
        line3: {
          value: "",
          font: "",
          size: "42",
          color: "#ffffff",
        },
      },
      music: {
        qr: "",
      },
      background: {
        bg: "",
        x: 0,
        y: 0,
        opacity: 40,
        circle: true,
      },
      customize: {
        size: "A3",
        frame: "#212121",
        background: "#000000",
        wallpaper: "",
        dot: true,
        star: true,
        constellation: true,
        constellationText: true,
      },
      filename: uuidv4() + ".svg",
    },
  },
  mutations: {
    setLoading(state, loading){
      state.loading = loading;
    },
    setCircle(state, circle){
      state.starmap.background.circle = circle;
    },
    setGeo(state, geo) {
      state.starmap.geo = geo;
    },
    setText(state, text) {
      state.starmap.text = text;
    },
    setCustomize(state, customize) {
      state.starmap.customize = customize;
    },
    setMusic(state, music) {
      state.starmap.music = music;
    },
    setBg(state, bg) {
      state.starmap.background = bg;
    },
    setImage(state, path) {
      state.path = path;
    },
    setShape(state, shape) {
      state.starmap.shape = shape;
    },
    setWallpaper(state, wallpaper) {
      state.starmap.customize.wallpaper = wallpaper;
    },
    setProduct(state, product){
      state.starmap = product
    },
    setRoban(state, roban){
      state.starmap.roban = roban
    },
  },
  actions: {
    async getStarMap(context) {
      context.commit("setLoading", true);
      await setTimeout(() => {
        axios
          .post("/api/starmap", context.state.starmap)
          .then((response) => {
            if (response.data.result) {
              context.commit("setImage", response.data.path + `?${Date.now()}`);
            }
            context.commit("setLoading", false);
          })
          .catch((error) => {
            console.log(error);
            context.commit("setLoading", false);
          });
      }, 500);
    },
  },
});

new Vue({
  router,
  vuetify,
  store,
  render: (h) => h(App),
}).$mount("#app");