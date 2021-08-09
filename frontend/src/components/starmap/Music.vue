<template>
  <div>
    <v-row align="baseline" class="mb-5">
      <v-col cols="12" xl="6" lg="6" md="12" sm="12">
        <p style="font-size:1.3rem">موزیک دلخواه خود را بیافزایید</p>
      </v-col>
      <v-col cols="12" xl="6" lg="6" md="12" sm="12">
        <p class="text-center" style="font-size:.6rem">
          اگر مایل به افزودن QR کد نیستید وارد مرحله‌ی بعدی شوید
        </p>
      </v-col>
    </v-row>
    <v-switch
      v-model="wantMusic"
      inset
      :label="wantMusic ? `آره میخوام` : `نه نمیخوام`"
    ></v-switch>
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
      <v-col cols="6" xl="6" lg="6" md="6" sm="6">
        <v-btn @click="$emit('update:stepper', 2)" color="error" outlined block
          >مرحله‌ی قبلی</v-btn
        >
      </v-col>
      <v-col cols="6" xl="6" lg="6" md="6" sm="6">
        <v-btn
          v-if="!wantMusic"
          :disabled="wantMusic"
          color="primary"
          @click="uploadMusic"
          block
          >مرحله‌ی بعدی</v-btn
        >
        <v-btn
          v-if="wantMusic"
          :disabled="mp3.length===0 || cover.length===0"
          color="primary"
          @click="uploadMusic"
          block
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
              this.$emit("update:stepper", 4); // Moves to next step
            } else {
              alert("خطایی پیش آمده است...");
            }
          });
      } else {
        this.$store.commit("setLoading", false)
        this.$emit("update:stepper", 4); // Moves to next step
      }
    },
  },
};
</script>

<style></style>
