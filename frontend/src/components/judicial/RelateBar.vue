<template>
<div v-if="this.status==1">
    <!-- Service Start -->
    <div class="container-xxl">
        <div class="container">
          <br/>
            <div class="text-center wow fadeInUp" data-wow-delay="0.1s">
                <h6 class="section-title bg-white text-center text-primary px-3" v-on:click="test">“{{this.text}}”的相关条目</h6>
            </div>
            <div class="allresult row g-4">
                <div v-for="item in data" :key="item" class="service-item rounded pt-3" v-on:click="display(item.address)">
                    <div class="p-4">
                        <i class="fa fa-3x fa-cog text-primary mb-4"></i>
                        <h5>{{item.case_number}}</h5>
                <p v-html="item.full_text.slice(0,300)+'......'"></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Service End -->
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
import { getrelatedata, getrelatedatapage } from '@/utils/judicial.js'
export default {
  name: 'RelateBar',
  components: {
  },
  props: {
    type: {
      type: Number,
      default: 0
    },
    id: {
      type: Number,
      default: 0
    },
    text: {
      type: String,
      default: ''
    },
    to_display: {
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
      totalnum: 0,
      status: 0
    }
  },
  methods: {
    display(addr) {
      this.to_display(addr)
      const el = document.getElementsByClassName('alltop')[0]
      this.$nextTick(function () {
        window.scrollTo({ behavior: 'smooth', top: el.offsetTop })
      })
    },
    changepage(page) {
      this.pageid = page
      getrelatedatapage(this, this.type, this.id, this.pageid)
      const el = document.getElementsByClassName('allresult')[0]
      this.$nextTick(function () {
        window.scrollTo({ behavior: 'smooth', top: el.offsetTop })
      })
    },
    test() {
      console.log(this.data)
    }
  },
  watch: {
    text: {
      handler(text) {
        this.status = 0
        getrelatedata(this, this.type, this.id)
      }
    }
  }
}
</script>

<style scoped></style>
