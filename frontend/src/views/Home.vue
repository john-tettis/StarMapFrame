<template>
  <div style="min-height: 2000px">
    <div class="bg-dark bg-wallpaper">
      <Hero />
      <div class="custom-shape-divider-bottom-1626886743">
        <svg
          data-name="Layer 1"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 1200 120"
          preserveAspectRatio="none"
        >
          <path
            d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
            class="shape-fill"
          ></path>
        </svg>
      </div>
    </div>
    <div class="bg-dark py-16">
      <Features />
    </div>
    <div>
      <Info/>
    </div>
    
  </div>
</template>

<script>
import Hero from "@/components/landing/Hero";
import Features from "@/components/landing/Features";
import Info from '@/components/landing/Info';

export default {
  name: "Home",
  components: {
    Hero,
    Features,
    Info
  },
};
</script>

<style>
.bg-wallpaper {
  background-image: url("../assets/hero-wallpaper.jpg");
  background-repeat: no-repeat;
  background-size: cover;
}
.bg-dark {
  background-color: #272727;
}
.custom-shape-divider-bottom-1626886743 {
  position: relative;
  bottom: 0;
  left: 0;
  width: 100%;
  overflow: hidden;
  line-height: 0;
  transform: rotate(180deg);
}

.custom-shape-divider-bottom-1626886743 svg {
  position: relative;
  display: block;
  width: calc(140% + 1.3px);
  height: 165px;
}

.custom-shape-divider-bottom-1626886743 .shape-fill {
  fill: #272727;
}
</style>
