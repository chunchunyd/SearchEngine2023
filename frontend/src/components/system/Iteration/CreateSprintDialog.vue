<template>
  <el-dialog
    style="text-align: center"
    title="添加迭代计划"
    v-model="visible"
    :show-close="false"
    width="40%"
    :before-close="handleClose"
  >
    <div>
      <el-form>
        <el-form-item label="名称">
          <el-input v-model="sprintname" />
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="描述">
          <el-input type="textarea" :rows="8" v-model="sprintdescrip" />
        </el-form-item>
      </el-form>
    </div>
    <!-- 确定 -->
    <template v-slot:footer>
      <span class="dialog-footer">
        <el-button v-on:click="cancel">返回</el-button>
        <el-button
          type="primary"
          :disabled="!sprintname || !sprintdescrip"
          v-on:click="post"
        >
          <span>确定</span>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { createsprint } from '@/utils/com_system.js'
export default {
  name: 'CreateSprintDialog',
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
    }
  },
  computed: {
    visible: function () {
      return this.dialogVisible
    }
  },
  data() {
    return {
      // sprint的名称和简介
      sprintname: '',
      sprintdescrip: ''
    }
  },
  methods: {
    cancel() {
      this._cancel()
    },
    post() {
      // 创建sprint
      if (this.sprintname.length > 30) {
        this.$alert('sprint名称应在1-30位之间!')
        return
      }
      if (this.sprintdescrip.length > 300) {
        this.$alert('sprint简介应在1-300位之间!')
        return
      }
      const createdata = {
        sprintname: this.sprintname,
        sprintdescrip: this.sprintdescrip
      }
      createsprint(this, createdata)
    },
    handleClose() {
      this._cancel()
    }
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === false) {
          this.sprintname = ''
          this.sprintdescrip = ''
        }
      }
    }
  }
}
</script>

<style scoped></style>
