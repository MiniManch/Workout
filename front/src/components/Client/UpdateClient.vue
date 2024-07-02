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
        <button class="btn update-btn" type="submit">Update Client</button>
      </form>
    </div>
    <div v-if="clientSessions.length" class="sessionsList">
      <h2>Client Sessions</h2>
      <ul>
        <li v-for="session in sortedSessions" :key="session.id" class="session">
          <div class="">
          {{ formatDate(session.Date) }} - {{ session.StartTime.substring(0, session.StartTime. length - 3)  }} {{ session.SessionName }}, {{ session.Duration }} Minutes
          </div>
          <button class="btn btn-warning" @click="confirmAction(session.id)">Delete</button>
        </li>
      </ul>
    </div>
    <PopUpModal v-if="showModal" :type="modalType" :message="modalMessage" @close="handleModalClose"/>
    <YesOrNoModal v-if="showYesNoModal" @close="handleYesNoModalClose" @yes="performAction" />
  </div>
</template>

<script>
import PopUpModal from '../General/PopUpModal.vue';
import YesOrNoModal from '@/components/General/YesOrNoModal.vue';

export default {
  components: {
    PopUpModal,
    YesOrNoModal
  },
  data() {
    return {
      coach:JSON.parse(localStorage.getItem('coach')) || {},
      newClient: {
        name: '',
        email: '',
        phone: ''
      },
      message: '',
      modalType: '',
      showModal: false,
      showYesNoModal:false,
      clientId: this.$route.params.id || null,
      clientSessions: [],
      itemToDelete:''
    };
  },
  computed: {
    sortedSessions() {
      return [...this.clientSessions].sort((a, b) => {
        const dateA = new Date(`${a.Date} ${a.StartTime}`);
        const dateB = new Date(`${b.Date} ${b.StartTime}`);
        return dateA - dateB;
      });
    }
  },
  mounted() {
    if (this.clientId) {
      this.fetchClientById(this.clientId);
      this.fetchClientSessions(this.clientId);
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
    async fetchClientSessions(clientId) {
      try {
        const response = await fetch(`/api/session/get_client_sessions/${clientId}`);
        const data = await response.json();
        if (response.ok) {
          this.clientSessions = data.sessions;
          console.log(data.sessions)
        
        } else {
          this.message = data.error || 'Failed to fetch client sessions';
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
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('en-US', options);
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
    },
    handleYesNoModalClose() {
      this.showYesNoModal = false;
      this.itemToDelete = null;
    },
    confirmAction(itemId) {
      console.log(itemId)
      this.itemToDelete = itemId;
      this.showYesNoModal = true;
    },
    async performAction() {
      await this.deleteItem({ itemId: this.itemToDelete });
      this.showYesNoModal = false;
      this.itemToDelete = null;
      this.modalMessage = `Session was deleted.`;
      this.modalType = 'success';
      this.showModal = true;
    },
    async deleteItem({ itemId }) {
      try {
        const response = await fetch(`/api/session/delete/${this.coach.id}/${itemId}`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        this.modalType = response.ok ? 'success' : 'error';
        this.modalMessage = data.message || `Failed to delete ${this.typeOfData}`;
        if (response.ok) {
          this.clientSessions = this.clientSessions.filter(session => session.id !== itemId);
        }
        this.showModal = true;
      } catch (error) {
        this.modalType = 'error';
        this.modalMessage = `An error occurred: ${error.message}`;
        this.showModal = true;
      }
    },
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

.update-btn {
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

.sessionsList {
  width: fit-content;
  margin-top: 20px;

  display:flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.sessionsList h2 {
  width:fit-content;
  font-size: 2em;
  margin-bottom: 10px;
}

.sessionsList ul {
  list-style: none;
  width:20vw;
  padding: 0;
}

.sessionsList li {
  background-color: #c73659;
  padding: 10px;
  margin-bottom: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
.session{
  display:flex;
  justify-content: space-between;
  align-items: center;
}

.session > button{
  padding: 5px 10px;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
