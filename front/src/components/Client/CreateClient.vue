<template>
  <div class="containerOfAll">
    <h1>Add New Client</h1>
    <div class="addClientForm">
      <form @submit.prevent="checkData">
        <div class="inputDiv">
          <label for="clientName">Name:</label>
          <input type="text" id="clientName" v-model="newClient.name" required>
        </div>
        <div class="inputDiv">
          <label for="clientEmail">Email:</label>
          <input type="email" id="clientEmail" v-model="newClient.email" required>
        </div>
        <div class="inputDiv">
          <label for="clientPhone">Phone Number:</label>
          <input type="tel" id="clientPhone" v-model="newClient.phone" required>
        </div>
        <AnimatedButton buttonText="Create Client" />
      </form>
    </div>
    <PopUpModal v-if="showModal" :type="modalType" :message="modalMessage" @close="handleModalClose"/>
  </div>
</template>

<script>
import PopUpModal from '../General/PopUpModal.vue';
import AnimatedButton from '@/components/General/buttons/AnimatedButton.vue';


export default {
  components: {
    PopUpModal,
    AnimatedButton
  },
  data() {
    return {
      newClient: {
        name: '',
        email: '',
        phone: ''
      },
      message: '',
      modalType: '',
      showModal: false,
      coach: JSON.parse(localStorage.getItem('coach'))
    };
  },
  methods: {
    async addClient() {
      try {
        const response = await fetch(`/api/client/coach/${this.coach.id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.newClient)
        });

        const data = await response.json();
        if (response.ok) {
          this.message = data.message;
          this.modalType = 'success';
          this.showModal = true;
          // Optionally reset the form fields after successful submission
          this.newClient.name = '';
          this.newClient.email = '';
          this.newClient.phone = '';
        } else {
          this.message = data.message || 'Failed to add client';
          this.modalType = 'error';
          this.showModal = true;
        }
      } catch (error) {
        this.message = 'An error occurred: ' + error.message;
        this.modalType = 'error';
        this.showModal = true;
      }
    },
    checkData() {
      // Validation functions
      const isNameValid = /^[a-zA-Z\s]+$/.test(this.newClient.name);
      const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.newClient.email);
      const isPhoneValid = /^\d{10}$/.test(this.newClient.phone);

      // Display error modal if any validation fails
      if (!isNameValid) {
        this.modalType = 'error';
        this.modalMessage = 'Invalid name format. Only letters and spaces are allowed.';
        this.showModal = true;
        return;
      }
      if (!isEmailValid) {
        this.modalType = 'error';
        this.modalMessage = 'Invalid email format. Please enter a valid email address.';
        this.showModal = true;
        return;
      }
      if (!isPhoneValid) {
        this.modalType = 'error';
        this.modalMessage = 'Invalid phone number format. Please enter a 10-digit phone number.';
        this.showModal = true;
        return;
      }

      // If all validations pass, proceed to addClient
      this.addClient();
    },
    handleModalClose() {
      this.showModal = false;
      this.modalType = '';
      this.modalMessage = '';
    }
  }
};
</script>

<style scoped>
.containerOfAll {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top:10vh;
}

h1 {
  margin-top: 3vh;
}

.addClientForm {
  width: 25vw;
  margin-top: 3vh;
  padding: 4vh 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgba(130, 130, 130, 0.25);

}

.inputDiv {
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

label {
  margin-bottom: 5px;
  font-size: 1.5em;
}

input {
  width: 15vw;
  padding: 8px;
  margin-bottom:3vh;
  box-sizing: border-box;
  font-size: 1.4em;
}

button {
  padding: 10px 20px;
  font-size: 1.5em;
  background-color: #eeeeee;
  color: #c73659;
  margin-top: 2vh;
  width: fit-content;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
