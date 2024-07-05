<template>
  <div class="header">
    <video autoplay muted loop playsinline class="background-video">
      <source src="videos/homepage.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    <div class="overlay">
      <CallToActionBtn text="Your Profile" @clicked="goTo('/coach_profile')" v-if='coach'/>
      <div class='logging' v-else>
        <CallToActionBtn text="Login" @clicked="goTo('/login')"/>
        <CallToActionBtn text="Register" @clicked="goTo('/register')"/>
      </div>
    </div>
  </div>
</template>

<script>
import CallToActionBtn from "@/components/General/buttons/CallToActionBtn.vue";

export default {
  components:{
    CallToActionBtn
  },
  data(){
    const coach = JSON.parse(localStorage.getItem('coach'));
    return{
      coach,
    }  
  },
  methods:{
    goTo(link){
      this.$router.push(link);
    },
  }
};
</script>

<style scoped>
.header {
  position: relative;
  width: 100%;
  height: 100vh;
}

.background-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1; 
}

.overlay {
  position: relative;
  height: 100%;
  width: 100vw;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2; 
}

.logging{
  width:10vw;
  display:flex;
  justify-content: space-between;
}
</style>
