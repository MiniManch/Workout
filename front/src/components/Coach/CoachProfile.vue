<template>
  <div class="containerOfAll">
    <div class="coachProfile">
      <h1>Your Profile!</h1>
      <form @submit.prevent="">
        <div v-for="field in fields" :key="field.id" class="inputDiv">
          <label :for="field.id">{{ field.label }}:</label>
          <input :type="field.type" :id="field.id" v-model="field.value" required>
          <AnimatedButton :buttonText="`Update ${ field.label }`" @clicked="updateField(field.id)"/>
        </div>
      </form>
    </div>
    <PopUpModal v-if="showModal" :type="modalType" :message="modalMessage" @close="handleModalClose" />
  </div>
</template>

<script>
import AnimatedButton from '@/components/General/buttons/AnimatedButton.vue';
import PopUpModal from '@/components/General/PopUpModal.vue';


export default {
  components:{
    AnimatedButton,
    PopUpModal,
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
      showModal: false,
      modalMessage: '',
      modalType: '',
    };
  },
  mounted() {
    if (!this.coach.id) {
      this.$router.push({ name: 'Login' });
    }
  },
  methods: {
    async updateField(field) {
      const fieldValue = this.fields.find(f => f.id === field).value;
      if (fieldValue === this.coach[field]) {
        console.log('heyo')
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
    handleModalClose() {
      this.showModal = false;
      this.modalMessage = '';
      this.modalType = '';
    },
  }
};
</script>

<style scoped>


.containerOfAll {
  width: 100%;
  height: 80%;
  padding-top:10vh;
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
  background-color: rgba(130, 130, 130, 0.25);
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
  margin-bottom:2vh;
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
