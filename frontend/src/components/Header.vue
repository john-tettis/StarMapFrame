<template>
  <header class="d-flex align-center justify-space-between" style="background: #121212;height:50px">
    <div>
      <img src="@/assets/logo.png" width="64"/>
    </div>
    <div>
      <ul class="nav">
        <li><router-link to="/">خانه</router-link></li>
        <li><router-link to="/builder">ستاره ساز</router-link></li>
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
      font-size: .8rem;
      font-family: auto;
    }
  }
}
</style>