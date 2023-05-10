// com_user.js中的函数用于 用户注册、登录、修改个人信息时与后端的通信
import axios from 'axios'
import {
  myhash
} from '@/utils/hash'
import CookieOperation from '@/utils/tools'
import {
  getMyProject
} from './com_main'

export function getuserid(_this, username) {
  // 在cookie里存user的id
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('/api/Search/' + username + '/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      CookieOperation.setCookie('userid', response.data.id, 1e9)
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function comlogin(_this) {
  axios.post('/api/authorizations/', {
    username: _this.id,
    password: myhash(_this.pw)
  }).then((response) => {
    const data = response.data
    if (response.status === 200) {
      const user = data.username
      const token = data.token
      _this.login_post(user, token)
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('登陆失败!')
  })
}

export function comreg(_this) {
  axios.get('api/usernames/' + _this.form.id + '/count/')
    .then((response) => {
      if (response.status === 200) {
        if (response.data.count === 1) {
          _this.$alert('用户名已存在！')
        } else {
          axios.post('/api/Register/', {
            username: _this.form.id,
            password: myhash(_this.form.pw),
            nickname: _this.form.nickname,
            email: _this.form.mailbox,
            gender: _this.form.sex
          }).then((response) => {
            if (response.status === 201) {
              _this.$alert('注册成功!欢迎您,' + _this.form.id)
              _this.cancel()
            } else {
              _this.$alert('注册失败!')
            }
          }).catch(function (error) {
            console.log(error)
            _this.$alert('注册失败!')
          })
        }
      } else {
        _this.$alert('注册失败!')
      }
    }).catch(function (error) {
      console.log(error)
      _this.$alert('注册失败!')
    })
}

export function getinfo(_this) {
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('/api/Search/' + _this.username + '/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.nickname = response.data.nickname
      _this.email = response.data.email
      _this.gender = response.data.gender
      _this.gitid = response.data.git_id
      if (_this.username_valid === true) {
        getMyProject(_this)
        getavatar(_this)
      }
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function changeinfo(_this) {
  let data
  // 先判断需要修改的是哪个
  if (_this.value === 'nickname') {
    data = {
      nickname: _this.nickname,
      gender: _this._gender,
      email: _this._email
    }
  } else if (_this.value === 'gender') {
    data = {
      nickname: _this._nickname,
      gender: _this.gender,
      email: _this._email
    }
  } else if (_this.value === 'email') {
    data = {
      nickname: _this._nickname,
      gender: _this._gender,
      email: _this.email
    }
  } else if (_this.value === 'gitid') {
    data = {
      git_id: _this.gitid
    }
  } else return
  const userid = CookieOperation.getCookie('userid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.put('/api/UserDetail/' + userid + '/', data, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this._changeinfo() // 告知父部件修改成功，以更新前端信息
      _this.$alert('修改成功!')
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function changepassword(_this) {
  const userid = CookieOperation.getCookie('userid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.put('/api/ChangePswd/' + userid + '/', {
    old_password: myhash(_this.oldpw),
    password: myhash(_this.newpw)
  }, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this._changepw() // 告知父部件修改成功，以更新前端信息
      _this.$alert('修改成功!')
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function changeavatar(_this) {
  const userid = CookieOperation.getCookie('userid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.put('/api/UserDetail/' + userid + '/', _this.avatar, {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this._changeavatar() // 告知父部件修改成功，以更新前端信息
      _this.$alert('修改成功!')
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getavatar(_this) {
  const userid = CookieOperation.getCookie('userid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('/api/UserDetail/' + userid + '/', {
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.avatar = response.data.avatar
    }
  }).catch(function (error) {
    console.log(error)
  })
}
