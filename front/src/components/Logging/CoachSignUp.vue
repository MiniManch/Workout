<template>
  <div class="containerOfAll">
    <div class="register-form">
      <h1>Sign Up as a Coach!</h1>
      <form @submit.prevent="register">
        <div>
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="name" required>
        </div>
        <div>
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" required>
        </div>
        <div>
          <label for="phone">Phone Number:</label>
          <input type="tel" id="phone" v-model="phone" required>
        </div>
        <button class="btn" type="submit">Register</button>
      </form>
    </div>
    <PopUpModal v-if="showModal" :type="modalType" :message="modalMessage" @close="handleModalClose"/>
  </div>
</template>

<script>
import PopUpModal from '@/components/General/PopUpModal.vue';

export default {
  components: {
    PopUpModal,
  },
  data() {
    return {
      name: '',
      email: '',
      phone: '',
      message: '',
      messageClass: '',
      showModal: false,
      modalType: '',
      modalMessage: '',
    };
  },
  methods: {
    async register() {
      try {
        const response = await fetch(`/api/coach/create`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.name,
            email: this.email,
            phone: this.phone,
          }),
        });

        const data = await response.json();
        if (response.ok) {
          this.modalMessage = data.message;
          this.modalType = 'success';
          this.showModal = true;
        } else if (response.status === 409) {
          this.modalMessage = data.message;
          this.modalType = 'error';
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
      this.$router.push({ name: 'CoachProfile' });
    },
  },
};
</script>
  
  <style scoped>
  .containerOfAll{
    width:100%;
    height:60%;

    display:flex;
    flex-direction:column;
    justify-content: center;
    align-items: center;
  }

  .register-form {
    font-family: "Jost";
    
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  form{
    margin-top:3vh;
    width:25vw;
    padding:4vh 0 4vh 0;
    display:flex;
    flex-direction: column;
    align-items: center;
    background-color: #c73659;

  }
  .register-form div {
    margin-bottom: 10px;
  }
  .register-form label {
    display: block;
    margin-bottom: 5px;
    font-size: 1.5em;
  }
  .register-form input {
    width:15vw;
    padding: 8px;
    box-sizing: border-box;
  }
  .register-form button {
    padding: 10px 20px;
    font-size: 1.5em;
    background-color: #eeeeee;
    color:#c73659;

    margin-top: 2vh;
  }
  .success {
    color: green;
  }
  .error {
    color: red;
  }
  </style>
  