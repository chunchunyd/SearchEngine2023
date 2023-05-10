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

export function changeSRstate(_this, changedata) {
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.put('api/SRState/' + changedata.srid + '/', {
    state: changedata.newstate
  }, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.$alert('SR状态修改成功!')
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
