<template>
  <div class="containerOfAll">
    <h1>Update Session</h1>
    <div class="updateSessionForm">
      <form @submit.prevent="checkData">
        <div class="inputDiv">
          <label for="sessionName">Session Name:</label>
          <input type="text" id="sessionName" v-model="updatedSession.SessionName" required>
        </div>
        <div class="inputDiv">
          <label for="sessionDate">Date:</label>
          <input type="date" id="sessionDate" v-model="updatedSession.Date" required>
        </div>
        <div class="inputDiv">
          <label for="sessionTime">Time:</label>
          <select id="sessionTime" v-model="updatedSession.StartTime" required>
            <option value="">Select Time</option>
            <option v-for="time in times" :key="time" :value="time">{{ time }}</option>
          </select>
        </div>
        <div class="inputDiv">
          <label for="sessionDuration">Duration (minutes):</label>
          <select id="sessionDuration" v-model="updatedSession.Duration" required>
            <option value="">Select Duration</option>
            <option value="30">30 minutes</option>
            <option value="45">45 minutes</option>
            <option value="60">60 minutes</option>
          </select>
        </div>
        <div class="inputDiv">
          <label for="sessionClientID">Client:</label>
          <select id="sessionClientID" v-model="updatedSession.ClientID" required>
            <option value="">Select Client</option>
            <option v-for="client in clients" :key="client.id" :value="client.id">{{ client.name }}</option>
          </select>
        </div>
        <button class="btn" type="submit">Update Session</button>
      </form>
    </div>
    <PopUpModal v-if="showModal" :type="modalType" :message="modalMessage" @close="handleModalClose" />
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
      updatedSession: {
        SessionID: null,
        SessionName: '',
        Date: '',
        StartTime: '', // Ensure this matches one of the options in this.times
        Duration: '',
        ClientID: ''
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
    async fetchSessionData(sessionId) {
      try {
        const response = await fetch(`/api/session/get_session/${sessionId}/${this.coach.id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch session data');
        }
        
        const data = await response.json();
        const session = data.session;

        this.updatedSession.SessionID = session.SessionID;
        this.updatedSession.SessionName = session.SessionName;
        this.updatedSession.Date = session.Date; 
        this.updatedSession.StartTime = this.formatTime(session.StartTime);
        this.updatedSession.Duration = session.Duration;
        this.updatedSession.ClientID = session.ClientID;
      } catch (error) {
        console.error('Error fetching session data:', error.message);
        this.modalType = 'error';
        this.modalMessage = 'Error fetching session data: ' + error.message;
        this.showModal = true;
      }
    },
    async updateSession() {
      try {
        const response = await fetch(`/api/session/update/${this.updatedSession.SessionID}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.updatedSession)
        });

        const data = await response.json();
        if (response.ok) {
          this.message = data.message;
          this.modalType = 'success';
          this.showModal = true;
        } else {
          this.message = data.message || 'Failed to update session';
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

          // Optionally, select the client associated with the session by default
          if (this.clients.length > 0) {
            this.updatedSession.ClientID = this.clients[0].id;
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
      console.log(this.times)
    },
    formatTime(timeString) {
      const [hours, minutes] = timeString.split(':');
      const formattedHours = ('0' + hours).slice(-2); // Ensure two-digit format
      const formattedMinutes = ('0' + minutes).slice(-2); // Ensure two-digit format
      return `${formattedHours}:${formattedMinutes}`;
    },

    checkData() {
      this.updateSession();
    },
    handleModalClose() {
      this.showModal = false;
      this.modalType = '';
      this.modalMessage = '';
    }
  },
  mounted() {
    const sessionId = this.$route.params.id;
    if (sessionId) {
      this.fetchSessionData(sessionId);
    } else {
      // Handle if session ID is not provided in the URL
      console.error('Session ID not found in URL');
      this.modalType = 'error';
      this.modalMessage = 'Session ID not found in URL';
      this.showModal = true;
    }
    this.fetchClients();
    this.generateTimeOptions(); // Generate time options on component mount
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

.updateSessionForm {
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
