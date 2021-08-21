<template>
  <div>
    <v-form ref="form" v-model="valid">
      <p style="font-size:1.3rem">انتخاب بکگراند کلی</p>
      <v-row>
        <v-col cols="6" lg="6" xl="6" md="6" sm="6">
          <v-radio-group @change="updateStar" v-model="showWallpaper">
            <v-radio @click="removeWallpaper" key="color" label="رنگی" :value="false" />
            <v-radio key="wallpaper" label="عکسی" :value="true" selected />
          </v-radio-group>
        </v-col>
      </v-row>
      <div v-show="showWallpaper === false">
        <v-row align="baseline">
          <v-col cols="6" lg="6" xl="6" md="6" sm="6">
            <p>رنگ بکگراند</p>
          </v-col>
        </v-row>
        <v-menu
          v-model="bgMenu"
          :close-on-content-click="false"
          :nudge-right="40"
          transition="scale-transition"
          offset-y
          min-width="290px"
          max-width="290px"
        >
          <template v-slot:activator="{ on }">
            <v-text-field
              label="رنگ"
              prepend-inner-icon="mdi-palette"
              readonly
              hide-details
              :value="bgValue"
              v-on="on"
              outlined
              dense
              class="mb-7"
            ></v-text-field>
          </template>

          <v-color-picker
            show-swatches
            hide-canvas
            hide-sliders
            hide-inputs
            :swatches="swatches"
            v-model="bgValue"
            @input="updateStar"
            no-title
          ></v-color-picker>
        </v-menu>
      </div>

      <div v-show="showWallpaper === true">
        <v-row align="baseline">
          <v-col cols="6">
            <p>عکس بکگراند</p>
          </v-col>
        </v-row>
        <v-container>
          <v-row>
            <v-col cols="12" xl="12" lg="12" md="12" sm="12">
              <swiper ref="wallpapers" :options="wallpaperOptions">
                <swiper-slide v-for="wallpaper in wallpapers" :key="wallpaper">
                  <img
                    class="wallpaper"
                    :src="
                      `https://sky.respina.store/api/assets/get/wallpapers/` + wallpaper
                    "
                    alt="bg"
                    width="100%"
                    height="300"
                  />
                </swiper-slide>
                <div class="swiper-pagination" slot="pagination"></div>
              </swiper>
              <p style="IRANSansX !important" class="text-center text--disabled text-caption">برای دیدن باقی عکس‌ها به چپ و یا راست بکشید</p>
            </v-col>
          </v-row>
        </v-container>
      </div>

      <v-divider class="my-5"></v-divider>

      <v-row dir="rtl">
        <v-col cols="12">
          <p class="mb-0">شخصی سازی ستاره ها و صور فلکی</p>
        </v-col>
        <v-col cols="12" xl="6" lg="6" md="12" sm="12">
          <v-switch @click="updateStar" v-model="showDot" inset label="نقطه‌ها" hide-details></v-switch>
        </v-col>
        <v-col cols="12" xl="6" lg="6" md="12" sm="12">
          <v-switch @click="updateStar" v-model="showStar" inset label="ستاره‌ها" hide-details></v-switch>
        </v-col>
        <v-col cols="12" xl="6" lg="6" md="12" sm="12">
          <v-switch
            @click="
            () => {
              updateStar();
              showConstellation ? '' : (showConstellationText = false);
            }
            "
            v-model="showConstellation"
            inset
            label="صور فلکی"
            hide-details
          ></v-switch>
        </v-col>
        <v-col cols="12" xl="6" lg="6" md="12" sm="12">
          <v-switch
            @click="updateStar"
            :disabled="!showConstellation ? true : false"
            v-model="showConstellationText"
            inset
            label="نام صور فلکی"
            hide-details
          ></v-switch>
        </v-col>
      </v-row>

      <v-divider class="my-5"></v-divider>

      <v-row no-gutters>
        <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
          <v-btn
            @click="$emit('update:stepper', 2)"
            color="error"
            outlined
            style="width:98%"
          >مرحله‌ی قبلی</v-btn>
        </v-col>
        <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
          <v-btn @click="$emit('update:stepper', 4)" style="width:98%" color="primary">مرحله‌ی بعدی</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script>
