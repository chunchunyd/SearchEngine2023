<template>
  <main role="main" class="col-md-10 pt-3 px-4" v-show="visible">
    <el-header><h4>项目概况</h4></el-header>
    <el-button type="primary" plain v-if="is_owner" v-on:click="modify"
      >修改</el-button
    >
    <el-button type="primary" plain v-if="is_owner" v-on:click="del"
      >删除</el-button
    >
    <el-button type="primary" plain v-if="is_owner" v-on:click="webhook"
      >Webhook</el-button
    >
    <el-main>
      <el-descriptions size="large" span="1" border v-loading="loading">
        <el-descriptions-item label="项目名称" width="50px">{{
          this.projname
        }}</el-descriptions-item>
        <el-descriptions-item label="项目ID" width="50px">{{
          this.id
        }}</el-descriptions-item>
        <el-descriptions-item label="拥有者" width="50px">{{
          owner
        }}</el-descriptions-item>
        <el-descriptions-item label="创建日期" width="50px">{{
          datetime(createdate)
        }}</el-descriptions-item>
        <el-descriptions-item label="工程师数目" width="50px">{{
          engineernum
        }}</el-descriptions-item>
        <el-descriptions-item label="Gitlab ID" width="50px">{{
          git_id
        }}</el-descriptions-item>
        <el-descriptions-item v-if="is_owner" label="邀请码" width="50px">{{
          propswd
        }}</el-descriptions-item>
        <el-descriptions-item label="描述" width="50px"
          >{{ description }}
        </el-descriptions-item>
      </el-descriptions>
    </el-main>

    <el-main>
      <el-divider>
        <el-icon><star-filled /></el-icon>
      </el-divider>
      <el-collapse v-model="activeName">
        <el-collapse-item name="1">
          <template #title>
            Tips1:如何与Gitlab Repo关联?<el-icon class="header-icon">
              <info-filled />
            </el-icon>
          </template>
          <el-table :data="notice1" style="width: 100%">
            <el-table-column prop="name" label="名称" width="150" />
            <el-table-column prop="func" label="功能" width="500" />
            <el-table-column prop="method" label="如何获取、使用" width="700" />
            <el-table-column prop="style" label="格式" />
          </el-table>
        </el-collapse-item>
        <el-collapse-item name="2">
          <template #title>
            Tips2:如何使用关联的Gitlab Repo功能<el-icon class="header-icon">
              <info-filled />
            </el-icon>
          </template>
          <el-table :data="notice2" style="width: 100%">
            <el-table-column prop="user" label="用户" width="180" />
            <el-table-column prop="func" label="支持的功能" width="500" />
            <el-table-column prop="type" label="类型" width="180" />
            <el-table-column prop="style" label="格式" />
          </el-table>
        </el-collapse-item>
      </el-collapse>
    </el-main>

    <el-dialog
      v-model="webhook_dialogVisible"
      title="Gitlab Webhook"
      width="70%"
      :before-close="handleClose"
    >
      <el-descriptions class="margin-top" :column="1" :size="size" border>
        <template #extra>
          <el-button type="success" v-on:click="newwebhook"
            >生成新Webhook</el-button
          >
        </template>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon :style="iconStyle">
                <location />
              </el-icon>
              Webhook Path
            </div>
          </template>
          https://front-end-teamliquid.app.secoder.net/api/payload/{{
            webhook_path
          }}/
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon :style="iconStyle">
                <office-building />
              </el-icon>
              Webhook Token
            </div>
          </template>
          {{ webhook_token }}
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="webhook_dialogVisible = false"
            >确认</el-button
          >
        </span>
      </template>
    </el-dialog>

    <ModifyProjectDialog
      :_cancel="modify_cancel"
      :_reload="reload"
      :dialogVisible="modify_dialogVisible"
      :o_descrip="modify_descrip"
      :o_name="modify_name"
      :o_pswd="modify_pswd"
      :o_id="modify_id"
      :o_token="modify_token"
      :o_home="modify_home"
    />
  </main>
</template>

<script>
import ModifyProjectDialog from './ModifyProjectDialog.vue'
import {
  getprodetail,
  getpropswd,
  deleteproj,
  getwebhook,
  genwebhook
} from '@/utils/com_ui'
import CookieOperation from '@/utils/tools'
import {
  StarFilled,
  InfoFilled,
  Location,
  OfficeBuilding
} from '@element-plus/icons-vue'

