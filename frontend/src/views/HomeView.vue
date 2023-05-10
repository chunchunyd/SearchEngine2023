<template>
  <div class="home">
    <!--下面是顶部菜单栏-->
    <div class="container-fluid">
      <div class="row bg-secondary py-2 px-lg-5">
        <div class="col-lg-6 text-center text-lg-left mb-2 mb-lg-0">
          <div class="d-inline-flex align-items-center">
            <a class="px-3"><router-link to="/">Home</router-link></a>
            <span class="text-white">|</span>
            <a class="px-3"><router-link to="/about">About</router-link></a>
          </div>
        </div>
        <div class="col-lg-6 text-center text-lg-right">
          <div class="d-inline-flex align-items-center">
            <label class="text-white px-3">Welcome, Dear Engineer</label>
          </div>
        </div>
      </div>
    </div>
    <!--顶部菜单栏结束-->
    <!-- 下面是首页图片展示框 -->
    <div class="container-fluid p-0">
      <div id="header-carousel" class="carousel slide" data-ride="carousel">
        <div class="carousel-inner">
          <div class="carousel-item active">
            <img class="w-100" src="../../public/water2.jpg" alt="Image" />
            <div
              class="carousel-caption d-flex flex-column align-items-center justify-content-center"
            >
              <div class="p-3" style="max-width: 900px">
                <h3 class="text-white mb-3 d-none d-sm-block">
                  Best Project Manager
                </h3>
                <h1 class="display-3 text-white mb-3">Team Liquid</h1>
                <h5 class="text-white mb-3 d-none d-sm-block">
                  welcome！
                </h5>
                <a class="btn btn-lg btn-primary mt-3 mt-md-4 px-4"
                  ><a v-on:click="login">Login Now</a></a
                >
                <a class="btn btn-lg btn-secondary mt-3 mt-md-4 px-4"
                  ><a v-on:click="reg">Register Now</a></a
                >
              </div>
            </div>
          </div>
          <div class="carousel-item">
            <img class="w-100" src="../../public/water3.jpg" alt="Image" />
            <div
              class="carousel-caption d-flex flex-column align-items-center justify-content-center"
            >
              <div class="p-3" style="max-width: 900px">
                <h3 class="text-white mb-3 d-none d-sm-block">
                  Best Demand Manager
                </h3>
                <h1 class="display-3 text-white mb-3">Team Liquid</h1>
                <h5 class="text-white mb-3 d-none d-sm-block">
                  this page is still developing
                </h5>
                <a class="btn btn-lg btn-primary mt-3 mt-md-4 px-4"
                  ><a v-on:click="login">Login Now</a></a
                >
                <a class="btn btn-lg btn-secondary mt-3 mt-md-4 px-4"
                  ><a v-on:click="reg">Register Now</a></a
                >
              </div>
            </div>
          </div>
        </div>
        <a
          class="carousel-control-prev"
          href="#header-carousel"
          data-slide="prev"
        >
          <div
            class="btn btn-primary rounded"
            style="width: 45px; height: 45px"
          >
            <span class="carousel-control-prev-icon mb-n2"></span>
          </div>
        </a>
        <a
          class="carousel-control-next"
          href="#header-carousel"
          data-slide="next"
        >
          <div
            class="btn btn-primary rounded"
            style="width: 45px; height: 45px"
          >
            <span class="carousel-control-next-icon mb-n2"></span>
          </div>
        </a>
      </div>
    </div>
    <!-- 首页图片展示框结束 -->

    <LoginDialog
      :login_cancel="login_cancel"
      :login_post="login_post"
      :dialogVisible="login_dialogVisible"
      :dialogError="login_dialogError"
    ></LoginDialog>
    <RegisterDialog
      :reg_cancel="reg_cancel"
      :dialogVisible="reg_dialogVisible"
      :dialogError="reg_dialogError"
    ></RegisterDialog>
  </div>
</template>

<script>
import LoginDialog from '@/components/user/LoginDialog.vue'
import RegisterDialog from '@/components/user/RegisterDialog.vue'
import { getuserid } from '@/utils/com_user.js'
import CookieOperation from '@/utils/tools'

export default {
  name: 'HomeView',
  components: {
    LoginDialog,
    RegisterDialog
  },
  data() {
    return {
      login_dialogVisible: false,
      login_dialogError: '',
      reg_dialogVisible: false,
      reg_dialogError: ''
    }
  },
  mounted() {
    CookieOperation.setCookie('token', 0, 0)
    CookieOperation.setCookie('userid', 0, 0)
    CookieOperation.setCookie('username', 0, 0)
    CookieOperation.setCookie('projid', 0, 0)
  },
  methods: {
    login() {
      this.login_dialogVisible = true
    },
    reg() {
      this.reg_dialogVisible = true
    },
    login_cancel() {
      this.login_dialogVisible = false
    },
    login_post(user, token) {
      // 登录成功后的操作
      CookieOperation.setCookie('username', user, 1e9)
      CookieOperation.setCookie('token', token, 1e9)
      getuserid(this, user)
      this.$router.push('/main')
    },
    login_post_id(id) {
      // 登录成功后设置id到cookie
      CookieOperation.setCookie('userid', id, 1e9)
    },
    reg_cancel() {
      this.reg_dialogVisible = false
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/css/style.css';
@import 'https://fonts.googleapis.com/css2?family=Nunito+Sans&family=Nunito:wght@600;700;800&display=swap';
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #ffffff;
}
label {
  color: #d8142e;
  font-weight: bold;
}
</style>
