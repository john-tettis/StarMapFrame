<template>
  <div class="pa-5">
    <v-row>
      <v-col>
        <v-row align="center" class="my-2">
          <v-col cols="6">
            <h2>لیست سفارشات</h2>
          </v-col>
          <v-col cols="6">
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  @click="getOrders"
                  color="green"
                  class="white--text float-left"
                  fab
                  small
                  v-bind="attrs"
                  v-on="on"
                >
                  <v-icon>mdi-update</v-icon>
                </v-btn>
              </template>
              <span>بروزرسانی</span>
            </v-tooltip>
          </v-col>
        </v-row>

        <v-divider class="mb-5"></v-divider>
        <v-data-table
          :headers="headers"
          :items="orders"
          :items-per-page="5"
          class="elevation-1"
        >
          <template v-slot:[`item.amount`]="{ item }">
            <span v-if="item.amount !== undefined">{{
              parseInt(item.amount).toLocaleString()
            }}</span>
          </template>
          <template v-slot:[`item.is_paid`]="{ item }">
            <span v-if="parseInt(item.is_paid) === 0">پرداخت نشده</span>
            <span v-else>پرداخت شده</span>
          </template>
          <template v-slot:[`item.is_deliverd`]="{ item }">
            <span v-if="parseInt(item.is_deliverd) === 0">تحویل نشده</span>
            <span v-else>تحویل مشتری</span>
          </template>
          <template v-slot:[`item.starmap`]="{ item }">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  v-bind="attrs"
                  v-on="on"
                  color="primary"
                  fab
                  dark
                  x-small
                  outlined
                  @click="downloadStarmap(item.product)"
                >
                  <v-icon>mdi-map-plus</v-icon>
                </v-btn>
              </template>
              <span>دانلود نقشه‌ی ستار‌ه‌ای</span>
            </v-tooltip>
          </template>
          <template v-slot:[`item.data`]>
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  v-bind="attrs"
                  v-on="on"
                  color="pink"
                  fab
                  dark
                  x-small
                  outlined
                >
                  <v-icon>mdi-data-matrix</v-icon>
                </v-btn>
              </template>
              <span>دانلود دیتاهای این کاربر</span>
            </v-tooltip>
          </template>
          <template v-slot:[`item.deleteItem`]="{ item }">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  v-bind="attrs"
                  v-on="on"
                  color="pink"
                  fab
                  dark
                  x-small
                  text
                  @click.stop="deleteOrder(item.id)"
                >
                  <v-icon>mdi-delete-outline</v-icon>
                </v-btn>
              </template>
              <span>حذف سفارش</span>
            </v-tooltip>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
    <Loading :isLoading="loading" />
  </div>
</template>

<script>
import cities from "@/assets/city.json";
import provinces from "@/assets/provinces.json";
import Loading from "@/components/Loading";

export default {
  name: "AdminPanel",
  components: {
    Loading,
  },
  data() {
    return {
      loading: false,
      headers: [
        { text: "مبلغ (ریال)", value: "amount" },
        { text: "نام و نام خانوادگی", value: "name" },
        { text: "موبایل", value: "mobile" },
        { text: "استان", value: "province" },
        { text: "شهر", value: "city" },
        { text: "کدپستی", value: "post" },
        { text: "آدرس کامل", value: "address" },
        { text: "وضعیت پرداخت", value: "is_paid" },
        { text: "وضعیت تحویل", value: "is_deliverd" },
        { text: "", value: "starmap", sortable: false, width: 1 },
        { text: "", value: "data", sortable: false, width: 1 },
        { text: "", value: "deleteItem", sortable: false, width: 1 },
      ],
      orders: [],
    };
  },
  mounted() {
    this.getOrders();
  },
  methods: {
    getOrders() {
      this.loading = true;
      this.axios.get("/api/orders").then((res) => {
        this.orders = res.data.data;
        this.orders.forEach(async (elm) => {
          elm.city = cities.filter(
            (item) => item.id === parseInt(elm.city)
          )[0].name;
          elm.province = provinces.filter(
            (item) => item.id === parseInt(elm.province)
          )[0].name;
        });
        this.loading = false;
      });
    },
    deleteOrder(id) {
      this.loading = true;
      this.axios.delete(`/api/orders/${id}`).then((res) => {
        if (res.status === 200) {
          this.getOrders();
        }
        this.loading = false;
      });
    },
    downloadStarmap(product) {
      this.loading = true;
      let star = product
        .replaceAll("True", "true")
        .replaceAll("False", "false")
        .replaceAll("'", '"');
      star = JSON.parse(star);
      this.axios.post("/api/starmap", star).then((res) => {
        this.loading = false;
        window.open(res.data.path);
      });
    },
  },
};
</script>
