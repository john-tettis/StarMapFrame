<template>
  <v-app>
    <Header/>
    <v-main
      :style="$route.path === '/login' ? 'position:relative;top:-64px;' : ''"
    >
      <router-view />
    </v-main>
    <Footer/>
  </v-app>
</template>

<script>
import Header from '@/components/Header';
import Footer from '@/components/Footer';
export default {
  name: "App",
  components:{
    Header,
    Footer,
  },
};
</script>

<style>
::v-deep .v-toolbar__content {
  height: 45px;
}
ul.navbar {
  list-style-type: none;
}
ul.navbar li {
  display: inline;
}
ul.navbar a {
  text-decoration: none;
  padding: 11px 25px;
  font-weight: bold;
  border-radius: 5px;
  font-size: 12px;
  color: #fff;
}
ul.navbar a:hover {
  background-color: hsl(0, 0%, 20%);
}

ul.mobile {
  display: block !important;
  z-index: 99999;
  background-color: #eee;
  position: relative;
  top: 84px;
  width: 100%;
  padding-left: 0 !important;
  box-shadow: 1px 0 10px rgba(0, 0, 0, 0.4);
  border-radius: 0 0 5px 5px;
}

ul.mobile > li {
  display: block;
  width: 100%;
  text-align: center;
  margin: 10px auto;
}
ul.mobile a {
  color: #212121 !important;
  text-align: center;
}
.menu-icon {
  display: none !important;
}

@media screen and (max-width: 990px) {
  ul.navbar {
    display: none;
  }
  .menu-icon {
    display: block !important;
  }
}
</style>
