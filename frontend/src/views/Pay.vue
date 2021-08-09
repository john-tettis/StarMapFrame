<template>
  <div>
    <v-row class="mt-5 border-1" justify="center">
      <v-col cols="11" xl="5" lg="5" md="5" sm="11">
        <v-card class="elevation-4">
          <v-card-text>
            <h3 class="mb-5" style="font-size:1.3rem">
              جزییات سفارش
              <v-icon>mdi-basket</v-icon>
            </h3>
            <div>
              <p class="d-flex justify-space-between">
                قیمت قاب:
                <span>
                  {{ product.customize.size }} -
                  {{ sizePriceCal().toLocaleString("fa") }}
                </span>
              </p>
              <p class="d-flex justify-space-between">
                قیمت کد موزیک:
                <span>{{ !!product.music.qr ? " ۱۵,۰۰۰ ریال" : "ندارد" }}</span>
              </p>
              <p class="d-flex justify-space-between">
                قیمت بکگراند:
                <span>{{ !!product.background.bg ? "۱۵,۰۰۰ ریال" : "ندارد" }}</span>
              </p>
              <p class="d-flex justify-space-between">
                قیمت ربان:
                <span>{{product.roban ? "۱۵,۰۰۰ ریال" : "ندارد"}}</span>
              </p>
              <p class="d-flex justify-space-between">
                مبلغ کل:
                <span>{{ amount.toLocaleString("fa") }} ریال</span>
              </p>
              <div class="d-flex justify-space-between align-baseline">
                <div>
                  <p>کد تخفیف دارید:</p>
                </div>
                <div class="d-flex justify-space-between align-center">
                  <v-text-field v-model="code" label="کد تخفیف"></v-text-field>
                  <v-btn
                    @click="checkDiscount"
                    small
                    class="mr-1"
                    color="secondary"
                    outlined
                    :disabled="discount"
                  >ثبت</v-btn>
                </div>
              </div>
              <h3
                class="text-center"
                v-show="discount"
                style="font-size:1rem"
              >این کد شامل {{ discountAmount.toLocaleString("fa") }} ریال تخفیف است!</h3>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center" class="pb-5 mt-1">
      <v-col cols="11" xl="5" lg="5" md="5" sm="11">
        <v-card elevation="2">
          <v-card-text>
            <h2 class="mb-5" style="font-size:1.3rem">
              مشخصات گیرنده
              <v-icon>mdi-post</v-icon>
            </h2>
            <p>فیلد شماره موبایل و کد پستی را با اعداد انگلیسی پر کنید!</p>
            <v-divider class="mb-5"></v-divider>
            <v-form>
              <v-text-field
                v-model="payment.name"
                required
                outlined
                dense
                label="نام و نام خانوادگی"
                @input="$v.payment.name.$touch()"
                @blur="$v.payment.name.$touch()"
              />
              <v-text-field
                v-model="payment.mobile"
                required
                outlined
                dense
                label="شماره موبایل"
                @input="$v.payment.mobile.$touch()"
                @blur="$v.payment.mobile.$touch()"
              />
              <v-text-field
                v-model="payment.address"
                required
                outlined
                dense
                label="آدرس"
                @input="$v.payment.address.$touch()"
                @blur="$v.payment.address.$touch()"
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
                @input="$v.payment.province.$touch()"
                @blur="$v.payment.province.$touch()"
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
                @input="$v.payment.city.$touch()"
                @blur="$v.payment.city.$touch()"
              />
              <v-text-field
                v-model="payment.post"
                required
                outlined
                dense
                label="کدپستی"
                @input="$v.payment.post.$touch()"
                @blur="$v.payment.post.$touch()"
              />
              <v-btn
                @click="addOrder"
                color="primary"
                :disabled="$v.payment.name.$invalid || 
                $v.payment.mobile.$invalid || 
                $v.payment.address.$invalid ||
                $v.payment.province.$invalid ||
                $v.payment.city.$invalid ||
                $v.payment.post.$invalid"
                block
              >ارسال به درگاه پرداخت</v-btn>
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

import { validationMixin } from 'vuelidate';
import { required, numeric } from "vuelidate/lib/validators"

export default {
  name: "Pay",
  mixins: [validationMixin],
  validations: {
    payment:{
      name: {
        required
      },
      mobile: {
        required,
        numeric
      },
      post: {
        numeric,
        required
      },
      address:{
        required
      },
      city: {
        required
      },
      province: {
        required
      }
    }
  },
  data() {
    return {
      discount: false,
      discountAmount: 0,
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
      code: "",
    };
  },
  mounted() {
    this.product = JSON.parse(localStorage.getItem("product"));
    if (this.product.customize.size === "A2") this.amount = 3500000;
    if (this.product.customize.size === "A3") this.amount = 2800000;
    if (this.product.customize.size === "A4") this.amount = 2000000;
    if (this.product.customize.size === "A5") this.amount = 1600000;
    if (this.product.music.qr) this.amount += 150000;
    if (this.product.background.bg) this.amount += 150000;
    if (this.product.roban) this.amount += 150000;

    this.provincesList = provinces;
    this.citiesList = cities;
  },
  methods: {
    sizePriceCal() {
      if (this.product.customize.size === "A2") return 3500000;
      if (this.product.customize.size === "A3") return 2800000;
      if (this.product.customize.size === "A4") return 2000000;
      if (this.product.customize.size === "A5") return 1600000;
    },
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
        .post("/api/orders", data)
        .then(async (response) => {
          if (response.status === 200 && response.data.result) {
            localStorage.setItem("orderId", response.data.id);
            const API = process.env.VUE_APP_PAYIR_API || "test";
            const redirect = "http://sky.respina.store/verify";
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
    percentage(num, per) {
      return Math.round((num / 100) * per);
    },
    checkDiscount() {
      this.axios.post(`/api/discounts/${this.code}`).then((response) => {
        if (response.status === 200 && response.data.result) {
          if (response.data.discount === null) {
            alert("این کد تخفیف وجود ندارد...");
            return;
          }
          this.discountAmount = this.percentage(
            this.amount,
            response.data.discount[2]
          );
          this.amount -= this.discountAmount;
          this.discount = true;
        }
      });
    },
  },
};
</script>
