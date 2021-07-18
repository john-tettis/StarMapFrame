<template>
  <div>
    <h2 class="mb-5">متن دلخواه خود را بنویسید</h2>
    <v-form ref="form" v-model="valid">
      <div id="line1">
        <v-text-field
          label="متن اول"
          outlined
          dense
          prepend-inner-icon="mdi-pencil"
          v-model="line1.value"
          @change="updateStars"
        />
        <v-select
          label="فونت متن"
          :items="availableFonts"
          v-model="line1.font"
          outlined
          dense
          @change="updateStars"
        />
        <v-text-field
          label="سایز متن"
          outlined
          dense
          prepend-inner-icon="mdi-pencil"
          v-model="line1.size"
          @change="updateStars"
        />
      </div>

      <v-divider class="my-5"></v-divider>

      <div id="line2">
        <v-text-field
          label="متن اول"
          outlined
          dense
          prepend-inner-icon="mdi-pencil"
          v-model="line2.value"
          @change="updateStars"
        />
        <v-select
          label="فونت متن"
          :items="availableFonts"
          v-model="line2.font"
          outlined
          dense
          @change="updateStars"
        />
        <v-text-field
          label="سایز متن"
          outlined
          dense
          prepend-inner-icon="mdi-pencil"
          v-model="line2.size"
          @change="updateStars"
        />
      </div>

      <v-divider class="my-5"></v-divider>

      <div id="line3">
        <v-text-field
          label="متن اول"
          outlined
          dense
          prepend-inner-icon="mdi-pencil"
          v-model="line3.value"
          @change="updateStars"
        />
        <v-select
          label="فونت متن"
          :items="availableFonts"
          v-model="line3.font"
          outlined
          dense
          @change="updateStars"
        />
        <v-text-field
          label="سایز متن"
          outlined
          dense
          prepend-inner-icon="mdi-pencil"
          v-model="line3.size"
          @change="updateStars"
        />
      </div>
      <v-row>
        <v-col cols="6">
          <v-btn @click="$emit('update:stepper', 1)" block color="error" outlined> مرحله‌ی قبلی </v-btn>
        </v-col>
        <v-col cols="6">
          <v-btn @click="$emit('update:stepper', 3)" block color="primary"> مرحله‌ی بعدی </v-btn>
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
      line1: {
        value: "",
        size: "42",
        font: "Roboto",
      },
      line2: {
        value: "",
        size: "42",
        font: "Roboto",
      },
      line3: {
        value: "",
        size: "42",
        font: "Roboto",
      },
      availableFonts: [],
    };
  },
  methods: {
    updateStars(){
      this.$store.commit('setText', {line1: this.line1, line2: this.line2, line3: this.line3})
      console.log(this.$store.state.starmap)
      this.axios.post("/api/starmap", this.$store.state.starmap).then(response=>{
        if(response.data.result){
          this.$store.commit('setImage', response.data.path+`?${Date.now()}`)
        }
      })
    }
  },
  mounted(){
    this.axios.get('/api/fonts').then(response=>{
      this.availableFonts = response.data.fonts
    })
  }
};
</script>
