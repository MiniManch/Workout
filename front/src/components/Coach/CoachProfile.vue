<template>
    <div class="containerOfAll">
      <div class="coachProfile">
        <h1>Your Profile!</h1>
        <form @submit.prevent="">
          <div class="inputDiv">
            <label for="name">Name:</label>
            <input type="text" id="name" v-model="name" required>
            <button class="btn" @click="updateField('name')">Update Name</button>
          </div>
          <div class="inputDiv">
            <label for="email">Email:</label>
            <input type="email" id="email" v-model="email" required>
            <button class="btn" @click="updateField('email')">Update Email</button>
          </div>
          <div class="inputDiv">
            <label for="phone">Phone Number:</label>
            <input type="tel" id="phone" v-model="phone" required>
            <button class="btn" @click="updateField('phone')">Update Phone</button>
          </div>
        </form>
  
        <!-- Table of Coach's Clients -->
        <div class="clientTable" v-if="clients.length > 0">
          <h2>Your Clients</h2>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="client in clients" :key="client.id">
                <td>{{ client.name }}</td>
                <td>{{ client.email }}</td>
                <td>{{ client.phone }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <PopUpModal v-if="showModal" :type="modalType" :message="modalMessage" @close="handleModalClose"/>
      </div>
    </div>
  </template>
  
  <script>
  import PopUpModal from '@/components/General/PopUpModal.vue';
  
  export default {
    components: {
      PopUpModal
    },
    data() {
      return {
        coach: JSON.parse(localStorage.getItem("coach")),
        name: null,
        email: null,
        phone: null,
        clients: [], // Array to hold coach's clients
        message: '',
        messageClass: '',
        showModal: false,
        modalType: '',
        modalMessage: '',
      };
    },
    mounted() {
      if (!this.coach) {
        this.$router.push({ name: 'Login' });
      } else {
        this.name = this.coach.name;
        this.email = this.coach.email;
        this.phone = this.coach.phone;
  
        // Fetch coach's clients
        this.fetchClients();
      }
    },
    methods: {
      async fetchClients() {
        try {
          const response = await fetch(`/api/client/${this.coach.id}/clients`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            }
          });
  
          if (response.ok) {
            const data = await response.json();
            this.clients = data.clients;
          } else {
            throw new Error('Failed to fetch clients');
          }
        } catch (error) {
          console.error('Error fetching clients:', error.message);
        }
      },
      async updateField(field) {
        const newValue = this[field];
        const currentValue = this.coach[field];
  
        // Check if the new value is the same as the current value
        if (newValue === currentValue) {
          this.message = `You didn't change anything for ${field}. No update performed.`;
          this.messageClass = 'error';
          this.modalType = 'error';
          this.modalMessage = this.message;
          this.showModal = true;
          return;
        }
  
        const payload = { value: newValue };
  
        try {
          const response = await fetch(`/api/coach/update/${field}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'CoachID': this.coach.id
            },
            body: JSON.stringify(payload)
          });
  
          const data = await response.json();
          if (response.ok) {
            this.message = data.message;
            this.messageClass = 'success';
            this.modalType = 'success';
            this.modalMessage = data.message;
  
            // Update local storage
            this.coach[field] = newValue;
            localStorage.setItem('coach', JSON.stringify(this.coach));
  
            this.showModal = true;
          } else {
            this.message = data.message || 'An error occurred';
            this.messageClass = 'error';
            this.modalType = 'error';
            this.modalMessage = data.message || 'An error occurred';
            this.showModal = true;
          }
        } catch (error) {
          this.message = 'An error occurred: ' + error.message;
          this.messageClass = 'error';
          this.modalType = 'error';
          this.modalMessage = 'An error occurred: ' + error.message;
          this.showModal = true;
        }
      },
      handleModalClose() {
        this.showModal = false;
        this.$router.push({ name: 'CoachProfile' });
      }
    }
  };
  </script>
  
  <style scoped>
  .containerOfAll {
    width: 100%;
    height: 80%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  
  .coachProfile {
    margin-top: 6vh;
    font-family: "Jost";
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  
  form {
    margin-top: 3vh;
    width: 25vw;
    padding: 4vh 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #c73659;
  }
  
  .inputDiv {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .coachProfile div {
    margin-bottom: 10px;
  }
  
  .coachProfile label {
    display: block;
    margin-bottom: 5px;
    font-size: 1.5em;
  }
  
  .coachProfile input {
    width: 15vw;
    padding: 8px;
    box-sizing: border-box;
    font-size: 1.4em;
  }
  
  .coachProfile button {
    padding: 10px 20px;
    font-size: 1.5em;
    background-color: #eeeeee;
    color: #c73659;
    margin-top: 2vh;
    width: fit-content;
  }
  
  .success {
    color: green;
  }
  
  .error {
    color: red;
  }
  
  .clientTable {
    margin-top: 3vh;
    width: 25vw;
  }
  
  .clientTable h2 {
    font-size: 1.8em;
    margin-bottom: 1vh;
  }
  
  .clientTable table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .clientTable th,
  .clientTable td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  .clientTable th {
    background-color: #f2f2f2;
    color: #333;
  }
  </style>
  