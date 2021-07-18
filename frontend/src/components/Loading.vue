<template>
  <v-overlay :value="isLoading" :z-index="999999">
    <v-progress-circular
      :size="50"
      color="primary"
      indeterminate
    ></v-progress-circular>
  </v-overlay>
</template>

<script>
export default {
  name: "Loading",
  props: ["isLoading"],
};
</script>

<style></style>