<template>
  <body v-show="visible">
    <div class="container-fluid">
      <div class="row">
        <nav class="bg-light sidebar">
          <div class="sidebar-sticky">
            <ul class="nav flex-column">
              <li
                class="nav-item"
                v-for="item in side_labels"
                v-bind:key="item"
              >
                <router-link
                  class="nav-link"
                  to="/main"
                  v-on:click="click(item)"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="feather"
                  >
                    <path
                      v-if="item[1] == 1"
                      d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"
                    ></path>
                    <path
                      v-if="item[1] == 2"
                      d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"
                    ></path>
                    <circle v-if="item[1] == 2" cx="9" cy="7" r="4"></circle>
                    <path
                      v-if="item[1] == 2"
                      d="M23 21v-2a4 4 0 0 0-3-3.87"
                    ></path>
                    <path
                      v-if="item[1] == 2"
                      d="M16 3.13a4 4 0 0 1 0 7.75"
                    ></path>
                    <polygon
                      v-if="item[1] == 3"
                      points="12 2 2 7 12 12 22 7 12 2"
                    ></polygon>
                    <polyline
                      v-if="item[1] == 3"
                      points="2 17 12 22 22 17"
                    ></polyline>
                    <polyline
                      v-if="item[1] == 3"
                      points="2 12 12 17 22 12"
                    ></polyline>
                    <line
                      v-if="item[1] == 4"
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="20"
                    ></line>
                    <line
                      v-if="item[1] == 4"
                      x1="0"
                      y1="20"
                      x2="20"
                      y2="20"
                    ></line>
                    <line
                      v-if="item[1] == 4"
                      x1="0"
                      y1="0"
                      x2="20"
                      y2="0"
                    ></line>
                    <line
                      v-if="item[1] == 4"
                      x1="20"
                      y1="0"
                      x2="20"
                      y2="20"
                    ></line>
                    <line
                      v-if="item[1] == 5"
                      x1="12"
                      y1="4"
                      x2="2"
                      y2="18"
                    ></line>
                    <line
                      v-if="item[1] == 5"
                      x1="12"
                      y1="4"
                      x2="22"
                      y2="18"
                    ></line>
                    <line
                      v-if="item[1] == 5"
                      x1="2"
                      y1="18"
                      x2="22"
                      y2="18"
                    ></line>
                    <line
                      v-if="item[1] == 6"
                      x1="18"
                      y1="20"
                      x2="18"
                      y2="10"
                    ></line>
                    <line
                      v-if="item[1] == 6"
                      x1="12"
                      y1="20"
                      x2="12"
                      y2="4"
                    ></line>
                    <line
                      v-if="item[1] == 6"
                      x1="6"
                      y1="20"
                      x2="6"
                      y2="14"
                    ></line>
                    <circle v-if="item[1] == 7" cx="12" cy="8" r="6"></circle>
                    <circle v-if="item[1] == 7" cx="8" cy="15" r="6"></circle>
                    <circle v-if="item[1] == 7" cx="16" cy="15" r="6"></circle>
                    <line
                      v-if="item[1] == 8"
                      x1="4"
                      y1="4"
                      x2="12"
                      y2="12"
                    ></line>
                    <line
                      v-if="item[1] == 8"
                      x1="4"
                      y1="20"
                      x2="12"
                      y2="12"
                    ></line>
                    <line
                      v-if="item[1] == 8"
                      x1="10"
                      y1="4"
                      x2="18"
                      y2="12"
                    ></line>
                    <line
                      v-if="item[1] == 8"
                      x1="10"
                      y1="20"
                      x2="18"
                      y2="12"
                    ></line>
                    <circle v-if="item[1] == 9" cx="12" cy="12" r="10"></circle>
                    <line
                      v-if="item[1] == 9"
                      x1="12"
                      y1="12"
                      x2="12"
                      y2="5"
                    ></line>
                    <line
                      v-if="item[1] == 9"
                      x1="12"
                      y1="12"
                      x2="17"
                      y2="12"
                    ></line>
                  </svg>
                  {{ item[0] }}
                </router-link>
              </li>
            </ul>
          </div>
        </nav>

        <IntroduceTable :visible="components[1]" />
        <PartnerList :visible="components[2]" />
        <IRList :visible="components[3]" />
        <SystemServiceDash :visible="components[4]" />
        <IterationBoard :visible="components[5]" />
        <MrBoard :visible="components[6]" />
        <IssueBoard :visible="components[7]" />
        <PayloadBoard :visible="components[8]" />
      </div>
    </div>
  </body>
</template>

<script>
import IRList from './IRList.vue'
import MrBoard from './MrBoard.vue'
import IntroduceTable from '../ui/Introduce.vue'
import PartnerList from '../ui/PartnerList.vue'
import IterationBoard from './IterationBoard.vue'
import SystemServiceDash from '../ui/SystemService.vue'
import IssueBoard from './IssueBoard.vue'
import PayloadBoard from './PayloadBoard.vue'

export default {
  name: 'QualityDash',
  components: {
    IRList,
    MrBoard,
    IntroduceTable,
    PartnerList,
    IterationBoard,
    SystemServiceDash,
    IssueBoard,
    PayloadBoard
  },
  props: {
    visible: {
      type: Boolean,
      default: () => false
    }
  },
  data() {
    return {
      components: [],
      component_num: 9,
      display: 0,
      side_labels: [
        ['项目概况', 1],
        ['人员列表', 2],
        ['需求列表', 3],
        ['项目标签', 4],
        ['迭代计划', 5],
        ['MR信息', 6],
        ['Issue信息', 7],
        ['交付情况', 8],
        ['项目数据', 9]
      ]
    }
  },
  methods: {
    datetime: function (timestamp) {
      // 时间戳生成时间
      const d = new Date()
      if (timestamp < 10000000000) {
        d.setTime(timestamp * 1000)
      } else {
        d.setTime(timestamp)
      }
      return d.toLocaleString()
    },
    click(item) {
      if (item[1] === 9) {
        window.open('/data', '_blank')
      } else {
        for (let i = 1; i <= this.component_num; i++) {
          this.components[i] = false
        }
        this.components[item[1]] = true
      }
    }
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === false) {
          for (let i = 1; i <= this.component_num; i++) {
            this.components[i] = false
          }
        } else {
          for (let i = 1; i <= this.component_num; i++) {
            this.components[i] = false
          }
          this.components[1] = true
        }
      }
    }
  }
}
</script>

<style scoped>
body {
  font-size: 0.875rem;
}

.feather {
  width: 16px;
  height: 16px;
  vertical-align: text-bottom;
}

.sidebar {
  position: relative;
  width: 150px;
  height: 2000px;
  bottom: 0 fixed;
  left: 0;
  z-index: 100; /* Behind the navbar */
  padding: 0;
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, 0.1);
}

.sidebar-sticky {
  position: -webkit-sticky;
  position: sticky;
  top: 48px; /* Height of navbar */
  height: calc(100vh - 48px);
  padding-top: 0.5rem;
  overflow-x: hidden;
  overflow-y: auto; /* Scrollable contents if viewport is shorter than content. */
}

.sidebar .nav-link {
  font-weight: 500;
  color: #333;
}

.sidebar .nav-link .feather {
  margin-right: 4px;
  color: #999;
}

.sidebar .nav-link.active {
  color: #007bff;
}

.sidebar .nav-link:hover .feather,
.sidebar .nav-link.active .feather {
  color: inherit;
}

.sidebar-heading {
  font-size: 0.75rem;
  text-transform: uppercase;
}
</style>
