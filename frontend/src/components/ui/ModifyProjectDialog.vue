<template>
  <el-dialog
    style="text-align: center"
    title="修改项目信息"
    v-model="visible"
    :show-close="false"
    width="40%"
    :before-close="handleClose"
  >
    <div>
      <el-form>
        <el-form-item label="名称">
          <el-input v-model="name" />
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="描述">
          <el-input v-model="descrip" />
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="邀请码">
          <el-input v-model="pswd" />
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="Gitlab home">
          <el-input v-model="git_home" />
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="Git ID">
          <el-input v-model="git_id" />
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="Gitlab token">
          <el-input v-model="token" />
        </el-form-item>
      </el-form>
    </div>
    <!-- 确定 -->
    <template v-slot:footer>
      <span class="dialog-footer">
        <el-button v-on:click="cancel">返回</el-button>
        <el-button
          type="primary"
          :disabled="!name || !descrip || !pswd"
          v-on:click="post"
        >
          <span>确定</span>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { modifyproj } from '@/utils/com_ui.js'

export default {
  name: 'ModifyProjectDialog',
  props: {
    dialogVisible: {
      type: Boolean,
      default: () => false
    },
    _cancel: {
      type: Function,
      default: () => {}
    },
    _reload: {
      // 父组件自动刷新
      type: Function,
      default: () => {}
    },
    o_name: {
      // 原先的名称，下同
      type: String,
      default: () => ''
    },
    o_descrip: {
      type: String,
      default: () => ''
    },
    o_pswd: {
      type: String,
      default: () => ''
    },
    o_id: {
      type: String,
      default: () => ''
    },
    o_token: {
      type: String,
      default: () => ''
    },
    o_home: {
      type: String,
      default: () => ''
    }
  },
  computed: {
    visible: function () {
      return this.dialogVisible
    }
  },
  data() {
    return {
      name: '',
      descrip: '',
      pswd: '',
      git_id: '',
      token: '',
      git_home: ''
    }
  },
  methods: {
    cancel() {
      this._cancel()
    },
    post() {
      // 修改信息
      if (this.name.length > 50) {
        this.$alert('项目名长度过长')
        return
      }
      if (this.descrip.length > 150) {
        this.$alert('项目描述过长')
        return
      }
      if (this.pswd.length > 50) {
        this.$alert('邀请码过长')
        return
      }
      if (this.token.length > 100) {
        this.$alert('Gitlab token过长')
        return
      }
      const modifydata = {
        project_name: this.name,
        description: this.descrip,
        pswd: this.pswd,
        git_id: this.git_id,
        git_token: this.token,
        git_home: this.git_home
      }
      modifyproj(this, modifydata)
    },
    handleClose() {
      this._cancel()
    }
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === true) {
          this.name = this.o_name
          this.descrip = this.o_descrip
          this.pswd = this.o_pswd
          this.git_id = this.o_id
          this.token = this.o_token
          this.git_home = this.o_home
        }
      }
    }
  }
}
</script>

<style scoped></style>
