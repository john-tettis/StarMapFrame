<template>
  <div>
    <h2>موزیک دلخواه خود را آپلود کنید</h2>
    <v-form ref="form" v-model="valid">
      <v-file-input accept="music/*" label="فایل موزیک" outlined dense></v-file-input>
      <v-file-input accept="image/*" label="فایل کاور" outlined dense></v-file-input>
      <v-text-field dense outlined v-model="singer" label="خواننده"/>
      <v-text-field dense outlined v-model="name" label="نام موسیقی"/>
      <v-row>
        <v-col cols="6">
          <v-btn @click="$emit('update:stepper', 2)" color="error" block outlined>مرحله‌ی قبلی</v-btn>
        </v-col>
        <v-col cols="6">
          <v-btn color="primary" block @click="$emit('update:stepper', 4)">مرحله‌ی بعدی</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script>
export default {
  name: "star-music",
  data() {
    return {
      valid: false,
    };
  },
};
</script>

<style></style>
