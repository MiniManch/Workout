<template>
  <div class="header">
    <LoadingModal :show="loading" />
    <video 
      v-show="!loading"
      autoplay 
      muted 
      loop 
      playsinline 
      class="background-video"
      @loadeddata="handleVideoLoad"
      @error="handleVideoError"
    >
      <source src="videos/homepage.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    <div class="overlay" v-show="!loading">
      <CallToActionBtn text="Your Profile" @clicked="goTo('/coach_profile')" v-if="coach" />
      <div class="logging" v-else>
        <CallToActionBtn text="Login" @clicked="goTo('/login')" />
        <CallToActionBtn text="Register" @clicked="goTo('/register')" />
      </div>
    </div>
  </div>
</template>

<script>
import CallToActionBtn from "@/components/General/buttons/CallToActionBtn.vue";
import LoadingModal from '@/components/General/LoadingModal.vue';

export default {
  components: {
    CallToActionBtn,
    LoadingModal,
  },
  data() {
    const coach = JSON.parse(localStorage.getItem('coach'));
    return {
      coach,
      loading: true,
    };
  },
  methods: {
    goTo(link) {
      this.$router.push(link);
    },
    handleVideoLoad() {
      setTimeout(() => {
        this.loading = false;
      }, 1000);
    },
    handleVideoError() {
      console.error('Failed to load video.');
      this.loading = false;
    },
  },
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

.logging {
  width: 10vw;
  display: flex;
  justify-content: space-between;
}
</style>
