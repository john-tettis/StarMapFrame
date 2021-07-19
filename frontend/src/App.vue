<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <img src="@/assets/logo.png" alt="logo" width="32"/>
      </div>

      <v-spacer></v-spacer>
      <ul class="navbar">
          <li>
            <router-link class="white--text" to="/">
              صفحه‌ی اصلی
            </router-link>
          </li>
          <li>
            <router-link class="white--text" to="/builder">
              ستاره ساز
            </router-link>
          </li>
        </ul>

    </v-app-bar>

    <v-main class="my-5">
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
};
</script>

<style>
::v-deep .v-toolbar__content{
  height: 45px;
}
ul.navbar{
  list-style-type: none;
}
ul.navbar li{
  display:inline;
}
ul.navbar a{
  text-decoration: none;
  padding: 11px 25px;
  font-weight: bold;
}
ul.navbar a:hover{
  background-color: rgba(56, 100, 103, 0.2);
}
</style>
