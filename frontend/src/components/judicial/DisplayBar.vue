<template>
<div>
  <div class="displayboard">
  <el-collapse v-model="activeName">
  <el-collapse-item name="1">
    <template v-slot:title>
        <h6 class="text-black px-3">全文</h6>
        <el-button size="small" v-on:click="download">下载</el-button>
    </template>
    <div class="service-item2 rounded pt-3">
       <div class="p-4">
           <h5>{{parsedata.WS}}</h5>
           <p>{{parsedata.QW}}</p>
        </div>
    </div>
  </el-collapse-item>
  <el-collapse-item name="2">
    <template v-slot:title>
        <h6 class="text-black px-3">详细信息</h6>
    </template>
    <el-main>
      <el-descriptions size="large" border :column="6"  direction="vertical">
        <el-descriptions-item label="文书制作单位">{{parsedata.WSZZDW}}</el-descriptions-item>
        <el-descriptions-item label="法院文书种类">{{parsedata.FYWSZL}}</el-descriptions-item>
        <el-descriptions-item label="经办法院" :span="2">{{parsedata.JBFY}}</el-descriptions-item>
        <el-descriptions-item label="法院层级码">{{parsedata.FYCJM}}</el-descriptions-item>
        <el-descriptions-item label="法院级别">{{parsedata.FYJB}}</el-descriptions-item>

        <el-descriptions-item label="行政区划(省)">{{parsedata.XZQH_P}}</el-descriptions-item>
        <el-descriptions-item label="行政区划(市)">{{parsedata.XZQH_C}}</el-descriptions-item>
        <el-descriptions-item label="文书名称" :span="2">{{parsedata.WSMC}}</el-descriptions-item>
        <el-descriptions-item label="案号" :span="2">{{parsedata.AH}}</el-descriptions-item>

        <el-descriptions-item label="字号">{{parsedata.ZH}}</el-descriptions-item>
        <el-descriptions-item label="立案年度">{{parsedata.LAND}}</el-descriptions-item>
        <el-descriptions-item label="案号顺序号">{{parsedata.AHSXH}}</el-descriptions-item>
        <el-descriptions-item label="案件类别">{{parsedata.AJLB}}</el-descriptions-item>
        <el-descriptions-item label="审判程序" :span="2">{{parsedata.SPCX}}</el-descriptions-item>

        <el-descriptions-item label="当事人" :span="6">{{parsedata.DSR}}</el-descriptions-item>
        <el-descriptions-item label="诉讼记录" :span="6">{{parsedata.SSJL}}</el-descriptions-item>
        <el-descriptions-item label="判决结果" :span="6">{{parsedata.PJJG}}</el-descriptions-item>
        <el-descriptions-item label="审判组织">{{parsedata.SPZZ}}</el-descriptions-item>
        <el-descriptions-item label="被告人反诉">{{parsedata.BGRFS}}</el-descriptions-item>
        <el-descriptions-item label="提出管辖权异议">{{parsedata.GXQYY}}</el-descriptions-item>
        <el-descriptions-item label="裁判时间">{{parsedata.CPSJ}}</el-descriptions-item>
      </el-descriptions>
    </el-main>
  </el-collapse-item>
</el-collapse>

  </div>
</div>
</template>

<script>
import { getxml } from '@/utils/judicial.js'
import { ParseXml } from '@/utils/parse.js'
export default {
  name: 'DisplayBar',
  components: {
  },
  props: {
    addr: {
      type: String,
      default: () => ''
    }
  },
  computed: {
  },
  data() {
    return {
      xml_data: '',
      parsedata: {},
      activeName: ['1', '2']
    }
  },
  methods: {
    getdata(path) {
      getxml(this, path)
    },
    parsexml() {
      ParseXml(this, this.xml_data)
    },
    test() {
      console.log(this.parsedata)
    },
    download() {
      const url = URL.createObjectURL(new Blob([this.xml_data]))
      const link = document.createElement('a')
      link.style.display = 'none'
      link.href = url
      const name = this.parsedata.WS + '.xml'
      link.setAttribute('download', name)
      document.body.appendChild(link)
      link.click()
      URL.revokeObjectURL(url)
    }
  },
  watch: {
    addr: {
      handler(addr) {
        this.getdata(addr)
      }
    }
  }
}
</script>

<style scoped></style>
