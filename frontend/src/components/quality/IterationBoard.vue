<template>
  <main role="main" class="col-md-10 pt-3 px-4" v-show="visible">
    <el-header
      ><h4>迭代计划</h4>
      <el-button type="primary" plain v-on:click="reload"
        >刷新</el-button
      ></el-header
    >
    <el-main>
      <el-form class="opt">
        <el-form-item label="选择要查看的迭代计划：">
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
      <!--下面是迭代整体情况 -->
      <el-descriptions
        v-if="iteration_id !== ''"
        size="large"
        span="1"
        border
        v-loading="loading"
        column="5"
      >
        <el-descriptions-item label="SR数量" width="10%">{{ sr_num }}</el-descriptions-item>
        <el-descriptions-item label="迭代状态" width="10%">
          <el-tag
            size="medium"
            :style="{
              'background-color': iteration_color[sprint_state],
              color: '#000000'
            }"
            >{{ iteration_state[sprint_state] }}</el-tag
          >
        </el-descriptions-item>
        <el-descriptions-item label="已交付数量" width="10%">{{
          complete_num
        }}</el-descriptions-item>
        <el-descriptions-item label="开发中数量" width="10%">{{
          doing_num
        }}</el-descriptions-item>
        <el-descriptions-item label="待开发数量" width="10%">{{
          init_num
        }}</el-descriptions-item>
      </el-descriptions>
      <br v-if="iteration_id !== ''" />

      <el-table stripe :data="sr" style="width: 100%">
        <el-table-column prop="" label="" width="50" />
        <el-table-column sortable prop="sr_name" label="编号" width="130" />
        <el-table-column prop="description" label="内容" width="300" />
        <el-table-column prop="developer_name" label="开发者" align="center" />
        <el-table-column prop="iteration_name" label="迭代" align="center">
          <template #default="scope">
            <el-tag size="medium">{{ scope.row.iteration_name }}</el-tag>
          </template></el-table-column
        >
        <el-table-column prop="service_name" label="系统服务" align="center">
          <template #default="scope">
            <el-tag size="medium">{{ scope.row.service_name }}</el-tag>
          </template></el-table-column
        >
        <el-table-column prop="state" label="状态" align="center">
          <template #default="scope">
            <el-tag
              size="medium"
              :style="{
                'background-color': sr_state_color[scope.row.state],
                color: '#000000'
              }"
              >{{ sr_state[scope.row.state] }}</el-tag
            >
          </template></el-table-column
        >
      </el-table>
    </el-main>
  </main>
</template>

<script>
import { getsprint, getSprintSr } from '@/utils/com_quality'

export default {
  name: 'IterationDash',
  components: {},
  props: {
    visible: {
      type: Boolean,
      default: () => false
    }
  },
  data() {
    return {
      // 组件可视程度
      // 迭代列表
      sprintlist: [],
      // 选择的迭代id
      iteration_id: '',
      // 迭代状态
      iteration_state: {
        undef: '未定义',
        init: '待开发',
        undergo: '开发中',
        done: '已交付'
      },
      iteration_color: {
        undef: '#ffffff',
        init: '#ccffcc',
        undergo: 'ffdd22',
        done: '#aaffaa'
      },
      // sr状态
      sr_state: {
        init: '待开发',
        undergo: '开发中',
        done: '已交付'
      },
      // sr状态颜色
      sr_state_color: {
        init: '#ccffcc',
        undergo: 'ffdd22',
        done: '#aaffaa'
      },
      // 所有sr
      sr: []
    }
  },
  computed: {
    sr_num: function () {
      return this.sr.length
    },
    complete_num: function () {
      let num = 0
      for (let i = 0; i < this.sr.length; i++) {
        if (this.sr[i].state === 'done') {
          num = num + 1
        }
      }
      return num
    },
    doing_num: function () {
      let num = 0
      for (let i = 0; i < this.sr.length; i++) {
        if (this.sr[i].state === 'undergo') {
          num = num + 1
        }
      }
      return num
    },
    init_num: function () {
      let num = 0
      for (let i = 0; i < this.sr.length; i++) {
        if (this.sr[i].state === 'init') {
          num = num + 1
        }
      }
      return num
    },
    sprint_state: function () {
      // -1:未定义 0：待开发 1：开发中 2：已交付
      if (this.sr.length === 0) {
        return 'undef'
      }
      let state = 2
      for (let i = 0; i < this.sr.length; i++) {
        if (this.sr[i].state !== 'done') {
          state = 1
          break
        }
      }
      if (state === 2) {
        return 'done'
      }
      state = 0
      for (let i = 0; i < this.sr.length; i++) {
        if (this.sr[i].state !== 'init') {
          state = 1
          break
        }
      }
      if (state === 1) {
        return 'undergo'
      }
      return 'init'
    }
  },
  methods: {
    reload() {
      // 重新加载
      getsprint(this)
    }
    // function
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === true) {
          // 如果组件变得可见，获得迭代列表
          getsprint(this)
        }
      }
    },
    iteration_id: {
      handler(id) {
        if (this.visible === true && id !== '') {
          // 筛选对应的迭代获得sr
          getSprintSr(this, id)
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
