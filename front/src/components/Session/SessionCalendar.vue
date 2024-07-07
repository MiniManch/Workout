<template>
  <div class="containerOfAll">
    <div class="calendar">
      <div class="header">
        <AnimatedButton
          @clicked="prevMonth"
          :style="{'margin-left':'0','margin-right':'0'}"
        >
          <img src="/icons/back-50.png" alt="Previous Month">
        </AnimatedButton>
        <span class="currentMonth">{{ currentMonthYear }}</span>
        <AnimatedButton
          @clicked="nextMonth"
          :style="{'margin-left':'0','margin-right':'0'}"
        >
          <img src="/icons/next-50.png" alt="Next Month">
        </AnimatedButton>
      </div>
      <div class="days">
        <div
          class="day"
          v-for="day in days"
          :key="day.date"
        >
          <div :class="{ today: isToday(day.date) }">
            <span class="date-and-icon">
              {{ day.date.getDate() }}
              <img v-if="isToday(day.date)" v-tooltip="'today'" src="/icons/today-50.png" alt="Today" class="today-icon">
            </span>
            <template v-if="isToday(day.date)">
              <GeneralButton
                @clicked="redirectToSessionPage(day.date)"
                buttonText="Add Session"
                class="center-button"
              />
            </template>
          </div>
          <template v-if="shouldDisplayAddSessionButton(day)">
            <GeneralButton
              v-if="day.date > currentDate"
              @clicked="redirectToSessionPage(day.date)"
              buttonText="Add Session"
              class="center-button"
            />
          </template>
          <template v-else-if="day.appointments.length > 0">
            <GeneralButton
              @clicked="openTable(day)"
              buttonText="View Appointments"
              class="center-button"
            />
          </template>
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
import AnimatedButton from "@/components/General/buttons/AnimatedButton.vue"; 
import GeneralButton from "@/components/General/buttons/GeneralButton.vue";

export default {
  components: {
    PopUpModal,
    PaginatedTableModal,
    YesOrNoModal,
    AnimatedButton,
    GeneralButton
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
      showYesNoModal: false,
      itemToDelete: null,
      typeOfData: '',
    };
  },
  computed: {
    currentMonthYear() {
      const options = {
        year: 'numeric',
        month: 'long'
      };
      return this.currentDate.toLocaleDateString('en-US', options);
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
        const response = await fetch(`/api/session/coach/${this.coach.id}`, {
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
    shouldDisplayAddSessionButton(day) {
      const today = new Date();
      return this.formatDate(day.date) > this.formatDate(today) && day.appointments.length === 0;
    },
    openTable(day) {
      this.tableData = day.appointments;
      this.tableTitle = `Appointments on ${day.date.toLocaleDateString('en-US')}`; // Set the locale to English (United States)
      this.typeOfData = 'session';
      this.showTable = true;
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
      await this.fetchAppointments(); // Refresh the appointments list
      this.refreshTableData();
      this.showYesNoModal = false;
      this.itemToDelete = null;
      this.modalMessage = `Appointment was deleted.`;
      this.modalType = 'success';
      this.showModal = true;
    },
    async deleteItem({ itemId }) {
      try {
        const response = await fetch(`/api/session/${itemId}/coach/${this.coach.id}`, {
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
    refreshTableData() {
      const selectedDay = this.tableTitle.split('Appointments on ')[1];
      const dayDate = new Date(selectedDay);
      this.tableData = this.getAppointmentsForDay(dayDate);
    },
    handleUpdate(data) {
      this.$router.push(`/update/${this.typeOfData}/${data.itemId}`);
    },
    handleYesNoModalClose() {
      this.showYesNoModal = false;
      this.itemToDelete = null;
    },
    redirectToSessionPage(date) {
      const formattedDate = this.formatDate(date); // Use a utility function to format the date as needed
      this.$router.push(`/create_session/${formattedDate}`);
    },
    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
  }
};
</script>

<style scoped>
*{
  user-select: none;
  font-family: "Jost";
}
.containerOfAll {
  width: 100%;
  height: 80%;
  padding-top: 10vh;
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
  flex-direction: column;
}

.date-and-icon {
  display: flex;
  align-items: center;
}

.today-icon {
  margin-left: 5px;
  width: 20px;
  height: 20px;
}

.center-button {
  margin-top: 5px;
  align-self: center;
  font-size: 0.9rem;
}

.appointment {
  background-color: rgba(130, 130, 130, 0.25);
  margin-top: 5px;
  padding: 2px 5px;
  border-radius: 3px;
  color: white;
  padding: 10px;
  cursor: pointer;
}
</style>
