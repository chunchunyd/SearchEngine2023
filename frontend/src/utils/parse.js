export function _ParseXml() {
  var stringContainingXMLSource = '<!DOCTYPE html> <html lang="en"> <head> <title>wuyujin1997</title> </head> <body> <div id="wyj"> <h2><a href="https://wuyujin.blog.csdn.net/">wuyujin1997 DOMParser demo</a></h2> </div> </body> </html>'
  var parser = new DOMParser()
  var doc = parser.parseFromString(stringContainingXMLSource, 'text/html')
  console.log('type: ', Object.prototype.toString.call(doc))
  console.log(doc)
  console.log(doc.querySelector('div#wyj'))
  console.log(doc.getElementById('wyj').textContent)
}

export function ParseXml(str) {
  var parser = new DOMParser()
  var doc = parser.parseFromString(str, 'text/xml')
  const data = {}
  var a
  try {
    a = doc.getElementsByTagName('QW')
    data.QW = a[0].attributes[1].value
  } catch (err) {
    data.QW = ''
  }
  try {
    a = doc.getElementsByTagName('WS')
    data.WS = a[0].attributes[1].value
  } catch (err) {
    data.WS = ''
  }
  try {
    a = doc.getElementsByTagName('WSZZDW')
    data.WSZZDW = a[0].attributes[1].value
  } catch (err) {
    data.WSZZDW = ''
  }
  try {
    a = doc.getElementsByTagName('FYWSZL')
    data.FYWSZL = a[0].attributes[1].value
  } catch (err) {
    data.FYWSZL = ''
  }
  try {
    a = doc.getElementsByTagName('JBFY')
    data.JBFY = a[0].attributes[1].value
  } catch (err) {
    data.JBFY = ''
  }
  try {
    a = doc.getElementsByTagName('FYCJM')
    data.FYCJM = a[0].attributes[1].value
  } catch (err) {
    data.FYCJM = ''
  }
  try {
    a = doc.getElementsByTagName('BZFYMC')
    data.BZFYMC = a[0].attributes[1].value
  } catch (err) {
    data.BZFYMC = ''
  }
  try {
    a = doc.getElementsByTagName('FYJB')
    data.FYJB = a[0].attributes[1].value
  } catch (err) {
    data.FYJB = ''
  }
  try {
    a = doc.getElementsByTagName('XZQH_P')
    data.XZQH_P = a[0].attributes[1].value
  } catch (err) {
    data.XZQH_P = ''
  }
  try {
    a = doc.getElementsByTagName('XZQH_C')
    data.XZQH_C = a[0].attributes[1].value
  } catch (err) {
    data.XZQH_C = ''
  }
  try {
    a = doc.getElementsByTagName('WSMC')
    data.WSMC = a[0].attributes[1].value
  } catch (err) {
    data.WSMC = ''
  }
  try {
    a = doc.getElementsByTagName('AH')
    data.AH = a[0].attributes[1].value
  } catch (err) {
    data.AH = ''
  }
  try {
    a = doc.getElementsByTagName('ZH')
    data.ZH = a[0].attributes[1].value
  } catch (err) {
    data.ZH = ''
  }
  try {
    a = doc.getElementsByTagName('AJLB_YJ')
    data.AJLB_YJ = a[0].attributes[1].value
  } catch (err) {
    data.AJLB_YJ = ''
  }
  try {
    a = doc.getElementsByTagName('AJLB_EJ')
    data.AJLB_EJ = a[0].attributes[1].value
  } catch (err) {
    data.AJLB_EJ = ''
  }
  try {
    a = doc.getElementsByTagName('LAND')
    data.LAND = a[0].attributes[1].value
  } catch (err) {
    data.LAND = ''
  }
  try {
    a = doc.getElementsByTagName('FYJC')
    data.FYJC = a[0].attributes[1].value
  } catch (err) {
    data.FYJC = ''
  }
  try {
    a = doc.getElementsByTagName('AHSXH')
    data.AHSXH = a[0].attributes[1].value
  } catch (err) {
    data.AHSXH = ''
  }
  try {
    a = doc.getElementsByTagName('AJLB')
    data.AJLB = a[0].attributes[1].value
  } catch (err) {
    data.AJLB = ''
  }
  try {
    a = doc.getElementsByTagName('WSZL')
    data.WSZL = a[0].attributes[1].value
  } catch (err) {
    data.WSZL = ''
  }
  try {
    a = doc.getElementsByTagName('SPCX')
    data.SPCX = a[0].attributes[1].value
  } catch (err) {
    data.SPCX = ''
  }
  try {
    a = doc.getElementsByTagName('AJLX')
    data.AJLX = a[0].attributes[1].value
  } catch (err) {
    data.AJLX = ''
  }
  // 当事人
  try {
    a = doc.getElementsByTagName('DSR')
    data.DSR = a[0].attributes[1].value
  } catch (err) {
    data.DSR = ''
  }
  try {
    a = doc.getElementsByTagName('SSJL')
    data.SSJL = a[0].attributes[1].value
  } catch (err) {
    data.SSJL = ''
  }
  try {
    a = doc.getElementsByTagName('AY')
    data.AY = a[0].attributes[1].value
  } catch (err) {
    data.AY = ''
  }
  try {
    a = doc.getElementsByTagName('AYDM')
    data.AYDM = a[0].attributes[1].value
  } catch (err) {
    data.AYDM = ''
  }
  try {
    a = doc.getElementsByTagName('FJM')
    data.FJM = a[0].attributes[1].value
  } catch (err) {
    data.FJM = ''
  }
  try {
    a = doc.getElementsByTagName('SSQQ')
    data.SSQQ = a[0].attributes[1].value
  } catch (err) {
    data.SSQQ = ''
  }
  try {
    a = doc.getElementsByTagName('YSAJSYCX')
    data.YSAJSYCX = a[0].attributes[1].value
  } catch (err) {
    data.YSAJSYCX = ''
  }
  try {
    a = doc.getElementsByTagName('DRSP')
    data.DRSP = a[0].attributes[1].value
  } catch (err) {
    data.DRSP = ''
  }
  try {
    a = doc.getElementsByTagName('JYZPT')
    data.JYZPT = a[0].attributes[1].value
  } catch (err) {
    data.JYZPT = ''
  }
  try {
    a = doc.getElementsByTagName('YSAJLY')
    data.YSAJLY = a[0].attributes[1].value
  } catch (err) {
    data.YSAJLY = ''
  }
  try {
    a = doc.getElementsByTagName('SPZZ')
    data.SPZZ = a[0].attributes[1].value
  } catch (err) {
    data.SPZZ = ''
  }
  // 案件基本情况
  try {
    a = doc.getElementsByTagName('AJJBQK')
    data.AJJBQK = a[0].attributes[1].value
  } catch (err) {
    data.AJJBQK = ''
  }
  try {
    a = doc.getElementsByTagName('SFQDSMHT')
    data.SFQDSMHT = a[0].attributes[1].value
  } catch (err) {
    data.SFQDSMHT = ''
  }
  try {
    a = doc.getElementsByTagName('HTDBQKSFCZ')
    data.HTDBQKSFCZ = a[0].attributes[1].value
  } catch (err) {
    data.HTDBQKSFCZ = ''
  }
  try {
    a = doc.getElementsByTagName('BGRFS')
    data.BGRFS = a[0].attributes[1].value
  } catch (err) {
    data.BGRFS = ''
  }
  try {
    a = doc.getElementsByTagName('PJJG')
    data.PJJG = a[0].attributes[1].value
  } catch (err) {
    data.PJJG = ''
  }
  try {
    a = doc.getElementsByTagName('GXQYY')
    data.GXQYY = a[0].attributes[1].value
  } catch (err) {
    data.GXQYY = ''
  }
  try {
    a = doc.getElementsByTagName('YSJAFS')
    data.YSJAFS = a[0].attributes[1].value
  } catch (err) {
    data.YSJAFS = ''
  }
  // 文尾
  try {
    a = doc.getElementsByTagName('CPSJ')
    data.CPSJ = a[0].attributes[1].value
  } catch (err) {
    data.CPSJ = ''
  }
  try {
    a = doc.getElementsByTagName('JAND')
    data.JAND = a[0].attributes[1].value
  } catch (err) {
    data.JAND = ''
  }
  console.log(data)
}
