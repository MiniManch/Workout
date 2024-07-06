<template>
    <div>
      <img
        src="/images/background.jpg"
        alt=""
        class="backgroundImage"
        @load="handleImageLoad"
        @error="handleImageError"
        v-show="!loading"
      />
      <div class="overlay" v-show="!loading"></div>
      <LoadingModal :show="loading" />
    </div>
  </template>
  
  <script>
  import LoadingModal from '@/components/General/LoadingModal.vue';
  
  export default {
    data() {
      return {
        loading: true,
      };
    },
    components: {
      LoadingModal,
    },
    methods: {
      handleImageLoad() {
        setTimeout(()=>{
            this.loading = false;
        },1000)
      },
      handleImageError() {
        console.error('Failed to load background image.');
        this.loading = false;
      },
    },
  };
  </script>
  
  <style>
  .backgroundImage {
    position: absolute;
    top: 0;
    left: 0;
    z-index: -3;
    height: 100vh;
    width: 100vw;
  }
  
  .overlay {
    position: absolute;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: -2;
  }
  </style>
  