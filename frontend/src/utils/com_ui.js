// 项目概况和人员列表
import axios from 'axios'
import CookieOperation from '@/utils/tools'

export function getprodetail(_this) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('/api/Project/' + projid + '/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      const data = response.data
      _this.id = data.id
      _this.owner = data.owner
      _this.createdate = data.create_date
      _this.description = data.description
      _this.engineernum = data.engineer.length
      _this.projname = data.project_name
      _this.git_id = data.git_id
      _this.git_home = data.git_home
      _this.git_token = data.git_token
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getvisibledetail(_this) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('/api/Project/' + projid + '/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      const data = response.data
      _this.projname = data.project_name
      _this.irnum = data.ir_num.total_num
      _this.irnum_raw = data.ir_num.raw_num
      _this.irnum_init = data.ir_num.init_num
      _this.irnum_undergo = data.ir_num.undergo_num
      _this.irnum_done = data.ir_num.done_num
      _this.srnum = data.sr_num.total_num
      _this.srnum_init = data.sr_num.init_num
      _this.srnum_undergo = data.sr_num.undergo_num
      _this.srnum_done = data.sr_num.done_num
      _this.finish += 1
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })

  axios.get('/api/Enrolled/', {
    params: {
      proj_id: projid,
      ordering: '-sr_allocated'
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      const data = response.data
      _this.sr_alloc = data
      _this.finish += 1
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })

  axios.get('/api/Enrolled/', {
    params: {
      proj_id: projid,
      ordering: '-sr_done'
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      const data = response.data
      _this.sr_done = data
      _this.finish += 1
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })

  axios.get('/api/Enrolled/', {
    params: {
      proj_id: projid,
      ordering: 'sr_avg_time'
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      const data = response.data
      _this.sr_time = data
      _this.finish += 1
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })

  axios.get('/api/Enrolled/', {
    params: {
      proj_id: projid,
      ordering: '-mr_merged'
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      const data = response.data
      _this.mr = data
      _this.finish += 1
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })

  axios.get('/api/Enrolled/', {
    params: {
      proj_id: projid,
      ordering: '-commit_submitted'
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      const data = response.data
      _this.commit = data
      _this.finish += 1
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })

  axios.get('/api/Enrolled/', {
    params: {
      proj_id: projid,
      ordering: '-lines_total'
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      const data = response.data
      _this.line = data
      _this.finish += 1
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })

  axios.get('/api/Enrolled/', {
    params: {
      proj_id: projid,
      ordering: '-issue_allocated'
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      const data = response.data
      _this.issue = data
      _this.finish += 1
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })

  axios.get('/api/Enrolled/', {
    params: {
      proj_id: projid,
      ordering: '-issue_done'
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      const data = response.data
      _this.issue_done = data
      _this.finish += 1
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })

  axios.get('/api/Enrolled/', {
    params: {
      proj_id: projid,
      ordering: 'issue_avg_time'
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      const data = response.data
      _this.issue_time = data
      _this.finish += 1
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })

  axios.get('/api/ProjectChangeLog/', {
    params: {
      proj_id: projid
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      const data = response.data
      _this.log = data
      _this.finish += 1
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getpropswd(_this) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('/api/ProjectPswd/' + projid + '/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      const data = response.data
      _this.propswd = data.password
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function deleteproj(_this) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.delete('/api/Project/' + projid + '/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 204) {
      _this.$alert('项目已删除！')
      _this.$parent.$parent.role = ''
      _this.$parent.$parent.role_valid = false
      _this.$parent.$parent.project_reload()
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function modifyproj(_this, modifydata) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.patch('/api/Project/' + projid + '/', {
    project_name: modifydata.project_name,
    password: modifydata.pswd,
    description: modifydata.description,
    git_id: modifydata.git_id,
    git_home: modifydata.git_home,
    git_token: modifydata.git_token
  }, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.$alert('修改成功！')
      _this._cancel()
      _this._reload()
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('项目名称重复或者其它错误')
  })
}

export function getpartner(_this) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  // 获取系统工程师
  axios.get('/api/Userlist/', {
    params: {
      proj_id: projid,
      user_role: 'system'
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.systemlist = response.data
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
  // 获取开发工程师
  axios.get('/api/Userlist/', {
    params: {
      proj_id: projid,
      user_role: 'develop'
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.developlist = response.data
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
  // 获取质量保证工程师
  axios.get('/api/Userlist/', {
    params: {
      proj_id: projid,
      user_role: 'quality'
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.qualitylist = response.data
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getwebhook(_this) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('/api/Project/' + projid + '/WebhookToken/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.webhook_path = response.data.git_webhook_path
      _this.webhook_token = response.data.git_webhook_token
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('无法获得Webhook!')
  })
}

export function genwebhook(_this) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.post('/api/Project/' + projid + '/WebhookToken/', {}, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 201) {
      _this.webhook_path = response.data.webhook_path
      _this.webhook_token = response.data.webhook_token
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('无法生成Webhook!')
  })
}
