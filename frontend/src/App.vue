<template>
  <v-app>
    <!-- <Header/> -->
    <v-main
      :class="$route.path === '/login' ? 'isLoginClass' : ''"
    >
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
// import Header from '@/components/Header';
export default {
  name: "App",
  components:{
    // Header,
  },
};
</script>

<style lang="scss">
@import "@/assets/styles/main.scss";
.isLoginClass {
  position:relative;top:-64px;
}
</style>
