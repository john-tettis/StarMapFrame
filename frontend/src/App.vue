<template>
  <v-app>
    <!-- <Header/> -->
    <v-main
      :style="$route.path === '/login' ? 'position:relative;top:-64px;' : ''"
    >
      <router-view></router-view>
    </v-main>
    <!-- <Footer/> -->
  </v-app>
</template>

<script>
// import Header from '@/components/Header';
// import Footer from '@/components/Footer';
export default {
  name: "App",
  components:{
    // Header,
    // Footer,
  },
};
</script>

<style lang="scss">
@import "@/assets/styles/main.scss";
</style>
