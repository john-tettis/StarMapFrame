<template>
  <v-row no-gutters class="py-16">
    <v-col cols="12" xl="7" lg="7" md="12" sm="12" class="px-10">
      <v-stepper alt-labels v-model="step">
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
            <StarMusic :stepper.sync="step" />
          </v-stepper-content>

          <v-stepper-content step="4">
            <StarCustomize :stepper.sync="step" />
          </v-stepper-content>

          <v-stepper-content step="5">
            <StarBackground :stepper.sync="step" />
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-col>
    <v-col cols="12" xl="5" lg="5" md="12" sm="12">
      <div
        id="frame"
        :style="'border:10px solid' + $store.state.starmap.customize.frame + '; height: 540px;width:400px;margin:25px auto;border-radius:1px'"
      >
        <inline-svg
          style="scale: 0.509; position: relative; top: -260px;left: 188px;direction:ltr;z-index:0"
          :src="$store.state.path"
        />
      </div>
    </v-col>
  </v-row>
</template>

<script>
import StarGeo from "@/components/starmap/Geo";
import StarText from "@/components/starmap/Text";
import StarMusic from "@/components/starmap/Music";
import StarCustomize from "@/components/starmap/Customize";
import StarBackground from "@/components/starmap/Background";

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
  },
  data() {
    return {
      step: 1,
      svgSource: this.$store.state.path,
    };
  },
};
</script>

<style></style>
