<template>
  <el-dialog
    style="text-align: center"
    title="加入项目"
    v-model="visible"
    :show-close="false"
    width="40%"
    :before-close="handleClose"
  >
    <div>
      <el-form>
        <el-form-item label="项目ID">
          <el-input v-model="projid" />
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="角色">
          <el-select v-model="role" class="m-2" placeholder="Select">
            <el-option label="系统工程师" value="system" />
            <el-option label="开发工程师" value="develop" />
            <el-option label="质量保证工程师" value="quality" />
          </el-select>
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="邀请码">
          <el-input v-model="invitecode" />
        </el-form-item>
      </el-form>
    </div>
    <!-- 确定 -->
    <template v-slot:footer>
      <span class="dialog-footer">
        <el-button v-on:click="cancel">返回</el-button>
        <el-button type="primary" :disabled="projid === 0" v-on:click="post">
          <span>确定</span>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { joinProject } from '@/utils/com_main.js'

export default {
  name: 'JoinProjectDialog',
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
      projid: 0,
      role: 'develop',
      invitecode: ''
    }
  },
  methods: {
    cancel() {
      this._cancel()
    },
    post() {
      // 申请加入项目
      const joindata = {
        project_id: this.projid,
        user_role: this.role,
        invitecode: this.invitecode
      }
      joinProject(this, joindata)
    },
    handleClose() {
      this._cancel()
    }
  },
  watch: {}
}
</script>

<style scoped></style>
