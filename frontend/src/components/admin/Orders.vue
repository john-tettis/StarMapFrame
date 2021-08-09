<template>
  <div>
    <v-row>
      <v-col>
        <v-row align="center" class="my-2">
          <v-col cols="8">
            <h2>لیست سفارشات</h2>
          </v-col>
          <v-col cols="4">
            <v-row align="center" justify="end">
              <v-col cols="4" xl="2" lg="2" md="2" sm="4">
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
              <v-col cols="4" xl="2" lg="2" md="2" sm="4">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      fab
                      small
                      v-on="on"
                      v-bind="attrs"
                      @click="multiPrint"
                      color="teal lighten-3"
                      class="white--text my-5 float-left"
                    >
                      <v-icon> mdi-printer </v-icon>
                    </v-btn>
                  </template>
                  <span>پرینت چندتایی</span>
                </v-tooltip>
              </v-col>
              <v-col cols="4" xl="2" lg="2" md="2" sm="4">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      fab
                      small
                      v-on="on"
                      v-bind="attrs"
                      @click="logout"
                      color="red darken-4"
                      class="white--text my-5 float-left"
                    >
                      <v-icon> mdi-logout-variant </v-icon>
                    </v-btn>
                  </template>
                  <span>خروج</span>
                </v-tooltip>
              </v-col>
            </v-row>
          </v-col>
        </v-row>

        <v-data-table
          v-model="selected"
          :headers="headers"
          :items="orders"
          :sort-by="['timestamp']"
          :sort-desc="[true]"
          :items-per-page="10"
          class="elevation-1"
          show-select
          :single-select="false"
        >
          <template v-slot:[`item.mobile`]="{ item }">
            <span>{{ toFarsiNumber(item.mobile) }}</span>
          </template>
          <template v-slot:[`item.post`]="{ item }">
            <span>{{ toFarsiNumber(item.post) }}</span>
          </template>
          <template v-slot:[`item.timestamp`]="{ item }">
            {{ convertUnixTimeIntoDate(item.timestamp) }}
          </template>
          <template v-slot:[`item.amount`]="{ item }">
            <span v-if="item.amount !== undefined">{{
              parseInt(item.amount).toLocaleString("fa")
            }}</span>
          </template>
          <template v-slot:[`item.is_paid`]="{ item }">
            <span v-if="parseInt(item.is_paid) === 0">پرداخت نشده</span>
            <span v-else>پرداخت شده</span>
          </template>
          <template v-slot:[`item.roban`]="{ item }">
            <span v-if="item.product.roban">دارد</span>
            <span v-else>ندارد</span>
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
          <template v-slot:[`item.data`]="{ item }">
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
                  @click="downloadInvoice(item)"
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
                  @click.stop="openDeleteOrderDialog(item.id)"
                >
                  <v-icon>mdi-delete-outline</v-icon>
                </v-btn>
              </template>
              <span>حذف سفارش</span>
            </v-tooltip>
          </template>
          <template v-slot:[`item.editItem`]="{ item }">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  v-bind="attrs"
                  v-on="on"
                  color="pink"
                  fab
                  dark
                  x-small
                  @click.stop="editOrder(item)"
                >
                  <v-icon>mdi-pencil-plus-outline</v-icon>
                </v-btn>
              </template>
              <span>ویرایش سفارش</span>
            </v-tooltip>
          </template>
          <template v-slot:[`item.is_printed`]="{ item }">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  @click="setAsPrinted(item.id, item.is_printed)"
                  fab
                  x-small
                  text
                  v-on="on"
                  v-bind="attrs"
                  color="green"
                >
                  <v-icon>mdi-file-find</v-icon>
                </v-btn>
              </template>
              <span v-if="item.is_printed === 1">پرینت شده</span>
              <span v-else>پرینت نشده</span>
            </v-tooltip>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
    <!---Delete Order Dialog-->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>حذف</v-card-title>
        <v-card-text>آیا از حذف کردن این سفارش مطمئن هستید؟</v-card-text>
        <v-card-actions>
          <v-btn color="red" class="white--text" @click="deleteOrder"
            >بله</v-btn
          >
          <v-btn color="gray" text @click="deleteDialog = false">خیر</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import moment from "moment-jalaali";

import cities from "@/assets/city.json";
import provinces from "@/assets/provinces.json";

