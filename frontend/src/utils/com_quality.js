// com_system.js 中用于develop engineer部分
import CookieOperation from './tools'
import axios from 'axios'

export function getIrList(_this) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/IRequest/', {
    params: {
      proj_id: projid
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.ir = response.data
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getMyIr(_this) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const username = CookieOperation.getCookie('username', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/IRequest/', {
    params: {
      proj_id: projid,
      ir_sr__developer_id__username: username
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      let tempir = []
      tempir = response.data
      _this.filter(tempir)
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getsprint(_this) {
  // 获取系统服务
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/Iteration/', {
    params: {
      proj_id: projid
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.sprintlist = response.data
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getSprintSr(_this, id) {
  // 获得对应迭代id的所有sr
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/SRequest/', {
    params: {
      ir_id__proj_id: projid,
      iteration_id: id
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.sr = response.data
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getMr(_this) {
  // 获得对应项目的所有mr
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/MR/', {
    params: {
      proj_id: projid
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.mr = response.data
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function modifyTarget(_this, data) {
  // 修改mr指向的sr
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.patch('api/MR/' + data.mrid + '/', {
    target_sr: data.srid
  }, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.$alert('关联成功!')
      _this._reload()
      _this._cancel()
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getIssue(_this) {
  // 获得对应项目的所有issue
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/Issue/', {
    params: {
      proj_id: projid
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.issue = response.data
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getSr(_this) {
  // 获得所有sr
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/SRequest/', {
    params: {
      ir_id__proj_id: projid
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.sr = response.data
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getSrMr(_this, srid) {
  // 获得对应Sr的所有mr
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/MR/', {
    params: {
      proj_id: projid,
      target_sr: srid
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.sr_mr = response.data
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getIssueMr(_this, issueid) {
  // 获得对应Issue的所有mr
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/MR/', {
    params: {
      proj_id: projid,
      target_issue: issueid
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.issue_mr = response.data
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}
