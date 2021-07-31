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
