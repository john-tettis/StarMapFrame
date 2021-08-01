<template>
  <div>
    <v-row align="baseline" class="mb-5">
      <v-col cols="12" xl="6" lg="6" md="12" sm="12">
        <h2>موزیک دلخواه خود را بیافزایید</h2>
      </v-col>
      <v-col cols="12" xl="6" lg="6" md="12" sm="12">
        <h6 class="text-right">
          اگر مایل به افزودن QR کد نیستید وارد مرحله‌ی بعدی شوید
        </h6>
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
        accept="image/*"
        label="فایل کاور"
        outlined
        dense
        :clearable="false"
        append-outer-icon="mdi-close-box-outline"
        @click:append-outer="cover=[]"
      ></v-file-input>
    </v-form>
    <v-row>
      <v-col cols="12" xl="6" lg="6" md="12" sm="12">
        <v-btn @click="$emit('update:stepper', 2)" color="error" block outlined
          >مرحله‌ی قبلی</v-btn
        >
      </v-col>
      <v-col cols="12" xl="6" lg="6" md="12" sm="12">
        <v-btn
          :disabled="wantMusic && mp3.length === 0 || cover.length===0"
          color="primary"
          block
          @click="uploadMusic"
          >مرحله‌ی بعدی</v-btn
        >
      </v-col>
    </v-row>
    <Loading :isLoading="loading" />
  </div>
</template>

<script>
import Loading from "@/components/Loading";

export default {
  name: "star-music",
  components: {
    Loading,
  },
  data() {
    return {
      wantMusic: false,
      loading: false,
      valid: false,
      mp3: [],
      cover: [],
    };
  },
  methods: {
    uploadMusic() {
      this.loading = true;
      if (this.wantMusic) {
        const formData = new FormData();
        formData.append("music", this.mp3);
        formData.append("cover", this.cover);
        formData.append("password", "respina1234");
        this.axios
          .post("https://respina.store/player/uploader.php", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((response) => {
            if (response.data.result) {
              this.$store.commit("setMusic", { qr: response.data.details.qr });
              setTimeout(() => {
                this.axios
                  .post("/api/starmap", this.$store.state.starmap)
                  .then((response) => {
                    if (response.data.result) {
                      this.$store.commit(
                        "setImage",
                        response.data.path + `?${Date.now()}`
                      );
                      this.$emit("update:stepper", 4); // Moves to next step
                    }
                    this.loading = false;
                  })
                  .catch((error) => {
                    this.loading = false;
                    console.log(error);
                  });
              }, 500);
            } else {
              alert("something wrong happend");
            }
          });
      } else {
        this.$emit("update:stepper", 4); // Moves to next step
      }
    },
  },
};
</script>

<style></style>
