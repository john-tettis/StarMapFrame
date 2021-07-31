<template>
  <div class="bg-dark bg-wallpaper fill-height pt-16">
    <v-row justify="center" class="pt-16 pb-16">
      <v-col cols="11" xl="4" lg="4" md="4" sm="11">
        <v-card elevation="2">
          <v-card-text>
            <img src="@/assets/logo.png" width="120" class="d-block mx-auto" />
            <v-form v-show="form === 'login'">
              <v-alert
                v-show="loginAlert"
                dark
                color="deep-purple accent-4"
                class="white--text"
                icon="mdi-sticker-emoji"
                dense
                type="warning"
              >
                {{ loginAlertText }}
              </v-alert>
              <v-text-field
                v-model="login.username"
                outlined
                dense
                label="نام کاربری"
              ></v-text-field>
              <v-text-field
                v-model="login.password"
                type="password"
                outlined
                dense
                label="رمزعبور"
              ></v-text-field>
              <v-row class="mb-3">
                <v-col>
                  <v-btn @click="doLogin" color="primary" class="float-left"
                    >ورود</v-btn
                  >
                </v-col>
              </v-row>
            </v-form>
            <v-form v-show="form === 'signup'">
              <v-alert
                v-show="registerAlert"
                dark
                color="deep-purple accent-4"
                class="white--text"
                icon="mdi-sticker-emoji"
                dense
                type="warning"
              >
                {{ registerAlertText }}
              </v-alert>
              <v-text-field
                v-model="register.name"
                outlined
                dense
                label="نام"
              ></v-text-field>
              <v-text-field
                v-model="register.username"
                outlined
                dense
                label="نام کاربری"
              ></v-text-field>
              <v-text-field
                v-model="register.password"
                type="password"
                outlined
                dense
                label="رمزعبور"
              ></v-text-field>
              <v-row class="mb-3">
                <v-col>
                  <v-btn @click="doRegister" color="primary" class="float-left"
                    >ثبت نام</v-btn
                  >
                </v-col>
              </v-row>
            </v-form>
            <span v-show="form === 'login'"
              >اکانت ندارید؟
              <a @click="form = 'signup'">همین حالا ثبت نام کنید...</a></span
            >
            <span v-show="form === 'signup'"
              >حساب کاربری دارید؟
              <a @click="form = 'login'">وارد حساب کاربری خود شوید...</a></span
            >
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "login",
  data() {
    return {
      registerAlert: false,
      registerAlertText: "",
      loginAlert: false,
      loginAlertText: "",
      form: "login",
      login: {
        username: "",
        password: "",
      },
      register: {
        name: "",
        username: "",
        password: "",
      },
    };
  },
  methods: {
    doRegister() {
      // this.axios.post("/api/register", this.register).then((response) => {
      //   if (response.status === 200 && response.data.result) {
      //     this.$router.push("/builder");
      //   } else {
      //     this.registerAlert = true;
      //     this.registerAlertText = response.data.message;
      //     setTimeout(() => {
      //       this.registerAlert = false;
      //     }, 5000);
      //   }
      // });
      alert("ثبت نام غیر فعال است");
    },
    doLogin() {
      this.axios.post("/api/login", this.login).then((response) => {
        if (response.status === 200 && response.data.result) {
          this.$cookies.set('token', response.data.token, "1D");
          this.$router.push("/admin");
        } else {
          this.loginAlert = true;
          this.loginAlertText = response.data.message;
          setTimeout(() => {
            this.loginAlert = false;
          }, 5000);
        }
      });
    },
  },
};
</script>

<style scoped>
.bg-wallpaper {
  background-image: url("../assets/sky.jpg");
  min-height: 700px;
  height: 100vh;
}
</style>
