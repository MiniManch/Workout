<template >
    <div>
      <button class="profileButton" role="button" @click='clicked'><span class="text">{{text}}</span></button>
    </div>
</template>
<script>
export default {
    props: {
    text: {
      type: String,
      default: null
    },
  },
  methods: {
    clicked() {
      this.$emit('clicked');
    }
  }
}
</script>

<style>
.profileButton {
    appearance: none;
    text-decoration: none;
    color: white;
    background-color: rgba(0, 0, 0, 0);
    border-width: 0;
    box-sizing: border-box;
    cursor: pointer;
    display: inline-block;
    font-family: "Jost";
    font-size: 20px;
    font-weight: 500;
    letter-spacing: 0;
    line-height: 1em;
    margin: 0;
    opacity: 1;
    outline: 0;
    padding: 1.5em 2.2em;
    position: relative;
    text-align: center;
    text-rendering: geometricprecision;
    text-transform: uppercase;
    transition: opacity 300ms cubic-bezier(.694, 0, 0.335, 1), background-color 100ms cubic-bezier(.694, 0, 0.335, 1), color 100ms cubic-bezier(.694, 0, 0.335, 1);
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    vertical-align: baseline;
    white-space: nowrap;
    z-index: 3; /* Highest z-index */
  }
  
  .profileButton:before {
    animation: opacityFallbackOut .5s step-end forwards;
    backface-visibility: hidden;
    background-color: #EBEBEB;
    clip-path: polygon(-1% 0, 0 0, -25% 100%, -1% 100%);
    content: "";
    height: 100%;
    left: 0;
    position: absolute;
    top: 0;
    transform: translateZ(0);
    transition: clip-path .5s cubic-bezier(.165, 0.84, 0.44, 1), -webkit-clip-path .5s cubic-bezier(.165, 0.84, 0.44, 1);
    width: 100%;
  }
  
  .profileButton:hover:before {
    animation: opacityFallbackIn 0s step-start forwards;
    clip-path: polygon(0 0, 101% 0, 101% 101%, 0 101%);
  }
  
  .profileButton:after {
    background-color: #FFFFFF;
  }
  
  .profileButton:hover {
    color: black;
  }
  
  .profileButton span {
    position: relative;
  }
</style>
