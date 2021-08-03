<template>
  <v-app-bar
    app
    color="dark"
    dark
    :style="
      $route.path === '/login' ? 'background: transparent !important' : ''
    "
  >
    <div class="d-flex align-center">
      <router-link to="/"
        ><img src="@/assets/logo.png" alt="logo" width="52"
      /></router-link>
    </div>

    <v-spacer></v-spacer>
    <ul class="navbar">
      <li>
        <router-link to="/"> صفحه‌ی اصلی </router-link>
      </li>
      <li>
        <router-link to="/builder">
          ستاره ساز
        </router-link>
      </li>
      <li v-if="!$cookies.isKey('token') && $cookies.get('token') === null">
        <router-link to="/login">
          ورود
        </router-link>
      </li>
      <li v-if="$cookies.isKey('token') && $cookies.get('token') !== null">
        <router-link to="/admin">
          ادمین
        </router-link>
      </li>
    </ul>
    <v-icon class="menu-icon" @click="openMenu">mdi-menu</v-icon>
  </v-app-bar>
</template>

<script>
export default {
  name: "Header",
  methods: {
    openMenu() {
      const navbar = document.querySelector("ul.navbar");
      if (navbar.classList.contains("mobile")) {
        navbar.classList.remove("mobile");
      } else {
        navbar.classList.add("mobile");
      }
    },
  },
};
</script>
