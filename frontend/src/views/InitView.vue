<template>
  <div class="home">
    <!-- Topbar Start -->
    <div class="container-fluid bg-dark px-5 d-none d-lg-block">
        <div class="row gx-0">
            <div class="col-lg-8 text-center text-lg-start mb-2 mb-lg-0">
                <div class="d-inline-flex align-items-center" style="height: 45px;">
                    <small class="me-3 text-light"><i class="fa fa-map-marker-alt me-2" v-on:click="home">Home</i></small>
                    <small class="me-3 text-light"><i class="fa fa-phone-alt me-2"><router-link to="/about">About</router-link></i></small>
                    <small class="me-3 text-light"><i class="fa fa-phone-alt me-2" v-on:click="back">Back</i></small>
                    <small class="me-3 text-light"><i class="fa fa-phone-alt me-2" v-on:click="court">Court</i></small>
                    <small class="me-3 text-light"><i class="fa fa-phone-alt me-2" v-on:click="judge">Judge</i></small>
                </div>
            </div>
        </div>
    </div>
    <!-- Topbar End -->
    <SearchBar v-show="status==0"
    :to_display="to_display"></SearchBar>
    <DisplayBar  v-show="status==1"
    :addr="display_idx" :to_relate="to_relate"></DisplayBar>
    <AllCourt  v-show="status==2"
    :to_relate="to_relate"></AllCourt>
    <AllJudge  v-show="status==3"
    :to_relate="to_relate"></AllJudge>
    <RelateBar  v-show="status==4"
    :type="relatetype" :id="relateid" :text="relatetext" :to_display="to_display"></RelateBar>
  </div>
</template>

<script>
import SearchBar from '@/components/judicial/SearchBar.vue'
import DisplayBar from '@/components/judicial/DisplayBar.vue'
import AllCourt from '@/components/judicial/AllCourt.vue'
import AllJudge from '@/components/judicial/AllJudge.vue'
import RelateBar from '@/components/judicial/RelateBar.vue'
export default {
  name: 'InitView',
  components: {
    SearchBar,
    DisplayBar,
    AllCourt,
    AllJudge,
    RelateBar
  },
  data() {
    return {
      status: 0,
      display_idx: 0,
      relatetype: 0,
      relateid: 0,
      relatetext: '',
      prevstatus: []
    }
  },
  mounted() {
  },
  methods: {
    to_display (addr) {
      this.display_idx = addr
      this.prevstatus.push(this.status)
      this.status = 1
    },
    to_relate (type, id, text) {
      this.relatetype = type
      this.relateid = id
      this.relatetext = text
      this.prevstatus.push(this.status)
      this.status = 4
    },
    back() {
      if (this.prevstatus.length > 0) {
        // 弹出prevstatus数组的最后一项
        this.status = this.prevstatus.pop()
      }
    },
    home() {
      this.prevstatus.push(this.status)
      this.status = 0
    },
    court() {
      this.prevstatus.push(this.status)
      this.status = 2
    },
    judge() {
      this.prevstatus.push(this.status)
      this.status = 3
    }
  }
}
</script>

<style scoped lang="scss">
a {
  color: #ffffff;
}
</style>
