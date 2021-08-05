<template>
  <div>
    <h2>کد‌های تخفیف</h2>
    <v-row justify="center">
      <v-col cols="5">
        <v-card>
          <v-card-title>افزودن کد تخفیف</v-card-title>
          <v-card-text>
            <v-text-field
              v-model="code"
              outlined
              dense
              label="کد تخفیف"
            ></v-text-field>
            <v-text-field
              v-model="amount"
              outlined
              dense
              label="درصد تخفیف"
            ></v-text-field>
            <v-btn @click="addDiscount" block color="primary" outlined
              >افزودن</v-btn
            >
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="7">
        <v-data-table :headers="headers" :items="discounts" class="elevation-1">
          <template v-slot:[`item.amount`]="{ item }">
            <span>{{ parseInt(item.amount).toLocaleString("fa") }} %</span>
          </template>
          <template v-slot:[`item.delete`]="{ item }">
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  fab
                  x-small
                  text
                  v-on="on"
                  v-bind="attrs"
                  color="red"
                  @click="openDeleteDialog(item.id)"
                >
                  <v-icon x-small>mdi-delete</v-icon>
                </v-btn>
              </template>
              <span>حذف</span>
            </v-tooltip>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
    <v-dialog v-model="deleteDiscountDialog" max-width="400">
      <v-card>
        <v-card-title>حذف تخفیف</v-card-title>
        <v-card-text>
          آیا از حذف این تخفیف مطمئن هستید؟
        </v-card-text>
        <v-card-actions>
          <v-btn color="red" class="white--text" @click="deleteDiscount"
            >حذف</v-btn
          >
          <v-btn color="dark" text @click="deleteDiscountDialog = false">لغو</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: "AdminDiscounts",
  data() {
    return {
      deleteDiscountDialog: false,
      discountID: null,
      code: "",
      amount: "",
      discounts: [],
      headers: [
        { text: "کد تخفیف", value: "code" },
        { text: "درصد تخفیف", value: "amount" },
        { text: "", value: "delete" },
      ],
    };
  },
  mounted() {
    this.getDiscounts();
  },
  methods: {
    addDiscount() {
      this.$emit('update:loading', true);
      if(this.code===null){
        alert("کد تخفیف نباید خالی باشد!")
        return;
      }
      if(this.amount===null){
        alert("درصد تخفیف نباید خالی باشد");
        return;
      }

      this.axios.post("/api/discounts", {
        code: this.code, amount: this.amount
      }).then(response=>{
        if(response.status === 200 && response.data.result){
          alert("کد تخفیف جدید اضافه شد...");
          this.getDiscounts();
        }
        this.$emit('update:loading', false);
      })
    },
    getDiscounts() {
      this.axios.get("/api/discounts").then((response) => {
        if (response.status === 200 && response.data.result) {
          this.discounts = response.data.discounts;
        }
      });
    },
    openDeleteDialog(id){
      this.deleteDiscountDialog = true;
      this.discountID = id
    },
    deleteDiscount(){
      this.$emit('update:loading', true);
      this.axios.delete(`/api/discounts/${this.discountID}`).then(response=>{
        if(response.status === 200 && response.data.result){
          alert("با موفقیت حذف شد!")
          this.getDiscounts();
        }
        this.$emit('update:loading', false);
        this.deleteDiscountDialog = false
      }).catch(error=>{
        console.log(error);
        this.$emit('update:loading', false);
      })
    }
  },
};
</script>
