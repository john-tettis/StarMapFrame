<template>
  <div>
    <v-row class="mt-5 border-1" justify="center">
      <v-col cols="11" xl="5" lg="5" md="5" sm="11">
        <v-card class="elevation-4">
          <v-card-text>
            <h3 class="mb-5 p-title">
              <v-icon>mdi-basket</v-icon>فاکتور سفارش
            </h3>
            <div class="remove-p-m">
              <p class="d-flex justify-space-between">
                ساخت آسمان + قاب:
                <span>
                  {{ product.customize.size }} -
                  {{ sizePriceCal().toLocaleString("fa") }}
                </span>
              </p>
              <p class="d-flex justify-space-between">
                بارکد موسیقی:
                <span>{{
                  !!product.music.qr ? " ۲۰,۰۰۰ تومان" : "ندارد"
                }}</span>
              </p>
              <p class="d-flex justify-space-between">
                بکگراند ستاره:
                <span>{{
                  !!product.background.bg ? "۱۵,۰۰۰ تومان" : "ندارد"
                }}</span>
              </p>
              <p class="d-flex justify-space-between">
                ربان:
                <span>{{ product.roban ? "۱۵,۰۰۰ تومان" : "ندارد" }}</span>
              </p>
              <v-divider class="my-2" />
              <p class="d-flex justify-space-between">
                مبلغ کل:
                <span v-if="amount !== undefined"
                  >{{ amount.toLocaleString("fa") }} تومان</span
                >
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
                    >ثبت</v-btn
                  >
                </div>
              </div>
              <h3
                class="text-center text-lg"
                v-show="discount"
                v-if="discountAmount !== undefined"
              >
                مبلغ {{ discountAmount.toLocaleString("fa") }} تومان تخفیف اعمال
                شد.
              </h3>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center" class="pb-5 mt-1">
      <v-col cols="11" xl="5" lg="5" md="5" sm="11">
        <v-card elevation="2">
          <v-card-text>
            <h2 class="mb-5 p-title">
              <v-icon>mdi-post</v-icon>مشخصات گیرنده
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
                maxlength="11"
              />
              <v-select
                :items="provincesList"
                v-model="payment.province"
                item-text="title"
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
                item-text="title"
                item-value="id"
                required
                outlined
                dense
                label="شهر"
                @input="$v.payment.city.$touch()"
                @blur="$v.payment.city.$touch()"
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
              <v-text-field
                v-model="payment.post"
                required
                outlined
                dense
                label="کدپستی (اختیاری)"
                @input="$v.payment.post.$touch()"
                @blur="$v.payment.post.$touch()"
                maxlength="10"
              />
              <v-btn
              id="submitOrder"
                @click="addOrder"
                color="primary"
                :disabled="
                  $v.payment.name.$invalid ||
                  $v.payment.mobile.$invalid ||
                  $v.payment.address.$invalid ||
                  $v.payment.province.$invalid ||
                  $v.payment.city.$invalid ||
                  $v.payment.post.$invalid
                "
                block
                >پرداخت سفارش</v-btn
              >
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import provinces from "@/assets/province.json";
import cities from "@/assets/cities.json";

import { validationMixin } from "vuelidate";
import { required, numeric, maxLength } from "vuelidate/lib/validators";

export default {
  name: "Pay",
  mixins: [validationMixin],
  validations: {
    payment: {
      name: {
        required,
      },
      mobile: {
        required,
        numeric,
        maxLength: maxLength(11),
      },
      post: {
        numeric,
        maxLength: maxLength(10),
      },
      address: {
        required,
      },
      city: {
        required,
      },
      province: {
        required,
      },
    },
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
      product: JSON.parse(localStorage.getItem("product")),
      provincesList: [],
      citiesList: [],
      code: "",

      is_submited: false,
      orderId: null,
    };
  },
  mounted() {
    history.pushState(null, null, location.href);
    window.onpopstate = function () {
      history.go(1);
    };

    this.product = JSON.parse(localStorage.getItem("product"));
    if (this.product.customize.size === "A2") this.amount = 450000;
    if (this.product.customize.size === "A3") this.amount = 300000;
    if (this.product.customize.size === "A4") this.amount = 260000;
    if (this.product.customize.size === "A5") this.amount = 190000;
    if (this.product.music.qr) this.amount += 20000;
    if (this.product.background.bg) this.amount += 15000;
    if (this.product.roban) this.amount += 15000;

    this.provincesList = provinces;
    this.citiesList = cities;
  },
  methods: {
    sizePriceCal() {
      if (this.product.customize.size === "A2") return 450000;
      if (this.product.customize.size === "A3") return 300000;
      if (this.product.customize.size === "A4") return 260000;
      if (this.product.customize.size === "A5") return 190000;
    },
    filterCity() {
      this.citiesList = cities;
      this.citiesList = this.citiesList.filter(
        (item) => this.payment.province === item.province_id
      );
    },
    generateTrackingCode() {
      return Math.random().toString(36).substring(7);
    },
    setOrderData(tracking) {
      return {
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
    },
    async addOrder() {
      const orderButton = document.getElementById("submitOrder");
      orderButton.disabled = true;
      
      if (this.is_submited) {
        await this.goToPay(this.orderId);
        return;
      }
      // Generate Tracking code and set it to localestorage
      const tracking = this.generateTrackingCode();
      localStorage.setItem("tracking", tracking)

      // Build order data schema as json and post it
      const data = this.setOrderData(tracking);
      this.axios
        .post("/api/orders", data)
        .then(async (response) => {
          if (response.status === 200 && response.data.result) {
            this.is_submited = true;
            this.orderId = response.data.id;
            
            await this.goToPay(this.orderId);
          }
        })
        .catch((error) => {
          console.log(error);
          alert("خطایی پیش آمده است. لطفا مجددا تلاش کنید...");
        });
    },
    async goToPay(id) {
     const response = await this.axios.post(`/api/orders/pay/${id}/${this.amount}/${this.payment.mobile}/${this.payment.name}`);
     if(response.status === 200 && response.data.result){
       window.location.replace(response.data.url)
     }
    },
    percentage(num, per) {
      return Math.round((num / 100) * per);
    },
    checkDiscount() {
      this.code = this.code.toLowerCase();
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

<style>
.remove-p-m p {
  margin: 0 !important;
}
</style>
