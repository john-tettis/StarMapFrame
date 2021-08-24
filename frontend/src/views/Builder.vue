<template>
  <v-row id="builder" no-gutters class="py-sm-3">
    <v-col
      v-if="windowWidth < 900"
      cols="12"
      class="order-4"
      style="position: absolute; top: 0; left: 0; right: 0; z-index: 9999"
    >
      <img src="@/assets/logo.png" class="d-block mx-auto" width="85" />
    </v-col>
    <v-col v-else cols="12" class="order-0">
      <img src="@/assets/logo.png" class="d-block mx-auto" width="100" />
    </v-col>
    <v-col cols="12" xl="7" lg="7" md="12" sm="12" class="px-10">
      <v-stepper v-model="step" class="mb-5">
        <!-- <v-stepper-header>
          <v-stepper-step step="1"> لوکیشن </v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step step="2"> متن </v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step step="3"> موسیقی </v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step step="4"> شخصی سازی </v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step step="5"> بکگراند </v-stepper-step>
        </v-stepper-header> -->

        <v-stepper-items>
          <v-stepper-content step="1">
            <StarGeo :stepper.sync="step" />
          </v-stepper-content>

          <v-stepper-content step="2">
            <StarText :stepper.sync="step" />
          </v-stepper-content>

          <v-stepper-content step="3">
            <StarCustomize :stepper.sync="step" />
          </v-stepper-content>

          <v-stepper-content step="4">
            <StarBackground :stepper.sync="step" />
          </v-stepper-content>

          <v-stepper-content step="5">
            <AlbumCustomization :stepper.sync="step" />
          </v-stepper-content>

          <v-stepper-content step="6">
            <StarMusic :stepper.sync="step" />
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-col>
    <v-col cols="12" xl="5" lg="5" md="12" sm="12" id="frame_wrapper" class="d-flex justify-center">
      <v-card height="425" width="400" class="elevation-0">
        <div
          id="frame"
          :style="
            'border:10px solid' + $store.state.starmap.customize.frame + ';'
          "
        >
          <v-overlay :absolute="true" :value="$store.state.loading">
            <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </v-overlay>
          <inline-svg
            style="
              scale: 0.509;
              position: relative;
              top: -260px;
              left: 188px;
              direction: ltr;
              z-index: 0;
            "
            :src="$store.state.path"
          />
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import StarGeo from "@/components/starmap/Geo";
import StarText from "@/components/starmap/Text";
import StarMusic from "@/components/starmap/Music";
import StarCustomize from "@/components/starmap/Customize";
import StarBackground from "@/components/starmap/Background";
import AlbumCustomization from "@/components/starmap/AlbumCustomization";

import InlineSvg from "vue-inline-svg";

export default {
  name: "StarmapBuilder",
  components: {
    StarGeo,
    StarText,
    StarMusic,
    StarCustomize,
    StarBackground,
    InlineSvg,
    AlbumCustomization,
  },
  data() {
    return {
      step: 1,
      windowWidth: window.innerWidth,
      svgSource: this.$store.state.path,
    };
  },
  mounted() {
    const editMode = localStorage.getItem("editMode");
    if (editMode) {
      this.step = 2;
    }
    this.windowWidth = window.innerWidth;
    window.onresize = () => {
      this.windowWidth = window.innerWidth;
    };
  },
};
</script>

<style>
/*
* Prefixed by https://autoprefixer.github.io
* PostCSS: v8.3.6,
* Autoprefixer: v10.3.1
* Browsers: last 4 version
*/

#frame {
  height: 540px;
  width: 400px;
  margin: 25px auto;
  border-radius: 1px;
}

@media screen and (max-width: 400px) {
  #frame {
    width: 343px !important;
    height: 465px !important;
  }
  svg {
    -webkit-transform: scale(
      0.43
    ); /*Webkit:Scale down image to 0.8x original size*/
    -moz-transform: scale(0.43); /*Mozilla scale version*/
    -o-transform: scale(0.43); /*Opera scale version*/
    scale: 0.43 !important;
    left: 216px !important;
    top: -297px !important;
  }

  #builder {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: reverse;
    -ms-flex-flow: column-reverse wrap;
    flex-flow: column-reverse wrap;
  }
  #frame_wrapper {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    -ms-flex-flow: column;
    flex-flow: column;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin-bottom: 25px;
    margin-top: 25px;
  }
}

@media screen and (max-width: 900px) {
  #frame {
    width: 295px !important;
    height: 404px !important;
  }
  svg {
    -webkit-transform: scale(
      0.37
    ); /*Webkit:Scale down image to 0.8x original size*/
    -moz-transform: scale(0.37); /*Mozilla scale version*/
    -o-transform: scale(0.37); /*Opera scale version*/
    scale: 1 !important;
    left: 240px !important;
    top: -328px !important;
  }

  #builder {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: reverse;
    -ms-flex-flow: column-reverse wrap;
    flex-flow: column-reverse wrap;
  }
  #frame_wrapper {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    -ms-flex-flow: column;
    flex-flow: column;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin-bottom: 25px;
    margin-top: 45px;
  }
}
</style>
