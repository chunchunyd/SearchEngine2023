<template>
  <main role="main" class="col-md-10 pt-3 px-4" v-show="visible">
    <el-header
      ><h4>SR交付情况</h4>
      <el-button type="primary" plain v-on:click="reload"
        >刷新</el-button
      ></el-header
    >
    <el-main>
      <el-form class="opt">
        <el-form-item label="选择要查看的SR：">
          <el-select v-model="sr_id" class="m-2" placeholder="Select">
            <el-option
              v-for="item in sr"
              :key="item"
              :label="item.sr_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <el-table stripe :data="sr_mr" style="width: 100%">
        <el-table-column prop="" label="" width="80" />
        <el-table-column prop="title" label="标题" width="300" />
        <el-table-column
          prop="description"
          label="简介"
          align="center"
          width="300"
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
                'background-color': mr_state_color[scope.row.state],
                color: '#000000'
              }"
              >{{ mr_state[scope.row.state] }}</el-tag
            >
          </template></el-table-column
        >
        <el-table-column prop="author_name" label="工程师" align="center" />
      </el-table>
    </el-main>

    <el-header
      ><h4>Issue交付情况</h4>
      <el-button type="primary" plain v-on:click="reload"
        >刷新</el-button
      ></el-header
    >
    <el-main>
      <el-form class="opt">
        <el-form-item label="选择要查看的Issue：">
          <el-select v-model="issue_id" class="m-2" placeholder="Select">
            <el-option
              v-for="item in issue"
              :key="item"
              :label="item.title"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <el-table stripe :data="issue_mr" style="width: 100%">
        <el-table-column prop="" label="" width="80" />
        <el-table-column prop="title" label="标题" width="300" />
        <el-table-column
          prop="description"
          label="简介"
          align="center"
          width="300"
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
                'background-color': mr_state_color[scope.row.state],
                color: '#000000'
              }"
              >{{ mr_state[scope.row.state] }}</el-tag
            >
          </template></el-table-column
        >
        <el-table-column prop="author_name" label="工程师" align="center" />
      </el-table>
    </el-main>
  </main>
</template>

<script>
import { getSr, getIssue, getSrMr, getIssueMr } from '@/utils/com_quality'

export default {
  name: 'PayloadBoard',
  components: {},
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
      // mr列表
      sr_mr: [],
      issue_mr: [],
      // 指向sr,issue
      sr_id: '',
      issue_id: '',
      // 所有SR,Issue
      sr: [],
      issue: []
    }
  },
  computed: {},
  methods: {
    reload() {
      // 重新加载
      getSr(this)
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
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === true) {
          // 如果组件变得可见
          getSr(this)
          getIssue(this)
        }
      }
    },
    sr_id: {
      handler(id) {
        if (this.visible === true && id !== '') {
          // 筛选sr对应的mr
          getSrMr(this, id)
        }
      }
    },
    issue_id: {
      handler(id) {
        if (this.visible === true && id !== '') {
          // 筛选sr对应的mr
          getIssueMr(this, id)
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
