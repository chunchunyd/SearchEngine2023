<template>
  <main role="main" class="col-md-10 pt-3 px-4" v-show="visible">
    <el-header><h4>工作台</h4></el-header>

    <!-- 系统服务 -->
    <el-container>
      <el-header
        ><h5>系统服务</h5>
        <el-button type="primary" plain v-on:click="service_add"
          >添加</el-button
        >
        <el-button type="primary" plain v-on:click="service_reload"
          >刷新</el-button
        ></el-header
      >
      <el-main>
        <el-space wrap>
          <div v-for="item in servicelist" :key="item">
            <el-card class="box-card" shadow="hover" style="fill">
              <template #header>
                <div class="card-header">
                  <span>{{ item.service_name }}</span>
                  <el-button
                    class="button"
                    type="text"
                    v-on:click="service_edit(item.id)"
                    >编辑</el-button
                  >
                </div>
              </template>
              <div class="text item">
                {{ item.description }}
              </div>
            </el-card>
          </div>
        </el-space>
      </el-main>
    </el-container>
    <el-divider />

    <!-- 迭代计划 -->
    <el-container>
      <el-header
        ><h5>迭代计划</h5>
        <el-button type="primary" plain v-on:click="sprint_add">添加</el-button>
        <el-button type="primary" plain v-on:click="sprint_reload"
          >刷新</el-button
        ></el-header
      >
      <el-main>
        <el-space wrap>
          <div v-for="item in sprintlist" :key="item">
            <el-card class="box-card" shadow="hover" style="fill">
              <template #header>
                <div class="card-header">
                  <span>{{ item.it_name }}</span>
                  <el-button
                    class="button"
                    type="text"
                    v-on:click="sprint_edit(item.id)"
                    >编辑</el-button
                  >
                </div>
              </template>
              <div class="text item">
                {{ item.description }}
              </div>
            </el-card>
          </div>
        </el-space>
      </el-main>
    </el-container>

    <CreateServiceDialog
      :dialogVisible="create_service_visible"
      :_cancel="service_cancel"
      :_reload="service_reload"
    />

    <ModifyServiceDialog
      :dialogVisible="modify_service_visible"
      :_cancel="service_cancel"
      :_reload="service_reload"
      :serviceid="modify_service_id"
    />

    <CreateSprintDialog
      :dialogVisible="create_sprint_visible"
      :_cancel="sprint_cancel"
      :_reload="sprint_reload"
    />

    <ModifySprintDialog
      :dialogVisible="modify_sprint_visible"
      :_cancel="sprint_cancel"
      :_reload="sprint_reload"
      :sprintid="modify_sprint_id"
    />
  </main>
</template>

<script>
import CreateServiceDialog from '@/components/system/SystemService/CreateServiceDialog.vue'
import ModifyServiceDialog from '@/components/system/SystemService/ModifyServiceDialog.vue'
import CreateSprintDialog from '@/components/system/Iteration/CreateSprintDialog.vue'
import ModifySprintDialog from '@/components/system/Iteration/ModifySprintDialog.vue'
import { getservice, getsprint } from '@/utils/com_system'

export default {
  name: 'WorkTable',
  components: {
    CreateServiceDialog,
    ModifyServiceDialog,
    CreateSprintDialog,
    ModifySprintDialog
  },
  props: {
    visible: {
      type: Boolean,
      default: () => false
    }
  },
  data() {
    return {
      // data
      servicelist: [],
      sprintlist: [],
      // component visible
      create_service_visible: false,
      modify_service_visible: false,
      create_sprint_visible: false,
      modify_sprint_visible: false,
      // record modify numbers
      modify_service_id: 0,
      modify_sprint_id: 0
    }
  },
  methods: {
    // 系统服务
    service_add() {
      if (this.create_service_visible === true) {
        this.create_service_visible = false
      } else {
        this.create_service_visible = true
      }
    },
    service_reload() {
      getservice(this)
    },
    service_edit(serviceid) {
      this.modify_service_id = serviceid
      if (this.modify_service_visible === true) {
        this.modify_service_visible = false
      } else {
        this.modify_service_visible = true
      }
    },
    service_cancel() {
      this.create_service_visible = false
      this.modify_service_visible = false
      this.modify_service_id = 0
    },
    // 迭代计划
    sprint_add() {
      if (this.create_sprint_visible === true) {
        this.create_sprint_visible = false
      } else {
        this.create_sprint_visible = true
      }
    },
    sprint_reload() {
      getsprint(this)
    },
    sprint_edit(sprintid) {
      this.modify_sprint_id = sprintid
      if (this.modify_sprint_visible === true) {
        this.modify_sprint_visible = false
      } else {
        this.modify_sprint_visible = true
      }
    },
    sprint_cancel() {
      this.create_sprint_visible = false
      this.modify_sprint_visible = false
      this.modify_sprint_id = 0
    }
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === true) {
          getservice(this)
          getsprint(this)
        } else {
          this.servicelist = []
          this.sprintlist = []
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
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.text {
  font-size: 14px;
}
.item {
  margin-bottom: 18px;
}
.box-card {
  width: 480px;
}
</style>
