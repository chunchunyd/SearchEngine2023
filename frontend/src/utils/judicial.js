import axios from 'axios'

export function search(_this, par) {
  axios.get('/api/text_search/', {
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
      _this.status = 1
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function searchpage(_this, par, page) {
  axios.get('/api/text_search/', {
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

function getcarddata(_this) {
  axios.get('/api/court/' + _this.court + '/', {
    params: {
    }
  }).then((response) => {
    const d = response.data
    if (response.status === 200) {
      _this.courtdata = d
      _this.status += 1
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
  _this.judgedata = []
  //  遍历_this.judge数组
  for (let i = 0; i < _this.judge.length; i++) {
    axios.get('/api/judge/' + _this.judge[i] + '/', {
      params: {
      }
    }).then((response) => {
      const d = response.data
      if (response.status === 200) {
        _this.judgedata.push(d)
        _this.status += 1
      } else {
        _this.$alert('error!')
      }
    }).catch(function (error) {
      console.log(error)
      _this.$alert('error!')
    })
  }
}

export function getxml(_this, addr) {
// 获得xml数据，并解析（展示时根据doctype展示）
  axios.get('/' + addr, {
    params: {
    }
  }).then((response) => {
    const d = response.data
    if (response.status === 200) {
      _this.xml_data = d
      _this.parsexml()
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })

  // 串行获得doc_type，根据doc_type并行解析数据、获得卡片信息等
  axios.get('/api/document/', {
    params: {
      address: addr
    }
  }).then((response) => {
    const d = response.data
    if (response.status === 200) {
      _this.type = d.results[0].doc_type
      if (_this.type === '判决书' || _this.type === '裁定书' || _this.type === '调解书' || _this.type === '决定书' || _this.type === '应诉通知书' || _this.type === '起诉状') {
        axios.get('/api/judgment/', {
          params: {
            address: addr
          }
        }).then((response) => {
          const d = response.data
          if (response.status === 200) {
            _this.court = d.results[0].court
            _this.judge = d.results[0].judge
            _this.status = -_this.judge.length
            getcarddata(_this)
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

export function searchcourt(_this) {
  axios.get('/api/court/', {
    params: {
    }
  }).then((response) => {
    const d = response.data
    if (response.status === 200) {
      _this.data = d.results
      _this.totalnum = d.count
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function searchcourtpage(_this, page) {
  axios.get('/api/court/', {
    params: {
      offset: (page - 1) * 10
    }
  }).then((response) => {
    const d = response.data
    if (response.status === 200) {
      _this.data = d.results
      _this.totalnum = d.count
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}
export function searchjudge(_this) {
  axios.get('/api/judge/', {
    params: {
    }
  }).then((response) => {
    const d = response.data
    if (response.status === 200) {
      _this.data = d.results
      _this.totalnum = d.count
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function searchjudgepage(_this, page) {
  axios.get('/api/judge/', {
    params: {
      offset: (page - 1) * 10
    }
  }).then((response) => {
    const d = response.data
    if (response.status === 200) {
      _this.data = d.results
      _this.totalnum = d.count
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getrelatedata(_this, type, id) {
  let par = {}
  if (type === 0) {
    par = {
      court_id: id
    }
  } else {
    par = {
      judge: id
    }
  }
  axios.get('/api/judgment/', {
    params: par
  }).then((response) => {
    const d = response.data
    if (response.status === 200) {
      _this.data = d.results
      _this.totalnum = d.count
      _this.status = 1
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}

export function getrelatedatapage(_this, type, id, page) {
  let par = {}
  if (type === 0) {
    par = {
      court_id: id,
      offset: (page - 1) * 10
    }
  } else {
    par = {
      judge: id,
      offset: (page - 1) * 10
    }
  }
  axios.get('/api/judgment/', {
    params: par
  }).then((response) => {
    const d = response.data
    if (response.status === 200) {
      _this.data = d.results
      _this.totalnum = d.count
    } else {
      _this.$alert('error!')
    }
  }).catch(function (error) {
    console.log(error)
    _this.$alert('error!')
  })
}
