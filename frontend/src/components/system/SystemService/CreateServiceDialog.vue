<template>
  <el-dialog
    style="text-align: center"
    title="添加系统服务"
    v-model="visible"
    :show-close="false"
    width="40%"
    :before-close="handleClose"
  >
    <div>
      <el-form>
        <el-form-item label="名称">
          <el-input v-model="servicename" />
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="描述">
          <el-input type="textarea" :rows="8" v-model="servicedescrip" />
        </el-form-item>
      </el-form>
    </div>
    <!-- 确定 -->
    <template v-slot:footer>
      <span class="dialog-footer">
        <el-button v-on:click="cancel">返回</el-button>
        <el-button
          type="primary"
          :disabled="!servicename || !servicedescrip"
          v-on:click="post"
        >
          <span>确定</span>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { createservice } from '@/utils/com_system.js'
export default {
  name: 'CreateServiceDialog',
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
      // service的名称和简介
      servicename: '',
      servicedescrip: ''
    }
  },
  methods: {
    cancel() {
      this._cancel()
    },
    post() {
      // 创建service
      if (this.servicename.length > 30) {
        this.$alert('service名称应在1-30位之间!')
        return
      }
      if (this.servicedescrip.length > 300) {
        this.$alert('service简介应在1-300位之间!')
        return
      }
      const createdata = {
        servicename: this.servicename,
        servicedescrip: this.servicedescrip
      }
      createservice(this, createdata)
    },
    handleClose() {
      this._cancel()
    }
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === false) {
          this.servicename = ''
          this.servicedescrip = ''
        }
      }
    }
  }
}
</script>

<style scoped></style>
