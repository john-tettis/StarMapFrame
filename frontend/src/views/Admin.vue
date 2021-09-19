<template>
  <div class="pa-5">
    <orders-list :loading.sync="loading"/>

    <v-divider class="mt-5 mb-1"></v-divider>
    <v-divider class="mb-5 mt-1"></v-divider>

    <uploads-images :loading.sync="loading" />

    <v-divider class="mt-5 mb-1"></v-divider>
    <v-divider class="mb-5 mt-1"></v-divider>

    <discounts-list :loading.sync="loading" />

    <loading-overlay :is-loading="loading" />
  </div>
</template>

<script>
import OrdersList from "@/components/admin/Orders";
import UploadsImages from "@/components/admin/Uploads";
import DiscountsList from "@/components/admin/Discounts";
import LoadingOverlay from "@/components/Loading";

export default {
  name: "AdminPanel",
  components: {
    OrdersList,
    UploadsImages,
    DiscountsList,
    LoadingOverlay,
  },
  data() {
    return {
      loading: false,
    };
  },
};
</script>

<style>
tbody,
thead {
  white-space: nowrap;
}
</style>
