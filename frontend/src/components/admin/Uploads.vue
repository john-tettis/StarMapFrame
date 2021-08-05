<template>
  <div>
    <v-row justify="center">
      <v-col cols="12" xl="6" lg="6" md="6" sm="12">
        <v-card>
          <v-card-title>آپلود والپیپر</v-card-title>
          <v-card-text>
            از این بخش می‌تونی والپیپر پشت ستاره‌ی آسمان رو آپلود کنی
            <v-file-input
              v-model="wallpaper"
              label="فایل عکس"
              dense
              outlined
              class="mt-5"
            />
            <v-btn
              color="primary"
              block
              outlined
              @click="wallpaperUpload"
              :disabled="wallpaper.length === 0"
              >آپلود</v-btn
            >
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" xl="6" lg="6" md="6" sm="12">
        <v-card>
          <v-card-title>آپلود بکگراند</v-card-title>
          <v-card-text>
            از این بخش می‌تونی بکگراند پشت ستاره‌ی آسمان رو آپلود کنی
            <v-file-input
              v-model="background"
              label="فایل عکس"
              dense
              outlined
              class="mt-5"
            />
            <v-btn
              color="primary"
              block
              outlined
              @click="backgroundUpload"
              :disabled="background.length === 0"
              >آپلود</v-btn
            >
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <h2 class="my-5">لیست تمامی عکس‌های آپلود شده</h2>
        <v-data-table :headers="fileHeaders" :items="files" class="elevation-1">
          <template v-slot:[`item.preview`]="{ item }">
            <img
              class="d-block mx-auto"
              :src="item.preview"
              :alt="item.filename"
              width="128"
              height="128"
            />
          </template>
          <template v-slot:[`item.deleteImage`]>
            <v-btn color="red" text>
              <v-icon small>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "AdminUploads",
  data() {
    return {
      fileHeaders: [
        { text: "نوع", value: "type" },
        { text: "نام", value: "filename" },
        { text: "پیش نمایش", value: "preview" },
        { text: "", value: "deleteImage", sortable: false },
      ],
      wallpapers: [],
      backgrounds: [],
      files: [],
      wallpaper: [],
      background: [],
    };
  },
  mounted() {
    this.getWallpapers();
    this.getBackgrounds();
    setTimeout(() => {
      this.files = [...this.wallpapers, ...this.backgrounds];
    }, 1500);
  },
  methods: {
    getWallpapers() {
      this.axios
        .post("/api/assets/get", {
          wallpapers: true,
        }, {headers: {
            token: this.$cookies.get("token"),
          },})
        .then((response) => {
          if (response.status === 200 && response.data.result) {
            let wallpapers = response.data.files;
            let images = [];
            wallpapers.forEach((filename) => {
              images.push({
                type: "والپیپر",
                filename: filename,
                preview: `${process.env.VUE_APP_BACKEND}/assets/get/wallpapers/${filename}`,
              });
            });
            this.wallpapers = images;
          }
        });
    },
    getBackgrounds() {
      this.axios
        .post("/api/assets/get", {
          backgrounds: true,
        }, {headers: {
            token: this.$cookies.get("token"),
          },})
        .then((response) => {
          if (response.status === 200 && response.data.result) {
            let backgrounds = response.data.files;
            let images = [];
            backgrounds.forEach((filename) => {
              images.push({
                type: "بکگراند",
                filename: filename,
                preview: `${process.env.VUE_APP_BACKEND}/assets/get/backgrounds/${filename}`,
              });
            });
            this.backgrounds = images;
          }
        });
    },
    wallpaperUpload() {
      this.$emit("update:loading", true);
      if (typeof this.wallpaper === "object") {
        const formData = new FormData();
        formData.append("wallpaper", this.wallpaper);
        this.axios
          .post("/api/assets/upload", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
              "token": this.$cookies.get('token')
            },
          })
          .then((response) => {
            if (response.status === 200 && response.data.result) {
              alert("با موفقیت آپلود شد....");
            }
            this.$emit("update:loading", false);
          })
          .catch((error) => {
            console.log(error);
            alert("خطایی پیش آمده است....");
            this.$emit("update:loading", false);
          });
      }
    },
    backgroundUpload() {
      this.$emit("update:loading", true);

      if (typeof this.wallpaper === "object") {
        const formData = new FormData();
        formData.append("background", this.background);
        this.axios
          .post("/api/assets/upload", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
              "token": this.$cookies.get('token')
            },
          })
          .then((response) => {
            if (response.status === 200 && response.data.result) {
              alert("با موفقیت آپلود شد....");
            }
            this.$emit("update:loading", true);
          })
          .catch((error) => {
            console.log(error);
            alert("خطایی پیش آمده است....");
            this.$emit("update:loading", true);
          });
      }
    },
  },
};
</script>
