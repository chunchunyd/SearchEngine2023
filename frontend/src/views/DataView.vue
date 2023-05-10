<template>
  <div class="data">
    <br />
    <h4></h4>
    <el-row :gutter="20">
      <el-col :span="24"
        ><div class="grid-content-thin bg-purple box">
          <br /><br />
          <h4>{{ this.projname }} 数据统计</h4>
          <br /></div
      ></el-col>
    </el-row>
    <!-- 图表容器 DOM -->
    <el-row :gutter="20">
      <el-col :span="4"
        ><div class="grid-content bg-purple-dark box"></div
      ></el-col>
      <el-col :span="12"
        ><div id="container1" class="grid-content bg-purple"></div
      ></el-col>
      <el-col :span="8"
        ><div class="grid-content bg-purple-light box">
          <br /><br /><br /><br /><br /><br /><br />
          <span>IR是项目的原始需求</span><br />
          <span>IR被分解为功能需求SR后，进行开发和交付</span>
        </div></el-col
      >
    </el-row>
    <el-row :gutter="20">
      <el-col :span="8"
        ><div class="grid-content bg-purple-light box">
          <br /><br /><br /><br /><br /><br /><br />
          <span>SR是项目的功能需求</span><br />
          <span>工程师们，赶快完成你们负责的SR吧!</span>
        </div></el-col
      >
      <el-col :span="12"
        ><div id="container2" class="grid-content bg-purple"></div
      ></el-col>
      <el-col :span="4"
        ><div class="grid-content bg-purple-dark box"></div
      ></el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="8"
        ><div class="grid-content-thin bg-purple-light box">
          <br /><br /><span>看看谁被分配的任务数量更多</span><br />
          <span>能者多劳~</span>
        </div></el-col
      >
      <el-col :span="8"
        ><div class="grid-content-thin bg-purple box">
          <br /><br /><span>交付的任务多，说明没有摸鱼哦</span>
        </div></el-col
      >
      <el-col :span="8"
        ><div class="grid-content-thin bg-purple-dark box">
          <br /><br /><span>谁能花更少的时间完成任务？</span><br />
          <span>速度比拼！</span>
        </div></el-col
      >
    </el-row>
    <el-row :gutter="20">
      <el-col :span="8"
        ><div id="container3" class="grid-content bg-purple"></div
      ></el-col>
      <el-col :span="8"
        ><div id="container4" class="grid-content bg-purple"></div
      ></el-col>
      <el-col :span="8"
        ><div id="container5" class="grid-content bg-purple"></div
      ></el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="4"
        ><div class="grid-content bg-purple-dark box"></div
      ></el-col>
      <el-col :span="12"
        ><div id="container12" class="grid-content bg-purple"></div
      ></el-col>
      <el-col :span="8"
        ><div class="grid-content bg-purple-light box">
          <br /><br /><br /><br /><br /><br /><br />
          <span>项目总提交数量统计</span>
        </div></el-col
      >
    </el-row>
    <!-- <el-row :gutter="20">
      <el-col :span="8"
        ><div class="grid-content bg-purple-light box">
          <br /><br /><br /><br /><br /><br /><br />
          <span>项目总代码行数统计</span>
        </div></el-col
      >
      <el-col :span="12"
        ><div id="container13" class="grid-content bg-purple"></div
      ></el-col>
      <el-col :span="4"
        ><div class="grid-content bg-purple-dark box"></div
      ></el-col>
    </el-row> -->
    <el-row :gutter="20">
      <el-col :span="8"
        ><div class="grid-content-thin bg-purple-light box">
          <br /><br /><span>MR多多，仓库常新</span>
        </div></el-col
      >
      <el-col :span="8"
        ><div class="grid-content-thin bg-purple box">
          <br /><br /><span>提交要少量多次，避免粒度过大</span>
        </div></el-col
      >
      <!-- <el-col :span="8"
        ><div class="grid-content-thin bg-purple-dark box">
          <br /><br /><span>谁写的代码更多？</span><br />
          <span>代码行数比拼！</span>
        </div></el-col
      > -->
    </el-row>
    <el-row :gutter="20">
      <el-col :span="8"
        ><div id="container6" class="grid-content bg-purple"></div
      ></el-col>
      <el-col :span="8"
        ><div id="container7" class="grid-content bg-purple"></div
      ></el-col>
      <el-col :span="8"
        ><div id="container8" class="grid-content bg-purple"></div
      ></el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="8"
        ><div class="grid-content-thin bg-purple-light box">
          <br /><br /><span>被分配了issue一定要去做哦</span>
        </div></el-col
      >
      <el-col :span="8"
        ><div class="grid-content-thin bg-purple box">
          <br /><br /><span>认真完成issue，是一种态度</span>
        </div></el-col
      >
      <el-col :span="8"
        ><div class="grid-content-thin bg-purple-dark box">
          <br /><br /><span>谁能花更少的时间完成issue？</span><br />
          <span>速度比拼！</span>
        </div></el-col
      >
    </el-row>
    <el-row :gutter="20">
      <el-col :span="8"
        ><div id="container9" class="grid-content bg-purple"></div
      ></el-col>
      <el-col :span="8"
        ><div id="container10" class="grid-content bg-purple"></div
      ></el-col>
      <el-col :span="8"
        ><div id="container11" class="grid-content bg-purple"></div
      ></el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="24"
        ><div class="grid-content-thin bg-purple-dark box">
          <br /><br /><span>这是底部啦</span><br /></div
      ></el-col>
    </el-row>
    <WaveBottom />
  </div>
