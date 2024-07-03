<template>
  <div class="containerOfAll">
    <div class="coachProfile">
      <h1>Your Profile!</h1>
      <form @submit.prevent="">
        <div v-for="field in fields" :key="field.id" class="inputDiv">
          <label :for="field.id">{{ field.label }}:</label>
          <input :type="field.type" :id="field.id" v-model="field.value" required>
          <button class="btn" @click="updateField(field.id)">Update {{ field.label }}</button>
        </div>
      </form>
    </div>

    <div class="actions">
      <button class="btn" @click="fetchData('client')"><img src="/icons/team-50.png" alt="">Your Clients</button>
      <button class="btn" @click="fetchData('session')"><img src="/icons/schedule-60.png" alt=""> Your Sessions</button>
      <button class="btn"><a href="/create_client"><img src="/icons/trainee-50.png" alt=""> Add new client!</a></button>
      <button class="btn"><a href="/create_session"><img src="/icons/workout-50.png" alt="">  Create Session! </a></button>
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
      :type="typeOfData"
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
    const coach = JSON.parse(localStorage.getItem('coach')) || {};
    return {
      coach,
      fields: [
        { id: 'name', label: 'Name', type: 'text', value: coach.name || '' },
        { id: 'email', label: 'Email', type: 'email', value: coach.email || '' },
        { id: 'phone', label: 'Phone Number', type: 'tel', value: coach.phone || '' },
      ],
      tableData: [],
      typeOfData: null,
      showModal: false,
      showYesNoModal: false,
      modalMessage: '',
      modalType: '',
      showTable: false,
      tableTitle: '',
      itemToDelete: null
    };
  },
  mounted() {
    if (!this.coach.id) {
      this.$router.push({ name: 'Login' });
    }
  },
  methods: {
    async fetchData(type) {
      try {
        const response = await fetch(`/api/${type}/get_coach_${type}_data/${this.coach.id}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) throw new Error(`Failed to fetch ${type}s`);

        const data = await response.json();
        this.tableData = type === 'client' ? data.clients : data.sessions;
        this.typeOfData = type;
        this.tableTitle = `Your ${type[0].toUpperCase() + type.slice(1)}s`;
        this.showTable = true;
      } catch (error) {
        this.modalType = 'error';
        this.modalMessage = `Error fetching ${type}s: ${error.message}`;
        this.showModal = true;
      }
    },
    async updateField(field) {
      const fieldValue = this.fields.find(f => f.id === field).value;

      if (fieldValue === this.coach[field]) {
        this.modalType = 'error';
        this.modalMessage = `No change in ${field}. Update not performed.`;
        this.showModal = true;
        return;
      }

      try {
        const response = await fetch(`/api/coach/update/${field}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'CoachID': this.coach.id
          },
          body: JSON.stringify({ value: fieldValue })
        });

        const data = await response.json();
        this.modalType = response.ok ? 'success' : 'error';
        this.modalMessage = data.message || 'An error occurred';
        if (response.ok) {
          this.coach[field] = fieldValue;
          localStorage.setItem('coach', JSON.stringify(this.coach));
        }
        this.showModal = true;
      } catch (error) {
        this.modalType = 'error';
        this.modalMessage = `An error occurred: ${error.message}`;
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
      this.modalMessage = `${this.typeOfData[0].toUpperCase() + this.typeOfData.slice(1)} was deleted.`;
      this.modalType = 'success';
      this.showModal = true;
    },
    async deleteItem({ itemId }) {
      try {
        const response = await fetch(`/api/${this.typeOfData}/delete/${this.coach.id}/${itemId}`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        this.modalType = response.ok ? 'success' : 'error';
        this.modalMessage = data.message || `Failed to delete ${this.typeOfData}`;
        if (response.ok) {
          this.tableData = this.tableData.filter(item => item.id !== itemId);
          this.fetchData(this.typeOfData); // Re-fetch data after successful deletion
        }
        this.showModal = true;
      } catch (error) {
        this.modalType = 'error';
        this.modalMessage = `An error occurred: ${error.message}`;
        this.showModal = true;
      }
    },
    handleYesNoModalClose() {
      this.showYesNoModal = false;
      this.itemToDelete = null;
    },
    handleModalClose() {
      this.showModal = false;
      this.modalMessage = '';
      this.modalType = '';
    },
    closeTable() {
      this.showTable = false;
      this.tableData = [];
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

button > img{
  margin-right:1vw;
}
button > a > img{
  margin-right:1vw;
}
</style>
