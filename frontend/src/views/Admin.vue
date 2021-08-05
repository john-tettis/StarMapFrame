<template>
  <div class="pa-5">
    
    <orders :loading.sync="loading"/>

    <v-divider class="mt-5 mb-1"></v-divider>
    <v-divider class="mb-5 mt-1"></v-divider>
    
    <uploads :loading.sync="loading"/>
    
    <v-divider class="mt-5 mb-1"></v-divider>
    <v-divider class="mb-5 mt-1"></v-divider>
    
    <discounts :loading.sync="loading"/>
    
    <Loading :isLoading="loading" />
  </div>
</template>

<script>
import Orders from '@/components/admin/Orders'
import Uploads from '@/components/admin/Uploads'
import Discounts from '@/components/admin/Discounts';
import Loading from "@/components/Loading";

export default {
  name: "AdminPanel",
  components: {
    Orders,
    Uploads,
    Discounts,
    Loading,
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
