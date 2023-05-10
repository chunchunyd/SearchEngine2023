<template>
  <el-dialog
    style="text-align: center"
    title="关联SR"
    v-model="visible"
    :show-close="false"
    width="40%"
    :before-close="handleClose"
  >
    <div>
      <el-form class="opt">
        <el-form-item label="选择指向的SR：">
          <el-select v-model="srid" class="m-2" placeholder="Select">
            <el-option
              v-for="item in sr"
              :key="item"
              :label="item.sr_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
    </div>
    <!-- 确定 -->
    <template v-slot:footer>
      <span class="dialog-footer">
        <el-button v-on:click="cancel">返回</el-button>
        <el-button type="primary" :disabled="!srid" v-on:click="post">
          <span>确定</span>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { modifyTarget, getSr } from '@/utils/com_quality.js'
export default {
  name: 'SrTargetDialog',
  props: {
    dialogVisible: {
      type: Boolean,
      default: () => false
    },
    mr_id: {
      type: Number,
      default: () => 0
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
      // 修改后的sr的id
      srid: '',
      // 所有sr
      sr: []
    }
  },
  methods: {
    cancel() {
      this._cancel()
    },
    post() {
      // 修改target
      const data = {
        mrid: this.mr_id,
        srid: this.srid
      }
      modifyTarget(this, data)
    },
    handleClose() {
      this._cancel()
    }
  },
  watch: {
    // 获得所有sr
    dialogVisible: {
      handler(v) {
        if (v === true) {
          getSr(this)
        }
      }
    }
  }
}
</script>

<style scoped></style>
