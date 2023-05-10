<template>
  <div id="service" class="Services" v-show="visible">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <div class="titlepage">
            <h3>项目列表</h3>
            <p>请选择您要进入的项目</p>
          </div>
        </div>
      </div>
      <div class="row">
        <div
          v-for="item in my_project"
          :key="item"
          class="col-xl-4 col-lg-4 col-md-4 col-sm-12"
        >
          <div class="Services-box">
            <i
              ><img
                src="../../../public/project_icon.png"
                alt="#"
                v-on:click="change_project(item.project_name, item.id)"
            /></i>
            <h3>{{ item.project_name }}</h3>
            <p>项目ID：{{ item.id }}</p>
            <p>创建者：{{ item.owner }}</p>
            <p>创建时间：{{ datetime(item.create_date) }}</p>
          </div>
        </div>
      </div>
      <a class="project_more" v-on:click="create_project">创建项目</a>
      <a class="project_more" v-on:click="join_project">申请加入</a>
      <a class="project_more" v-on:click="_reload">刷新</a>
    </div>

    <CreateProjectDialog
      :dialogVisible="create_dialogVisible"
      :_cancel="create_cancel"
    ></CreateProjectDialog>

    <JoinProjectDialog
      :dialogVisible="join_dialogVisible"
      :_cancel="join_cancel"
    ></JoinProjectDialog>
  </div>
</template>

<script>
import CookieOperation from '@/utils/tools'
import CreateProjectDialog from '@/components/proj/CreateProjectDialog.vue'
import JoinProjectDialog from '@/components/proj/JoinProjectDialog.vue'
import { getRole } from '@/utils/com_main.js'

export default {
  name: 'ProjectList',
  components: {
    CreateProjectDialog,
    JoinProjectDialog
  },
  props: {
    listvisible: {
      type: Boolean,
      default: () => false
    },
    my_project: {
      type: Array,
      default: () => []
    },
    _changeproject: {
      type: Function,
      default: () => {}
    },
    _reload: {
      type: Function,
      default: () => {}
    }
  },
  computed: {
    visible: function () {
      return this.listvisible
    }
  },
  data() {
    return {
      // prj:所有项目
      prj: [],
      create_dialogVisible: false,
      join_dialogVisible: false
    }
  },
  methods: {
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
    create_project: function () {
      // 创建新的项目
      if (this.create_dialogVisible === false) {
        this.create_dialogVisible = true
      } else {
        this.create_dialogVisible = false
      }
    },
    create_cancel: function () {
      // 回调函数
      this.create_dialogVisible = false
    },
    join_cancel: function () {
      // 回调函数
      this.join_dialogVisible = false
    },
    join_project: function () {
      // 加入新的项目
      if (this.join_dialogVisible === false) {
        this.join_dialogVisible = true
      } else {
        this.join_dialogVisible = false
      }
    },
    change_project: function (projname, projid) {
      // 切换到项目，首先要获得用户在此项目中的角色
      getRole(this, projid, projname)
    }
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === true) {
          CookieOperation.setCookie('projid', 0, 0)
        }
      }
    }
  }
}
</script>

<style scoped></style>
