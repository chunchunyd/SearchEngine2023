<template>
  <main role="main" class="col-md-10 pt-3 px-4" v-show="visible">
    <el-header
      ><h4>Issue信息</h4>
      <el-button type="primary" plain v-on:click="reload"
        >刷新</el-button
      ></el-header
    >
    <el-main>
      <el-table stripe :data="issue" style="width: 100%">
        <el-table-column prop="" label="" width="50" />
        <el-table-column prop="title" label="标题" width="200" />
        <el-table-column
          prop="description"
          label="简介"
          align="center"
          width="350"
        />
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
                'background-color': issue_state_color[scope.row.state],
                color: '#000000'
              }"
              >{{ issue_state[scope.row.state] }}</el-tag
            >
          </template></el-table-column
        >
        <el-table-column prop="author_name" label="工程师" align="center" />
        <el-table-column prop="target_sr_name" label="指向SR" align="center" />
      </el-table>
    </el-main>
  </main>
</template>

<script>
import { getIssue } from '@/utils/com_quality'

export default {
  name: 'IssueBoard',
  components: {},
  props: {
    visible: {
      type: Boolean,
      default: () => false
    }
  },
  data() {
    return {
      // 状态
      issue_state: {
        opened: '待完成',
        closed: '已完成'
      },
      // 状态颜色
      issue_state_color: {
        opened: '#ccffcc',
        closed: '#aaffaa'
      },
      // 所有issue
      issue: []
    }
  },
  computed: {},
  methods: {
    reload() {
      // 重新加载
      getIssue(this)
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
    }
    // function
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === true) {
          // 如果组件变得可见，获得mr列表
          getIssue(this)
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
