<template>
    <div class="loginForm">
      <h1>Login</h1>
      <form @submit.prevent="LogInCoach">
        <input class='form-control' type="text" v-model="coachName" placeholder="Enter coach name" />
        <AnimatedButton buttonText="Login!"/>
      </form>
    </div>
    <PopUpModal 
      v-if="showModal"
      :message="modalMessage"
      :type="modalType"
      @close="handleModalClose"
    />
  </template>
  
<script>
import PopUpModal from "@/components/General/PopUpModal.vue";
import AnimatedButton from "../General/buttons/AnimatedButton.vue";

export default {
  components: {
    PopUpModal,
    AnimatedButton
  },
  data() {
    return {
      coachName: '',
      showModal: false,
      modalType: 'success', // or 'error'
      modalMessage: '',
    };
  },
  methods: {
    async LogInCoach() {
      try {
        const response = await fetch(`/api/coach/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name: this.coachName })
        });

        const data = await response.json();
        if (response.ok) {
          this.modalMessage = data.message;
          this.modalType = 'success';
          localStorage.setItem('coach', JSON.stringify(data.coach_data)); // Store the full coach data in localStorage
          
          this.showModal = true;
        } else {
          this.modalMessage = data.message || 'An error occurred';
          this.modalType = 'error';
          this.showModal = true;
        }
      } catch (error) {
        this.modalMessage = 'An error occurred: ' + error.message;
        this.modalType = 'error';
        this.showModal = true;
      }
    },
    handleModalClose() {
      this.showModal = false;
      if (this.modalType === 'success') {
        this.$router.push('/');
      }
    }
  }
};
</script>
  
  <style scoped>
  .loginForm {
    width: 100%;
    height: 60%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    font-size: 2em;
  }
  
  form {
    width: 25vw;
    height: 20vh;
    background-color: rgba(130, 130, 130, 0.4);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2vh;
  }
  
  input {
    width: 20vw;
    height: 5vh;
  }
  
  button {
    font-size: 1em;
    background-color: #eeeeee;
    color:#c73659;
  }

  p {
    margin-top: 1em;
    font-size: 1em;
  }
  h1{
    margin-bottom:3vh;
  }
  </style>
  