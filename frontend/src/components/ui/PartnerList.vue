<template>
  <main role="main" class="col-md-10 pt-3 px-4" v-show="visible">
    <el-header><h4>人员列表</h4></el-header>
    <el-main>
      <h6>系统工程师</h6>
      <el-table :data="systemlist" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="180" />
        <el-table-column prop="username" label="Username" width="180" />
        <el-table-column prop="nickname" label="Nickname" width="300" />
        <el-table-column prop="email" label="email" width="300" />
        <el-table-column prop="gender" label="gender" />
      </el-table>
    </el-main>

    <el-main>
      <h6>开发工程师</h6>
      <el-table :data="developlist" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="180" />
        <el-table-column prop="username" label="Username" width="180" />
        <el-table-column prop="nickname" label="Nickname" width="300" />
        <el-table-column prop="email" label="email" width="300" />
        <el-table-column prop="gender" label="gender" />
      </el-table>
    </el-main>

    <el-main>
      <h6>质量保证工程师</h6>
      <el-table :data="qualitylist" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="ID" width="180" />
        <el-table-column prop="username" label="Username" width="180" />
        <el-table-column prop="nickname" label="Nickname" width="300" />
        <el-table-column prop="email" label="email" width="300" />
        <el-table-column prop="gender" label="gender" />
      </el-table>
    </el-main>
  </main>
</template>

<script>
import { getpartner } from '@/utils/com_ui'

export default {
  name: 'PartnerList',
  components: {},
  props: {
    visible: {
      type: Boolean,
      default: () => false
    }
  },
  data() {
    return {
      systemlist: [],
      developlist: [],
      qualitylist: []
    }
  },
  methods: {},
  watch: {
    visible: {
      handler(visible) {
        if (visible === true) {
          getpartner(this)
        } else {
          this.systemlist = []
          this.developlist = []
          this.qualitylist = []
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
