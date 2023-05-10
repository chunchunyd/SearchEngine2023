<template>
  <main role="main" class="col-md-10 pt-3 px-4" v-show="visible">
    <el-header><h4>需求列表</h4></el-header>
    <el-button type="primary" plain v-on:click="ir_add">添加</el-button>
    <el-button type="primary" plain v-on:click="reload">刷新</el-button>

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
              <el-table-column
                prop="developer"
                label="开发者"
                width="90"
                align="center"
              />
              <el-table-column
                prop="iteration"
                label="迭代"
                width="90"
                align="center"
              >
                <template #default="scope">
                  <el-tag size="medium">{{ scope.row.iteration }}</el-tag>
                </template></el-table-column
              >
              <el-table-column
                prop="service"
                label="系统服务"
                width="90"
                align="center"
              >
                <template #default="scope">
                  <el-tag size="medium">{{ scope.row.service }}</el-tag>
                </template></el-table-column
              >
              <el-table-column
                prop="state"
                label="状态"
                width="140"
                align="center"
              >
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
              <el-table-column label="操作" align="center"
                ><template #default="scope">
                  <el-button
                    type="success"
                    v-on:click="sr_allocate(scope.row.id)"
                    size="small"
                    >分派</el-button
                  >
                  <el-button
                    type="warning"
                    v-on:click="
                      sr_edit(
                        scope.row.id,
                        scope.row.sr_name,
                        scope.row.description,
                        scope.row.iteration,
                        scope.row.service
                      )
                    "
                    size="small"
                    >编辑</el-button
                  >
                  <el-button
                    type="danger"
                    v-on:click="sr_remove(scope.row.id)"
                    size="small"
                    >删除</el-button
                  >
                </template></el-table-column
              >
            </el-table>
          </template>
        </el-table-column>
        <el-table-column sortable prop="ir_name" label="编号" width="220" />
        <el-table-column prop="description" label="内容" width="540" />
        <el-table-column prop="state" label="状态" width="140" align="center">
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
        <el-table-column label="操作" align="center"
          ><template #default="scope">
            <el-button
              type="success"
              v-on:click="sr_add(scope.row.id)"
              size="small"
              >分解</el-button
            >
            <el-button
              type="warning"
              v-on:click="
                ir_edit(scope.row.id, scope.row.ir_name, scope.row.description)
              "
              size="small"
              >编辑</el-button
            >
            <el-button
              type="danger"
              v-on:click="ir_remove(scope.row.id)"
              size="small"
              >删除</el-button
            >
          </template></el-table-column
        >
      </el-table>
    </el-main>

    <CreateIrDialog
      :dialogVisible="create_dialogVisible"
      :_cancel="create_cancel"
      :_reload="reload"
    ></CreateIrDialog>
    <ModifyIrDialog
      :dialogVisible="modify_dialogVisible"
      :_cancel="modify_cancel"
      :_reload="reload"
      :o_name="modify_name"
      :o_descrip="modify_descrip"
      :modify_id="modify_id"
    ></ModifyIrDialog>
    <CreateSrDialog
      :dialogVisible="create_sr_dialogVisible"
      :_cancel="create_sr_cancel"
      :_reload="reload"
      :irid="sr_add_irid"
    ></CreateSrDialog>
    <ModifySrDialog
      :dialogVisible="modify_sr_dialogVisible"
      :_cancel="modify_sr_cancel"
      :_reload="reload"
      :o_srid="modify_sr_id"
      :o_name="modify_sr_name"
      :o_des="modify_sr_descrip"
    ></ModifySrDialog>
    <AllocateSrDialog
      :dialogVisible="allocate_sr_dialogVisible"
      :_cancel="allocate_sr_cancel"
      :_reload="reload"
      :srid="sr_alloc_id"
    ></AllocateSrDialog>
  </main>
</template>

<script>
import { getIrList, deleteIr, deleteSr } from '@/utils/com_system'
import CreateIrDialog from './IR/CreateIrDialog.vue'
import ModifyIrDialog from './IR/ModifyIrDialog.vue'
import CreateSrDialog from './SR/CreateSrDialog.vue'
import ModifySrDialog from './SR/ModifySrDialog.vue'
import AllocateSrDialog from './SR/AllocateSrDialog.vue'
export default {
  name: 'IRList',
  components: {
    CreateIrDialog,
    ModifyIrDialog,
    CreateSrDialog,
    ModifySrDialog,
    AllocateSrDialog
  },
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
      ir: [],
      create_dialogVisible: false,
      modify_dialogVisible: false,
      // 所有sr
      create_sr_dialogVisible: false,
      modify_sr_dialogVisible: false,
      allocate_sr_dialogVisible: false,
      // 编辑ir时记录信息
      modify_id: 0,
      modify_name: '',
      modify_descrip: '',
      // 分解ir时，传参irid
      sr_add_irid: 0,
      // 编辑sr时记录信息
      modify_sr_id: 0,
      modify_sr_name: '',
      modify_sr_descrip: '',
      // 分配sr的id
      sr_alloc_id: 0
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
    },
    create_cancel() {
      this.create_dialogVisible = false
    },
    modify_cancel() {
      this.modify_dialogVisible = false
    },
    create_sr_cancel() {
      this.create_sr_dialogVisible = false
    },
    ir_add() {
      // 添加IR
      if (this.create_dialogVisible === false) {
        this.create_dialogVisible = true
      } else {
        this.create_dialogVisible = false
      }
    },
    ir_edit(id, name, des) {
      if (this.modify_dialogVisible === false) {
        this.modify_id = id
        this.modify_name = name
        this.modify_descrip = des
        this.modify_dialogVisible = true
      } else {
        this.modify_dialogVisible = false
      }
    },
    ir_remove(irid) {
      // 删除一个ir
      if (confirm('确定要删除吗?') === true) {
        deleteIr(this, irid)
      }
    },
    sr_add(irid) {
      // 分解一个ir
      this.sr_add_irid = irid
      if (this.create_sr_dialogVisible === false) {
        this.create_sr_dialogVisible = true
      } else {
        this.create_sr_dialogVisible = false
      }
    },
    sr_allocate(srid) {
      // 分配sr
      this.sr_alloc_id = srid
      if (this.allocate_sr_dialogVisible === false) {
        this.allocate_sr_dialogVisible = true
      } else {
        this.allocate_sr_dialogVisible = false
      }
    },
    allocate_sr_cancel() {
      this.allocate_sr_dialogVisible = false
    },
    sr_edit(id, name, des) {
      // 编辑sr
      if (this.modify_sr_dialogVisible === false) {
        this.modify_sr_id = id
        this.modify_sr_name = name
        this.modify_sr_descrip = des
        this.modify_sr_dialogVisible = true
      } else {
        this.modify_sr_dialogVisible = false
      }
    },
    modify_sr_cancel() {
      this.modify_sr_dialogVisible = false
    },
    sr_remove(srid) {
      // 删除一个sr
      if (confirm('确定要删除吗?') === true) {
        deleteSr(this, srid)
      }
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
