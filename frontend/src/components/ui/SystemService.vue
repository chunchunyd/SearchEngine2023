<template>
  <main role="main" class="col-md-10 pt-3 px-4" v-show="visible">
    <el-header><h4>项目标签</h4></el-header>

    <!-- 系统服务 -->
    <el-container>
      <el-header
        ><h5>系统服务</h5>
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
  </main>
</template>

<script>
import { getservice, getsprint } from '@/utils/com_system'

export default {
  name: 'SystemServiceDash',
  components: {},
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
      sprintlist: []
    }
  },
  methods: {
    // 系统服务
    service_reload() {
      getservice(this)
    },
    // 迭代计划
    sprint_reload() {
      getsprint(this)
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
