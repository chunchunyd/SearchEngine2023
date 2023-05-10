<template>
  <div class="home">
    <!-- Topbar Start -->
    <div class="container-fluid bg-dark px-5 d-none d-lg-block">
        <div class="row gx-0">
            <div class="col-lg-8 text-center text-lg-start mb-2 mb-lg-0">
                <div class="d-inline-flex align-items-center" style="height: 45px;">
                    <small class="me-3 text-light"><i class="fa fa-map-marker-alt me-2"><router-link to="/">Home</router-link></i></small>
                    <small class="me-3 text-light"><i class="fa fa-phone-alt me-2"><router-link to="/about">About</router-link></i></small>
                    <small class="me-3 text-light"><i class="fa fa-phone-alt me-2" v-on:click="back">Back</i></small>
                </div>
            </div>
        </div>
    </div>
    <!-- Topbar End -->

    <SearchBar v-show="status==0"
    :to_display="to_display"></SearchBar>
    <DisplayBar  v-show="status==1"
    :addr="display_idx"></DisplayBar>
  </div>
</template>

<script>
import SearchBar from '@/components/judicial/SearchBar.vue'
import DisplayBar from '@/components/judicial/DisplayBar.vue'
export default {
  name: 'InitView',
  components: {
    SearchBar,
    DisplayBar
  },
  data() {
    return {
      status: 0,
      display_idx: 0
    }
  },
  mounted() {
  },
  methods: {
    to_display (addr) {
      this.display_idx = addr
      this.status = 1
    },
    back() {
      this.status = 0
    }
  }
}
</script>

<style scoped lang="scss">
a {
  color: #ffffff;
}
</style>
