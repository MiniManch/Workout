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
    </div>

    <div class="actions">
      <button class="btn" @click="fetchClients">Your Clients</button>
      <button class="btn" @click="fetchSessions">Your Sessions</button>
      <button class="btn"><a href="/create_client">Add new client!</a></button>
      <button class="btn"><a href="/create_session">Create Session!</a></button>
    </div>

    <!-- Pop-up modal for general messages -->
    <PopUpModal v-if="showModal" :type="modalType" :message="modalMessage" @close="handleModalClose" />
    <YesOrNoModal v-if="showYesNoModal" @close="handleYesNoModalClose" @yes="performAction" />

    <!-- Paginated table modal for clients or sessions -->
    <PaginatedTableModal
      v-if="showTable"
      :show="showTable"
      :data="tableData"
      :itemsPerPage="5"
      :title="tableTitle"
      @close="closeTable"
      @delete-item="confirmAction"       
      @update-item="handleUpdate"
    />
  </div>
</template>

<script>
import PopUpModal from '@/components/General/PopUpModal.vue';
import YesOrNoModal from '@/components/General/YesOrNoModal.vue';
import PaginatedTableModal from '@/components/General/PaginatedTableModal.vue';

export default {
  components: {
    PopUpModal,
    PaginatedTableModal,
    YesOrNoModal
  },
  data() {
    return {
      coach: JSON.parse(localStorage.getItem('coach')),
      name: null,
      email: null,
      phone: null,
      tableData: [],
      typeOfData: null,
      message: '',
      messageClass: '',
      showModal: false,
      showYesNoModal: false,
      modalTitle: '',
      modalMessage: '',
      modalType: '',
      showTable: false,
      tableTitle: '',
      itemToDelete: null
    };
  },
  mounted() {
    if (!this.coach) {
      this.$router.push({ name: 'Login' });
    } else {
      this.name = this.coach.name;
      this.email = this.coach.email;
      this.phone = this.coach.phone;
    }
  },
  methods: {
    async fetchClients() {
      try {
        const response = await fetch(`/api/client/${this.coach.id}/clients`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
          const data = await response.json();
          this.tableData = data.clients;
          this.typeOfData = 'client';
          this.tableTitle = 'Your Clients';
          this.showTable = true;
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
    async fetchSessions() {
      try {
        const response = await fetch(`/api/session/get_coach_sessions/${this.coach.id}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
          const data = await response.json();
          this.tableData = data.sessions;
          this.typeOfData = 'session';
          this.tableTitle = 'Your Sessions';
          this.showTable = true;
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
    async updateField(field) {
      const newValue = this[field];
      const currentValue = this.coach[field];

      if (newValue === currentValue) {
        this.modalType = 'error';
        this.modalMessage = `You didn't change anything for ${field}. No update performed.`;
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
          this.modalType = 'success';
          this.modalMessage = data.message;
          this.coach[field] = newValue;
          localStorage.setItem('coach', JSON.stringify(this.coach));
          this.showModal = true;
        } else {
          this.modalType = 'error';
          this.modalMessage = data.message || 'An error occurred';
          this.showModal = true;
        }
      } catch (error) {
        this.modalType = 'error';
        this.modalMessage = 'An error occurred: ' + error.message;
        this.showModal = true;
      }
    },
    confirmAction({ itemId }) {
      this.itemToDelete = itemId;
      this.showYesNoModal = true;
    },
    async performAction() {
      await this.deleteItem({ itemId: this.itemToDelete });
      this.showYesNoModal = false;
      this.itemToDelete = null;
      this.modalMessage = `${this.typeOfData[0].toUpperCase() + this.typeOfData[1]} was deleted.`
      this.modalType = 'success';
      this.showModal = true;
    },
    async deleteItem({ itemId}) {
      try {
        const response = await fetch(`/api/${this.typeOfData}/delete/${this.coach.id}/${itemId}`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        if (response.ok) {
          this.modalMessage = data.message;
          this.modalType = 'success';
          this.showModal = true;
          this.tableData = this.tableData.filter(item => item.id !== itemId);
        } else {
          this.modalMessage = data.message || `Failed to delete ${this.typeOfData}`;
          this.modalType = 'error';
          this.showModal = true;
        }
      } catch (error) {
        this.modalMessage = 'An error occurred: ' + error.message;
        this.modalType = 'error';
        this.showModal = true;
      }
    },
    handleYesNoModalClose() {
      this.showYesNoModal = false;
      this.itemToDelete = null;
    },
    handleModalClose() {
      this.modalMessage = '';
      this.modalType = '';
      this.showModal = false;
    },
    closeTable() {
      this.showTable = false;
      this.tableData = null;
      this.typeOfData = null;
      this.tableTitle = '';
    },
    handleUpdate(data) {
      this.$router.push(`/update/${this.typeOfData}/${data.itemId}`);
    }
  }
};
</script>
  
<style scoped>
.containerOfAll {
  width: 100%;
  height: 80%;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 5vw;
}

.coachProfile {
  margin-top: 3vh;
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

table {
  margin-top: 3vh;
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

.actions {
  margin-top: 3vh;
  display: flex;
  flex-direction: column;
  gap: 2vh;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  background-color: #A91D3A;
  color: white;
}

button:hover {
  background-color: white;
  color: #A91D3A;
}
</style>