export default {
  name: "AdminOrders",
  mounted() {
    this.getOrders();
  },
  data() {
    return {
      deleteDialog: false,
      orderID: null,
      selected: [],
      headers: [
        { text: "کد پیگیری", value: "tracking" },
        { text: "تاریخ", value: "timestamp" },
        { text: "مبلغ (ریال)", value: "amount" },
        { text: "نام و نام خانوادگی", value: "name" },
        { text: "موبایل", value: "mobile" },
        { text: "استان", value: "province" },
        { text: "شهر", value: "city" },
        { text: "کدپستی", value: "post" },
        { text: "آدرس کامل", value: "address" },
        { text: "وضعیت پرداخت", value: "is_paid" },
        { text: "ربان", value: "roban" },
        { text: "", value: "editItem", sortable: false, width: 1 },
        { text: "", value: "starmap", sortable: false, width: 1 },
        { text: "", value: "data", sortable: false, width: 1 },
        { text: "", value: "deleteItem", sortable: false, width: 1 },
        { text: "", value: "is_printed", sortable: false, width: 1 },
      ],
      orders: [],
    };
  },
  methods: {
    getOrders() {
      this.$emit("update:loading", true);
      this.axios
        .get("/api/orders", {
          headers: {
            token: this.$cookies.get("token"),
          },
        })
        .then((res) => {
          if (res.data.result) {
            this.orders = res.data.data;
            this.orders.forEach(async (elm) => {
              elm.city = cities.filter(
                (item) => item.id === parseInt(elm.city)
              )[0].name;
              elm.province = provinces.filter(
                (item) => item.id === parseInt(elm.province)
              )[0].name;
            });
          } else {
            alert("شما وارد حساب کاربری خود نشدید");
          }
          this.$emit("update:loading", false);
        });
    },
    openDeleteOrderDialog(id) {
      this.orderID = id;
      this.deleteDialog = true;
    },
    deleteOrder() {
      this.$emit("update:loading", true);
      this.axios
        .delete(`/api/orders/${this.orderID}`, {
          headers: {
            token: this.$cookies.get("token"),
          },
        })
        .then((res) => {
          if (res.status === 200 && res.data.result) {
            this.getOrders();
            this.orderID = null;
          } else {
            alert("توکن شما منقضی شده است...");
          }
          this.$emit("update:loading", false);

          this.deleteDialog = false;
        });
    },
    downloadStarmap(product) {
      this.$emit("update:loading", true);
      let star = product
        .replaceAll("True", "true")
        .replaceAll("False", "false")
        .replaceAll("'", '"');
      star = JSON.parse(star);
      const data = {
        ...star,
        MODE: "PROD",
      };
      this.axios.post("/api/starmap", data).then((res) => {
        this.$emit("update:loading", false);

        window.open(res.data.path);
      });
    },
    downloadInvoice(item) {
      window.open(
        `${process.env.VUE_APP_INVOICE_API}/invoice.php?name=${item.name}&mobile=${item.mobile}&city=${item.city}&province=${item.province}&address=${item.address}&post=${item.post}&tracking=${item.tracking}`
      );
    },
    multiPrint() {
      if (this.selected.length > 0) {
        let selectedItems = this.selected;
        selectedItems.forEach((item) => {
          delete item["product"];
        });

        selectedItems = JSON.stringify(selectedItems);
        console.log(selectedItems);
        window.open(
          `${process.env.VUE_APP_INVOICE_API}/invoice.php?items=${selectedItems}`
        );
      } else {
        alert("ابتدا باید موردی را انتخاب کنید...");
      }
    },
    editOrder(order) {
      let product = order.product
        .replaceAll("True", "true")
        .replaceAll("False", "false")
        .replaceAll("'", '"');
      product = JSON.parse(product);
      localStorage.setItem("orderID", order.id);
      localStorage.setItem("editMode", true);
      this.$store.commit("setProduct", product);
      this.$store.commit(
        "setImage",
        `${process.env.VUE_APP_BACKEND || "http://localhost:8000"}/download/${
          product.filename
        }`
      );
      //setTimeout(()=>{
      this.$router.push("/builder");
      //}, 1500)
    },
    setAsPrinted(id, status) {
      this.$emit("update:loading", true);
      let is_printed = 0;
      if (status === 0) {
        is_printed = 1;
      } else if (status === 1) {
        is_printed = 0;
      } else {
        is_printed = 0;
      }
      this.axios
        .post(
          `/api/orders/setPrinted/${id}`,
          { status: is_printed },
          {
            headers: {
              token: this.$cookies.get("token"),
            },
          }
        )
        .then((response) => {
          if (response.status === 200 && response.data.result) {
            alert("وضعیت پرینتر تغییر یافت...");
            this.getOrders();
          }
          this.$emit("update:loading", false);
        })
        .catch((error) => {
          console.log(error);
          this.$emit("update:loading", false);
        });
    },
    logout() {
      this.$cookies.remove("token");
      this.$router.push("/");
    },
    convertUnixTimeIntoDate(unix) {
      moment.locale("fa");
      return moment.unix(unix / 1000).format("jYYYY/jMM/jDD");
    },
    toFarsiNumber(n) {
      const farsiDigits = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];
      return n.toString().replace(/\d/g, (x) => farsiDigits[x]);
    },
  },
};
</script>
