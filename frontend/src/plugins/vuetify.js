import Vue from 'vue';
import Vuetify, {
    VLayout, VStepper, VAppBar, VMain, VApp, VRow, VCol, VFileInput, VSelect, VTextField, VForm, VColorPicker, VDivider, VMenu
    , VOverlay, VProgressCircular, VBtn, VRadio, VRadioGroup, VSlider, VContainer, VSwitch, VDataTable, VDialog, VCard, VCardTitle, VCardActions, VCardText, VTooltip, VStepperContent, VStepperItems
} from 'vuetify/lib';
import fa from 'vuetify/lib/locale/fa';

Vue.use(Vuetify, {
    components: {
        VAppBar,
        VLayout,
        VStepper,
        VStepperContent,
        VStepperItems,
        VMain,
        VApp,
        VRow,
        VCol,
        VFileInput,
        VTextField,
        VSelect,
        VForm,
        VColorPicker,
        VDivider,
        VMenu,
        VOverlay,
        VProgressCircular,
        VBtn,
        VRadio,
        VRadioGroup,
        VSlider,
        VContainer,
        VSwitch,
        VDataTable,
        VDialog,
        VCard,
        VCardTitle,
        VCardActions,
        VCardText,
        VTooltip
    }
});

export default new Vuetify({
    lang: {
        locales: { fa },
        current: 'fa',
    },
    rtl: true,
    defaultAssets: false,
});
