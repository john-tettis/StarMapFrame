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
      </v-row>

      <v-divider class="my-5"></v-divider>

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
        <v-btn color="primary" class="float-left" @click="uploadBg"
          >ثبت عکس</v-btn
        >
      </v-form>
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
        <v-btn color="primary" block>ثبت سفارش</v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "star-background",
  data() {
    return {
      valid: true,
      shape: false,
      haveBg: false,
      selectedImage: "",
      bg: [],
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
    uploadBg() {
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
            this.$store.commit("setBg", {
              bg: response.data.path,
              x: 0,
              y: -50,
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
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    disableBg() {
      if (!this.haveBg) {
        this.$store.commit("setBg", {
          bg: "",
          x: 0,
          y: 0,
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
      }
    },
    changeShape(){
      this.$store.commit('setShape', this.shape)
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
    }
  },
};
</script>

<style>
img.active-img {
  border: 5px solid blue;
}
</style>
