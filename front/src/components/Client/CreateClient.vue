<template>
    <div class="containerOfAll">
        <h1>Add New Client</h1>
        <div class="addClientForm">
            <form @submit.prevent="addClient">
                <div class="inputDiv">
                <label for="clientName">Name:</label>
                <input type="text" id="clientName" v-model="newClient.name" required>
                </div>
                <div class="inputDiv">
                <label for="clientEmail">Email:</label>
                <input type="email" id="clientEmail" v-model="newClient.email" required>
                </div>
                <div class="inputDiv">
                <label for="clientPhone">Phone Number:</label>
                <input type="tel" id="clientPhone" v-model="newClient.phone" required>
                </div>
                <button class="btn" type="submit">Add Client</button>
            </form>
        </div>
      <PopUpModal v-if="showModal" :type="modalType" :message="modalMessage" @close="handleModalClose"/>
    </div>
</template>
  
  <script>
  import PopUpModal from '../General/PopUpModal.vue';
  export default {
    components:{
        PopUpModal
    },
    data() {
      return {
        newClient: {
          name: '',
          email: '',
          phone: ''
        },
        message: '',
        modalType: '',
        showModal:false,
        coach:JSON.parse(localStorage.getItem('coach')),
      };
    },
    methods: {
      async addClient() {
        try {
          const response = await fetch(`/api/client/add/${this.coach.id}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.newClient)
          });
  
          const data = await response.json();
          if (response.ok) {
            this.message = data.message;
            this.modalType = 'success';
            this.showModal = true;
            // Optionally reset the form fields after successful submission
            this.newClient.name = '';
            this.newClient.email = '';
            this.newClient.phone = '';
          } else {
            this.message = data.message || 'Failed to add client';
            this.messageClass = 'error';
          }
        } catch (error) {
          this.message = 'An error occurred: ' + error.message;
          this.modalType = 'error';
          this.showModal = true;

        }
      },
      handleModalClose() {
        this.showModal = false;
      }
    }
  };
  </script>
  
  <style scoped>
  .containerOfAll{
    width: 100%;

    display:flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  h1{
    margin-top: 3vh;
  }
  
  .addClientForm {
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
  
  input {
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
  form{
    display: flex;
    flex-direction: column;

    align-items: center;
    justify-content: center;
  }
  </style>
  