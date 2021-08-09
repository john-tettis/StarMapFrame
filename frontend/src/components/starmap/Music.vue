<template>
  <div>
    <v-row align="baseline">
      <v-col cols="12" xl="6" lg="6" md="12" sm="12">
        <p style="font-size:1.3rem">اضافه کردن بارکد موسیقی</p>
      </v-col>
    </v-row>
    <v-radio-group v-model="wantMusic">
      <v-radio key="نمی‌خوام" label="نمی‌خوام" :value="false" @click="wantMusic=false" selected/>
      <v-radio key="می‌خوام" label="می‌خوام" :value="true" />
    </v-radio-group>
    <v-form v-if="wantMusic" ref="form" v-model="valid">
      <v-file-input
        ref="mp3"
        v-model="mp3"
        :show-size="1000"
        accept="audio/*"
        label="فایل موزیک"
        outlined
        dense
        :clearable="false"
        append-outer-icon="mdi-close-box-outline"
        @click:append-outer="mp3=[]"
      ></v-file-input>
      <v-file-input
        ref="cover"
        v-model="cover"
        :show-size="1000"
        accept="image/jpeg"
        label="فایل کاور"
        outlined
        dense
        :clearable="false"
        append-outer-icon="mdi-close-box-outline"
        @click:append-outer="cover=[]"
      ></v-file-input>
    </v-form>
    <v-row no-gutters>
      <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
        <v-btn @click="$emit('update:stepper', 2)" color="error" outlined style="width:120px"
          >مرحله‌ی قبلی</v-btn
        >
      </v-col>
      <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
        <v-btn
          v-if="!wantMusic"
          :disabled="wantMusic"
          color="primary"
          @click="uploadMusic"
          style="width:120px"
          >مرحله‌ی بعدی</v-btn
        >
        <v-btn
          v-if="wantMusic"
          :disabled="mp3.length===0 || cover.length===0"
          color="primary"
          @click="uploadMusic"
          style="width:120px"
          >آپلود موسیقی</v-btn
        >
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "star-music",
  data() {
    return {
      wantMusic: false,
      valid: false,
      mp3: [],
      cover: [],
    };
  },
  methods: {
    uploadMusic() {
      this.$store.commit("setLoading", true)
      if (this.wantMusic) {
        const formData = new FormData();
        formData.append("music", this.mp3);
        formData.append("cover", this.cover);
        formData.append("password", "respina1234");
        this.axios
          .post(process.env.VUE_APP_MUSIC_API || "https://respina.store/player/uploader.php", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((response) => {
            if (response.data.result) {
              this.$store.commit("setMusic", { qr: response.data.details.qr });
              this.$store.dispath("getStarMap");
              this.checkout()
            } else {
              alert("خطایی پیش آمده است...");
            }
          });
      } else {
        this.$store.commit("setLoading", false)
        this.checkout()
      }
    },
    checkout() {
      localStorage.setItem(
        "product",
        JSON.stringify(this.$store.state.starmap)
      );
      const editMode = localStorage.getItem("editMode");
      if (editMode) {
        const orderID = localStorage.getItem("orderID");
        this.axios
          .post(`/api/orders/edit/${orderID}`, {
            product: this.$store.state.starmap,
          })
          .then((response) => {
            if (response.data.result) {
              alert("محصول با موفقیت بروزرسانی شد!");
              localStorage.removeItem("editMode");
              localStorage.removeItem("orderID");
              this.$router.push("/admin");
            } else {
              alert("خطایی پیش آمده است...");
            }
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        this.$router.push("/pay");
      }
    },
    
  },
};
</script>

<style></style>
