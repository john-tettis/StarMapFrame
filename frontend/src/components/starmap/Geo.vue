<template>
  <div>
    <p class="mb-5" style="font-size: 1.3rem">انتخاب تاریخ و مکان آسمان</p>
    <v-form ref="form" v-model="valid">
      <v-select
        v-model="province"
        dense
        outlined
        label="انتخاب استان"
        prepend-inner-icon="mdi-pin"
        :items="provinces"
        item-text="title"
        item-value="id"
        @input="filterCities();$v.province.$touch()"
        @blur="$v.province.$touch()"
      />
      <v-select
        v-model="city"
        dense
        outlined
        label="انتخاب شهر"
        prepend-inner-icon="mdi-city"
        :items="cities"
        item-text="title"
        :item-value="findLatLong"
        :disabled="province === null"
        @input="$v.city.$touch()"
        @blur="$v.city.$touch()"
      />

      <!--DatePicker-->
      <v-text-field
        id="custom-date-input"
        outlined
        dense
        v-model="dateValue"
        label="تاریخ"
        prepend-inner-icon="mdi-calendar"
        @input="$v.dateValue.$touch()"
        @blur="$v.dateValue.$touch()"
      ></v-text-field>
      <custom-date-picker
        element="custom-date-input"
        v-model="dateValue"
      ></custom-date-picker>
      <!-- </v-menu> -->
      <!--TimePicker-->
      <v-btn
        class="mt-8 mb-5"
        block
        color="primary"
        @click="submit($event)"
        :disabled="$v.timeValue.$invalid || $v.dateValue.$invalid || $v.city.$invalid"
        >مرحله‌ی بعدی</v-btn
      >
    </v-form>
  </div>
</template>

<script>
import provinces from "@/assets/province.json";
import cities from "@/assets/cities.json";

import moment from "moment-jalaali";
import { v4 as uuidv4 } from "uuid";
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";

export default {
  name: "star-geo",
  mixins: [validationMixin],
  validations: {
    timeValue: {
      required,
    },
    province: {
      required,
    },
    city: {
      required,
    },
    dateValue: {
      required,
    },
  },
  data() {
    return {
      loading: false,
      search: null,
      valid: true,
      dateValue: null,
      timeValue: "00:00",
      provinces: provinces,
      province: null,
      city: null,
      cities: cities,
      coordinate: {},
    };
  },
  methods: {
    filterCities(){
      this.cities = cities
      this.cities = cities.filter(item=>item.province_id===this.province)
    },
    findLatLong(item) {
      this.coordinate = {
        lat: item.latitude,
        lng: item.longitude,
      };
      return item.id
    },
    async submit(event) {
      event.preventDefault();
      if (this.valid) {
        setTimeout(async () => {
          await this.$store.commit("setGeo", {
            location: this.coordinate,
            time: moment(this.timeValue, "hh:mm").format("hh.mm.ss"),
            date: moment(this.dateValue, "jYYYY-jMM-jDD").format("DD.MM.YYYY"),
          });
          await this.$store.dispatch("getStarMap");
          this.$emit("update:stepper", 2);
        }, 800);
      }
    },
  },
  mounted() {
    history.pushState(null, null, location.href);
    window.onpopstate = function () {
      history.go(1);
    };
    const editMode = localStorage.getItem("editMode");
    if (!editMode) {
      this.$store.commit("setProduct", {
        paint: true,
        shape: false,
        geo: {
          location: "",
          date: "",
          time: "",
        },
        text: {
          line1: {
            value: "",
            font: "",
            size: "42",
            color: "#ffffff",
          },
          line2: {
            value: "",
            font: "",
            size: "42",
            color: "#ffffff",
          },
          line3: {
            value: "",
            font: "",
            size: "42",
            color: "#ffffff",
          },
        },
        music: {
          qr: "",
        },
        background: {
          bg: "",
          x: 0,
          y: 0,
          opacity: 40,
          wallpaper: "",
          circle: true,
        },
        customize: {
          size: "A3",
          frame: "#000000",
          background: "#000000",
          dot: true,
          star: true,
          constellation: true,
          constellationText: true,
        },
        filename: uuidv4() + ".svg",
      });
      this.$store.commit("setImage", "");
    }
  },
  props: ["stepper"],
};
</script>
