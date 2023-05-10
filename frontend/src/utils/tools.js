export function checkform(str) {
  const reg = /^[a-zA-Z0-9_-]{5,20}$/
  if (!reg.test(str)) {
    return false
  }
  return true
}

export function checkmail(str) {
  const reg = /^[A-Za-zd0-9]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z]{2,5}$/
  if (!reg.test(str)) {
    return false
  }
  return true
}

const CookieOperation = {
  getCookie: (key, defaultValue) => {
    const rgx = new RegExp('(?:^|(?:; ))' + key + '=([^;]*)')
    const result = document.cookie.match(rgx)
    if (result) {
      return unescape(result[1])
    } else {
      return defaultValue
    }
  },
  setCookie: (key, value, expire) => {
    const exdate = new Date()
    exdate.setTime(exdate.getTime() + expire)
    document.cookie = key + '=' + escape(value) + ';expires=' + exdate.toGMTString()
  }
}

export default CookieOperation
