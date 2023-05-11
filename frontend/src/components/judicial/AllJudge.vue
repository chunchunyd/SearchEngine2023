<template>
<div>
<div class="container-xxl py-5">
        <div class="container">
            <div class="text-center wow fadeInUp" data-wow-delay="0.1s">
                <h6 class="section-title bg-white text-center text-primary px-3">所有法官</h6>
            </div>
            <div class="row g-4">
                <div v-for="item in data" :key="item" class="col-lg-6" data-wow-delay="0.1s" v-on:click="display(item.id, item.name)">
                    <div class="service-item rounded pt-3 judgepic">
                        <div class="p-4">
                            <i class="fa fa-3x fa-globe text-primary mb-4"></i>
                            <h5>{{item.name}}</h5>
                            <p>{{cut(item.full_name)}}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="pagebar allwidth">
            <div class="block centerblock">
              <el-pagination
              @current-change="changepage"
              background
              :hide-on-single-page="true"
              layout="prev, pager, next"
              :total="this.totalnum"
              :page-size="10"
              :pager-count="15">
              </el-pagination>
            </div>
    </div>
</div>
</template>

<script>
import { searchjudge, searchjudgepage } from '@/utils/judicial.js'
export default {
  name: 'AllJudge',
  components: {
  },
  props: {
    to_relate: {
      // 回调函数
      type: Function,
      default: () => {}
    }
  },
  computed: {
  },
  data() {
    return {
      data: [],
      pageid: 0,
      totalnum: 0
    }
  },
  mounted () {
    searchjudge(this)
  },
  methods: {
    changepage(page) {
      this.pageid = page
      searchjudgepage(this, this.pageid)
      const el = document.getElementsByClassName('allresult')[0]
      this.$nextTick(function () {
        window.scrollTo({ behavior: 'smooth', top: el.offsetTop })
      })
    },
    display (id, text) {
      this.to_relate(1, id, text)
      const el = document.getElementsByClassName('alltop')[0]
      this.$nextTick(function () {
        window.scrollTo({ behavior: 'smooth', top: el.offsetTop })
      })
    },
    cut (str) {
      // 截取str中'_'之后的字符
      const idx = str.indexOf('_')
      return str.slice(idx + 1)
    },
    test() {
      console.log(this.data)
    }
  },
  watch: {
  }
}
</script>

<style scoped></style>
