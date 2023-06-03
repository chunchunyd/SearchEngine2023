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
                            <button type="button" class="btn btn-primary rounded-pill py-2 px-4 position-absolute top-0 end-1 me-2" v-on:click="click_search" style="margin-top: 7px;">检索</button>
                            <el-upload
                              class="upload-demo"
                              :before-upload="upload"
                              multiple
                              :limit="1"
                              :show-file-list="false">
                              <button type="button" class="btn btn-primary rounded-pill py-2 px-4 position-absolute top-0 end-0 me-2" style="margin-top: 7px;">上传</button>
                            </el-upload>
                        </div>
                        <div>
                            <el-checkbox v-model="checked" style="color: #ffffff">精确匹配</el-checkbox>
                            <span>\s</span>
                            <el-tooltip :content="tips" placement="bottom" effect="light">
                              <span style="color: #ffffff; font-size:16px">?</span>
                            </el-tooltip>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Navbar & Hero End -->

    <div v-if="this.status==1 && !this.avail">
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
                      <p v-html="item.short_text"></p>
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

    <div v-if="this.status==1 && this.avail">
      <el-row>
        <el-col :span="1"><div></div></el-col>
        <el-col :span="15">
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
                      <p v-html="item.short_text"></p>
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
        </el-col>
        <el-col :span="7">
          <!-- Service Start -->
          <div class="container-xxl" v-if="this.court_avail">
              <div class="container">
                  <div class="text-center wow fadeInUp" data-wow-delay="0.1s">
                      <h6 class="section-title bg-white text-center text-primary px-3">相关法院</h6>
                  </div>
                  <div class="allresult row g-4">
                      <div v-for="item in court" :key="item" class="service-item rounded pt-3" v-on:click="display_relate(item.id, item.name)">
                          <div class="p-4">
                              <i class="fa fa-3x fa-globe text-primary mb-4"></i>
                              <h5>{{item.name}}</h5>
                              <p>{{item.province}} | {{item.city}} | {{item.level}} | {{item.code}}</p>
                          </div>
                      </div>
                  </div>
              </div>
              <br/>
          </div>
          <!-- Service End -->

          <!-- Service Start -->
          <div class="container-xxl"  v-if="this.judge_avail">
              <div class="container">
                  <div class="text-center wow fadeInUp" data-wow-delay="0.1s">
                      <h6 class="section-title bg-white text-center text-primary px-3">相关法官</h6>
                  </div>
                  <div class="allresult row g-4">
                      <div v-for="item in judge" :key="item" class="service-item rounded pt-3" v-on:click="display_relate(item.id, item.name)">
                          <div class="p-4">
                            <i class="fa fa-3x fa-globe text-primary mb-4"></i>
                            <h5>{{item.name}}</h5>
                            <p>{{cut(item.full_name)}}</p>
                        </div>
                      </div>
                  </div>
              </div>
          </div>
          <!-- Service End -->
        </el-col>
        <el-col :span="1"><div></div></el-col>
      </el-row>
    </div>

    <div v-if="this.status==2">
      <el-row>
        <el-col :span="1"><div></div></el-col>
        <el-col :span="15">
          <!-- Service Start -->
          <div class="container-xxl">
              <div class="container">
                  <div class="text-center wow fadeInUp" data-wow-delay="0.1s">
                      <h6 class="section-title bg-white text-center text-primary px-3">相似条目</h6>
                  </div>
                  <div class="allresult row g-4">
                      <div v-for="item in similardata" :key="item" class="service-item rounded pt-3" v-on:click="display(item.address)">
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
        </el-col>
        <el-col :span="7">
          <!-- Service Start -->
          <div class="container-xxl">
              <div class="container">
                  <div class="text-center wow fadeInUp" data-wow-delay="0.1s">
                      <h6 class="section-title bg-white text-center text-primary px-3">相似法院</h6>
                  </div>
                  <div class="allresult row g-4">
                      <div v-for="item in similarcourt" :key="item" class="service-item rounded pt-3" v-on:click="display_relate(item.id, item.name)">
                          <div class="p-4">
                              <i class="fa fa-3x fa-globe text-primary mb-4"></i>
                              <h5>{{item.name}}</h5>
                              <p>{{item.province}} | {{item.city}} | {{item.level}} | {{item.code}}</p>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
          <!-- Service End -->
          <br/>
          <!-- Service Start -->
          <div class="container-xxl">
              <div class="container">
                  <div class="text-center wow fadeInUp" data-wow-delay="0.1s">
                      <h6 class="section-title bg-white text-center text-primary px-3">相似法官</h6>
                  </div>
                  <div class="allresult row g-4">
                      <div v-for="item in similarjudge" :key="item" class="service-item rounded pt-3" v-on:click="display_relate(item.id, item.name)">
                          <div class="p-4">
                            <i class="fa fa-3x fa-globe text-primary mb-4"></i>
                            <h5>{{item.name}}</h5>
                            <p>{{cut(item.full_name)}}</p>
                        </div>
                      </div>
                  </div>
              </div>
          </div>
          <!-- Service End -->
        </el-col>
        <el-col :span="1"><div></div></el-col>
      </el-row>
    </div>

    <div v-if="this.status==3">
      <div class="container-xxl">
          <div class="container">
              <div class="text-center wow fadeInUp" data-wow-delay="0.1s">
                  <h6 class="section-title bg-white text-center text-primary px-3">加载中...</h6>
              </div>
          </div>
      </div>
    </div>
