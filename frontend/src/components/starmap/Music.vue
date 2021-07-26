<template>
  <div>
    <v-row align="baseline">
      <v-col cols="6">
        <h2 class="mb-5">موزیک دلخواه خود را بیافزایید</h2>
      </v-col>
      <v-col cols="6">
        <h6 class="text-left">اگر مایل به افزودن QR کد نیستید وارد مرحله‌ی بعدی شوید</h6>
      </v-col>
    </v-row>
    <v-form ref="form" v-model="valid">
      <v-file-input
        v-model="mp3"
        :show-size="1000"
        accept="audio/*"
        label="فایل موزیک"
        outlined
        dense
      ></v-file-input>
      <v-file-input
        v-model="cover"
        :show-size="1000"
        accept="image/*"
        label="فایل کاور"
        outlined
        dense
      ></v-file-input>
      <v-text-field dense outlined v-model="singer" label="خواننده" />
      <v-text-field dense outlined v-model="name" label="نام موسیقی" />
      <v-row>
        <v-col>
          <v-btn
            block
            class="my-5 float-end"
            color="secondary"
            @click="uploadMusic"
          >
            آپلود موسیقی
          </v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6">
          <v-btn
            @click="$emit('update:stepper', 2)"
            color="error"
            block
            outlined
            >مرحله‌ی قبلی</v-btn
          >
        </v-col>
        <v-col cols="6">
          <v-btn color="primary" block @click="$emit('update:stepper', 4)"
            >مرحله‌ی بعدی</v-btn
          >
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script>
export default {
  name: "star-music",
  data() {
    return {
      valid: false,
      mp3: [],
      cover: [],
      singer: "",
      name: "",
    };
  },
  methods: {
    uploadMusic() {
      const formData = new FormData();
      formData.append("music", this.mp3);
      formData.append("cover", this.cover);
      formData.append("singer", this.singer);
      formData.append("name", this.name);
      formData.append("description", "");
      this.axios
        .post("https://respina.store/player/uploader.php", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          if (response.data.result) {
            this.$store.commit("setMusic", { qr: response.data.details.qr });
            console.log(response.data.details.qr);
          }
        });
    },
  },
};
</script>

<style></style>
