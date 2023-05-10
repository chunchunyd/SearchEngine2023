<template>
  <el-dialog
    style="text-align: center"
    title="登录"
    v-model="visible"
    :show-close="false"
    width="40%"
    :before-close="handleClose"
  >
    <span>请输入用户名和密码</span>
    <el-form :model="form" label-width="80px">
      <span style="color: red" v-if="dialogError !== ''">{{
        dialogError
      }}</span>
      <el-form-item label="用户名">
        <el-input v-model="id" :placeholder="text" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input
          v-model="pw"
          type="password"
          :placeholder="password"
          show-password
        />
      </el-form-item>
    </el-form>
    <template v-slot:footer>
      <span class="dialog-footer">
        <el-button v-on:click="cancel">返回</el-button>
        <el-button type="primary" :disabled="!id || !pw" v-on:click="post">
          <span>登录</span>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { comlogin } from '@/utils/com_user.js'

export default {
  name: 'LoginDialog',
  props: {
    dialogVisible: {
      type: Boolean,
      default: () => true
    },
    dialogError: {
      type: String,
      default: () => ''
    },
    login_cancel: {
      // 通知父部件取消登录
      type: Function,
      default: () => {}
    },
    login_post: {
      // 回调函数，通知父部件登陆成功
      type: Function,
      default: () => {}
    }
  },
  computed: {
    visible: function () {
      return this.dialogVisible
    }
  },
  data() {
    return {
      id: '',
      pw: ''
    }
  },
  methods: {
    cancel() {
      this.login_cancel()
    },
    post() {
      comlogin(this)
    },
    handleClose() {
      this.login_cancel()
    }
  },
  watch: {
    dialogVisible: {
      handler(dialogVisible) {
        if (dialogVisible === false) this.cancel()
        this.id = ''
        this.pw = ''
      }
    }
  }
}
</script>

<style scoped></style>
