<template>
  <div>
    <h2>آیا بکگراند میخواید</h2>
    <v-row>
      <v-col cols="6">
        <v-switch
          v-model="haveBg"
          @change="disableBg"
          inset
          :label="haveBg ? `آره میخوام` : `نه نمیخوام`"
        ></v-switch>
      </v-col>
      <v-col cols="6">
        <v-switch
          v-model="shape"
          @change="changeShape"
          inset
          :label="shape ? `قلبی` : `دایره‌ای`"
        ></v-switch>
      </v-col>
    </v-row>
    <div v-if="haveBg">
      <div v-if="sampleImg">
        <v-row>
          <v-col cols="4">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/id/11/500/300"
              alt="image"
            />
          </v-col>
          <v-col cols="4">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/id/11/500/300"
              alt="image"
            />
          </v-col>
          <v-col cols="4">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/510/300?random"
              alt="image"
            />
          </v-col>
          <v-col cols="4">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/id/11/500/300"
              alt="image"
            />
          </v-col>
          <v-col cols="4">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/id/11/500/300"
              alt="image"
            />
          </v-col>
          <v-col cols="4">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/510/300?random"
              alt="image"
            />
          </v-col>
          <v-col cols="4">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/id/11/500/300"
              alt="image"
            />
          </v-col>
          <v-col cols="4">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/510/300?random"
              alt="image"
            />
          </v-col>
          <v-col cols="4">
            <div
              @click="
                sampleImg = false;
                customImg = true;
              "
              style="max-width:100%;height:115px;cursor:pointer"
              class="d-flex justify-center align-center bg-dark"
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
        <h2>از این عکسا خوشت نمیاد؟</h2>
        <h3>یکی از عکسای خودتو آپلود کن</h3>
        <v-form class="mb-15">
          <v-file-input
            v-model="bg"
            accept="image/*"
            label="آپلود عکس"
            outlined
            dense
          ></v-file-input>

          <v-row>
            <v-col cols="12">
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

          <v-btn color="primary" class="float-left" @click="uploadBg"
            >ثبت عکس</v-btn
          >
          <v-btn
            color="secondary"
            class="float-left ml-2"
            @click="
              customImg = false;
              sampleImg = true;
            "
            >استفاده از عکس های آماده</v-btn
          >
        </v-form>
      </div>
    </div>
    <v-divider class="my-5"></v-divider>
    <h3>تمامی شخصی سازی ها انجام شد</h3>
    <p>حالا می‌تونی قاب ستاره‌ای خودتو سفارش بدی</p>
    <v-row>
      <v-col cols="6">
        <v-btn @click="$emit('update:stepper', 4)" color="error" block outlined
          >مرحله‌ی قبلی</v-btn
        >
      </v-col>
      <v-col cols="6">
        <v-btn @click="checkout" color="primary" block>ثبت سفارش</v-btn>
      </v-col>
    </v-row>

    <Loading :isLoading="loading" />
  </div>
</template>

<script>
import Loading from "@/components/Loading.vue";

export default {
  name: "star-background",
  components: {
    Loading,
  },
  data() {
    return {
      loading: false,
      valid: true,
      shape: false,
      haveBg: false,
      selectedImage: "",
      opacity: 40,
      bg: [],
      uploadedBg: "",
      uploadedBgOpacity: 40,
      sampleImg: true,
      customImg: false,
    };
  },
  methods: {
    selectImage(event) {
      const activeImages = document.getElementsByClassName("active-img");
      activeImages.forEach((el) => el.classList.remove("active-img"));

      this.selectedImage = event.target.getAttribute("src");
      event.target.setAttribute("class", "active-img");

      this.$store.commit("setBg", {
        bg: this.selectedImage,
        x: 10,
        y: -50,
        opacity: this.opacity,
      });
      this.loading = true;
      setTimeout(() => {
        this.axios
          .post("/api/starmap", this.$store.state.starmap)
          .then((response) => {
            if (response.data.result) {
              this.$store.commit(
                "setImage",
                response.data.path + `?${Date.now()}`
              );
            }
            this.loading = false;
          })
          .catch((error) => {
            this.loading = false;
            console.log(error);
          });
      }, 500);
    },
    uploadBg() {
      const formData = new FormData();
      formData.append("bg", this.bg);
      this.loading = true;

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
              y: -50,
              opacity: this.opacity,
            });
            setTimeout(() => {
              this.axios
                .post("/api/starmap", this.$store.state.starmap)
                .then((response) => {
                  if (response.data.result) {
                    this.$store.commit(
                      "setImage",
                      response.data.path + `?${Date.now()}`
                    );
                  }
                  this.loading = false;
                })
                .catch((error) => {
                  this.loading = false;
                  console.log(error);
                });
            }, 500);
          }
        })
        .catch((error) => {
          console.log(error);
          this.loading = false;
        });
    },
    disableBg() {
      if (!this.haveBg) {
        this.$store.commit("setBg", {
          bg: "",
          x: 0,
          y: 0,
          opacity: this.opacity,
        });
        this.loading = true;
        setTimeout(() => {
          this.axios
            .post("/api/starmap", this.$store.state.starmap)
            .then((response) => {
              if (response.data.result) {
                this.$store.commit(
                  "setImage",
                  response.data.path + `?${Date.now()}`
                );
              }
              this.loading = false;
            })
            .catch((error) => {
              console.log(error);
              this.loading = false;
            });
        }, 500);
      }
    },
    changeShape() {
      this.loading = true;
      this.$store.commit("setShape", this.shape);
      setTimeout(() => {
        this.axios
          .post("/api/starmap", this.$store.state.starmap)
          .then((response) => {
            if (response.data.result) {
              this.$store.commit(
                "setImage",
                response.data.path + `?${Date.now()}`
              );
              this.loading = false;
            }
          })
          .catch((error) => {
            console.log(error);
            this.loading = false;
          });
      }, 500);
    },
    updateOpacity() {
      this.$store.commit("setBg", {
        bg: this.selectedImage,
        x: 10,
        y: -50,
        opacity: this.opacity,
      });
      setTimeout(() => {
        this.axios
          .post("/api/starmap", this.$store.state.starmap)
          .then((response) => {
            if (response.data.result) {
              this.$store.commit(
                "setImage",
                response.data.path + `?${Date.now()}`
              );
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }, 500);
    },
    updateUploadedBgOpacity() {
      this.$store.commit("setBg", {
        bg: this.uploadedBg,
        x: 10,
        y: -50,
        opacity: this.uploadedBgOpacity,
      });
      setTimeout(() => {
        this.axios
          .post("/api/starmap", this.$store.state.starmap)
          .then((response) => {
            if (response.data.result) {
              this.$store.commit(
                "setImage",
                response.data.path + `?${Date.now()}`
              );
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }, 500);
    },
    checkout(){
      alert("DONE!")
      console.log(this.$store.state.starmap)
    }
  },
};
</script>

<style>
img.active-img {
  border: 5px solid blue;
}
</style>
