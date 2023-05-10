// 获得用户参与的所有项目及角色及项目简介
import axios from 'axios'
import CookieOperation from './tools'

// 获得用户参与的所有项目及角色及项目简介

export function getMyProject(_this) {
  const userid = CookieOperation.getCookie('userid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('/api/Project/', {
    params: {
      user1: userid
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this.my_project = response.data
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function createProject(_this, projdata) {
  const userid = CookieOperation.getCookie('userid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/Project/', {
    params: {
      owner_id: userid,
      project_name: projdata.project_name
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      if (response.data.length > 0) {
        _this.$alert('项目已存在！')
      } else {
        axios.post('/api/Project/', {
          project_name: projdata.project_name,
          description: projdata.description,
          owner: userid,
          password: projdata.invitecode
        }, {
          headers: {
            Authorization: header
          }
        }).then((response) => {
          if (response.status === 200) {
            const myid = response.data.id
            axios.post('/api/Enrolled/', {
              user_id: userid,
              proj_id: myid,
              user_role: projdata.role,
              proj_pswd: projdata.invitecode
            }, {
              headers: {
                Authorization: header
              }
            }).then((response) => {
              if (response.status === 201) {
                if (projdata.role === 'system') {
                  _this.$alert('项目创建成功，已经以系统工程师身份加入该项目！')
                } else if (projdata.role === 'develop') {
                  _this.$alert('项目创建成功，已经以开发工程师身份加入该项目！')
                } else if (projdata.role === 'quality') {
                  _this.$alert('项目创建成功，已经以质量保证工程师身份加入该项目！')
                }
                _this._cancel()
              } else {
                _this.$alert('error!')
              }
            }).catch(function (error) {
              console.log(error)
              _this.$alert('error!')
            })
            _this._cancel()
          } else {
            _this.$alert('error!')
          }
        }).catch(function (error) {
          console.log(error)
          _this.$alert('error!')
        })
      }
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function joinProject(_this, joindata) {
  const userid = CookieOperation.getCookie('userid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/Enrolled/', {
    params: {
      user_id: userid,
      proj_id: joindata.project_id
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      if (response.data.length > 0) {
        _this.$alert('您已加入该项目！')
      } else {
        axios.post('/api/Enrolled/', {
          user_id: userid,
          proj_id: joindata.project_id,
          user_role: joindata.user_role,
          proj_pswd: joindata.invitecode
        }, {
          headers: {
            Authorization: header
          }
        }).then((response) => {
          if (response.status === 201) {
            _this.$alert('加入项目成功！')
            _this._cancel()
          } else {
            _this.$alert('error!')
          }
        }).catch(function (error) {
          console.log(error)
          _this.$alert('项目不存在或其它错误!')
        })
      }
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getRole(_this, projid, projname) {
  // 切换项目时，通过此函数获得用户角色
  const userid = CookieOperation.getCookie('userid', 'NAN')
  const token = CookieOperation.getCookie('token', 'NAN')
  const header = 'JWT ' + token
  axios.get('api/Enrolled/', {
    params: {
      user_id: userid,
      proj_id: projid
    },
    headers: {
      Authorization: header
    }
  }).then((response) => {
    if (response.status === 200) {
      _this._changeproject(projname, response.data[0].user_role)
      // 将projid记录在cookie中
      CookieOperation.setCookie('projid', projid, 1e9)
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}
