<template>
<div>
  <!-- Navbar & Hero Start -->
    <div class="alltop container-fluid position-relative p-0">
        <div class="container-fluid bg-primary py-xxx mb-5 hero-header">
            <div class="container py-xxx">
                <div class="row justify-content-center py-xxx">
                    <div class="col-lg-10 pt-lg-5 mt-lg-5 text-center">
                        <h1 class="display-3 text-white mb-3 animated slideInDown">司法检索</h1>
                        <div class="position-relative w-75 mx-auto animated slideInDown">
                            <input class="form-control border-0 rounded-pill w-100 py-3 ps-4 pe-5" v-model="input" type="text" placeholder="例如：高启强 黑社会性质罪 京海市">
                            <button type="button" class="btn btn-primary rounded-pill py-2 px-4 position-absolute top-0 end-0 me-2" v-on:click="click_search" style="margin-top: 7px;">检索</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Navbar & Hero End -->

    <!-- Service Start -->
    <div class="container-xxl">
        <div class="container">
            <div class="text-center wow fadeInUp" data-wow-delay="0.1s">
                <h6 class="section-title bg-white text-center text-primary px-3">相关条目</h6>
            </div>
            <div class="allresult row g-4">
                <div v-for="item in data" :key="item" class="service-item rounded pt-3" v-on:click="display(item.address)">
                    <div class="p-4">
                        <i class="fa fa-3x fa-cog text-primary mb-4"></i>
                        <h5>{{item.title}}</h5>
                <p>{{item.short_text}}......</p>
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
import { search, searchpage } from '@/utils/judicial.js'
export default {
  name: 'SearchBar',
  components: {
  },
  props: {
    to_display: {
      // 回调函数
      type: Function,
      default: () => {}
    }
  },
  computed: {
    // usedata: function () {
    //  const tmp = []
    //  for (i in this.data.doc_list) {
    //    tmp.push([key, value])
    //  }
    //  return tmp
    // }
  },
  data() {
    return {
      input: '',
      prevsearch: '',
      data: [],
      pageid: 0,
      totalnum: 0,
      items: [['浙江省东阳市人民法院 民事判决书 （2016）浙0783民初17571号', '原告韦斌姬为与被告韦斌强、杜满萍民间借贷纠纷一案，于2016年12月1日向本院提起诉讼，请求判令两被告归还借款10万元，并支付利息（自起诉之日起按中国人民银行同期同档次贷款基准利率计算至实际履行之日止）。本院受理后，依法由审判员甘震适用简易程序独任审判。'],
        ['浙江省东阳市人民法院 民事判决书 （2016）浙0783民初17571号', '原告韦斌姬为与被告韦斌强、杜满萍民间借贷纠纷一案，于2016年12月1日向本院提起诉讼，请求判令两被告归还借款10万元，并支付利息（自起诉之日起按中国人民银行同期同档次贷款基准利率计算至实际履行之日止）。本院受理后，依法由审判员甘震适用简易程序独任审判。'],
        ['浙江省东阳市人民法院 民事判决书 （2016）浙0783民初17571号', '原告韦斌姬为与被告韦斌强、杜满萍民间借贷纠纷一案，于2016年12月1日向本院提起诉讼，请求判令两被告归还借款10万元，并支付利息（自起诉之日起按中国人民银行同期同档次贷款基准利率计算至实际履行之日止）。本院受理后，依法由审判员甘震适用简易程序独任审判。'],
        ['浙江省东阳市人民法院 民事判决书 （2016）浙0783民初17571号', '原告韦斌姬为与被告韦斌强、杜满萍民间借贷纠纷一案，于2016年12月1日向本院提起诉讼，请求判令两被告归还借款10万元，并支付利息（自起诉之日起按中国人民银行同期同档次贷款基准利率计算至实际履行之日止）。本院受理后，依法由审判员甘震适用简易程序独任审判。']]
    }
  },
  methods: {
    click_search() {
      if (this.input !== '') {
        this.prevsearch = this.input
        search(this, this.input)
      }
    },
    display(addr) {
      this.to_display(addr)
      const el = document.getElementsByClassName('alltop')[0]
      this.$nextTick(function () {
        window.scrollTo({ behavior: 'smooth', top: el.offsetTop })
      })
    },
    changepage(page) {
      this.pageid = page
      searchpage(this, this.prevsearch, this.pageid)
      const el = document.getElementsByClassName('allresult')[0]
      this.$nextTick(function () {
        window.scrollTo({ behavior: 'smooth', top: el.offsetTop })
      })
    }
  },
  watch: {
  }
}
</script>

<style scoped></style>
