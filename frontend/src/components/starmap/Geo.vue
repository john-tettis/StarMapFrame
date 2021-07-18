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
        v-model="dateMenu"
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="290px"
        max-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field
            label="تاریخ"
            prepend-inner-icon="mdi-calendar"
            readonly
            hide-details
            :value="dateValue"
            v-on="on"
            outlined
            dense
            class="mb-7"
          ></v-text-field>
        </template>

        <v-date-picker
          locale="fa-ir"
          v-model="dateValue"
          no-title
          @input="dateMenu = false"
        ></v-date-picker>
      </v-menu>
      <!--TimePicker-->
      <v-menu
        v-model="timeMenu"
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="290px"
        max-width="290px"
      >
        <template v-slot:activator="{ on }">
          <v-text-field
            label="ساعت"
            prepend-inner-icon="mdi-clock"
            readonly
            hide-details
            :value="timeValue"
            v-on="on"
            outlined
            dense
          ></v-text-field>
        </template>

        <v-time-picker
          v-model="timeValue"
          no-title
          @input="timeMenu = false"
        ></v-time-picker>
      </v-menu>
      <v-btn class="mt-8" block color="primary" @click="submit($event)">
        ثبت
      </v-btn>
    </v-form>
    <Loading :isLoading="loading"/>
  </div>
</template>

<script>
import { Client } from "@googlemaps/google-maps-services-js";
import moment from 'moment';
import Loading from '@/components/Loading';

export default {
  name: "star-geo",
  components:{
    Loading,
  },
  data() {
    return {
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
              this.loading = false
              if(response.data.result){
                this.$store.commit('setImage', response.data.path+`?${Date.now()}`)
                this.$emit("update:stepper", 2)
              }
            }).catch(error=>{
              this.loading = false
              console.log(error);
            });
        }, 1500);
      }
    },
  },
  props: ['stepper'],
};
</script>
