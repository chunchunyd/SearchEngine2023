// com_user.js中的函数用于 用户注册、登录、修改个人信息时与后端的通信
import axios from 'axios'

export function search(_this, par) {
  axios.get('/api/text_search', {
    params: {
      query: par
    }
  }).then((response) => {
    const d = response.data
    if (response.status === 200) {
      _this.data = d.result.doc_list
      _this.totalnum = d.result.total_page * 10
      _this.matchkey = d.result.word_list
      _this.computehighlight()
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function searchpage(_this, par, page) {
  axios.get('/api/text_search', {
    params: {
      query: par,
      page: page
    }
  }).then((response) => {
    const d = response.data
    if (response.status === 200) {
      _this.data = d.result.doc_list
      _this.totalnum = d.result.total_page * 10
      _this.matchkey = d.result.word_list
      _this.computehighlight()
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getxml(_this, addr) {
  axios.get('/' + addr, {
    params: {
    }
  }).then((response) => {
    const d = response.data
    if (response.status === 200) {
      _this.xml_data = d
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}
