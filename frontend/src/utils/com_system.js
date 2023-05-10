// com_system.js 中用于system engineer部分
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

export function createIr(_this, createdata) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.post('api/IRequest/', {
    proj_id: projid,
    ir_name: createdata.irname,
    description: createdata.irdescrip
  }, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 201) {
      _this.$alert('IR添加成功!')
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

export function deleteIr(_this, irid) {
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.delete('api/IRequest/' + irid + '/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 204) {
      _this.$alert('删除成功!')
      _this.reload()
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function modifyIr(_this, modifydata) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.put('api/IRequest/' + modifydata.irid + '/', {
    proj_id: projid,
    ir_name: modifydata.irname,
    description: modifydata.irdescrip
  }, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.$alert('IR修改成功!')
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

export function getservice(_this) {
  // 获取系统服务
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/SystemService/', {
    params: {
      proj_id: projid
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.servicelist = response.data
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function createservice(_this, createdata) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.post('api/SystemService/', {
    proj_id: projid,
    service_name: createdata.servicename,
    description: createdata.servicedescrip
  }, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 201) {
      _this.$alert('系统服务添加成功!')
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

export function getservicedetail(_this, serviceid) {
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/SystemService/' + serviceid + '/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.servicename = response.data.service_name
      _this.servicedescrip = response.data.description
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function modifyservice(_this, modifydata) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.put('api/SystemService/' + modifydata.serviceid + '/', {
    proj_id: projid,
    service_name: modifydata.servicename,
    description: modifydata.servicedescrip
  }, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.$alert('系统服务修改成功!')
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

export function deleteservice(_this, serviceid) {
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.delete('api/SystemService/' + serviceid + '/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 204) {
      _this.$alert('删除成功!')
      _this._cancel()
      _this._reload()
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

export function createsprint(_this, createdata) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.post('api/Iteration/', {
    proj_id: projid,
    it_name: createdata.sprintname,
    description: createdata.sprintdescrip
  }, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 201) {
      _this.$alert('迭代计划添加成功!')
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

export function getsprintdetail(_this, sprintid) {
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/Iteration/' + sprintid + '/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.sprintname = response.data.it_name
      _this.sprintdescrip = response.data.description
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function modifysprint(_this, modifydata) {
  const projid = CookieOperation.getCookie('projid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.put('api/Iteration/' + modifydata.sprintid + '/', {
    proj_id: projid,
    it_name: modifydata.sprintname,
    description: modifydata.sprintdescrip
  }, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.$alert('迭代计划修改成功!')
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

export function deletesprint(_this, sprintid) {
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.delete('api/Iteration/' + sprintid + '/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 204) {
      _this.$alert('删除成功!')
      _this._cancel()
      _this._reload()
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function createSr(_this, createdata) {
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.post('api/SRequest/', {
    ir_id: createdata.irid,
    sr_name: createdata.srname,
    description: createdata.srdescrip,
    iteration_id: createdata.iteration_id,
    service_id: createdata.service_id
  }, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 201) {
      _this.$alert('SR添加成功!')
      _this._reload()
      _this._cancel()
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('SR编号重复或其它错误!')
  })
}

export function deleteSr(_this, srid) {
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.delete('api/SRequest/' + srid + '/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 204) {
      _this.$alert('删除成功!')
      _this.reload()
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function modifySr(_this, modifydata) {
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.patch('api/SRequest/' + modifydata.srid + '/', {
    sr_name: modifydata.srname,
    description: modifydata.srdescrip,
    iteration_id: modifydata.iteration_id,
    service_id: modifydata.service_id
  }, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 201) {
      _this.$alert('SR修改成功!')
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

export function allocateSr(_this, allocdata) {
  const userid = CookieOperation.getCookie('userid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.patch('api/SRequest/' + allocdata.srid + '/', {
    distributor_id: userid,
    developer_id: allocdata.alloc_id
  }, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 201) {
      _this.$alert('SR分派成功!')
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
