<template>
  <div>
    <p class="p-title">انتخاب بکگراند ستاره‌ها</p>
    <v-row>
      <v-col cols="12" xl="6" lg="6" md="12" sm="12">
        <v-radio-group v-model="haveBg">
          <v-radio
            key="نمی‌خوام"
            label="نمی‌خوام"
            :value="false"
            @click="disableBg()"
            selected
          />
          <v-radio key="می‌خوام" label="می‌خوام" :value="true" />
        </v-radio-group>
      </v-col>
    </v-row>
    <div v-if="haveBg">
      <v-row class="mb-5">
         <v-col cols="6" lg="6" md="6" sm="6">
          <v-btn
            class="w-98"
            color="primary"
            @click="
              customImg = false;
              sampleImg = true;
            "
            :disabled="sampleImg"
            >عکس آماده</v-btn>
        </v-col>
        <v-col cols="6" lg="6" md="6" sm="6">
          <v-btn
            @click="
              customImg = true;
              sampleImg = false;
            "
            class="w-98"
            color="primary"
            :disabled="customImg"
            >عکس دلخواه</v-btn>
        </v-col>
      </v-row>
      <div v-if="sampleImg">
        <v-row>
          <v-col cols="12" xl="12" lg="12" md="12" sm="12">
            <swiper ref="backgrounds" :options="backgroundsOptions">
              <swiper-slide v-for="background in backgrounds" :key="background">
                <img
                  class="w-max-100"
                  @click="selectImage($event)"
                  :src="
                    'https://sky.respina.store/api/assets/get/backgrounds/' +
                    background
                  "
                  alt="image"
                  width="100%"
                  height="300"
                />
              </swiper-slide>
              <div class="swiper-pagination" slot="pagination"></div>
            </swiper>
            <p class="text-center text--disabled">برای دیدن باقی عکس‌ها به چپ و یا راست بکشید</p>
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
            label="برای آپلود عکس خودتان اینجا را کلیک کنید"
            @change="isUploadBg = false"
            outlined
            dense
            hide-details
            class="mb-3"
          ></v-file-input>
          <p class="text--disabled text-center">عکس انتخابی باید مربع باشد!</p>

          <v-row no-gutters>
            <v-col col="12" xl="12" lg="12" md="12" sm="12">
              <v-btn
                :color="isUploadBg ? 'green' : 'secondary'"
                @click="uploadBg"
                :disabled="isUploadBg"
                 class="w-98"
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
      <p class="p-title">دور ستاره‌ها دایره‌ای باشد؟</p>
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
           class="w-98"
          outlined
          >مرحله‌ی قبلی</v-btn
        >
      </v-col>
      <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
        <v-btn
          @click="$emit('update:stepper', 5)"
          color="primary"
           class="w-98"
          >مرحله‌ی بعدی</v-btn
        >
      </v-col>
    </v-row>
    <loading-overlay :is-loading="loading" />
  </div>
</template>

<script>
import LoadingOverlay from "@/components/Loading";
import { Swiper, SwiperSlide, directive } from "vue-awesome-swiper";
import "swiper/css/swiper.css";

export default {
  name: "star-background",
  props: {
    stepper: {
      type: Number,
    },
  },
  components: {
    LoadingOverlay,
    Swiper,
    SwiperSlide,
  },
  directives: {
    swiper: directive,
  },
  computed: {
    swiper() {
      return this.$refs.backgrounds.$swiper;
    },
  },
  data() {
    return {
      backgroundsOptions: {
        pagination: {
          el: ".swiper-pagination",
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
            spaceBetween: 10,
          },
          // when window width is >= 480px
          480: {
            slidesPerView: 1,
            spaceBetween: 10,
          },
          // when window width is >= 640px
          640: {
            slidesPerView: 2,
            spaceBetween: 10,
          },
        },
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
      if (activeImages.length > 0)
        activeImages.forEach((el) => el.classList.remove("active-img"));

      this.selectedImage = event.target.getAttribute("src");
      event.target.setAttribute("class", "active-img");

      this.$store.commit("setBg", {
        bg: this.selectedImage,
        x: 0,
        y: -180,
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
              y: -180,
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
        y: -180,
        opacity: this.opacity,
      });
      this.$store.dispatch("getStarMap");
    },
    updateUploadedBgOpacity() {
      this.$store.commit("setBg", {
        bg: this.uploadedBg,
        x: 0,
        y: -180,
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
    },
  },
  mounted() {
    this.getBackgrounds();
    if (this.stepper === 4) {
      this.swiper.slideTo(3, 1000, false);
    }
    const editMode = localStorage.getItem("editMode");
    if (editMode) {
      this.circle = this.$store.state.starmap.background.circle;
    }
  },
};
</script>

<style>
img.active-img {
  border: 5px solid blue;
}
</style>
