<template>
  <div class="container" :style='style'>
    <div class="center">
      <button class="btn" @click='clicked'>
        <svg width="180px" height="60px" viewBox="0 0 180 60" class="border">
          <polyline points="179,1 179,59 1,59 1,1 179,1" class="bg-line" />
          <polyline points="179,1 179,59 1,59 1,1 179,1" class="hl-line" />
        </svg>
        <span>
          <slot>{{ buttonText }}</slot>
        </span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    buttonText: {
      type: String,
      default: 'HOVER ME',
    },
    style:{
      type:String,
      default:null,
    }
  },
  methods:{
    clicked(){
      this.$emit('clicked');
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Lato:100&display=swap');

.container {
  height: fit-content;
  width: fit-content;
  transform: translate(-50%, -50%);
  display: flex;
  justify-content: center;
  align-items: center;

  padding-top: 5vh;
}

.center {
  width: 180px;
  height: 60px;
  position: absolute;
}

.btn {
  width: 180px;
  height: 60px;
  cursor: pointer;
  background: transparent;
  outline: none;
  transition: 1s ease-in-out;
}

svg {
  position: absolute;
  left: 0;
  top: 0;
  fill: none;
  stroke: #fff;
  stroke-dasharray: 150 480;
  stroke-dashoffset: 150;
  transition: 1s ease-in-out;
}

.btn:hover {
  transition: 1s ease-in-out;
  background: black;
  color: black;
}

.btn:hover svg {
  stroke-dashoffset: -480;
}

.btn span {
  color: white;
  font-size: 18px;
  font-family: "Jost";
}

.btn:hover span {
  color: white;
}
</style>
