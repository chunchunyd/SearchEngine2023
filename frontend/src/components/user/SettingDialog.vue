<template>
  <el-dialog
    style="text-align: center"
    title="设置"
    v-model="visible"
    :show-close="false"
    width="40%"
    :before-close="handleClose"
  >
    <!-- 选择框 -->
    <el-form class="opt">
      <el-form-item label="请选择">
        <el-select v-model="value" class="m-2" placeholder="Select">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
    </el-form>
    <!-- 修改昵称 -->
    <div v-if="value == options[0].value">
      <el-form>
        <el-form-item label="原昵称">
          <label> {{ _nickname }} </label>
        </el-form-item>
        <el-form-item label="新昵称">
          <el-input v-model="nickname" :placeholder="text" />
        </el-form-item>
      </el-form>
    </div>
    <!-- 更换性别 -->
    <div v-if="value == options[1].value">
      <el-form>
        <el-form-item label="原性别">
          <label> {{ _gender }} </label>
        </el-form-item>
        <el-form-item label="新性别">
          <el-radio-group v-model="gender">
            <el-radio label="male" />
            <el-radio label="female" />
            <el-radio label="other" />
          </el-radio-group>
        </el-form-item>
      </el-form>
    </div>
    <!-- 更换邮箱 -->
    <div v-if="value == options[2].value">
      <el-form>
        <el-form-item label="原邮箱">
          <label> {{ _email }} </label>
        </el-form-item>
        <el-form-item label="新邮箱">
          <el-input v-model="email" :placeholder="text" />
        </el-form-item>
      </el-form>
    </div>
    <!-- 修改头像 -->
    <div v-else-if="value == options[3].value">
      <el-form>
        <el-form-item label="新头像">
          <input type="file" @change="avatarformat" />
        </el-form-item>
      </el-form>
    </div>
    <!-- 修改密码 -->
    <div v-else-if="value == options[4].value">
      <el-form>
        <el-form-item label="原密码">
          <el-input v-model="oldpw" :placeholder="pw" show-password />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="newpw" :placeholder="pw1" show-password />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="newpw2" :placeholder="pw2" show-password />
        </el-form-item>
      </el-form>
    </div>
    <!-- 修改绑定的git信息 -->
    <div v-if="value == options[5].value">
      <el-form>
        <el-form-item label="原Gitlab ID">
          <label> {{ _gitid }} </label>
        </el-form-item>
        <el-form-item label="新Gitlab ID(8位数字)">
          <el-input v-model="gitid" :placeholder="text" />
        </el-form-item>
      </el-form>
    </div>
    <!-- 确定 -->
    <template v-slot:footer>
      <span class="dialog-footer">
        <el-button v-on:click="cancel">返回</el-button>
        <el-button type="primary" :disabled="0" v-on:click="post">
          <span>确定</span>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { checkform, checkmail } from '@/utils/tools'
import { changeinfo, changepassword, changeavatar } from '@/utils/com_user.js'

export default {
  name: 'SettingDialog',
  props: {
    dialogVisible: {
      type: Boolean,
      default: () => true
    },
    username: {
      type: String,
      default: () => ''
    },
    // 变量前有下划线，则说明是父组件传递的参数，否则则是本地变量，即需要修改的变量
    _nickname: {
      type: String,
      default: () => ''
    },
    _gender: {
      type: String,
      default: () => ''
    },
    _email: {
      type: String,
      default: () => ''
    },
    _gitid: {
      type: String,
      default: () => '1'
    },
    _cancel: {
      type: Function,
      default: () => {}
    },
    _changeinfo: {
      // 回调函数，告知父部件自己已经成功更改个人信息
      type: Function,
      default: () => {}
    },
    _changepw: {
      // 回调函数，告知父部件自己已经成功更改密码
      type: Function,
      default: () => {}
    },
    _changeavatar: {
      // 回调函数，告知父部件自己已经成功更改头像
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
      value: 'nickname',
      options: [
        { value: 'nickname', label: '修改昵称' },
        { value: 'gender', label: '修改性别' },
        { value: 'email', label: '修改邮箱' },
        { value: 'avatar', label: '修改头像' },
        { value: 'pw', label: '修改密码' },
        { value: 'gitid', label: '修改Gitlab绑定' }
      ],
      nickname: '',
      gender: '',
      email: '',
      avatar: '',
      oldpw: '',
      newpw: '',
      newpw2: '',
      gitid: ''
    }
  },
  methods: {
    cancel() {
      this._cancel()
    },
    post() {
      if (this.value === 'nickname') {
        // 修改昵称
        if (this.nickname.length > 30 || this.nickname.length < 1) {
          this.$alert('昵称需要在1~30位!')
          return
        }
        changeinfo(this)
      } else if (this.value === 'gender') {
        // 修改性别
        if (this._gender === this.gender) {
          this.$alert('如需修改性别,请选择不同性别!')
          return
        }
        changeinfo(this)
      } else if (this.value === 'email') {
        // 修改邮箱
        if (!checkmail(this.email)) {
          this.$alert('请输入正确的邮箱格式!')
          return
        }
        changeinfo(this)
      } else if (this.value === 'gitid') {
        // 修改邮箱
        const reg = /^[0-9]{8}$/
        if (!reg.test(this.gitid)) {
          this.$alert('请输入正确的Gitlab ID!')
          return
        }
        changeinfo(this)
      } else if (this.value === 'avatar') {
        // 修改头像
        changeavatar(this)
      } else if (this.value === 'pw') {
        // 修改密码
        if (!checkform(this.oldpw)) {
          this.$alert(
            '原密码的长度应该在6-20位之间,由大小写英文字母、数字和下划线组成!'
          )
          return
        }
        if (!checkform(this.newpw)) {
          this.$alert(
            '新密码的长度应该在6-20位之间,由大小写英文字母、数字和下划线组成!'
          )
          return
        }
        if (this.newpw !== this.newpw2) {
          this.$alert('请确保两次密码一致!')
          return
        }
        changepassword(this)
      }
    },
    avatarformat(e) {
      const file = e.target.files[0]
      if (file.size > 3 * 1024 * 1024) {
        this.$alert('头像大小不应该超过3M!')
        return
      }
      const formData = new FormData()
      formData.append('avatar', file)
      this.avatar = formData
    },
    handleClose() {
      this._cancel()
    }
  },
  watch: {
    dialogVisible: {
      handler(dialogVisible) {
        if (dialogVisible === false) this.cancel()
        this.nickname = ''
        this.avatar = ''
        this.oldpw = ''
        this.newpw = ''
        this.newpw2 = ''
        this.gitid = ''
      }
    }
  }
}
</script>

<style scoped>
.opt {
  z-index: -1000000;
}
</style>
