<template>
  <div>
    <header-component></header-component>
    <div class="d-flex flex-column align-center justify-center px-5 pb-16 sectionDark">
    <div class="white--text">
      <h2 class="text-center">آسمان را هدیه بدهید!</h2>
      <h3 class="text-center">هدیه‌ای به وسعت آسمان را برای عزیزان خود تهیه کنید!</h3>
      <p class="text-center">لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است و برای شرایط فعلی تکنولوژی مورد نیاز و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد کتابهای زیادی در شصت و سه درصد گذشته حال و آینده شناخت فراوان جامعه و متخصصان را می طلبد</p>
    </div>
    <div>
      <img src="https://positiveprints.com/wp-content/uploads/2021/01/star-map-quotes.jpg" alt="a starmap image" width="60%" class="d-block mx-auto" />
    </div>
  </div>
  </div>
</template>

<script>
import HeaderComponent from '@/components/Header';
export default {
  name: "Home",
  components: {
    HeaderComponent,
  }
};
</script>


<style scoped>
div.sectionDark {
  background: #121212;
}
</style>