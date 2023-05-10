<template>
  <div>
    <div class="water-group">
      <div
        class="water water1"
      ></div>
      <div
        class="water water2"
      ></div>
      <div
        class="water water3"
      ></div>
      <div
        class="water water4"
      ></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WaveBottom',
  props: {
  },
  computed: {
  },
  data() {
    return {
    }
  },
  methods: {
  },
  watch: {
  }
}
</script>

<style scoped>
.water-group {
  position: fixed;
  z-index: 200;
  bottom: -5px;
  height: 110px;
  width: 100%;
  overflow: hidden;
}
.water-group .water {
  position: absolute;
  width: 200%;
  height: 100%;
  background-image: url('../../../public/wave.png');
  background-size: 50% 100%;
}
.water-group .water1 {
  top: 20px;
  left: -100%;
  opacity: 0.2;
  animation: water-right 20s infinite linear;
}
.water-group .water2 {
  top: 30px;
  left: 0;
  opacity: 0.3;
  animation: water-left 30s infinite linear;
}
.water-group .water3 {
  top: 40px;
  left: -100%;
  opacity: 0.5;
  animation: water-right 40s infinite linear;
}
.water-group .water4 {
  top: 10px;
  left: 0;
  opacity: 0.1;
  animation: water-left 15s infinite linear;
}
@keyframes water-right {
  0% {
    transform: translateX(0) translateZ(0) scaleY(1);
  }
  50% {
    transform: translateX(25%) translateZ(0) scaleY(0.85);
  }
  100% {
    transform: translateX(50%) translateZ(0) scaleY(1);
  }
}
@keyframes water-left {
  from {
    transform: translate(0%, 0px);
  }
  to {
    transform: translate(-50%, 0px);
  }
}
</style>