</div>
</template>

<script>
import { search, searchpage, similarsearch } from '@/utils/judicial.js'
export default {
  name: 'SearchBar',
  components: {
  },
  props: {
    to_display: {
      // 回调函数
      type: Function,
      default: () => {}
    },
    to_relate: {
      // 回调函数
      type: Function,
      default: () => {}
    }
  },
  computed: {
    avail: function () {
      return this.court.length > 0 || this.judge.length > 0
    },
    court_avail: function () {
      return this.court.length > 0
    },
    judge_avail: function () {
      return this.judge.length > 0
    }
  },
  data() {
    return {
      tips: '支持多个检索词以交(&)、并(|)、补(-)等逻辑进行精确匹配。例如：“((豆浆 | 油条) & 包子) - 刑事”',
      htmlString: 'This is a <span class="highlighted">text</span> with some',
      input: '',
      prevsearch: '',
      data: [],
      court: [],
      judge: [],
      matchkey: [],
      pageid: 0,
      totalnum: 0,
      // status=1表示有搜索结果，status=0表示无搜索结果, status=2表示有相似结果，status=3表示正在搜索
      status: 0,
      checked: false,
      filecontent: '',
      similardata: [],
      similarcourt: [],
      similarjudge: []
    }
  },
  methods: {
    click_search() {
      if (this.input !== '') {
        this.status = 3
        if (this.checked) {
          this.prevsearch = 'EXACTLY: ' + this.input
          search(this, 'EXACTLY: ' + this.input)
        } else {
          this.prevsearch = this.input
          search(this, this.input)
        }
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
    },
    computehighlight() {
      // 遍历data字典
      for (const k in this.data) {
        let h = this.data[k].short_text
        // 在h中匹配matchkey中的所有字符串
        for (let j = 0; j < this.matchkey.length; j++) {
          // 将匹配到的字符串用span标签包裹起来
          h = h.replace(new RegExp(this.matchkey[j], 'g'), '<span class="highlighted">' + this.matchkey[j] + '</span>')
        }
        this.data[k].short_text = h + '......'
        // 构造relatedata
        this.data[k].relatedata = {
          court_id: this.data[k].court_id,
          court_name: this.data[k].court_name,
          judges: this.data[k].judges
        }
      }
    },
    upload(file) {
      // 读取文件内容,将内容赋值给input
      this.status = 3
      const formData = new FormData()
      formData.append('xml_file', file)
      similarsearch(this, formData)
      // const reader = new FileReader()
      // reader.onload = () => {
      //   this.filecontent = reader.result
      //   console.log(this.filecontent)
      //   similarsearch(this, this.filecontent)
      // }
      // reader.readAsText(file)
      return false
    },
    display_relate (id, text) {
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
