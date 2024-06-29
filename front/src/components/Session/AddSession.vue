<template>
    <div class="containerOfAll">
      <h1>Add New Session</h1>
      <div class="addSessionForm">
        <form @submit.prevent="checkData">
          <div class="inputDiv">
            <label for="sessionName">Session Name:</label>
            <input type="text" id="sessionName" v-model="newSession.name" required>
          </div>
          <div class="inputDiv">
            <label for="sessionDate">Date:</label>
            <input type="date" id="sessionDate" v-model="newSession.date" required>
          </div>
          <div class="inputDiv">
            <label for="sessionTime">Time:</label>
            <select id="sessionTime" v-model="newSession.time" required>
              <option value="">Select Time</option>
              <!-- Generate time options in 15-minute increments -->
              <option v-for="time in times" :key="time">{{ time }}</option>
            </select>
          </div>
          <div class="inputDiv">
            <label for="sessionDuration">Duration (minutes):</label>
            <select id="sessionDuration" v-model="newSession.duration" required>
              <option value="">Select Duration</option>
              <option value="30">30 minutes</option>
              <option value="45">45 minutes</option>
              <option value="60">60 minutes</option>
            </select>
          </div>
          <div class="inputDiv">
            <label for="sessionClientID">Client:</label>
            <select id="sessionClientID" v-model="newSession.client_id" required>
              <option value="">Select Client</option>
              <option v-for="client in clients" :key="client.id" :value="client.id">
                {{ client.name }}
              </option>
            </select>
          </div>
          <button class="btn" type="submit">Add Session</button>
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
        newSession: {
          name: '',
          date: '',
          time: '',
          duration: '',
          client_id: ''
        },
        message: '',
        modalType: '',
        showModal: false,
        coach: JSON.parse(localStorage.getItem('coach')),
        clients: [],
        times: [] // To store time options
      };
    },
    methods: {
      async addSession() {
        try {
          const response = await fetch(`api/session/add/${this.coach.id}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.newSession)
          });
  
          const data = await response.json();
          if (response.ok) {
            this.message = data.message;
            this.modalType = 'success';
            this.showModal = true;
            this.newSession.name = '';
            this.newSession.date = '';
            this.newSession.time = '';
            this.newSession.duration = '';
            this.newSession.client_id = '';
          } else {
            this.message = data.message || 'Failed to add session';
            this.modalType = 'error';
            this.showModal = true;
          }
        } catch (error) {
          this.message = 'An error occurred: ' + error.message;
          this.modalType = 'error';
          this.showModal = true;
        }
      },
      async fetchClients() {
        try {
          const response = await fetch(`/api/client/get_coach_client_data/${this.coach.id}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
          });
  
          if (response.ok) {
            const data = await response.json();
            this.clients = data.clients;
  
            // Optionally, select the first client by default
            if (this.clients.length > 0) {
              this.newSession.client_id = this.clients[0].id;
            }
          } else {
            throw new Error('Failed to fetch clients');
          }
        } catch (error) {
          console.error('Error fetching clients:', error.message);
          this.modalType = 'error';
          this.modalMessage = 'Error fetching clients: ' + error.message;
          this.showModal = true;
        }
      },
      generateTimeOptions() {
        const times = [];
        for (let hour = 0; hour < 24; hour++) {
          for (let minute = 0; minute < 60; minute += 15) {
            const formattedHour = ('0' + hour).slice(-2);
            const formattedMinute = ('0' + minute).slice(-2);
            times.push(`${formattedHour}:${formattedMinute}`);
          }
        }
        this.times = times;
      },
      checkData() {
        const isNameValid = /^[a-zA-Z\s]+$/.test(this.newSession.name);
        const isDateValid = this.newSession.date !== '';
        const isTimeValid = this.newSession.time !== '';
        const isDurationValid = ['30', '45', '60'].includes(this.newSession.duration);
        const isClientIDValid = /^\d+$/.test(this.newSession.client_id);
  
        // Additional validation: Check if the selected date is not in the past
        const selectedDate = new Date(this.newSession.date + 'T' + this.newSession.time);
        const currentDate = new Date();
  
        if (selectedDate < currentDate) {
          this.modalType = 'error';
          this.modalMessage = 'Cannot set a session in the past.';
          this.showModal = true;
          return;
        }
  
        // Display error modal if any validation fails
        if (!isNameValid) {
          this.modalType = 'error';
          this.modalMessage = 'Invalid session name format. Only letters and spaces are allowed.';
          this.showModal = true;
          return;
        }
        if (!isDateValid) {
          this.modalType = 'error';
          this.modalMessage = 'Please select a valid date.';
          this.showModal = true;
          return;
        }
        if (!isTimeValid) {
          this.modalType = 'error';
          this.modalMessage = 'Please select a valid time.';
          this.showModal = true;
          return;
        }
        if (!isDurationValid) {
          this.modalType = 'error';
          this.modalMessage = 'Please select a valid session duration.';
          this.showModal = true;
          return;
        }
        if (!isClientIDValid) {
          this.modalType = 'error';
          this.modalMessage = 'Invalid client ID format. Please enter a number.';
          this.showModal = true;
          return;
        }
  
        // If all validations pass, proceed to addSession
        this.addSession();
      },
      handleModalClose() {
        this.showModal = false;
        this.modalType = '';
        this.modalMessage = '';
      }
    },
    mounted() {
      this.fetchClients();
      this.generateTimeOptions(); // Generate time options on component mount
    },
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
  
  .addSessionForm {
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
  
  input,
  select {
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
  