<template>
  <div>
    <div class="wrapper col2">
      <div id="topbar">
        <div id="topnav">
          <ul>
            <li>
              <router-link to="/main" v-on:click="manage_project"
                >返回主页</router-link
              >
            </li>
            <!-- <li>
              <router-link to="/main">需求管理</router-link>
              <ul>
                <li><router-link to="/main">原始需求</router-link></li>
                <li><router-link to="/main">功能需求</router-link></li>
                <li><router-link to="/main">其他</router-link></li>
              </ul>
            </li>
            <li><router-link to="/main">质量监测</router-link></li> -->
            <li><router-link to="/about">关于</router-link></li>
            <li class="last"><router-link to="/">退出</router-link></li>
          </ul>
        </div>
        <br class="clear" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MenuBar',
  props: {
    manage_project: {
      // 管理项目
      type: Function,
      default: () => {}
    }
  },
  computed: {},
  data() {
    return {}
  },
  methods: {},
  watch: {}
}
</script>

<style scoped>
.clear {
  clear: both;
}
br.clear {
  clear: both;
  margin-top: -15px;
}

/* ----------------------------------------------Wrapper------------------------------------- */

div.wrapper {
  display: block;
  width: 100%;
  margin: 0;
  text-align: left;
}
div.wrapper h1,
div.wrapper h2,
div.wrapper h3,
div.wrapper h4,
div.wrapper h5,
div.wrapper h6 {
  margin: 0 0 20px 0;
  padding: 0 0 8px 0;
  font-size: 20px;
  font-weight: normal;
  font-family: Georgia, 'Times New Roman', Times, serif;
  border-bottom: 1px dotted #dddddd;
}
.col1 {
  color: #666666;
  background-color: #e3f1f9;
}
.col2 {
  color: #ffffff;
  background-color: #000000;
}
.col3,
.col4,
.col5 {
  color: #666666;
  background-color: #ffffff;
}
.col6 {
  color: #999999;
  background-color: #f3f3f3;
}
.col6 a {
  color: #2684b7;
  background-color: #f3f3f3;
}
.col7,
.col7 a {
  color: #ffffff;
  background-color: #29313c;
}

/* ----------------------------------------------Generalise------------------------------------- */

#header,
#topbar,
#intro,
#services,
#breadcrumb,
#container,
#footer,
#copyright {
  display: block;
  position: relative;
  width: 960px;
  margin-left: 5%;
}
/* ----------------------------------------------Topbar------------------------------------- */

#topbar {
  z-index: 1000;
}
#topbar #search {
  display: block;
  float: right;
  width: 242px;
  height: 36px;
  margin: 0;
  padding: 10px 0 0 17px;
  color: #ffffff;
  background-color: #000000;
  border-left: 1px dotted #666666;
  overflow: hidden;
}

#topnav {
  display: block;
  float: left;
  width: 660px;
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: 14px;
  font-weight: normal;
  font-family: Verdana, Arial, Helvetica, sans-serif;
  color: #ffffff;
  background-color: #000000;
}
#topnav ul,
#topnav li {
  float: left;
  list-style: none;
  margin: 0;
  padding: 0;
}
#topnav li a:link,
#topnav li a:visited,
#topnav li a:hover,
#topnav li span {
  display: block;
  margin: 0;
  padding: 15px 20px;
  color: #ffffff;
  background-color: #000000;
}
#topnav ul ul li a:link,
#topnav ul ul li a:visited {
  border: none;
}
#topnav li.last a {
  margin-right: 0;
}
#topnav li a:hover,
#topnav ul li.active {
  color: #ffffff;
  background-color: #059bd8;
}
#topnav li li a:link,
#topnav li li a:visited {
  width: 150px;
  float: none;
  margin: 0;
  padding: 7px 10px;
  font-size: 12px;
  font-weight: normal;
  color: #ffffff;
  background-color: #000000;
}
#topnav li li a:hover {
  color: #ffffff;
  background-color: #059bd8;
}
#topnav li ul {
  background: #ffffff;
  z-index: 9999;
  position: absolute;
  left: -999em;
  height: auto;
  width: 170px;
  border-left: 1px solid #ffffff;
  border-bottom: 1px solid #ffffff;
}
#topnav li ul a {
  width: 140px;
}
#topnav li ul ul {
  margin: -32px 0 0 0;
}
#topnav li:hover ul ul {
  left: -999em;
}
#topnav li:hover ul,
#topnav li li:hover ul {
  left: auto;
}
#topnav li:hover {
  position: static;
}
#topnav li.last a {
  margin-right: 0;
}
</style>
