<template>
  <div>
    <v-row align="baseline" class="mb-4">
      <v-col cols="12" xl="6" lg="6" md="12" sm="12">
        <p class="mb-0 p-title">اضافه کردن متن روی تابلو</p>
      </v-col>
    </v-row>
    <v-form ref="form" v-model="valid">
      <div v-show="counter >= 0" id="line1">
        <v-text-field
          label="متن"
          outlined
          dense
          prepend-inner-icon="mdi-pencil"
          v-model="line1.value"
          @change="updateStars"
        />
        <v-select
          label="فونت متن"
          :items="availableFonts"
          v-model="font1"
          outlined
          dense
          @change="setFont(0)"
        />
        <v-row>
          <v-col cols="6">
            <v-text-field
              label="سایز متن"
              outlined
              dense
              prepend-inner-icon="mdi-pencil"
              v-model="line1.size"
              @change="updateStars"
            />
          </v-col>
          <v-col cols="6">
            <v-menu
              v-model="line1Menu"
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
                  :value="line1.color"
                  @change="updateStars"
                  v-on="on"
                  outlined
                  dense
                  class="mb-7"
                ></v-text-field>
              </template>

              <v-color-picker v-model="line1.color" no-title></v-color-picker>
            </v-menu>
          </v-col>
        </v-row>
      </div>

      <v-divider v-show="counter >= 1" class="my-5"></v-divider>

      <div v-show="counter >= 1" id="line2">
        <v-text-field
          label="متن"
          outlined
          dense
          prepend-inner-icon="mdi-pencil"
          v-model="line2.value"
          @change="updateStars"
        />
        <v-select
          label="فونت متن"
          :items="availableFonts"
          v-model="font2"
          outlined
          dense
          @change="setFont(1)"
        />
        <v-row>
          <v-col cols="6">
            <v-text-field
              label="سایز متن"
              outlined
              dense
              prepend-inner-icon="mdi-pencil"
              v-model="line2.size"
              @change="updateStars"
            />
          </v-col>
          <v-col cols="6">
            <v-menu
              v-model="line2Menu"
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
                  :value="line2.color"
                  @change="updateStars"
                  v-on="on"
                  outlined
                  dense
                  class="mb-7"
                ></v-text-field>
              </template>

              <v-color-picker v-model="line2.color" no-title></v-color-picker>
            </v-menu>
          </v-col>
        </v-row>
      </div>

      <v-divider v-show="counter >= 2" class="my-5"></v-divider>

      <div v-show="counter >= 2" id="line3">
        <v-text-field
          label="متن"
          outlined
          dense
          prepend-inner-icon="mdi-pencil"
          v-model="line3.value"
          @change="updateStars"
        />
        <v-select
          label="فونت متن"
          :items="availableFonts"
          v-model="font3"
          outlined
          dense
          @change="setFont(2)"
        />
        <v-row>
          <v-col cols="6">
            <v-text-field
              label="سایز متن"
              outlined
              dense
              prepend-inner-icon="mdi-pencil"
              v-model="line3.size"
              @change="updateStars"
            />
          </v-col>
          <v-col cols="6">
            <v-menu
              v-model="line3Menu"
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
                  :value="line3.color"
                  @change="updateStars"
                  v-on="on"
                  outlined
                  dense
                  class="mb-7"
                ></v-text-field>
              </template>

              <v-color-picker v-model="line3.color" no-title></v-color-picker>
            </v-menu>
          </v-col>
        </v-row>
      </div>

      <v-row no-gutters justify="center">
        <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
          <v-btn
            color="secondary"
            outlined
            @click="deleteLine"
            :disabled="counter == 0"
            style="width:98%"
            >حذف پاراگراف</v-btn
          >
        </v-col>
        <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
          <v-btn
            color="secondary"
            style="width:98%"
            @click="
              () => {
                counter == 2 ? '' : counter++;
              }
            "
            :disabled="counter === 2"
            >افزودن پاراگراف</v-btn
          ></v-col
        >
      </v-row>

      <v-row no-gutters class="mt-3 mb-3" justify="center">
        <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
          <v-btn
            @click="$emit('update:stepper', 1)"
            color="error"
            outlined
            class="w-98"
          >
            مرحله‌ی قبلی
          </v-btn>
        </v-col>
        <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
          <v-btn @click="$emit('update:stepper', 3)" color="primary" class="w-98">
            مرحله‌ی بعدی
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script>
export default {
  name: "star-text",
  data() {
    return {
      valid: true,
      line1Menu: false,
      line2Menu: false,
      line3Menu: false,

      line1: {
        value: "",
        size: "42",
        font: "Roboto",
        color: "#FFFFFF",
      },
      line2: {
        value: "",
        size: "42",
        font: "Roboto",
        color: "#FFFFFF",
      },
      line3: {
        value: "",
        size: "42",
        font: "Roboto",
        color: "#FFFFFF",
      },
      availableFonts: [],
      counter: 0,
      font1: "Roboto-انگلیسی",
      font2: "Roboto-انگلیسی",
      font3: "Roboto-انگلیسی",
    };
  },
  methods: {
    updateStars() {
      this.$store.commit("setText", {
        line1: this.line1,
        line2: this.line2,
        line3: this.line3,
      });
      this.$store.dispatch("getStarMap");
    },
    deleteLine() {
      if(this.counter === 2){
        this.line3 = {
        value: "",
        size: "42",
        font: "Roboto",
        color: "#FFFFFF"
        };
        this.updateStars()
      }

      if (this.counter === 1) {
        this.line2 = {
          value: "",
          size: "42",
          font: "Roboto",
          color: "#FFFFFF",
        };
        this.updateStars();
      }

      if (this.counter === 0) {
        return;
      } else {
        this.counter -= 1;
      }
    },
    setFont(line){
      if(line===0){
        this.line1.font = (this.font1.split("-"))[0]
      }
      if(line===1){
        this.line2.font = (this.font2.split("-"))[0]
      }
      if(line===2){
        this.line3.font = (this.font3.split("-"))[0]
      }
      this.updateStars()
    }
  },
  mounted() {
    this.axios.get("/api/fonts").then((response) => {
      this.availableFonts = response.data.fonts;
    });
    const editMode = localStorage.getItem("editMode");
    if (editMode) {
      this.line1 = this.$store.state.starmap.text.line1;
      this.line2 = this.$store.state.starmap.text.line2;
      this.line3 = this.$store.state.starmap.text.line3;
      this.$store.dispatch("getStarMap")
    }
  },
};
</script>
