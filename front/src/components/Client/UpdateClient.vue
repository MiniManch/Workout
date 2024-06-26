<template>
  <div class="containerOfAll">
    <h1>Update Client</h1>
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
        <button class="btn" type="submit">Update Client</button>
      </form>
    </div>
    <PopUpModal v-if="showModal" :type="modalType" :message="modalMessage" @close="handleModalClose"/>
  </div>
</template>

<script>
import PopUpModal from '../General/PopUpModal.vue';

export default {
  components: {
    PopUpModal
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
      clientId: this.$route.params.id || null 
    };
  },
  mounted() {
    if (this.clientId) {
      this.fetchClientById(this.clientId);
    }
  },
  methods: {
    async fetchClientById(clientId) {
      try {
        const response = await fetch(`/api/client/get_client/${clientId}`);
        const data = await response.json();
        if (response.ok) {
          this.newClient = {
            name: data.client.name,
            email: data.client.email,
            phone: data.client.phone
          };
        } else {
          this.message = data.error || 'Failed to fetch client data';
          this.modalType = 'error';
          this.showModal = true;
        }
      } catch (error) {
        this.message = 'An error occurred: ' + error.message;
        this.modalType = 'error';
        this.showModal = true;
      }
    },
    async updateClient() {
      try {
        const response = await fetch(`/api/client/update/${this.clientId}`, {
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
        } else {
          this.message = data.message || 'Failed to update client';
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
      const isNameValid = /^[a-zA-Z\s]+$/.test(this.newClient.name);
      const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.newClient.email);
      const isPhoneValid = /^\d{10}$/.test(this.newClient.phone);

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

      this.updateClient();
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
  background-color: #c73659;
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
