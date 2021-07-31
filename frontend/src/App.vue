<template>
  <v-app>
    <v-app-bar
      app
      color="dark"
      dark
      :style="
        $route.path === '/login' ? 'background: transparent !important' : ''
      "
    >
      <div class="d-flex align-center">
        <img src="@/assets/logo.png" alt="logo" width="72" />
      </div>

      <v-spacer></v-spacer>
      <ul class="navbar">
        <li>
          <router-link class="white--text" to="/"> صفحه‌ی اصلی </router-link>
        </li>
        <li>
          <router-link class="white--text" to="/builder">
            ستاره ساز
          </router-link>
        </li>
        <li v-if="!$cookies.isKey('token') && $cookies.get('token') === null">
          <router-link class="white--text" to="/login">
            ورود
          </router-link>
        </li>
        <li v-if="$cookies.isKey('token') && $cookies.get('token') !== null">
          <router-link class="white--text" to="/admin">
            ادمین
          </router-link>
        </li>
      </ul>
    </v-app-bar>

    <v-main
      :style="$route.path === '/login' ? 'position:relative;top:-64px;' : ''"
    >
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",

  data: () => ({
    //
  }),
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
}
ul.navbar a:hover {
  background-color: hsl(0, 0%, 20%);
}
</style>
