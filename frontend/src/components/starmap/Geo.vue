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
        @keyup="updateGuess($event)"
      >
      </v-autocomplete>
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
      <v-btn class="mt-8" block color="primary" @click="submit($event)">
        ثبت
      </v-btn>
    </v-form>
    <Loading :isLoading="loading" />
  </div>
</template>

<script>
import { Client } from "@googlemaps/google-maps-services-js";
import moment from "moment";
import Loading from "@/components/Loading";

export default {
  name: "star-geo",
  components: {
    Loading,
  },
  watch: {
      dateMenu (val) {
        val && setTimeout(() => (this.activePicker = 'YEAR'))
      },
    },
  data() {
    return {
      activePicker: null,
      loading: false,
      valid: true,
      client: new Client({}),
      API_KEY: "AIzaSyBgBc9WzvrQY4A2AJNrahd1Od8LRI2lv9w",
      dateMenu: false,
      dateValue: null,
      timeMenu: false,
      timeValue: null,
      locationGuess: [],
      location: "",
      coordinate: {},
    };
  },
  methods: {
    updateGuess(event) {
      this.client
        .placeAutocomplete({
          params: {
            input: event.target.value,
            key: this.API_KEY,
          },
        })
        .then((r) => {
          this.locationGuess = [];
          r.data.predictions.forEach((location) => {
            this.locationGuess.push(location.description);
          });
        })
        .catch((e) => {
          console.log(e);
        });
    },
    getCoordinate(location) {
      this.client
        .geocode({
          params: {
            address: location,
            key: this.API_KEY,
          },
        })
        .then((r) => {
          this.coordinate = r.data.results[0].geometry.location;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    async submit(event) {
      event.preventDefault();
      this.loading = true;
      if (this.valid) {
        await this.getCoordinate(this.location);
        setTimeout(() => {
          this.$store.commit("setGeo", {
            location: this.coordinate,
            time: moment(this.timeValue, "hh:mm").format("hh.mm.ss"),
            date: moment(this.dateValue).format("DD.MM.YYYY"),
          });
          this.axios
            .post("/api/starmap", this.$store.state.starmap)
            .then((response) => {
              this.loading = false;
              if (response.data.result) {
                this.$store.commit(
                  "setImage",
                  response.data.path + `?${Date.now()}`
                );
                this.$emit("update:stepper", 2);
              }
            })
            .catch((error) => {
              this.loading = false;
              console.log(error);
            });
        }, 1500);
      }
    },
  },
  props: ["stepper"],
};
</script>
