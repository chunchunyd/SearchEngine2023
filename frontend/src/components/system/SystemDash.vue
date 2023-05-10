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
                      x1="18"
                      y1="20"
                      x2="18"
                      y2="10"
                    ></line>
                    <line
                      v-if="item[1] == 4"
                      x1="12"
                      y1="20"
                      x2="12"
                      y2="4"
                    ></line>
                    <line
                      v-if="item[1] == 4"
                      x1="6"
                      y1="20"
                      x2="6"
                      y2="14"
                    ></line>
                    <circle v-if="item[1] == 5" cx="12" cy="12" r="10"></circle>
                    <line
                      v-if="item[1] == 5"
                      x1="12"
                      y1="12"
                      x2="12"
                      y2="5"
                    ></line>
                    <line
                      v-if="item[1] == 5"
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

        <IRList :visible="irlist_visible" />
        <WorkTable :visible="worktable_visible" />
        <IntroduceTable :visible="introduce_visible" />
        <PartnerList :visible="partnerlist_visible" />
      </div>
    </div>
  </body>
</template>

<script>
import IRList from './IRList.vue'
import WorkTable from './WorkTable.vue'
import IntroduceTable from '../ui/Introduce.vue'
import PartnerList from '../ui/PartnerList.vue'

export default {
  name: 'SystemDash',
  components: {
    IRList,
    WorkTable,
    IntroduceTable,
    PartnerList
  },
  props: {
    visible: {
      type: Boolean,
      default: () => false
    }
  },
  data() {
    return {
      introduce_visible: false,
      partnerlist_visible: false,
      irlist_visible: false,
      worktable_visible: false,
      datadash_visible: false,
      display: 0,
      side_labels: [
        ['项目概况', 1],
        ['人员列表', 2],
        ['需求列表', 3],
        ['工作台', 4],
        ['项目数据', 5]
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
      if (item[1] === 1) {
        this.introduce_visible = true
        this.partnerlist_visible = false
        this.irlist_visible = false
        this.worktable_visible = false
        this.datadash_visible = false
      } else if (item[1] === 2) {
        this.introduce_visible = false
        this.partnerlist_visible = true
        this.irlist_visible = false
        this.worktable_visible = false
        this.datadash_visible = false
      } else if (item[1] === 3) {
        this.introduce_visible = false
        this.partnerlist_visible = false
        this.irlist_visible = true
        this.worktable_visible = false
        this.datadash_visible = false
      } else if (item[1] === 4) {
        this.introduce_visible = false
        this.partnerlist_visible = false
        this.irlist_visible = false
        this.worktable_visible = true
        this.datadash_visible = false
      } else if (item[1] === 5) {
        window.open('/data', '_blank')
      }
    }
  },
  watch: {
    visible: {
      handler(visible) {
        if (visible === false) {
          this.introduce_visible = false
          this.partnerlist_visible = false
          this.irlist_visible = false
          this.worktable_visible = false
          this.datadash_visible = false
        } else {
          this.introduce_visible = true
          this.partnerlist_visible = false
          this.irlist_visible = false
          this.worktable_visible = false
          this.datadash_visible = false
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
