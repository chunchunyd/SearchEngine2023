<template>
  <el-dialog
    style="text-align: center"
    title="编辑SR"
    v-model="visible"
    :show-close="false"
    width="40%"
    :before-close="handleClose"
  >
    <div>
      <el-form>
        <el-form-item label="SR编号">
          <el-input v-model="srname" />
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="SR内容">
          <el-input type="textarea" :rows="4" v-model="srdescrip" />
        </el-form-item>
      </el-form>
      <el-form class="opt">
        <el-form-item label="系统服务">
          <el-select v-model="service_id" class="m-2" placeholder="Select">
            <el-option
              v-for="item in servicelist"
              :key="item"
              :label="item.service_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <el-form class="opt">
        <el-form-item label="迭代计划">
          <el-select v-model="iteration_id" class="m-2" placeholder="Select">
            <el-option
              v-for="item in sprintlist"
              :key="item"
              :label="item.it_name"
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
        <el-button
          type="primary"
          :disabled="!srname || !srdescrip || !service_id || !iteration_id"
          v-on:click="post"
        >
          <span>确定</span>
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { modifySr, getservice, getsprint } from '@/utils/com_system.js'
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
    o_srid: {
      type: Number,
      default: () => 0
    },
    o_name: {
      type: String,
      default: () => ''
    },
    o_des: {
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
      // sr的名称和简介
      srname: '',
      srdescrip: '',
      // 系统服务和迭代
      sprintlist: [],
      servicelist: [],
      service_id: '',
      iteration_id: ''
    }
  },
  mounted() {},
  methods: {
    cancel() {
      this._cancel()
    },
    post() {
      // 修改SR
      if (this.srname.length > 30) {
        this.$alert('SR名称应在1-30位之间!')
        return
      }
      if (this.srdescrip.length > 300) {
        this.$alert('SR简介应在1-300位之间!')
        return
      }
      const modifydata = {
        srname: this.srname,
        srdescrip: this.srdescrip,
        srid: this.o_srid,
        iteration_id: this.iteration_id,
        service_id: this.service_id
      }
      modifySr(this, modifydata)
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
          this.srname = this.o_name
          this.srdescrip = this.o_des
          getservice(this)
          getsprint(this)
        }
      }
    }
  }
}
</script>

<style scoped></style>
