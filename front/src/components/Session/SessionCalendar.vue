<template>
  <div class="containerOfAll">
    <div class="calendar">
      <div class="header">
        <button class="btn" @click="prevMonth">
          <img src="/icons/back-50.png" alt="">
        </button>
        <span class="currentMonth">{{ currentMonthYear }}</span>
        <button class="btn" @click="nextMonth">
          <img src="/icons/next-50.png" alt="">
        </button>
      </div>
      <div class="days">
        <div
          class="day"
          v-for="day in days"
          :key="day.date"
          @click="openTable(day)"
        >
          <div :class="{ today: isToday(day.date) }">
            {{ day.date.getDate() }}
            <template v-if="isToday(day.date)">
              <img v-tooltip="'today'" src="/icons/today-50.png" alt="Today" class="today-icon">
            </template>
          </div>
          <div v-if="day.appointments.length > 1" class="appointment">
            Multiple appointments
          </div>
          <div v-else-if="day.appointments.length === 1" class="appointment">
            {{ day.appointments[0].ClientName }} at {{ formatTime(day.appointments[0].StartTime) }}
          </div>
        </div>
      </div>
    </div>
    <PopUpModal v-if="showModal" :type="modalType" :message="modalMessage" @close="handleModalClose" />
    <PaginatedTableModal
      v-if="showTable"
      :show="showTable"
      :data="tableData"
      :itemsPerPage="5"
      :title="tableTitle"
      type="session"
      @close="closeTable"
      @delete-item="confirmAction"       
      @update-item="handleUpdate"
    />
    <YesOrNoModal v-if="showYesNoModal" @close="handleYesNoModalClose" @yes="performAction" />
  </div>
</template>

<script>
import PopUpModal from '../General/PopUpModal.vue';
import PaginatedTableModal from "@/components/General/PaginatedTableModal.vue";
import YesOrNoModal from "@/components/General/YesOrNoModal.vue";

export default {
  components: {
    PopUpModal,
    PaginatedTableModal,
    YesOrNoModal
  },
  data() {
    return {
      coach: JSON.parse(localStorage.getItem('coach')),
      modalType: '',
      showModal: false,
      modalMessage: '',
      currentDate: new Date(),
      appointments: [],
      showTable: false,
      tableData: [],
      tableTitle: '',
    };
  },
  computed: {
    currentMonthYear() {
      const options = {
        year: 'numeric',
        month: 'long'
      };
      return this.currentDate.toLocaleDateString(undefined, options);
    },
    days() {
      const start = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), 1);
      const end = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 0);
      const days = [];
      for (let day = start; day <= end; day.setDate(day.getDate() + 1)) {
        const date = new Date(day);
        days.push({
          date,
          appointments: this.getAppointmentsForDay(date)
        });
      }
      return days;
    }
  },
  mounted() {
    this.fetchAppointments();
  },
  methods: {
    async fetchAppointments() {
      try {
        const response = await fetch(`/api/session/get_coach_session_data/${this.coach.id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          this.appointments = data.sessions;
        } else {
          throw new Error('Failed to fetch sessions');
        }
      } catch (error) {
        console.error('Error fetching sessions:', error.message);
        this.modalType = 'error';
        this.modalMessage = 'Error fetching sessions: ' + error.message;
        this.showModal = true;
      }
    },
    prevMonth() {
      this.currentDate.setMonth(this.currentDate.getMonth() - 1);
      this.currentDate = new Date(this.currentDate);
    },
    nextMonth() {
      this.currentDate.setMonth(this.currentDate.getMonth() + 1);
      this.currentDate = new Date(this.currentDate);
    },
    isToday(date) {
      const today = new Date();
      return date.getDate() === today.getDate() &&
        date.getMonth() === today.getMonth() &&
        date.getFullYear() === today.getFullYear();
    },
    handleModalClose() {
      this.modalType = '';
      this.modalMessage = '';
      this.showModal = false;
    },
    formatTime(timeString) {
      const [hours, minutes] = timeString.split(':');
      const period = +hours >= 12 ? 'PM' : 'AM';
      const formattedHours = +hours % 12 || 12;
      return `${formattedHours}:${minutes} ${period}`;
    },
    getAppointmentsForDay(date) {
      return this.appointments.filter(appointment => {
        const appointmentDate = new Date(appointment.Date);
        return appointmentDate.getFullYear() === date.getFullYear() &&
               appointmentDate.getMonth() === date.getMonth() &&
               appointmentDate.getDate() === date.getDate();
      });
    },
    openTable(day) {
      if (day.appointments.length > 0) {
        this.tableData = day.appointments;
        this.tableTitle = `Appointments on ${day.date.toLocaleDateString()}`;
        this.typeOfData = 'appointments';
        this.showTable = true;
      }
    },
    closeTable() {
      this.showTable = false;
      this.tableData = [];
      this.tableTitle = '';
      this.typeOfData = '';
    },
    confirmAction({ itemId }) {
      this.itemToDelete = itemId;
      this.showYesNoModal = true;
    },
    async performAction() {
      await this.deleteItem({ itemId: this.itemToDelete });
      this.showYesNoModal = false;
      this.itemToDelete = null;
      this.modalMessage = `Appointment was deleted.`;
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
        this.modalMessage = data.message || `Failed to delete appointment`;
        if (response.ok) {
          this.appointments = this.appointments.filter(appointment => appointment.id !== itemId);
        }
        this.showModal = true;
      } catch (error) {
        this.modalType = 'error';
        this.modalMessage = `An error occurred: ${error.message}`;
        this.showModal = true;
      }
    },
    handleUpdate(data) {
      this.$router.push(`/update/${this.typeOfData}/${data.itemId}`);
    },
    handleYesNoModalClose() {
      this.showYesNoModal = false;
      this.itemToDelete = null;
    },
  }
};
</script>


<style scoped>
.containerOfAll {
  width: 100%;
  height: 80%;
  margin-top: 5vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.calendar {
  width: 60vw;
  max-width: 60vw;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 10px;
}

button {
  height: fit-content;
  background-color: #c73659;
  padding: 10px;
  padding-top: 5px;
  padding-bottom: 5px;
  color: white;
}

.currentMonth {
  font-size: 3em;
}

.days {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
}

.day {
  width: 14.28%;
  height: 13vh;
  border: 1px solid #ddd;
  box-sizing: border-box;
  padding: 10px;
}

.today {
  display: flex;
  align-items: center;
}

.today-icon {
  width: 30px;
  height: 30px;
  margin-left: 5px;
}

.appointment {
  background-color: #f0f0f0;
  margin-top: 5px;
  padding: 2px 5px;
  border-radius: 3px;
  color: #c73659;
  padding: 10px;
  cursor:pointer;
}
</style>
