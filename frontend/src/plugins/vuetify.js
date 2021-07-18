import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import fa from 'vuetify/lib/locale/fa';

Vue.use(Vuetify);

export default new Vuetify({
    lang:{
        locales: { fa },
        current: 'fa',
    },
    rtl: true,
    defaultAssets: false,
});
