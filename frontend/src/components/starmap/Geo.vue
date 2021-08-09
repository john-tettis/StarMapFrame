<template>
  <div>
    <h2 class="mb-5">تاریخ و ساعت و لوکیشن را انتخاب کنید</h2>
    <v-form ref="form" v-model="valid">
      <v-autocomplete
        outlined
        dense
        v-model="location"
        prepend-inner-icon="mdi-map-marker"
        label="موقعیت جغرافیایی"
        :items="locationGuess"
        item-text="display_name"
        @keyup="updateGuess($event)"
      ></v-autocomplete>
      <!--DatePicker-->
      <v-menu
        ref="DateMenu"
        v-model="dateMenu"
        :close-on-content-click="false"
        transition="scale-transition"
        offset-y
        min-width="auto"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            outlined
            dense
            v-model="dateValue"
            label="تاریخ"
            prepend-inner-icon="mdi-calendar"
            readonly
            v-bind="attrs"
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker
          :locale-first-day-of-year="1"
          v-model="dateValue"
          :active-picker.sync="activePicker"
          :max="
            new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
              .toISOString()
              .substr(0, 10)
          "
          min="1950-01-01"
          @change="$refs.DateMenu.save(dateValue)"
        ></v-date-picker>
      </v-menu>
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
          ></v-text-field>
        </template>
        <v-time-picker
          v-model="timeValue"
          full-width
          @click:minute="$refs.TimeMenu.save(timeValue)"
        ></v-time-picker>
      </v-menu>
      <v-btn class="mt-8" block color="primary" @click="submit($event)">ثبت</v-btn>
    </v-form>
  </div>
</template>

<script>
import { Client } from "@googlemaps/google-maps-services-js";
import moment from "moment";
import { v4 as uuidv4 } from "uuid";

export default {
  name: "star-geo",
  watch: {
    dateMenu(val) {
      val && setTimeout(() => (this.activePicker = "YEAR"));
    },
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
      }).catch(error=>{
        console.log(error)
      })
    },
    async submit(event) {
      event.preventDefault();
      if (this.valid) {
        this.coordinate = {
          lat: this.location.lat,
          lng: this.location.lon
        }
        setTimeout(async () => {
          await this.$store.commit("setGeo", {
            coordinate: this.coordinate,
            time: moment(this.timeValue, "hh:mm").format("hh.mm.ss"),
            date: moment(this.dateValue).format("DD.MM.YYYY"),
          });
          await this.$store.dispatch("getStarMap");
          this.$emit("update:stepper", 2);
        }, 1500);
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
          x: "",
          y: "",
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
