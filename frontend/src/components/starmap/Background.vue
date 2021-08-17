<template>
  <div>
    <p style="font-size:1.3rem">انتخاب بکگراند ستاره‌ها</p>
    <v-row>
      <v-col cols="12" xl="6" lg="6" md="12" sm="12">
        <v-radio-group v-model="haveBg">
          <v-radio key="نمی‌خوام" label="نمی‌خوام" :value="false" @click="disableBg()" selected />
          <v-radio key="می‌خوام" label="می‌خوام" :value="true" />
        </v-radio-group>
      </v-col>
      <!-- <v-col cols="12" xl="6" lg="6" md="12" sm="12">
        <v-switch
          v-model="shape"
          @change="changeShape"
          inset
          :label="shape ? `قلبی` : `دایره‌ای`"
        ></v-switch>
      </v-col>-->
    </v-row>
    <div v-if="haveBg">
      <div v-if="sampleImg">
        <v-row>
          <v-col cols="12" xl="12" lg="12" md="12" sm="12">
            <swiper ref="backgrounds" :options="backgroundsOptions">
              <swiper-slide v-for="background in backgrounds" :key="background">
                <img
                  style="max-width:100%"
                  @click="selectImage($event)"
                  :src="
                    'https://sky.respina.store/api/assets/get/backgrounds/' + background
                  "
                  alt="image"
                  width="100%"
                  height="300"
                />
              </swiper-slide>
              <div class="swiper-pagination" slot="pagination"></div>
            </swiper>
          </v-col>
          <v-col cols="12" xl="12" lg="12" md="12" sm="12">
            <div
              @click="
              sampleImg = false;
              customImg = true;
              "
              style="max-width:100%;height:115px;cursor:pointer;background:#212121"
              class="d-flex justify-center align-center"
            >
              <span class="white--text">افزودن عکس دلخواه</span>
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <p>شفافیت</p>
            <v-slider
              hint="شفافیت تصویر"
              max="100"
              min="0"
              thumb-label="always"
              v-model="opacity"
              @change="updateOpacity"
            ></v-slider>
          </v-col>
        </v-row>
      </div>

      <div v-if="customImg">
        <v-form class="mb-15">
          <v-file-input
            v-model="bg"
            accept="image/*"
            label="آپلود عکس"
            @change="isUploadBg = false"
            outlined
            dense
          ></v-file-input>

          <v-row no-gutters>
            <v-col cols="6" xl="6" lg="6" md="6" sm="6">
              <v-btn
                style="width:98%"
                color="secondary"
                @click="
                customImg = false;
                sampleImg = true;
                "
              >عکس آماده</v-btn>
            </v-col>
            <v-col col="6" xl="6" lg="6" md="6" sm="6">
              <v-btn
                :color="isUploadBg ? 'green' : 'primary'"
                @click="uploadBg"
                :disabled="isUploadBg"
                style="width:98%"
              >
                <span v-if="isUploadBg">ثبت شد</span>
                <span v-else>ثبت عکس</span>
              </v-btn>
            </v-col>
            <v-col cols="12" class="mt-5">
              <p>شفافیت</p>
              <v-slider
                hint="شفافیت تصویر"
                max="100"
                min="0"
                thumb-label="always"
                v-model="uploadedBgOpacity"
                @change="updateUploadedBgOpacity"
              ></v-slider>
            </v-col>
          </v-row>
        </v-form>
      </div>
    </div>
    <v-divider class="my-5"></v-divider>

    <v-col cols="12" xl="6" lg="6" md="12" sm="12">
      <p style="font-size:1.3rem">دور ستاره‌ها دایره‌ای باشد؟</p>
      <v-radio-group @change="changeCircle" v-model="circle">
        <v-radio key="بله" label="بله" :value="true" />
        <v-radio key="خیر" label="خیر" :value="false" @click="circle = false" />
      </v-radio-group>
    </v-col>

    <v-row no-gutters justify="center">
      <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
        <v-btn
          @click="$emit('update:stepper', 3)"
          color="error"
          style="width:98%"
          outlined
        >مرحله‌ی قبلی</v-btn>
      </v-col>
      <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
        <v-btn @click="$emit('update:stepper', 5)" color="primary" style="width:98%">مرحله‌ی بعدی</v-btn>
      </v-col>
    </v-row>
    <Loading :isLoading="loading" />
  </div>
