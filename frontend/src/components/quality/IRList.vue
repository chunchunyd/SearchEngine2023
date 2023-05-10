<template>
  <main role="main" class="col-md-10 pt-3 px-4" v-show="visible">
    <el-header
      ><h4>需求列表</h4>
      <el-button type="primary" plain v-on:click="reload"
        >刷新</el-button
      ></el-header
    >
    <el-main>
      <el-table stripe :data="ir" style="width: 100%">
        <el-table-column type="expand">
          <template #default="scope">
            <el-table stripe :data="scope.row.sr_list" style="width: 100%">
              <el-table-column prop="" label="" width="50" />
              <el-table-column
                sortable
                prop="sr_name"
                label="编号"
                width="130"
              />
              <el-table-column prop="description" label="内容" width="340" />
              <el-table-column prop="developer" label="开发者" align="center" />
              <el-table-column prop="iteration" label="迭代" align="center">
                <template #default="scope">
                  <el-tag size="medium">{{ scope.row.iteration }}</el-tag>
                </template></el-table-column
              >
              <el-table-column prop="service" label="系统服务" align="center">
                <template #default="scope">
                  <el-tag size="medium">{{ scope.row.service }}</el-tag>
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
          </template>
        </el-table-column>
        <el-table-column sortable prop="ir_name" label="编号" width="220" />
        <el-table-column prop="description" label="内容" />
        <el-table-column prop="state" label="状态" align="center">
          <template #default="scope">
            <el-tag
              size="medium"
              :style="{
                'background-color': ir_state_color[scope.row.state],
                color: '#000000'
              }"
              >{{ ir_state[scope.row.state] }}</el-tag
            >
          </template></el-table-column
        >
      </el-table>
    </el-main>
  </main>
</template>

<script>
import { getIrList } from '@/utils/com_quality'

export default {
  name: 'IRList',
  components: {},
  props: {
    visible: {
      type: Boolean,
      default: () => false
    }
  },
  data() {
    return {
      // ir状态
      ir_state: {
        raw: '未分解',
        init: '已分解',
        undergo: '开发中',
        done: '已交付'
      },
      // ir状态颜色
      ir_state_color: {
        raw: '#ddddff',
        init: '#ffcccc',
        undergo: 'ffff00',
        done: '#80ff80'
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
      // 哪一个ir展示sr
      show_sr: -1,
      // 所有ir
      ir: []
    }
  },
  methods: {
    ellipsis: function (value) {
      // 过长文字截取
      if (!value) return ''
      if (value.length > 20) {
        return value.slice(0, 20) + '...'
      }
      return value
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
    showsr(id) {
      if (this.show_sr === id) {
        this.show_sr = -1
      } else {
        this.show_sr = id
      }
    },
    reload() {
      // 重新加载ir列表
      getIrList(this)
    }
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === true) {
          // 如果组件变得可见，获得IRList
          getIrList(this)
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
