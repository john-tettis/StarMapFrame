<template>
  <div>
    <h2>شخصی سازی کنید:</h2>
    <v-form ref="form" v-model="valid">
      <p>اندازه‌ی قاب:</p>
      <v-radio-group row @change="updateStar" v-model="radioGroup">
        <v-radio key="A1" label="A1" value="A1" />
        <v-radio key="A2" label="A2" value="A2" />
        <v-radio key="A3" label="A3" value="A3" />
        <v-radio key="A4" label="A4" value="A4" />
      </v-radio-group>

      <v-divider class="my-5"></v-divider>

      <div v-show="showWallpaper === false">
        <v-row align="baseline">
          <v-col cols="6">
            <p>رنگ بکگراند</p>
          </v-col>
          <v-col>
            <p
              @click="showWallpaper = true"
              class="text-left"
              style="font-size:10px;cursor:pointer"
            >
              یا میتونی عکس بندازی
            </p>
          </v-col>
        </v-row>
        <v-menu
          v-model="bgMenu"
          :close-on-content-click="false"
          :nudge-right="40"
          transition="scale-transition"
          offset-y
          min-width="290px"
          max-width="290px"
        >
          <template v-slot:activator="{ on }">
            <v-text-field
              label="رنگ"
              prepend-inner-icon="mdi-palette"
              readonly
              hide-details
              :value="bgValue"
              v-on="on"
              outlined
              dense
              class="mb-7"
            ></v-text-field>
          </template>

          <v-color-picker
            show-swatches
            hide-canvas
            hide-sliders
            hide-inputs
            :swatches="swatches"
            v-model="bgValue"
            @input="updateStar"
            no-title
          ></v-color-picker>
        </v-menu>
      </div>

      <div v-show="showWallpaper === true">
        <v-row align="baseline">
          <v-col cols="6">
            <p>عکس بکگراند</p>
          </v-col>
          <v-col cols="6">
            <p
              @click="showWallpaper = false;$store.commit('setWallpaper', '');"
              class="text-left"
              style="font-size:10px;cursor:pointer"
            >
              یا میتونی رنگ بندازی
            </p>
          </v-col>
        </v-row>
        <v-container>
          <v-row>
            <v-col cols="6" xl="4" lg="4" md="6" sm="6">
              <img
                class="wallpaper"
                src="@/assets/wallpapers/1.jpg"
                alt="bg"
                width="100%"
                height="150"
              />
            </v-col>
            <v-col cols="6" xl="4" lg="4" md="6" sm="6">
              <img
                class="wallpaper"
                src="@/assets/wallpapers/2.jpg"
                alt="bg"
                width="100%"
                height="150"
              />
            </v-col>
            <v-col cols="6" xl="4" lg="4" md="6" sm="6">
              <img
                class="wallpaper"
                src="@/assets/wallpapers/4.jpg"
                alt="bg"
                width="100%"
                height="150"
              />
            </v-col>
            <v-col cols="6" xl="4" lg="4" md="6" sm="6">
              <img
                class="wallpaper"
                src="@/assets/wallpapers/5.jpg"
                alt="bg"
                width="100%"
                height="150"
              />
            </v-col>
            <v-col cols="6" xl="4" lg="4" md="6" sm="6">
              <img
                class="wallpaper"
                src="@/assets/wallpapers/6.jpg"
                alt="bg"
                width="100%"
                height="150"
              />
            </v-col>
            <v-col cols="6" xl="4" lg="4" md="6" sm="6">
              <img
                class="wallpaper"
                src="@/assets/wallpapers/7.jpg"
                alt="bg"
                width="100%"
                height="150"
              />
            </v-col>
            <v-col cols="6" xl="4" lg="4" md="6" sm="6">
              <img
                class="wallpaper"
                src="@/assets/wallpapers/8.jpg"
                alt="bg"
                width="100%"
                height="150"
              />
            </v-col>
            <v-col cols="6" xl="4" lg="4" md="6" sm="6">
              <img
                class="wallpaper"
                src="@/assets/wallpapers/9.jpg"
                alt="bg"
                width="100%"
                height="150"
              />
            </v-col>
            <v-col cols="6" xl="4" lg="4" md="6" sm="6">
              <img
                class="wallpaper"
                src="@/assets/wallpapers/10.jpg"
                alt="bg"
                width="100%"
                height="150"
              />
            </v-col>
            <v-col cols="6" xl="4" lg="4" md="6" sm="6">
              <img
                class="wallpaper"
                src="@/assets/wallpapers/11.jpg"
                alt="bg"
                width="100%"
                height="150"
              />
            </v-col>
            <v-col cols="6" xl="4" lg="4" md="6" sm="6">
              <img
                class="wallpaper"
                src="@/assets/wallpapers/12.jpg"
                alt="bg"
                width="100%"
                height="150"
              />
            </v-col>
            <v-col cols="6" xl="4" lg="4" md="6" sm="6">
              <img
                class="wallpaper"
                src="@/assets/wallpapers/13.jpg"
                alt="bg"
                width="100%"
                height="150"
              />
            </v-col>
          </v-row>
        </v-container>
      </div>

      <p>رنگ قاب</p>
      <v-menu
        v-model="frameMenu"
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="290px"
        max-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field
            label="رنگ"
            prepend-inner-icon="mdi-palette"
            readonly
            hide-details
            :value="frameValue"
            v-on="on"
            outlined
            dense
            class="mb-7"
          ></v-text-field>
        </template>

        <v-color-picker
          show-swatches
          hide-canvas
          hide-sliders
          hide-inputs
          :swatches="swatches"
          v-model="frameValue"
          @input="updateStar"
          no-title
        ></v-color-picker>
      </v-menu>

      <v-divider class="my-5"></v-divider>

      <v-row dir="rtl">
        <v-col cols="12">
          <p class="mb-0">شخصی سازی ستاره ها و صور فلکی</p>
        </v-col>
        <v-col cols="12" xl="6" lg="6" md="12" sm="12">
          <v-switch
            @click="updateStar"
            v-model="showDot"
            inset
            label="نقطه‌ها"
          ></v-switch>
        </v-col>
        <v-col cols="12" xl="6" lg="6" md="12" sm="12">
          <v-switch
            @click="updateStar"
            v-model="showStar"
            inset
            label="ستاره‌ها"
          ></v-switch>
        </v-col>
        <v-col cols="12" xl="6" lg="6" md="12" sm="12">
          <v-switch
            @click="
              () => {
                updateStar();
                showConstellation ? '' : (showConstellationText = false);
              }
            "
            v-model="showConstellation"
            inset
            label="صور فلکی"
          ></v-switch>
        </v-col>
        <v-col cols="12" xl="6" lg="6" md="12" sm="12">
          <v-switch
            @click="updateStar"
            :disabled="!showConstellation ? true : false"
            v-model="showConstellationText"
            inset
            label="نام صور فلکی"
          ></v-switch>
        </v-col>
      </v-row>

      <v-divider class="my-5"></v-divider>

      <v-row>
        <v-col cols="12" xl="6" lg="6" md="12" sm="12">
          <v-btn
            @click="$emit('update:stepper', 3)"
            block
            color="error"
            outlined
          >
            مرحله‌ی قبلی
          </v-btn>
        </v-col>
        <v-col cols="12" xl="6" lg="6" md="12" sm="12">
          <v-btn @click="$emit('update:stepper', 5)" block color="primary">
            مرحله‌ی بعدی
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
    <Loading :isLoading="loading" />
  </div>
