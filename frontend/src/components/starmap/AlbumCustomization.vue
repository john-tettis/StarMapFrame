<template>
    <div>
        <v-form ref="form">
            <p>اندازه‌ی قاب:</p>
            <v-radio-group @change="updateStar" v-model="radioGroup">
                <v-radio key="A2" label="A2 (40*60 CM)" value="A2" />
                <v-radio key="A3" label="A3 (30*40 CM)" value="A3" />
                <v-radio key="A4" label="A4 (20*30 CM)" value="A4" />
                <v-radio key="A5" label="A5 (15*21 CM)" value="A5" />
            </v-radio-group>

            <p>رنگ قاب</p>
            <v-menu
                v-model="frameMenu"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="290px"
                max-width="290px"
            >
                <template v-slot:activator="{ on }">
                    <v-text-field
                        label="رنگ"
                        prepend-inner-icon="mdi-palette"
                        readonly
                        hide-details
                        :value="frameValue"
                        v-on="on"
                        outlined
                        dense
                        class="mb-7"
                    ></v-text-field>
                </template>

                <v-color-picker
                    show-swatches
                    hide-canvas
                    hide-sliders
                    hide-inputs
                    :swatches="swatches"
                    v-model="frameValue"
                    @input="updateStar"
                    no-title
                ></v-color-picker>
            </v-menu>

            <p>آیا ربان داشته باشد؟</p>
            <v-radio-group v-model="roban" @change="updateRoban">
                <v-radio key="بله" label="بله" :value="true" @click="roban = true" />
                <v-radio key="خیر" label="خیر" :value="false" @click="roban = false" />
            </v-radio-group>
        </v-form>

        <v-row no-gutters>
            <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
                <v-btn
                    @click="$emit('update:stepper', 4)"
                    color="error"
                    outlined
                    style="width:98%"
                >مرحله‌ی قبلی</v-btn>
            </v-col>
            <v-col cols="6" xl="6" lg="6" md="6" sm="6" class="d-flex justify-center">
                <v-btn
                    @click="$emit('update:stepper', 6)"
                    style="width:98%"
                    color="primary"
                >مرحله‌ی بعدی</v-btn>
            </v-col>
        </v-row>
    </div>
</template>

<script>
export default {
    name: "AlbumCustomization",
    data() {
        return {
            radioGroup: "A3",
            roban: true,
            swatches: [
                ["#000000", "#eeeeee"],
            ],
            frameMenu: false,
            frameValue: "#000000",
        }
    },
    methods: {
        updateStar() {
            this.$store.commit("setCustomize", {
                size: this.radioGroup,
                background: this.$store.state.starmap.customize.background,
                frame: this.frameValue,
                dot: this.$store.state.starmap.customize.dot,
                star: this.$store.state.starmap.customize.star,
                constellation: this.$store.state.starmap.customize.constellation,
                constellationText: this.$store.state.starmap.customize.constellationText,
                wallpaper: this.$store.state.starmap.customize.wallpaper,
            });
            this.$store.dispatch("getStarMap");
        },
        updateRoban() {
            this.$store.commit("setRoban", this.roban)
        }
    },
    mounted() {
        this.updateRoban();
        const editMode = localStorage.getItem("editMode");
        if (editMode) {
            this.radioGroup = this.$store.state.starmap.customize.size;
            this.frameValue = this.$store.state.starmap.customize.frame;
            this.roban = this.$store.state.starmap.roban;
        }
    }
}
</script>