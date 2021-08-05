<template>
  <div>
    <v-row v-if="accept" justify="center" class="py-5">
      <v-col cols="11" xl="5" lg="5" md="5" sm="11">
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
    <v-row justify="center" class="py-5" v-if="!accept">
      <v-col cols="11" xl="5" lg="5" md="5" sm="11">
        <v-card>
          <v-card-title>فاکتور شما به شرح زیر است</v-card-title>
          <v-card-text>
            <p>
              <span style="font-weight:bold">مبلغ قابل پرداخت: </span
              >{{ amount.toLocaleString("fa") }} ریال
            </p>
            <p>
              <span style="font-weight: bold">سایز قاب: </span
              >{{ product.customize.size }}
            </p>
            <p>
              <span style="font-weight: bold">کد موزیک: </span>
              {{ product.music.qr ? 'دارد' : 'ندارد' }}
            </p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" block outlined @click="accept=true">تایید</v-btn>
          </v-card-actions>
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
      accept: false,
      payment: {
        name: "",
        mobile: "",
        address: "",
        province: "",
        city: "",
        post: "",
      },
      amount: 0,
      product: {},
      provincesList: [],
      citiesList: [],
    };
  },
  mounted() {
    this.product = JSON.parse(localStorage.getItem("product"))
    if (this.product.customize.size === "A2") this.amount = 3500000;
    if (this.product.customize.size === "A3") this.amount = 2800000;
    if (this.product.customize.size === "A4") this.amount = 2000000;
    if (this.product.customize.size === "A5") this.amount = 1600000;
    if (this.product.music.qr) this.amount += 150000;
    if (this.product.background.bg) this.amount += 150000;

    this.provincesList = provinces;
    this.citiesList = cities;
  },
  methods: {
    filterCity() {
      this.citiesList = cities;
      this.citiesList = this.citiesList.filter(
        (item) => this.payment.province === item.province_id
      );
    },
    addOrder() {
      let tracking = Math.random()
        .toString(36)
        .substring(7);
      localStorage.setItem("tracking", tracking);
      const data = {
        product: this.product,
        name: this.payment.name,
        mobile: this.payment.mobile,
        address: this.payment.address,
        province: this.payment.province,
        city: this.payment.city,
        post: this.payment.post,
        amount: this.amount,
        is_paid: 0,
        is_deliverd: 0,
        tracking: tracking,
        timestamp: Date.now(),
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
              amount: this.amount,
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