</template>

<script>
import Highcharts from 'highcharts'
import { getvisibledetail } from '@/utils/com_ui'
import WaveBottom from '@/components/ui/WaveBottom.vue'

export default {
  name: 'AboutView',
  components: {
    WaveBottom
  },
  data() {
    return {
      finish: 0,
      projname: '',
      // ir
      irnum: '',
      irnum_raw: '',
      irnum_init: '',
      irnum_undergo: '',
      irnum_done: '',
      ir_chart: {
        chart: {
          type: 'bar' // 指定图表的类型，默认是折线图（line）
        },
        title: {
          text: '项目IR数量'
        },
        xAxis: {
          categories: ['总数', '未分解', '已分解', '进行中', '已交付']
        },
        yAxis: {
          title: {
            text: '数量'
          }
        },
        series: [
          {
            colorByPoint: true,
            name: '本项目',
            data: [0, 0, 0, 0, 0]
          }
        ],
        credits: {
          enabled: false
        },
        legend: {
          enabled: false
        }
      },
      // sr
      srnum: '',
      srnum_init: '',
      srnum_undergo: '',
      srnum_done: '',
      sr_chart: {
        chart: {
          type: 'bar' // 指定图表的类型，默认是折线图（line）
        },
        title: {
          text: '项目SR数量'
        },
        xAxis: {
          categories: ['总数', '初始化', '进行中', '已交付']
        },
        yAxis: {
          title: {
            text: '数量'
          }
        },
        series: [
          {
            colorByPoint: true,
            name: '本项目',
            data: [0, 0, 0, 0]
          }
        ],
        credits: {
          enabled: false
        },
        legend: {
          enabled: false
        }
      },
      // sr数量排行
      sr_alloc: [],
      sr_alloc_chart: {
        chart: {
          type: 'column', // 指定图表的类型，默认是折线图（line）
          inverted: false
        },
        title: {
          text: '个人被分配SR数量排行'
        },
        xAxis: {
          categories: []
        },
        yAxis: {
          title: {
            text: '数量'
          }
        },
        series: [
          {
            colorByPoint: true,
            name: '本项目',
            data: []
          }
        ],
        credits: {
          enabled: false
        },
        legend: {
          enabled: false
        }
      },
      // sr完成数量排行
      sr_done: [],
      sr_done_chart: {
        chart: {
          type: 'column', // 指定图表的类型，默认是折线图（line）
          inverted: false
        },
        title: {
          text: '个人已交付SR数量排行'
        },
        xAxis: {
          categories: []
        },
        yAxis: {
          title: {
            text: '数量'
          }
        },
        series: [
          {
            colorByPoint: true,
            name: '本项目',
            data: []
          }
        ],
        credits: {
          enabled: false
        },
        legend: {
          enabled: false
        }
      },
      // sr时间排行
      sr_time: [],
      sr_time_chart: {
        chart: {
          type: 'column', // 指定图表的类型，默认是折线图（line）
          inverted: false
        },
        title: {
          text: '个人完成SR平均用时排行'
        },
        xAxis: {
          categories: []
        },
        yAxis: {
          title: {
            text: '小时'
          }
        },
        series: [
          {
            colorByPoint: true,
            name: '本项目',
            data: []
          }
        ],
        credits: {
          enabled: false
        },
        legend: {
          enabled: false
        }
      },
      // 完成mr数量
      mr: [],
      mr_chart: {
        chart: {
          type: 'column', // 指定图表的类型，默认是折线图（line）
          inverted: false
        },
        title: {
          text: '个人完成MR数量排行'
        },
        xAxis: {
          categories: []
        },
        yAxis: {
          title: {
            text: '数量'
          }
        },
        series: [
          {
            colorByPoint: true,
            name: '本项目',
            data: []
          }
        ],
        credits: {
          enabled: false
        },
        legend: {
          enabled: false
        }
      },
      // commit排行
      commit: [],
      commit_chart: {
        chart: {
          type: 'column', // 指定图表的类型，默认是折线图（line）
          inverted: false
        },
        title: {
          text: '个人提交commit数量排行'
        },
        xAxis: {
          categories: []
        },
        yAxis: {
          title: {
            text: '小时'
          }
        },
        series: [
          {
            colorByPoint: true,
            name: '本项目',
            data: []
          }
        ],
        credits: {
          enabled: false
        },
        legend: {
          enabled: false
        }
      },
      // line排行
      line: [],
      line_chart: {
        chart: {
          type: 'column', // 指定图表的类型，默认是折线图（line）
          inverted: false
        },
        title: {
          text: '个人代码行数排行'
        },
        xAxis: {
          categories: []
        },
        yAxis: {
          title: {
            text: '行'
          }
        },
        series: [
          {
            colorByPoint: true,
            name: '本项目',
            data: []
          }
        ],
        credits: {
          enabled: false
        },
        legend: {
          enabled: false
        }
      },
      // issue排行
      issue: [],
      issue_chart: {
        chart: {
          type: 'column', // 指定图表的类型，默认是折线图（line）
          inverted: false
        },
        title: {
          text: '个人被分配issue数量排行'
        },
        xAxis: {
          categories: []
        },
        yAxis: {
          title: {
            text: '数量'
          }
        },
        series: [
          {
            colorByPoint: true,
            name: '本项目',
            data: []
          }
        ],
        credits: {
          enabled: false
        },
        legend: {
          enabled: false
        }
      },
      // issue完成排行
      issue_done: [],
      issue_done_chart: {
        chart: {
          type: 'column', // 指定图表的类型，默认是折线图（line）
          inverted: false
        },
        title: {
          text: '个人完成issue数量排行'
        },
        xAxis: {
          categories: []
        },
        yAxis: {
          title: {
            text: '数量'
          }
        },
        series: [
          {
            colorByPoint: true,
            name: '本项目',
            data: []
          }
        ],
        credits: {
          enabled: false
        },
        legend: {
          enabled: false
        }
      },
      // issue时间排行
      issue_time: [],
      issue_time_chart: {
        chart: {
          type: 'column', // 指定图表的类型，默认是折线图（line）
          inverted: false
        },
        title: {
          text: '个人完成issue平均用时排行'
        },
        xAxis: {
          categories: []
        },
        yAxis: {
          title: {
            text: '小时'
          }
        },
        series: [
          {
            colorByPoint: true,
            name: '本项目',
            data: []
          }
        ],
        credits: {
          enabled: false
        },
        legend: {
          enabled: false
        }
      },
      // 日志
      log: [],
      log_chart: {
        title: {
          text: '项目总提交数量'
        },
        yAxis: {
          title: {
            text: '数量'
          }
        },
        legend: {
          enabled: false
        },
        xAxis: {
          categories: []
        },
        series: [
          {
            name: 'commit数量',
            data: []
          }
        ],
        responsive: {
          rules: [
            {
              condition: {
                maxWidth: 500
              },
              chartOptions: {
                legend: {
                  layout: 'horizontal',
                  align: 'center',
                  verticalAlign: 'bottom'
                }
              }
            }
          ]
        },
        credits: {
          enabled: false
        }
      }
      // log_chart2: {
      //   title: {
      //     text: '项目总代码行数'
      //   },
      //   yAxis: {
      //     title: {
      //       text: '行数'
      //     }
      //   },
      //   legend: {
      //     enabled: false
      //   },
      //   xAxis: {
      //     categories: []
      //   },
      //   series: [
      //     {
      //       name: '行数',
      //       data: []
      //     }
      //   ],
      //   responsive: {
      //     rules: [
      //       {
      //         condition: {
      //           maxWidth: 500
      //         },
      //         chartOptions: {
      //           legend: {
      //             layout: 'horizontal',
      //             align: 'center',
      //             verticalAlign: 'bottom'
      //           }
      //         }
      //       }
      //     ]
      //   },
      //   credits: {
      //     enabled: false
      //   }
      // }
    }
  },
  mounted() {
    getvisibledetail(this)
  },
  watch: {
    finish: {
      handler(finish) {
        if (finish === 11) {
          // 数据获取完成，开始处理数据、绘制
          // IR
          this.ir_chart.series[0].data = [
            this.irnum,
            this.irnum_raw,
            this.irnum_init,
            this.irnum_undergo,
            this.irnum_done
          ]
          Highcharts.chart('container1', this.ir_chart)
          // SR
          this.sr_chart.series[0].data = [
            this.srnum,
            this.srnum_init,
            this.srnum_undergo,
            this.srnum_done
          ]
          Highcharts.chart('container2', this.sr_chart)
          for (let i = 0; i < this.sr_alloc.length; i++) {
            if (this.sr_alloc[i].user_role === 'develop') {
              this.sr_alloc_chart.series[0].data.push(
                this.sr_alloc[i].sr_allocated
              )
              this.sr_alloc_chart.xAxis.categories.push(
                this.sr_alloc[i].user_name
              )
            }
          }
          Highcharts.chart('container3', this.sr_alloc_chart)
          for (let i = 0; i < this.sr_done.length; i++) {
            if (this.sr_done[i].user_role === 'develop') {
              this.sr_done_chart.series[0].data.push(this.sr_done[i].sr_done)
              this.sr_done_chart.xAxis.categories.push(
                this.sr_done[i].user_name
              )
            }
          }
          Highcharts.chart('container4', this.sr_done_chart)
          for (let i = 0; i < this.sr_time.length; i++) {
            if (this.sr_time[i].user_role === 'develop') {
              this.sr_time_chart.series[0].data.push(
                this.sr_time[i].sr_avg_time / 3600
              )
              this.sr_time_chart.xAxis.categories.push(
                this.sr_time[i].user_name
              )
            }
          }
          Highcharts.chart('container5', this.sr_time_chart)
          for (let i = 0; i < this.mr.length; i++) {
            this.mr_chart.series[0].data.push(this.mr[i].mr_merged)
            this.mr_chart.xAxis.categories.push(this.mr[i].user_name)
          }
          Highcharts.chart('container6', this.mr_chart)
          for (let i = 0; i < this.commit.length; i++) {
            this.commit_chart.series[0].data.push(
              this.commit[i].commit_submitted
            )
            this.commit_chart.xAxis.categories.push(this.commit[i].user_name)
          }
          Highcharts.chart('container7', this.commit_chart)
          for (let i = 0; i < this.line.length; i++) {
            this.line_chart.series[0].data.push(this.line[i].lines_total)
            this.line_chart.xAxis.categories.push(this.line[i].user_name)
          }
          // Highcharts.chart('container8', this.line_chart)
          for (let i = 0; i < this.issue.length; i++) {
            this.issue_chart.series[0].data.push(this.issue[i].issue_allocated)
            this.issue_chart.xAxis.categories.push(this.issue[i].user_name)
          }
          Highcharts.chart('container9', this.issue_chart)
          for (let i = 0; i < this.issue_done.length; i++) {
            this.issue_done_chart.series[0].data.push(
              this.issue_done[i].issue_done
            )
            this.issue_done_chart.xAxis.categories.push(
              this.issue_done[i].user_name
            )
          }
          Highcharts.chart('container10', this.issue_done_chart)
          for (let i = 0; i < this.issue_time.length; i++) {
            this.issue_time_chart.series[0].data.push(
              this.issue_time[i].issue_avg_time / 3600
            )
            this.issue_time_chart.xAxis.categories.push(
              this.issue_time[i].user_name
            )
          }
          Highcharts.chart('container11', this.issue_time_chart)
          for (let i = 0; i < this.log.length; i++) {
            this.log_chart.series[0].data.push(this.log[i].commit_submitted)
            this.log_chart.xAxis.categories.push(this.log[i].time.slice(0, 10))
          }
          Highcharts.chart('container12', this.log_chart)
          for (let i = 0; i < this.log.length; i++) {
            this.log_chart2.series[0].data.push(this.log[i].lines_total)
            this.log_chart2.xAxis.categories.push(this.log[i].time.slice(0, 10))
          }
          // Highcharts.chart('container13', this.log_chart2)
        }
      }
    }
  }
}
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
  height: 500px;
}
.grid-content-thin {
  border-radius: 4px;
  height: 150px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
.box {
  text-align: center;
  vertical-align: middle;
  font-size: 18px;
}
</style>