import { Swiper, SwiperSlide, directive } from 'vue-awesome-swiper'
import 'swiper/css/swiper.css';
export default {
  name: "star-customize",
  components: {
    Swiper,
    SwiperSlide
  },
  directives: {
    swiper: directive
  },
  watch: {
    showWallpaper: function () {
      if (this.showWallpaper) {
        const wallpapers = document.querySelectorAll(".wallpaper");
        wallpapers.forEach((wallpaper) => {
          wallpaper.addEventListener("click", () => {
            wallpapers.forEach((item) => (item.style.border = ""));
            wallpaper.style.border = "5px solid blue";
            this.$store.commit("setWallpaper", wallpaper.src);
            this.$store.dispatch("getStarMap");
          });
        });
      }
    },
  },
  computed: {
    swiper() {
      return this.$refs.wallpapers.$swiper
    }
  },
  data() {
    return {
      wallpaperOptions: {
        pagination: {
          el: '.swiper-pagination'
        },
        autoplay: {
          delay: 5000,
        },
        slidesPerView: 2,
        spaceBetween: 10,
        breakpoints: {
          // when window width is >= 320px
          320: {
            slidesPerView: 1,
            spaceBetween: 10
          },
          // when window width is >= 480px
          480: {
            slidesPerView: 1,
            spaceBetween: 10
          },
          // when window width is >= 640px
          640: {
            slidesPerView: 2,
            spaceBetween: 10
          }
        }
      },
      showWallpaper: false,
      valid: true,
      bgValue: "#000000",
      bgMenu: false,
      swatches: [
        ["#263238", "#212121", "#455A64", "#00ACC1"],
        ["#3949AB", "#004D40", "#C51162", "#4A148C"],
        ["#000000", "#81D4FA", "#FF6E40", "#2979FF"],
      ],

      showDot: true,
      showStar: true,
      showConstellation: true,
      showConstellationText: true,

      wallpapers: [],
    };
  },
  methods: {
    updateStar() {
      this.$store.commit("setCustomize", {
        size: this.$store.state.starmap.customize.size,
        background: this.bgValue,
        frame: this.$store.state.starmap.customize.frame,
        dot: this.showDot,
        star: this.showStar,
        constellation: this.showConstellation,
        constellationText: this.showConstellationText,
        wallpaper: this.$store.state.starmap.customize.wallpaper,
      });
      this.$store.dispatch("getStarMap");
    },
    removeWallpaper() {
      this.$store.commit("setCustomize", {
        size: this.$store.state.starmap.customize.size,
        background: this.bgValue,
        frame: this.$store.state.starmap.customize.frame,
        dot: this.showDot,
        star: this.showStar,
        constellation: this.showConstellation,
        constellationText: this.showConstellationText,
        wallpaper: "",
      });
      this.$store.dispatch("getStarMap");
    },
    getWallpapers() {
      this.axios
        .post("/api/assets/get", { wallpapers: true })
        .then((response) => {
          if (response.status === 200 && response.data.result) {
            this.wallpapers = response.data.files;
          }
        });
    },
  },
  mounted() {
    this.swiper.slideTo(3, 1000, false)

    const editMode = localStorage.getItem("editMode");
    if (editMode) {
      this.bgValue = this.$store.state.starmap.customize.background;
      this.showDot = this.$store.state.starmap.customize.dot;
      this.showStar = this.$store.state.starmap.customize.star;
      this.showConstellation = this.$store.state.starmap.customize.constellation;
      this.showConstellationText = this.$store.state.starmap.customize.constellationText;
    }
    this.getWallpapers();
  },
};
</script>
