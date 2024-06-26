<template>
    <div class="modal">
      <div class="modal-content" :class="modalTypeClass">
        <h2>{{ modalTitle }}</h2>
        <p>{{ message }}</p>
        <button :class='buttonClass' @click="closeModal">OK</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      type: {
        type: String,
        required: true,
      },
      message: {
        type: String,
        required: true,
      }
    },
    computed: {
      modalTypeClass() {
        return {
          'modal-error': this.type === 'error',
          'modal-success': this.type === 'success',
        };
      },
      modalTitle() {
        return this.type === 'error' ? 'Oops! There\'s an error' : 'Success!';
      },
      buttonClass(){
        return this.type === 'error' ? 'btn btn-danger' : 'btn btn-success';
      }
    },
    methods: {
      closeModal() {
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
    z-index: 6;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgb(0,0,0);
    background-color: rgba(0,0,0,0.4);
  }
  
  .modal-content {
    background-color: #fefefe;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    max-width: 500px;
    text-align: center;
  }
  
  .modal-error {
    border: 5px solid red;
    color:red;
  }
  
  .modal-success {
    border: 5px solid green;
    color:green;
  }
  
  .close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }
  
  .close:hover,
  .close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
  </style>
  