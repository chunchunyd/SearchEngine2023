<template>
  <div class="main">
    <!--下面是顶部菜单栏-->
    <div class="container-fluid">
      <div class="row bg-secondary py-1 px-lg-5">
        <div class="col-lg-6 text-center py-2 text-lg-left">
          <h2 class="white">Promanager</h2>
        </div>
        <div class="col-lg-6 text-center py-1_5 text-lg-right">
          <div class="d-inline-flex align-items-center">
            <label v-if="username_valid == true" class="text-white px-3"
              >您好,{{ nickname }}!</label
            >
            <label v-else class="text-white px-3">您还没有登录！</label>
            <label v-if="username_valid == false" class="text-white px-3">
              <router-link to="/">回到主页</router-link>
            </label>
            <label v-else-if="role_valid == false" class="text-white px-3"
              >请选择项目</label
            >
            <label v-else class="text-white px-3"
              >当前项目：{{ this.project_name }}</label
            >
            <label
              v-if="role_valid && this.role == 'system'"
              class="text-white px-3"
              >您的角色：系统工程师</label
            >
            <label
              v-if="role_valid && this.role == 'develop'"
              class="text-white px-3"
              >您的角色：开发工程师</label
            >
            <label
              v-if="role_valid && this.role == 'quality'"
              class="text-white px-3"
              >您的角色：质量保证工程师</label
            >
            <label class="text-white px-3" v-on:click="setting">设置</label>
            <div>
              <el-avatar :src="avatar" size="large" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <!--顶部菜单栏结束-->
    <MenuBar :manage_project="manage_project" />

    <ProjectList
      :my_project="my_project"
      :listvisible="project_list_visible"
      :_changeproject="project_change"
      :_reload="project_reload"
    ></ProjectList>

    <SettingDialog
      :dialogVisible="setting_dialogVisible"
      :_cancel="setting_cancel"
      :username="username"
      :_nickname="nickname"
      :_email="email"
      :_gitid="gitid"
      :_gender="gender"
      :_changeinfo="setting_info"
      :_changepw="setting_pw"
      :_changeavatar="setting_avatar"
    ></SettingDialog>

    <SystemDash :visible="systemdash_visible" />

    <DevelopDash :visible="developdash_visible" />

    <QualityDash :visible="qualitydash_visible" />

  </div>
</template>

<script>
import CookieOperation from '@/utils/tools'
import ProjectList from '@/components/proj/ProjectList.vue'
import SettingDialog from '@/components/user/SettingDialog.vue'
import MenuBar from '@/components/ui/MenuBar.vue'
import SystemDash from '@/components/system/SystemDash.vue'
import DevelopDash from '@/components/develop/DevelopDash.vue'
import QualityDash from '@/components/quality/QualityDash.vue'
import { getMyProject } from '@/utils/com_main'
import { getinfo, getavatar } from '@/utils/com_user.js'

export default {
  name: 'HomeView',
  components: {
    ProjectList,
    SettingDialog,
    MenuBar,
    SystemDash,
    DevelopDash,
    QualityDash
  },
  data() {
    return {
      // 组件可视
      setting_dialogVisible: false,
      project_list_visible: true,
      systemdash_visible: false,
      developdash_visible: false,
      qualitydash_visible: false,
      // 个人信息
      username: '',
      username_valid: false,
      nickname: '',
      email: '',
      gender: '',
      avatar: '',
      gitid: '',
      // 项目有关
      role: '',
      project_name: '',
      role_valid: false,
      my_project: [], // my_project是该用户的所有参与的项目，每一项{"project_name":...,"user_role":...,'discription':...}
      // 测试有关
      online: false
    }
  },
  beforeCreate() {
    // 设置背景颜色
    document.querySelector('body').setAttribute('style', 'background: #dddddd')
  },
  mounted() {
    const usr = CookieOperation.getCookie('username', 'NAN')
    if (usr !== 'NAN') {
      this.username = usr
      this.username_valid = true
      getinfo(this)
    }
  },
  methods: {
    // 项目有关
    project() {
      getMyProject(this)
      this.project_dialogVisible = true
    },
    project_cancel() {
      this.project_dialogVisible = false
    },
    project_post(info) {
      // projectdialog确定时调用回调函数
      this.project_name = info[0]
      this.role = info[1]
      this.role_valid = true
    },
    project_change(projname, role) {
      this.project_name = projname
      this.role = role
      this.role_valid = true
    },
    manage_project() {
      // 显示项目列表
      getMyProject(this)
      this.project_name = ''
      this.role = ''
      this.role_valid = ''
    },
    project_reload() {
      getMyProject(this)
    },
    // 设置相关
    setting_cancel() {
      this.setting_dialogVisible = false
    },
    setting() {
      this.setting_dialogVisible = true
    },
    setting_info() {
      getinfo(this)
      this.setting_dialogVisible = false
    },
    setting_pw() {
      this.username_valid = false
      this.setting_dialogVisible = false
    },
    setting_avatar() {
      this.setting_dialogVisible = false
      getavatar(this)
      getinfo(this)
    }
  },
  watch: {
    role: {
      handler(newrole) {
        if (newrole === 'system') {
          this.project_list_visible = false
          this.systemdash_visible = true
          this.developdash_visible = false
          this.qualitydash_visible = false
        } else if (newrole === 'develop') {
          this.project_list_visible = false
          this.systemdash_visible = false
          this.developdash_visible = true
          this.qualitydash_visible = false
        } else if (newrole === 'quality') {
          this.project_list_visible = false
          this.systemdash_visible = false
          this.developdash_visible = false
          this.qualitydash_visible = true
        } else {
          this.project_list_visible = true
          this.systemdash_visible = false
          this.developdash_visible = false
          this.qualitydash_visible = false
        }
      }
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/css/style.css';
@import 'https://fonts.googleapis.com/css2?family=Nunito+Sans&family=Nunito:wght@600;700;800&display=swap';
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #ffffff;
}
label {
  color: #d8142e;
  font-weight: bold;
}
</style>
