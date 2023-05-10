<template>
  <el-dialog
    style="text-align: center"
    title="分派SR"
    v-model="visible"
    :show-close="false"
    width="40%"
    :before-close="handleClose"
  >
    <div>
      <el-form class="opt">
        <el-form-item label="指定开发人员">
          <el-select v-model="alloc_id" class="m-2" placeholder="Select">
            <el-option
              v-for="item in developlist"
              :key="item"
              :label="item.username"
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
        <el-button type="primary" :disabled="!alloc_id" v-on:click="post">
          <span>确定</span>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { getpartner } from '@/utils/com_ui'
import { allocateSr } from '@/utils/com_system.js'
export default {
  name: 'ModifySrDialog',
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
    srid: {
      type: Number,
      default: () => 0
    }
  },
  computed: {
    visible: function () {
      return this.dialogVisible
    }
  },
  data() {
    return {
      systemlist: [],
      developlist: [],
      qualitylist: [],
      // 分配开发者的id
      alloc_id: ''
    }
  },
  mounted() {},
  methods: {
    cancel() {
      this._cancel()
    },
    post() {
      // 分配SR
      const allocdata = {
        srid: this.srid,
        alloc_id: this.alloc_id
      }
      allocateSr(this, allocdata)
    },
    handleClose() {
      this._cancel()
    }
  },
  watch: {
    // 将原信息渲染出来
    dialogVisible: {
      handler(v) {
        if (v === true) {
          getpartner(this)
        }
      }
    }
  }
}
</script>

<style scoped></style>