</template>

<script>
import Loading from '@/components/Loading';
import { Swiper, SwiperSlide, directive } from 'vue-awesome-swiper'
import 'swiper/css/swiper.css';

export default {
  name: "star-background",
  components: {
    Loading,
    Swiper,
    SwiperSlide
  },
  directives: {
    swiper: directive
  },
  computed: {
    swiper() {
      return this.$refs.backgrounds.$swiper
    }
  },
  data() {
    return {
      backgroundsOptions: {
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
      loading: false,
      circle: true,
      valid: true,
      shape: false,
      haveBg: false,
      selectedImage: "",
      opacity: 40,
      bg: [],
      uploadedBg: "",
      isUploadBg: false,
      uploadedBgOpacity: 40,
      sampleImg: true,
      customImg: false,
      backgrounds: [],
    };
  },
  methods: {
    selectImage(event) {
      const activeImages = document.querySelectorAll(".active-img");
      if (activeImages.length > 0) activeImages.forEach((el) => el.classList.remove("active-img"));

      this.selectedImage = event.target.getAttribute("src");
      event.target.setAttribute("class", "active-img");

      this.$store.commit("setBg", {
        bg: this.selectedImage,
        x: 0,
        y: 0,
        opacity: this.opacity,
      });
      this.$store.dispatch("getStarMap");
    },
    uploadBg() {
      this.loading = true;
      const formData = new FormData();
      formData.append("bg", this.bg);

      this.axios
        .post("/api/uploadBackground", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          if (response.data.result) {
            this.uploadedBg = response.data.path;
            this.$store.commit("setBg", {
              bg: response.data.path,
              x: 0,
              y: 0,
              opacity: this.opacity,
            });
            this.$store.dispatch("getStarMap");
            this.isUploadBg = true;
            this.loading = false;
          }
        })
        .catch((error) => {
          console.log(error);
          this.loading = false;
        });
    },
    disableBg() {
      this.$store.commit("setBg", {
        bg: "",
        x: 0,
        y: 0,
        opacity: this.opacity,
      });
      this.$store.dispatch("getStarMap");
    },
    changeShape() {
      this.$store.commit("setShape", this.shape);
      this.$store.dispatch("getStarMap");
    },
    updateOpacity() {
      this.$store.commit("setBg", {
        bg: this.selectedImage,
        x: 0,
        y: 0,
        opacity: this.opacity,
      });
      this.$store.dispatch("getStarMap");
    },
    updateUploadedBgOpacity() {
      this.$store.commit("setBg", {
        bg: this.uploadedBg,
        x: 0,
        y: 0,
        opacity: this.uploadedBgOpacity,
      });
      this.$store.dispatch("getStarMap");
    },
    getBackgrounds() {
      this.axios
        .post("/api/assets/get", { backgrounds: true })
        .then((response) => {
          if (response.status === 200 && response.data.result) {
            this.backgrounds = response.data.files;
          }
        });
    },
    changeCircle() {
      this.$store.commit("setCircle", this.circle);
      this.$store.dispatch("getStarMap");
    }
  },
  mounted() {
    this.getBackgrounds();
    this.swiper.slideTo(3, 1000, false)

    const editMode = localStorage.getItem("editMode");
    if (editMode) {
      this.circle = this.$store.state.starmap.background.circle
    }
  },
};
</script>

<style>
img.active-img {
  border: 5px solid blue;
}
</style>
