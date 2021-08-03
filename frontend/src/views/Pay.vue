<template>
  <div>
    <v-row justify="center" class="py-5">
      <v-col cols="11" xl="4" lg="4" md="4" sm="11">
        <v-card elevation="2">
          <v-card-title>ثبت سفارش</v-card-title>
          <v-card-text>
            <v-divider class="mb-5"></v-divider>
            <v-form>
              <v-text-field
                v-model="payment.name"
                required
                outlined
                dense
                label="نام و نام خانوادگی"
              />
              <v-text-field
                v-model="payment.mobile"
                required
                outlined
                dense
                label="شماره موبایل"
              />
              <v-text-field
                v-model="payment.address"
                required
                outlined
                dense
                label="آدرس"
              />
              <v-select
                :items="provincesList"
                v-model="payment.province"
                item-text="name"
                item-value="id"
                required
                outlined
                dense
                label="استان"
                @change="filterCity"
              />
              <v-select
                :disabled="payment.province === null || payment.province === ''"
                :items="citiesList"
                v-model="payment.city"
                item-text="name"
                item-value="id"
                required
                outlined
                dense
                label="شهر"
              />
              <v-text-field
                v-model="payment.post"
                required
                outlined
                dense
                label="کدپستی"
              />
              <v-btn @click="addOrder" color="primary" block>
                ارسال به درگاه پرداخت
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import provinces from "@/assets/provinces.json";
import cities from "@/assets/city.json";

export default {
  name: "Pay",
  data() {
    return {
      payment: {
        name: "",
        mobile: "",
        address: "",
        province: "",
        city: "",
        post: "",
      },
      provincesList: [],
      citiesList: [],
    };
  },
  mounted() {
    this.provincesList = provinces;
    this.citiesList = cities;
  },
  methods: {
    filterCity() {
      this.citiesList = this.citiesList.filter(
        (item) => this.payment.province === item.province_id
      );
    },
    addOrder() {
      let tracking = Math.random()
        .toString(36)
        .substring(7);
      localStorage.setItem("tracking", tracking);

      const product = JSON.parse(localStorage.getItem("product"));
      let amount = 0;
      if (product.customize.size === "A1") amount = 3600000;
      if (product.customize.size === "A2") amount = 3500000;
      if (product.customize.size === "A3") amount = 2800000;
      if (product.customize.size === "A4") amount = 2000000;
      if (product.customize.size === "A5") amount = 1600000;
      if (product.music.qr) amount += 150000;
      if (product.background.bg) amount += 150000;

      const data = {
        product: product,
        name: this.payment.name,
        mobile: this.payment.mobile,
        address: this.payment.address,
        province: this.payment.province,
        city: this.payment.city,
        post: this.payment.post,
        amount: amount,
        is_paid: 0,
        is_deliverd: 0,
        tracking: tracking,
        timestamp: Date.now()
      };
      this.axios
        .post("http://localhost:5000/orders", data)
        .then(async (response) => {
          if (response.status === 200 && response.data.result) {
            localStorage.setItem("orderId", response.data.id);
            const API = process.env.VUE_APP_PAYIR_API || "test";
            const redirect = "http://localhost:8080/verify";
            const res = await this.axios.post("https://pay.ir/pg/send ", {
              api: API,
              amount: amount,
              redirect: redirect,
            });
            if (res.data.status === 1) {
              const token = res.data.token;
              localStorage.setItem("payment_token", token);
              window.location.replace(`https://pay.ir/pg/${token}`);
            }
          }
        })
        .catch((error) => {
          console.log(error);
          alert("خطایی پیش آمده است. لطفا مجددا تلاش کنید...");
        });
    },
  },
};
</script>
