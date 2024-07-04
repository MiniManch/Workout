<template>
  <div class="showSideBar" @mouseover="showTheSideBar">
    <img src="/icons/menu-50.png" alt="">
  </div>
  <div class="sidebar" :class="{ 'visible': showSideBar }" v-if="coach.id">
    <div class="close" @click="hideTheSideBar">X</div>
    <div class="buttons">
      <button class="btn" @click="fetchData('client')">
        <img src="/icons/team-50.png" alt="">
        <p>Your Clients</p>
      </button>
      <button class="btn" @click="fetchData('session')">
        <img src="/icons/schedule-60.png" alt="">
        <p>Your Sessions</p>
      </button>
      <button class="btn" @click="goTo('create_client')">
          <img src="/icons/trainee-50.png" alt="">
          <p>Add new client!</p>
      </button>
      <button class="btn" @click="goTo('create_session')">
          <img src="/icons/workout-50.png" alt="">
          <p>Create Session!</p>
      </button>
    </div>
  </div>

  <PopUpModal v-if="showModal" :type="modalType" :message="modalMessage" @close="handleModalClose" />
  <YesOrNoModal v-if="showYesNoModal" @close="handleYesNoModalClose" @yes="performAction" />
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
</template>

<script>
import PopUpModal from '@/components/General/PopUpModal.vue';
import YesOrNoModal from '@/components/General/YesOrNoModal.vue';
import PaginatedTableModal from '@/components/General/PaginatedTableModal.vue';

export default {
  components: {
    PopUpModal,
    YesOrNoModal,
    PaginatedTableModal,
  },
  data() {
    const coach = JSON.parse(localStorage.getItem('coach')) || {};
    return {
      coach,
      showSideBar: false,
      tableData: [],
      typeOfData: null,
      showModal: false,
      showYesNoModal: false,
      modalMessage: '',
      modalType: '',
      showTable: false,
      tableTitle: '',
      itemToDelete: null,
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
          headers: { 'Content-Type': 'application/json' },
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
            'CoachID': this.coach.id,
          },
          body: JSON.stringify({ value: fieldValue }),
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
          headers: { 'Content-Type': 'application/json' },
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
    goTo(link){
      this.$router.push(link);
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
    },
    showTheSideBar() {
      this.showSideBar = true;
    },
    hideTheSideBar() {
      this.showSideBar = false;
    },
  }
};
</script>

<style scoped>
* {
  user-select: none;
}
.showSideBar {
  position: fixed;
  top: 20vh;
  left: 1vw;
  z-index:1;
}
.sidebar {
  position: fixed;
  left: -220px;
  top: 0;
  height: 100vh;
  width: 200px;
  background-color: black;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 15px;
  z-index: 10;
  transition: left 0.3s ease;
}

.sidebar.visible {
  left: 0;
}
.close {
  font-size: 20px;
  cursor: pointer;
  position: absolute;
  top: 20px;
}
.buttons {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap:2vh;
  flex-grow: 1;
}

.sidebar .btn {
  background-color: rgba(130, 130, 130, 0.25);
  color: white;
  padding: 10px;
  text-align: left;
}
.sidebar .btn img {
  margin-right: 10px;
}
.sidebar .btn a {
  color: inherit;
  text-decoration: none;
}
</style>