export default {
  name: 'IntroduceTable',
  components: {
    ModifyProjectDialog,
    StarFilled,
    InfoFilled,
    Location,
    OfficeBuilding
  },
  props: {
    visible: {
      type: Boolean,
      default: () => false
    }
  },
  data() {
    return {
      id: '',
      owner: '',
      createdate: '',
      description: '',
      engineernum: '',
      projname: '',
      // 是否是创建者
      is_owner: false,
      propswd: '',
      git_id: '',
      git_home: '',
      git_token: '',
      // 修改项目信息
      modify_dialogVisible: false,
      modify_name: '',
      modify_descrip: '',
      modify_pswd: '',
      modify_id: '',
      modify_token: '',
      modify_home: '',
      // webhook
      webhook_dialogVisible: false,
      webhook_path: '',
      webhook_token: '',
      // notice
      notice1: [
        {
          name: 'Gitlab home',
          func: '项目使用的Gitlab站点的HOME地址',
          method:
            '将使用的Gitlab仓库HOME地址填入',
          style: 'https://gitlab.secoder.net/'
        },
        {
          name: 'Gitlab ID',
          func: '项目在Gitlab中对应项目的ID',
          method:
            '在Gitlab项目中查看ID,点击“修改”并将其填入',
          style: '12345678'
        },
        {
          name: 'Gitlab Token',
          func: 'Gitlab项目密钥，用于ProManager主动从Gitlab拉取数据',
          method:
            '在Gitlab的个人偏好界面"Acess Token"选项卡中生成Token,点击“修改”并将其填入',
          style: 'No fixed format'
        },
        {
          name: 'Webhook Path',
          func: 'Webhook的目标，用于Gitlab向ProManager提供实时变动数据',
          method:
            '点击"Webhook"键生成，在Gitlab的项目设置中新建Webhook并填入',
          style: 'https://front-end-teamliquid.app.secoder.net/api/payload/xxx'
        },
        {
          name: 'Webhook Token',
          func: 'Webhook的密钥，用于验证身份信息',
          method:
            '点击"Webhook"键生成，在Gitlab的项目设置中新建Webhook并填入',
          style: 'No fixed format'
        }
      ],
      notice2: [
        {
          user: '开发工程师',
          func: '基于commit修改功能需求SR状态,包括[init,undergo,done]',
          type: 'commit',
          style: '@sr:SR.001.001@ @state:init（将SR.001.001状态置为init）'
        },
        {
          user: '开发工程师',
          func: '将Merge Request与功能需求SR关联',
          type: 'Merge Request',
          style: '@sr:SR.001.001@（MR合并后会自动将SR.001.001状态置为done）'
        },
        {
          user: '开发工程师',
          func: '将Merge Request与Issue关联',
          type: 'Merge Request',
          style: '#xx（xx为issue在Gitlab项目中的编号）'
        },
        {
          user: '任何人',
          func: '将Issue与功能需求SR关联',
          type: 'Issue',
          style: '@sr:SR.001.001@（指明该issue为SR.001.001的缺陷）'
        }
      ]
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
    del: function () {
      // 删除项目
      if (confirm('确定要删除整个项目吗?') === true) {
        deleteproj(this)
      }
    },
    modify_cancel: function () {
      // 修改项目信息回调函数
      this.modify_dialogVisible = false
    },
    modify: function () {
      if (this.modify_dialogVisible === false) {
        this.modify_name = this.projname
        this.modify_descrip = this.description
        this.modify_pswd = this.propswd
        this.modify_id = this.git_id
        this.modify_token = this.git_token
        this.modify_home = this.git_home
        this.modify_dialogVisible = true
      } else {
        this.modify_dialogVisible = false
      }
    },
    reload: function () {
      getprodetail(this)
      if (
        this.visible === true &&
        this.owner === CookieOperation.getCookie('username', 'NAN')
      ) {
        getpropswd(this)
        this.is_owner = true
      } else {
        this.is_owner = false
      }
    },
    webhook() {
      getwebhook(this)
      this.webhook_dialogVisible = true
    },
    newwebhook() {
      genwebhook(this)
    },
    handleClose() {
      this.webhook_dialogVisible = false
    }
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === true) {
          getprodetail(this)
        } else {
          this.id = ''
          this.owner = ''
          this.createdate = ''
          this.description = ''
          this.engineernum = ''
          this.projname = ''
        }
      }
    },
    owner: {
      handler(owner) {
        if (
          this.visible === true &&
          owner === CookieOperation.getCookie('username', 'NAN')
        ) {
          getpropswd(this)
          this.is_owner = true
        } else {
          this.is_owner = false
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
