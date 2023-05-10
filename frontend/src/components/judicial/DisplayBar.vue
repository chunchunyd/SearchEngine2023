<template>
<div>
  <h2>展示条目 {{addr}}</h2>
  <h2 v-on:click="test">test button</h2>
  <b>{{xml_data}}</b>
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
      xml_data: 'xml_data'
    }
  },
  methods: {
    getdata(path) {
      getxml(this, path)
    },
    test() {
      ParseXml(this.xml_data)
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
