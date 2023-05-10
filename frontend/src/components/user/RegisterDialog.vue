<template>
  <el-dialog
    style="text-align: center"
    title="注册"
    v-model="visible"
    :show-close="false"
    width="40%"
    :before-close="handleClose"
  >
    <span>请输入用户名和密码</span>
    <el-form :model="form" label-width="80px" :rules="rules">
      <el-form-item label="用户名" prop="id">
        <el-input v-model="form.id" :placeholder="text" />
      </el-form-item>
      <el-form-item label="昵称" prop="nickname">
        <el-input v-model="form.nickname" :placeholder="text" />
      </el-form-item>
      <el-form-item label="输入密码" prop="pw">
        <el-input
          v-model="form.pw"
          type="password"
          :placeholder="password"
          show-password
        />
      </el-form-item>
      <el-form-item label="确认密码" prop="pw2">
        <el-input
          v-model="form.pw2"
          type="password"
          :placeholder="password"
          show-password
        />
      </el-form-item>
      <el-form-item label="邮箱" prop="mailbox">
        <el-input v-model="form.mailbox" :placeholder="text" />
      </el-form-item>
      <el-form-item label="性别" prop="sex">
        <el-radio-group v-model="form.sex">
          <el-radio label="male" />
          <el-radio label="female" />
          <el-radio label="other" />
        </el-radio-group>
      </el-form-item>
    </el-form>
    <template v-slot:footer>
      <span class="dialog-footer">
        <el-button v-on:click="cancel">返回</el-button>
        <el-button
          type="primary"
          :disabled="!form.id || !form.pw || !form.pw2"
          v-on:click="post"
        >
          <span>注册</span>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { comreg } from '@/utils/com_user.js'
import { checkform, checkmail } from '@/utils/tools'

export default {
  name: 'RegisterDialog',
  props: {
    dialogVisible: {
      type: Boolean,
      default: () => true
    },
    dialogError: {
      type: String,
      default: () => ''
    },
    reg_cancel: {
      // 通知父部件取消登录
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
      form: {
        id: '',
        pw: '',
        pw2: '',
        nickname: '',
        mailbox: '',
        sex: 'other'
      },
      rules: {
        id: [
          {
            required: true,
            message: '请输入用户名!',
            trigger: 'blur'
          },
          {
            min: 6,
            max: 20,
            message:
              '用户名的长度应该在6-20位之间,由大小写英文字母、数字和下划线组成!',
            trigger: ['blur', 'change']
          }
        ],
        nickname: [
          {
            required: true,
            message: '请输入昵称!',
            trigger: 'blur'
          },
          {
            min: 1,
            max: 30,
            message: '昵称需要在1~30位!',
            trigger: ['blur', 'change']
          }
        ],
        pw: [
          {
            required: true,
            message: '请输入密码!',
            trigger: 'change'
          },
          {
            min: 6,
            max: 20,
            message:
              '密码的长度应该在6-20位之间,由大小写英文字母、数字和下划线组成!',
            trigger: ['blur', 'change']
          }
        ],
        pw2: [
          {
            required: true,
            message: '请输入密码!',
            trigger: 'change'
          },
          {
            min: 6,
            max: 20,
            message:
              '密码的长度应该在6-20位之间,由大小写英文字母、数字和下划线组成!',
            trigger: ['blur', 'change']
          }
        ],
        mailbox: [
          {
            required: true,
            message: '请输入邮箱!',
            trigger: 'blur'
          },
          {
            type: 'email',
            message: '请输入正确的邮箱格式!',
            trigger: ['blur', 'change']
          }
        ],
        sex: []
      }
    }
  },
  methods: {
    cancel() {
      this.reg_cancel()
    },
    post() {
      if (!checkform(this.form.id)) {
        this.$alert(
          '用户名的长度应该在6-20位之间,由大小写英文字母、数字和下划线组成!'
        )
        return
      }
      if (this.form.nickname.length > 30 || this.form.nickname.length < 1) {
        this.$alert('昵称需要在1~30位!')
        return
      }
      if (!checkform(this.form.pw)) {
        this.$alert(
          '密码的长度应该在6-20位之间,由大小写英文字母、数字和下划线组成!'
        )
        return
      }
      if (!checkmail(this.form.mailbox)) {
        this.$alert('请输入正确的邮箱格式!')
        return
      }
      if (this.form.pw !== this.form.pw2) {
        this.$alert('请确保两次密码一致!')
        return
      }
      comreg(this)
    },
    handleClose() {
      this.reg_cancel()
    }
  },
  watch: {
    dialogVisible: {
      handler(dialogVisible) {
        if (dialogVisible === false) this.cancel()
        this.form.id = ''
        this.form.pw = ''
        this.form.pw2 = ''
        this.form.nickname = ''
        this.form.mailbox = ''
        this.form.sex = 'other'
      }
    }
  }
}
</script>

<style scoped></style>
