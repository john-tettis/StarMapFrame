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
          <template v-slot:[`item.deleteImage`]="{ item }">
            <v-btn color="red" text @click="openDeleteDialog(item)">
              <v-icon small>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
    <v-dialog v-model="deleteImageDialog" max-width="400">
      <v-card>
        <v-card-title>حذف تخفیف</v-card-title>
        <v-card-text>
          آیا از حذف این تخفیف مطمئن هستید؟
        </v-card-text>
        <v-card-actions>
          <v-btn color="red" class="white--text" @click="deleteImage"
            >حذف</v-btn
          >
          <v-btn color="dark" text @click="deleteImageDialog = false"
            >لغو</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: "AdminUploads",
  data() {
    return {
      deleteImageDialog: false,
      filetype: "",
      filename: "",
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
        .post(
          "/api/assets/get",
          {
            wallpapers: true,
          },
          {
            headers: {
              token: this.$cookies.get("token"),
            },
          }
        )
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
        .post(
          "/api/assets/get",
          {
            backgrounds: true,
          },
          {
            headers: {
              token: this.$cookies.get("token"),
            },
          }
        )
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
              token: this.$cookies.get("token"),
            },
          })
          .then((response) => {
            if (response.status === 200 && response.data.result) {
              alert("با موفقیت آپلود شد....");
              this.getWallpapers();
              this.getBackgrounds();
              setTimeout(() => {
                this.files = [...this.wallpapers, ...this.backgrounds];
              }, 500);
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
              token: this.$cookies.get("token"),
            },
          })
          .then((response) => {
            if (response.status === 200 && response.data.result) {
              alert("با موفقیت آپلود شد....");
              this.getWallpapers();
              this.getBackgrounds();
              setTimeout(() => {
                this.files = [...this.wallpapers, ...this.backgrounds];
              }, 500);
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
    openDeleteDialog(object) {
      this.filetype = object.type;
      this.filename = object.filename;
      this.deleteImageDialog = true;
    },
    async deleteImage() {
      let response = "";
      if (this.filetype === "بکگراند") {
        response = await this.axios.post(
          `/api/assets/backgrounds/delete/${this.filename}`,
          {},
          {
            headers: {
              token: this.$cookies.get("token"),
            },
          }
        );
      } else if (this.filetype === "والپیپر") {
        response = await this.axios.post(
          `/api/assets/wallpapers/delete/${this.filename}`,
          {},
          {
            headers: {
              token: this.$cookies.get("token"),
            },
          }
        );
      } else {
        alert("نوع عکس مشخص نشده است!");
        return;
      }
      this.$emit("update:loading", true);
      if (response.status === 200 && response.data.result) {
        alert("فایل با موفقیت حذف شد!");
      } else {
        alert("خطایی هنگام حذف فایل به وجود آمده است...");
      }
      this.deleteImageDialog = false;
      this.getWallpapers();
      this.getBackgrounds();
      setTimeout(() => {
        this.files = [...this.wallpapers, ...this.backgrounds];
      }, 500);
      this.$emit("update:loading", false);
    },
  },
};
</script>
