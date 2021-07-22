<template>
  <v-container class="white--text">
    <v-row class="py-16" align="center">
      <v-col cols="12" sm="12" md="12" lg="6" xl="6" class="px-10">
        <h1 class="h1">آسمان را به عزیزان خود هدیه بدید!</h1>
        <h2 class="h2 mb-3">
          نقشه‌ی ستاره‌ای خود را بر اساس تاریخ، ساعت و موقعیت مکانی دلخواه
          بسازید
        </h2>
        <p class="text-justify">
          لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده
          از طراحان گرافیک است. چاپگرها و متون بلکه روزنامه و مجله در ستون و
          سطرآنچنان که لازم است و برای شرایط فعلی تکنولوژی مورد نیاز و کاربردهای
          متنوع با هدف بهبود ابزارهای کاربردی می باشد. کتابهای زیادی در شصت و سه
          درصد گذشته، حال و آینده شناخت فراوان جامعه و متخصصان را می طلبد.
        </p>
        <v-btn color="primary" class="float-left" large>
          <router-link
            to="/builder"
            class="white--text"
            style="text-decoration: none"
          >
            شروع کنید
          </router-link>
        </v-btn>
      </v-col>
      <v-col class="pa-0" cols="12" sm="12" md="12" lg="6" xl="6">
        <img
          class="example-img elevation-5"
          src="https://i.pinimg.com/originals/d0/83/0e/d0830e579843eff3d01d6d8180e48967.png"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Hero",
};
</script>

<style lang="scss">
.example-img {
  display: block;
  margin: 0 auto;
  position: absolute;
  top: 50px;
  left: 100px;
  bottom: 0;
  width: 400px;
  height: 600px;
  border-radius: 5px;
  z-index: 1;
  @media only screen and (max-width: 1268px) {
    position: static;
  }
}
</style>
