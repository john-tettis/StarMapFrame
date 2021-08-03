<template>
  <div>
    <h2>آیا بکگراند میخواید</h2>
    <v-row>
      <v-col cols="12" xl="6" lg="6" md="12" sm="12">
        <v-switch
          v-model="haveBg"
          @change="disableBg"
          inset
          :label="haveBg ? `آره میخوام` : `نه نمیخوام`"
        ></v-switch>
      </v-col>
      <v-col cols="12" xl="6" lg="6" md="12" sm="12">
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
          <v-col cols="12" xl="4" lg="4" md="6" sm="12">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/id/11/500/300"
              alt="image"
            />
          </v-col>
          <v-col cols="12" xl="4" lg="4" md="6" sm="12">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/id/11/500/300"
              alt="image"
            />
          </v-col>
          <v-col cols="12" xl="4" lg="4" md="6" sm="12">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/510/300?random"
              alt="image"
            />
          </v-col>
          <v-col cols="12" xl="4" lg="4" md="6" sm="12">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/id/11/500/300"
              alt="image"
            />
          </v-col>
          <v-col cols="12" xl="4" lg="4" md="6" sm="12">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/id/11/500/300"
              alt="image"
            />
          </v-col>
          <v-col cols="12" xl="4" lg="4" md="6" sm="12">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/510/300?random"
              alt="image"
            />
          </v-col>
          <v-col cols="12" xl="4" lg="4" md="6" sm="12">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/id/11/500/300"
              alt="image"
            />
          </v-col>
          <v-col cols="12" xl="4" lg="4" md="6" sm="12">
            <img
              style="max-width:100%"
              @click="selectImage($event)"
              src="https://picsum.photos/510/300?random"
              alt="image"
            />
          </v-col>
          <v-col cols="12" xl="4" lg="4" md="6" sm="12">
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

            <v-col col="12" xl="6" lg="6" md="6" sm="12">
              <v-btn color="primary" @click="uploadBg"
                block>ثبت عکس</v-btn
              >
            </v-col>
            <v-col cols="12" xl="6" lg="6" md="6" sm="12">
              <v-btn
              block
                color="secondary"
                @click="
                  customImg = false;
                  sampleImg = true;
                "
                >استفاده از عکس های آماده</v-btn
              >
            </v-col>
          </v-row>
        </v-form>
      </div>
    </div>
    <v-divider class="my-5"></v-divider>
    <h3>تمامی شخصی سازی ها انجام شد</h3>
    <p>حالا می‌تونی قاب ستاره‌ای خودتو سفارش بدی</p>
    <v-row>
      <v-col cols="12" xl="6" lg="6" md="6" sm="12">
        <v-btn @click="$emit('update:stepper', 4)" color="error" block outlined
          >مرحله‌ی قبلی</v-btn
        >
      </v-col>
      <v-col cols="12" xl="6" lg="6" md="6" sm="12">
        <v-btn @click="checkout" color="primary" block>ثبت سفارش</v-btn>
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
      this.$store.dispatch("getStarMap")
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
            this.uploadedBg = response.data.path;
            this.$store.commit("setBg", {
              bg: response.data.path,
              x: 0,
              y: -50,
              opacity: this.opacity,
            });
            this.$store.dispatch("getStarMap");
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
          opacity: this.opacity,
        });
        this.$store.dispatch("getStarMap");
      }
    },
    changeShape() {
      this.$store.commit("setShape", this.shape);
      this.$store.dispatch("getStarMap");
    },
    updateOpacity() {
      this.$store.commit("setBg", {
        bg: this.selectedImage,
        x: 10,
        y: -50,
        opacity: this.opacity,
      });
      this.$store.dispatch("getStarMap");
    },
    updateUploadedBgOpacity() {
      this.$store.commit("setBg", {
        bg: this.uploadedBg,
        x: 10,
        y: -50,
        opacity: this.uploadedBgOpacity,
      });
      this.$store.dispatch("getStarMap");
    },
    checkout() {
      localStorage.setItem(
        "product",
        JSON.stringify(this.$store.state.starmap)
      );
      const editMode = localStorage.getItem("editMode");
      if(editMode){
        const orderID = localStorage.getItem("orderID");
        this.axios.post(`/api/orders/edit/${orderID}`, {product: this.$store.state.starmap}).then(response=>{
          if(response.data.result){
            alert("محصول با موفقیت بروزرسانی شد!");
            localStorage.removeItem("editMode");
            localStorage.removeItem("orderID");
            this.$router.push("/admin")
          }else{
            alert("خطایی پیش آمده است...")
          }
        }).catch(error=>{
          console.log(error)
        })
      }else{
        this.$router.push("/pay");
      }
    },
  },
};
</script>

<style>
img.active-img {
  border: 5px solid blue;
}
</style>
