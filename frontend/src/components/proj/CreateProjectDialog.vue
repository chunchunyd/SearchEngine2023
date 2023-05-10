<template>
  <el-dialog
    style="text-align: center"
    title="创建项目"
    v-model="visible"
    :show-close="false"
    width="40%"
    :before-close="handleClose"
  >
    <div>
      <el-form>
        <el-form-item label="项目名称">
          <el-input v-model="projname" />
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="项目简介">
          <el-input v-model="projdescrip" />
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="邀请码">
          <el-input v-model="invitecode" />
        </el-form-item>
      </el-form>
      <!-- 未来可以选择某种身份加入项目 -->
      <el-form>
        <el-form-item label="你在项目中的角色">
          <el-select v-model="role" class="m-2" placeholder="Select">
            <el-option label="系统工程师" value="system" />
            <el-option label="开发工程师" value="develop" />
            <el-option label="质量保证工程师" value="quality" />
          </el-select>
        </el-form-item>
      </el-form>
    </div>
    <!-- 确定 -->
    <template v-slot:footer>
      <span class="dialog-footer">
        <el-button v-on:click="cancel">返回</el-button>
        <el-button
          type="primary"
          :disabled="!projname || !invitecode"
          v-on:click="post"
        >
          <span>确定</span>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { createProject } from '@/utils/com_main.js'

export default {
  name: 'CreateProjectDialog',
  props: {
    dialogVisible: {
      type: Boolean,
      default: () => true
    },
    _cancel: {
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
      // 项目名称，简介，自己的角色
      projname: '',
      projdescrip: '',
      invitecode: '',
      role: 'system'
    }
  },
  methods: {
    cancel() {
      this._cancel()
    },
    post() {
      // 创建项目
      if (this.projname.length > 50) {
        this.$alert('项目名长度过长')
        return
      }
      if (this.projdescrip.length > 150) {
        this.$alert('项目描述过长')
        return
      }
      if (this.invitecode.length > 50) {
        this.$alert('邀请码过长')
      }
      const createdata = {
        project_name: this.projname,
        description: this.projdescrip,
        invitecode: this.invitecode,
        role: this.role
      }
      createProject(this, createdata)
    },
    handleClose() {
      this._cancel()
    }
  },
  watch: {}
}
</script>

<style scoped></style>
