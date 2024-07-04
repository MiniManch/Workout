<template>
    <div class="header">
      <video autoplay muted loop playsinline class="background-video">
        <source src="videos/homepage.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
      <div class="overlay">
      </div>
    </div>
    <button class="profileButton" role="button" @click='goToProfile'><span class="text">Coach Profile</span></button>
  </template>
  
  <script>
  export default {
    data() {
      return {
        coach: null,
      };
    },
    mounted() {
      this.coach = JSON.parse(localStorage.getItem('coach')) || null;
    },
    methods:{
        goToProfile(){
            this.$router.push('/coach_profile');
        }
    }
  };
  </script>
  
<style scoped>

.header {
    position: relative;
    width:100%;
    height:100vh;
}

.background-video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -4; 
}

.overlay {
    position: relative;
    height:100%;
    width:100vw;
    z-index: -3;
    background-color: rgba(0,0,0,0.6);

    display:flex;
    justify-content: center;
    align-items: center;

}
.profileButton {
  appearance: none;
  text-decoration: none;
    color: white;
  background-color: rgba(0,0,0,0);
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
  transition: opacity 300ms cubic-bezier(.694, 0, 0.335, 1),background-color 100ms cubic-bezier(.694, 0, 0.335, 1),color 100ms cubic-bezier(.694, 0, 0.335, 1);
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  vertical-align: baseline;
  white-space: nowrap;

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
.profileButton:hover{
  color:black;
}
.profileButton span {
  z-index: 1;
  position: relative;
}


</style>
  