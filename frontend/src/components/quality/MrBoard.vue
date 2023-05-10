<template>
  <main role="main" class="col-md-10 pt-3 px-4" v-show="visible">
    <el-header
      ><h4>MR信息</h4>
      <el-button type="primary" plain v-on:click="reload"
        >刷新</el-button
      ></el-header
    >
    <el-main>
      <el-table stripe :data="mr" style="width: 100%">
        <el-table-column prop="" label="" width="50" />
        <el-table-column prop="title" label="标题" width="200" />
        <el-table-column prop="description" label="简介" align="center" width="300" />
        <el-table-column prop="updated_at" label="最后修改于" align="center">
          <template #default="scope">
            {{ datetime(scope.row.updated_at) }}
          </template></el-table-column
        >
        <el-table-column prop="state" label="状态" align="center">
          <template #default="scope">
            <el-tag
              size="medium"
              :style="{
                'background-color': mr_state_color[scope.row.state],
                color: '#000000'
              }"
              >{{ mr_state[scope.row.state] }}</el-tag
            >
          </template></el-table-column
        >
        <el-table-column prop="author_name" label="工程师" align="center" />
        <el-table-column prop="target_sr_name" label="指向SR" align="center" />
        <el-table-column prop="target_issue_name" label="指向Issue" align="center" />
        <el-table-column label="操作" align="center"
          ><template #default="scope">
            <el-button
              type="warning"
              v-on:click="
                edit(scope.row.id)
              "
              size="small"
              >编辑</el-button
            >
          </template></el-table-column
        >
      </el-table>
    </el-main>
  </main>

  <SrTargetDialog
    :dialogVisible="target_dialogVisible"
    :mr_id="mrid"
    :_cancel="target_cancel"
    :_reload="reload"
  />
</template>

<script>
import { getMr } from '@/utils/com_quality'
import SrTargetDialog from './SrTargetDialog.vue'

export default {
  name: 'MrBoard',
  components: {
    SrTargetDialog
  },
  props: {
    visible: {
      type: Boolean,
      default: () => false
    }
  },
  data() {
    return {
      target_dialogVisible: false,
      // 要修改target的mr
      mrid: '',
      // mr状态
      mr_state: {
        opened: '待合并',
        merged: '已合并',
        closed: '已关闭'
      },
      // mr状态颜色
      mr_state_color: {
        opened: '#ccffcc',
        merged: 'ffdd22',
        closed: '#aaffaa'
      },
      // 所有mr
      mr: []
    }
  },
  computed: {
  },
  methods: {
    reload() {
      // 重新加载
      getMr(this)
    },
    datetime: function (timestamp) {
      // 时间戳生成时间
      const d = new Date()
      if (timestamp < 10000000000) {
        d.setTime(timestamp * 1000)
      } else {
        d.setTime(timestamp)
      }
      return d.toLocaleString()
    },
    target_cancel: function () {
      // 关闭target对话框
      this.target_dialogVisible = false
    },
    edit: function (mrid) {
      // 修改target sr
      this.mrid = mrid
      if (this.target_dialogVisible === false) {
        this.target_dialogVisible = true
      } else {
        this.target_dialogVisible = false
      }
    }
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === true) {
          // 如果组件变得可见，获得mr列表
          getMr(this)
        }
      }
    }
  }
}
</script>

<style scoped>
.msg_type {
  display: inline-block;
  height: 20px;
  line-height: 18px;
  padding: 0 5px;
  color: #4d4d4d;
  font-size: 12px;
  text-align: center;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  vertical-align: top;
}
.state0 {
  background-color: #ffaaaa;
}
.state1 {
  background-color: #aaaaff;
}
</style>
