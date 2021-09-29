<template>
  <div>
    <v-row align="baseline">
      <v-col cols="12" xl="6" lg="6" md="12" sm="12">
        <p class="p-title">اضافه کردن بارکد موسیقی</p>
      </v-col>
    </v-row>
    <v-radio-group v-model="wantMusic">
      <v-radio
        key="نمی‌خوام"
        label="نمی‌خوام"
        :value="false"
        @click="wantMusic = false"
        selected
      />
      <v-radio key="می‌خوام" label="می‌خوام" :value="true" />
    </v-radio-group>
    <div v-if="wantMusic">
      <v-form v-model="musicForm">
        <v-file-input
          v-if="getMobileOperatingSystem() === 'iOS'"
          :rules="rules"
          class="mb-0"
          v-model="mp3"
          :show-size="1000"
          accept="audio/*"
          label="فایل موزیک"
          outlined
          dense
          :clearable="true"
          @change="done = false"
          hide-details
        ></v-file-input>
        <v-file-input
          v-else
          :rules="rules"
          class="mb-0"
          v-model="mp3"
          :show-size="1000"
          accept="*.mp3"
          label="فایل موزیک"
          outlined
          dense
          :clearable="true"
          @change="done = false"
          hide-details
        ></v-file-input>
      </v-form>
      <span
        style="text-align: center; color: gray; display: block"
        class="mt-2 mb-4"
        >حداکثر سایز موسیقی ۱۵ مگابایت است.</span
      >
    </div>
    <v-row no-gutters>
      <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
        <v-btn
          @click="$emit('update:stepper', 5)"
          color="error"
          outlined
          class="w-98"
          >مرحله‌ی قبلی</v-btn
        >
      </v-col>
      <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
        <v-btn
          v-if="!wantMusic"
          :disabled="wantMusic"
          color="primary"
          @click="uploadMusic"
          class="w-98"
          >نهایی سازی سفارش</v-btn
        >
        <v-btn
          v-if="wantMusic"
          :disabled="mp3 === null || !musicForm || done"
          :color="done ? 'green' : 'primary'"
          class="white--text w-98"
          @click="uploadMusic"
        >
          <span v-if="done">ثبت شد</span>
          <span v-else>آپلود موسیقی</span>
        </v-btn>
      </v-col>
      <v-col cols="12" xl="12" lg="12" md="12" sm="12" class="my-3">
        <v-btn
          v-if="(done || !musicForm) && wantMusic"
          color="primary"
          @click="checkout"
          block
          >نهایی سازی سفارش</v-btn
        >
      </v-col>
    </v-row>
    <loading-overlay :is-loading="loading" />
  </div>
</template>

<script>
import LoadingOverlay from "@/components/Loading";

export default {
  name: "star-music",
  components: {
    LoadingOverlay,
  },
  data() {
    return {
      musicForm: false,
      rules: [
        (value) => !value || value.size < 15000000 || "این فایل مجاز نیست!",
      ],
      loading: false,
      wantMusic: false,
      mp3: null,
      done: false,
    };
  },
  methods: {
    uploadMusic() {
      this.loading = true;
      this.$store.commit("setLoading", true);
      if (this.wantMusic) {
        const formData = new FormData();
        formData.append("music", this.mp3);
        formData.append("password", "respina1234");
        this.axios
          .post(
            process.env.VUE_APP_MUSIC_API ||
              "https://respina.store/player/uploader.php",
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }
          )
          .then((response) => {
            if (response.data.result) {
              this.$store.commit("setMusic", { qr: response.data.details.qr });
              this.$store.dispatch("getStarMap");
              this.done = true;
            } else {
              alert("خطایی پیش آمده است...");
            }
            this.loading = false;
          })
          .catch((error) => {
            this.loading = false;
            console.log(error);
          });
      } else {
        this.loading = false;
        this.$store.commit("setLoading", false);
        this.checkout();
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
    /**
     * Determine the mobile operating system.
     * This function returns one of 'iOS', 'Android', 'Windows Phone', or 'unknown'.
     *
     * @returns {String}
     */
    getMobileOperatingSystem() {
      var userAgent = navigator.userAgent || navigator.vendor || window.opera;

      // Windows Phone must come first because its UA also contains "Android"
      if (/windows phone/i.test(userAgent)) {
        return "Windows Phone";
      }

      if (/android/i.test(userAgent)) {
        return "Android";
      }

      // iOS detection from: http://stackoverflow.com/a/9039885/177710
      if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
        return "iOS";
      }

      return "unknown";
    },
  },
};
</script>

