<template>
  <header class="d-flex align-center justify-space-between" style="background: #121212">
    <div>
      <img src="@/assets/logo.png" width="100"/>
    </div>
    <div>
      <ul class="nav">
        <li><router-link to="/">صفحه‌ی اصلی</router-link></li>
        <li><router-link to="/builder">ستاره‌ساز</router-link></li>
      </ul>
    </div>
  </header>
</template>

<script>
export default {
  name: "Header",
};
</script>

<style lang="scss">
ul.nav{
  list-style: none;
  li{
    display: inline;
    a{
      text-decoration: none;
      color: #fefefe;
      padding: 10px;
      font-family: IRANSansX;
      font-size: 14px;
    }
  }
}
</style>