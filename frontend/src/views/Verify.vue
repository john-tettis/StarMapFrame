<template>
  <div class="my-16">
    <v-row justify="center">
      <v-col cols="6">
        <v-card elevation="2">
          <v-card-title>
            وضعیت:
            <span v-show="parseInt(status) === 1"
              >پرداخت موفقیت آمیز بود.
              <v-icon color="green">mdi-check-decagram</v-icon></span
            >
            <span v-show="parseInt(status) === null"
              >نمی‌دونم چه اتفاقی افتاده</span
            >
          </v-card-title>
          <v-card-text>
            <div v-if="parseInt(status) === 1">
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
  props: {
    token: {
      type: String,
      default: null,
    },
    status: {
      type: String,
      default: null,
    },
  },
  methods: {
    getLocalToken() {
      const token = localStorage.getItem("payment_token");
      if (this.token === token) {
        return true;
      }
      return false;
    },
  },
  async created() {
    if (parseInt(this.status) === 1 && this.getLocalToken()) {
      const res = await this.axios.post("https://pay.ir/pg/verify", {
        api: "test",
        token: localStorage.getItem("payment_token"),
      });
      if (res.status === 200 && res.data.status === 1) {
        setTimeout(() => {
          this.$router.push("/");
        }, 60000);
      } else {
        alert("تراکنش ثبت نشد");
      }
    }
  },
};
</script>
