<template>
    <div class="modal" >
      <div class="modal-content">
        <span class="close" @click="handleClose">&times;</span>
        <h2>{{ title }}</h2>
        <p>{{ message }}</p>
        <div class="modal-actions">
          <button class="btn btn-yes" @click="handleYes">Yes</button>
          <button class="btn btn-no" @click="handleClose">No</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      title: {
        type: String,
        default: 'Confirmation'
      },
      message: {
        type: String,
        default: 'Are you sure?'
      }
    },
    methods: {
      handleYes() {
        this.$emit('yes');
      },
      handleClose() {
        this.$emit('close');
      }
    }
  };
  </script>
  
  <style scoped>
  .modal {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);

    z-index: 5;
  }
  
  .modal-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    width: 80%;
    max-width: 600px;
    text-align: center;
  }
  
  .close {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 1.5em;
    cursor: pointer;
  }
  
  .modal-actions {
    margin-top: 20px;
  }
  
  .btn {
    padding: 10px 20px;
    margin: 0 10px;
    cursor: pointer;
    border-radius: 5px;
    border: none;
    font-size: 1.2em;
    transition: background-color 0.3s ease;
  }
  
  .btn-yes {
    background-color: #4CAF50;
    color: white;
  }
  
  .btn-no {
    background-color: #f44336;
    color: white;
  }
  
  .btn-yes:hover, .btn-no:hover {
    opacity: 0.8;
  }
  </style>
  