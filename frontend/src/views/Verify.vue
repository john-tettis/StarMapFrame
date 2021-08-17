<template>
  <div class="my-16">
    <v-row justify="center">
      <v-col cols="11" xl="4" lg="4" md="4" sm="11">
        <v-card elevation="2">
          <v-card-title>
            وضعیت:
            <span v-show="parseInt(status) === 1">
              پرداخت موفقیت آمیز بود.
              <v-icon color="green">mdi-check-decagram</v-icon>
            </span>
            <span v-show="parseInt(status) === null">نمی‌دونم چه اتفاقی افتاده</span>
          </v-card-title>
          <v-card-text>
            <div v-if="parseInt(status) === 1">
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
              <v-btn @click="$router.push('/')" color="primary" block>بازگشت به صفحه‌ی اصلی</v-btn>
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
      code: ""
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
      this.amount = parseInt(localStorage.getItem("payment_amount"))
    },
    async updateOrder() {
      const orderId = localStorage.getItem("orderId")
      if(orderId === null) return false

      const response = await this.axiost.put(`/api/orders/${orderId}`);
      if(response.status===200 && response.data.result){
        console.log("سفارش با موفقیت آپدیت شد")
        return true;
      }
      return false
    }
  },
  async created() {
    this.getTrackingCode();

    this.axios.post("https://api.payping.ir/v2/pay/verify", {
      amount: this.amount,
      refId: this.$route.query.refId
    }, {
      headers: {
        "Authorization": `Bearer 1bb94f23b92de83830e798e8a70087d2cccf45496ca92bf3e4d9b1f18f121d86`,
        'Content-Type': 'application/json'
      }
    }).then(async (response) => {
      if (response.status === 200 && response.data.amount === 0) {
        console.log("پرداخت موفقیت آمیز بود!")
        await this.updateOrder()
      }
    }).catch(error => {
      alert("پرداخت تایید نشد!")
      console.log(error)
    })
  },
};
</script>
