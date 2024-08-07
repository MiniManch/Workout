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
        <AnimatedButton buttonText="Create" />
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
      times: [] 
    };
  },
  methods: {
    async addSession() {
      console.log('add')
      try {
        const response = await fetch(`/api/session/coach/${this.coach.id}`, {
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
        const response = await fetch(`/api/client/coach/${this.coach.id}`, {
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
    this.generateTimeOptions();
    
    const routeDate = this.$route.params.date;
    if (routeDate) {
      this.newSession.date = routeDate; 
    }
  },
};
</script>
<style scoped>
.containerOfAll {
  width: 100%;
  height: 80%;
  padding-top: 15vh;
  display: flex;
  flex-direction:column ;
  align-items: center;
  justify-content: center;
}

.addSessionForm {
  width: 25vw;
  padding: 4vh 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(130, 130, 130, 0.25);
}

form{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap:2vh;
}

.inputDiv {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

label {
  display: block;
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

h1 {
  margin-top: 3vh;
}
</style>