</template>

<script>
import Loading from "@/components/Loading";

export default {
  name: "star-customize",
  components: {
    Loading,
  },
  watch: {
    showWallpaper: function() {
      if (this.showWallpaper) {
        const wallpapers = document.querySelectorAll(".wallpaper");
        wallpapers.forEach((wallpaper) => {
          wallpaper.addEventListener("click", () => {
            wallpapers.forEach((item) => (item.style.border = ""));
            wallpaper.style.border = "5px solid blue";
            this.$store.commit("setWallpaper", wallpaper.src);
            this.$store.dispatch("getStarMap");
          });
        });
      }
    },
  },
  data() {
    return {
      showWallpaper: false,
      loading: false,
      valid: true,
      bgValue: "#000000",
      bgMenu: false,
      radioGroup: "A1",

      frameMenu: false,
      frameValue: "#212121",
      swatches: [
        ["#FF0000", "#AA0000", "#550000"],
        ["#FFFF00", "#AAAA00", "#555500"],
        ["#00FF00", "#00AA00", "#005500"],
        ["#00FFFF", "#00AAAA", "#005555"],
        ["#0000FF", "#0000AA", "#000055"],
      ],

      showDot: true,
      showStar: true,
      showConstellation: true,
      showConstellationText: true,
    };
  },
  methods: {
    updateStar() {
      this.loading = true;
      this.$store.commit("setCustomize", {
        size: this.radioGroup,
        background: this.bgValue,
        frame: this.frameValue,
        dot: this.showDot,
        star: this.showStar,
        constellation: this.showConstellation,
        constellationText: this.showConstellationText,
      });
      this.$store.dispatch("getStarMap");
      this.loading = false;
    },
  },
  mounted(){
    const editMode = localStorage.getItem("editMode");
    if(editMode){
      this.radioGroup = this.$store.state.starmap.customize.size;
      this.bgValue = this.$store.state.starmap.customize.background;
      this.frameValue = this.$store.state.starmap.customize.frame;
      this.showDot = this.$store.state.starmap.customize.dot;
      this.showStar = this.$store.state.starmap.customize.star;
      this.showConstellation = this.$store.state.starmap.customize.constellation;
      this.constellationText = this.$store.state.starmap.customize.constellationText;
    }
  }
};
</script>
