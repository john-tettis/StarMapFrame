<template>
  <div>
    <v-row justify="center" class="py-5">
      <v-col cols="6">
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
              <v-btn color="primary" block>
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
  },
};
</script>
