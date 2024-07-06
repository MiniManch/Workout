<template>
    <div v-if="show" class="loading-modal">
      <div class="loading-content">
        <img src="/videos/loading.gif" alt="Loading..." />
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      show: {
        type: Boolean,
        required: true
      },
    }
  };
  </script>
  
  <style scoped>
  .loading-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 5;
  }
  
  .loading-content {
    padding: 20px;
    border-radius: 10px;
  }
  
  .loading-content img {
    width: 100px;
    height: 100px;
  }
  </style>
  