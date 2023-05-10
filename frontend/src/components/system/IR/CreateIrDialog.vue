<template>
  <el-dialog
    style="text-align: center"
    title="添加IR"
    v-model="visible"
    :show-close="false"
    width="40%"
    :before-close="handleClose"
  >
    <div>
      <el-form>
        <el-form-item label="IR编号">
          <el-input v-model="irname" />
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="IR内容">
          <el-input type="textarea" :rows="8" v-model="irdescrip" />
        </el-form-item>
      </el-form>
    </div>
    <!-- 确定 -->
    <template v-slot:footer>
      <span class="dialog-footer">
        <el-button v-on:click="cancel">返回</el-button>
        <el-button
          type="primary"
          :disabled="!irname || !irdescrip"
          v-on:click="post"
        >
          <span>确定</span>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { createIr } from '@/utils/com_system.js'
export default {
  name: 'CreateIrDialog',
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
      // ir的名称和简介
      irname: '',
      irdescrip: ''
    }
  },
  methods: {
    cancel() {
      this._cancel()
    },
    post() {
      // 创建Ir
      if (this.irname.length > 30) {
        this.$alert('IR名称应在1-30位之间!')
        return
      }
      if (this.irdescrip.length > 300) {
        this.$alert('IR简介应在1-300位之间!')
        return
      }
      const createdata = { irname: this.irname, irdescrip: this.irdescrip }
      createIr(this, createdata)
    },
    handleClose() {
      this._cancel()
    }
  },
  watch: {}
}
</script>

<style scoped></style>
