<template>
  <div class="my-16">
    <v-row justify="center">
      <v-col cols="11" xl="4" lg="4" md="4" sm="11">
        <v-card elevation="2">
          <v-card-title>
            وضعیت:
            <span v-if="$route.query.status">
              پرداخت موفقیت آمیز بود.
              <v-icon color="green">mdi-check-decagram</v-icon>
            </span>
            <span v-else>نمی‌دونم چه اتفاقی افتاده</span>
          </v-card-title>
          <v-card-text>
            <div v-if="$route.query.status">
              <b>
                <span>کد پیگیری {{ tracking }}</span>
              </b>
              <br />
              پرداخت شما ثبت و تایید شد. لطفا منتظر بسته‌ی پستی درب منزل خود
              باشید :)
              <v-divider class="my-5"></v-divider>
              <p>
                از این که رسپینا را برای خرید انتخاب کردید سپاس گذاریم. سفارش
                شما در حال پردازش و تایید است. پس از گذشت ۲ تا ۳ روز کاری بسته‌ی
                شما تحویل پست می‌شود و کد رهگیری مرسوله‌ی پستی شما به شماره تماس
                شما ارسال می گردد.
              </p>
              <v-btn @click="$router.push('/')" color="primary" block
                >بازگشت به صفحه‌ی اصلی</v-btn
              >
            </div>
            <div v-else>
              در این بین خطایی رخ داده است. مبلغ در ۷۲ ساعت آینده به حساب شما
              باز می گردد. لطفا برای خرید دوباره تلاش کنید و مطمین شوید که VPN
              خود را غیر فعال کرده باشید.
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "verify",
  data() {
    return {
      tracking: "",
      amount: 0,
      code: "",
    };
  },
  methods: {
    getLocalToken() {
      const token = localStorage.getItem("payment_code");
      if (this.token === token) {
        return true;
      }
      return false;
    },
    getTrackingCode() {
      this.tracking = localStorage.getItem("tracking");
      this.code = localStorage.getItem("payment_code");
      this.amount = parseInt(localStorage.getItem("payment_amount"));
    },
  },
  async created() {
    this.getTrackingCode();

    if (!!this.$route.query.status && !!this.$route.query.updated) {
      alert("سفارش با موفقیت تایید شد....");
    } else {
      alert("پرداخت شما تایید نشد لطفا کد پیگیری بانک را نگهداری کنید...");
    }
  },
};
</script>
