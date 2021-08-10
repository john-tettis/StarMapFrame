<template>
  <div>
    <p class="mb-5" style="font-size:1.3rem">انتخاب تاریخ و مکان آسمان</p>
    <v-form ref="form" v-model="valid">
      <v-autocomplete
        outlined
        dense
        v-model="location"
        prepend-inner-icon="mdi-map-marker"
        label="موقعیت جغرافیایی"
        :items="locationGuess"
        item-text="display_name"
        :item-value="getLatLon"
        @keyup.stop="updateGuess($event)"
        @input="$v.location.$touch()"
        @blur="$v.location.$touch()"
      ></v-autocomplete>
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
      <custom-date-picker element="custom-date-input" v-model="dateValue"></custom-date-picker>
      <!-- </v-menu> -->
      <!--TimePicker-->
      <v-menu
        ref="TimeMenu"
        v-model="timeMenu"
        :close-on-content-click="false"
        :nudge-right="40"
        :return-value.sync="timeValue"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            outlined
            dense
            v-model="timeValue"
            label="زمان"
            prepend-inner-icon="mdi-clock-time-four-outline"
            readonly
            v-bind="attrs"
            v-on="on"
            @input="$v.timeValue.$touch()"
            @blur="$v.timeValue.$touch()"
          ></v-text-field>
        </template>
        <v-time-picker
          v-model="timeValue"
          full-width
          @click:minute="$refs.TimeMenu.save(timeValue)"
        ></v-time-picker>
      </v-menu>
      <v-btn
        class="mt-8 mb-5"
        block
        color="primary"
        @click="submit($event)"
        :disabled="$v.location.$invalid || $v.timeValue.$invalid || $v.dateValue.$invalid"
      >مرحله‌ی بعدی</v-btn>
    </v-form>
  </div>
</template>

<script>
import { Client } from "@googlemaps/google-maps-services-js";
import moment from "moment-jalaali";
import { v4 as uuidv4 } from "uuid";
import { validationMixin } from 'vuelidate';
import { required } from "vuelidate/lib/validators"

export default {
  name: "star-geo",
  watch: {
    dateMenu(val) {
      val && setTimeout(() => (this.activePicker = "YEAR"));
    },
  },
  mixins: [validationMixin],
  validations: {
    timeValue: {
      required
    },
    location: {
      required
    },
    dateValue: {
      required,
    }
  },
  data() {
    return {
      activePicker: null,
      valid: true,
      client: new Client({}),
      dateMenu: false,
      dateValue: null,
      timeMenu: false,
      timeValue: "00:00",
      locationGuess: [],
      location: "",
      coordinate: {},
    };
  },
  methods: {
    getLatLon(item){
      this.coordinate = {
        lat: item.lat,
        lng: item.lon
      }
    },
    truncateString(str, num) {
      if (str.length > num) {
        return str.slice(0, num) + "...";
      } else {
        return str;
      }
    },
    updateGuess(event) {
      this.axios.get(`https://heavens-above.com/api2/geocoder/?q=${encodeURI(event.target.value.trim())}`).then((response) => {
        if (response.status === 200) {
          const data = response.data
          data.forEach(item => {
            item.display_name = this.truncateString(item.display_name, 40) + '...'
          })
          this.locationGuess = data

        }
      }).catch(error => {
        console.log(error)
      })
    },
    async submit(event) {
      event.preventDefault();
      if (this.valid) {
        setTimeout(async () => {
          await this.$store.commit("setGeo", {
            coordinate: this.coordinate,
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
    const editMode = localStorage.getItem("editMode");
    if (!editMode) {
      this.$store.commit("setProduct", {
        paint: true,
        shape: false,
        geo: {
          coordinate: "",
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
        },
        customize: {
          size: "A3",
          frame: "#212121",
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
