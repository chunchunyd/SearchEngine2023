<template>
  <el-dialog
    style="text-align: center"
    title="修改SR状态"
    v-model="visible"
    :show-close="false"
    width="20%"
    :before-close="handleClose"
  >
    <el-form>
      <el-form-item label="修改状态">
        <el-select v-model="newstate" clearable placeholder="Select">
          <el-option
            v-for="item in states"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
    </el-form>
    <!-- 确定 -->
    <template v-slot:footer>
      <span class="dialog-footer">
        <el-button v-on:click="cancel">返回</el-button>
        <el-button type="primary" :disabled="!newstate" v-on:click="post">
          <span>确定</span>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { changeSRstate } from '@/utils/com_develop.js'

export default {
  name: 'ChangeDialog',
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
    },
    _srid: {
      type: Number,
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
      states: [
        { value: 'init', label: '初始化' },
        { value: 'undergo', label: '进行中' },
        { value: 'done', label: '已交付' }
      ],
      newstate: ''
    }
  },
  mounted() {},
  methods: {
    cancel() {
      this._cancel()
    },
    post() {
      // 修改SR
      const changedata = {
        srid: this._srid,
        newstate: this.newstate
      }
      changeSRstate(this, changedata)
    },
    handleClose() {
      this._cancel()
    }
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === false) {
          this.newstate = ''
        }
      }
    }
  }
}
</script>

<style scoped></style>
