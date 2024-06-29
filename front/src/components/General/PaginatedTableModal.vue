<template>
  <div class="modal" v-if="show">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2>{{ title }}</h2>
      <table>
        <thead>
          <tr>
            <th v-for="header in headers" :key="header">{{ header }}</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in paginatedData" :key="item.id">
            <td v-for="(value, key) in item" :key="key">{{ value }}</td>
            <td>
              <button class="delete-btn btn" @click="deleteItem(item)">Delete</button>
              <button class="update-btn btn btn-warning" @click="updateItem(item)">Update</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="pagination">
        <button class="btn" @click="prevPage" :disabled="currentPage === 1">Previous</button>
        <button class="btn" v-for="page in totalPages" :key="page" @click="goToPage(page)" :class="{ active: currentPage === page }">{{ page }}</button>
        <button class="btn" @click="nextPage" :disabled="currentPage === totalPages">Next</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    show: {
      type: Boolean,
      default: false
    },
    data: {
      type: Array,
      required: true
    },
    itemsPerPage: {
      type: Number,
      default: 5
    },
    title: {
      type: String,
      default: 'Table'
    },
    type: {
      type: String,
    },
  },
  data() {
    return {
      currentPage: 1
    };
  },
  computed: {
    headers() {
      return this.data.length > 0 ? Object.keys(this.data[0]) : [];
    },
    totalPages() {
      return Math.ceil(this.data.length / this.itemsPerPage);
    },
    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.data.slice(start, end);
    }
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    goToPage(page) {
      this.currentPage = page;
    },
    deleteItem(item) {
      let itemId;

      if(!item.id && this.type === 'session'){
        itemId= item.SessionID;
      }
      else{
        itemId = item.id;
      }

      this.$emit('delete-item', { itemId });
    },
    updateItem(item) {
      let itemId;

      if(!item.id && this.type === 'session'){
        itemId= item.SessionID;
      }
      else{
        itemId = item.id;
      }

      this.$emit('update-item', { itemId });
    }
  }
};
</script>

<style scoped>
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  color: #A91D3A;
  z-index: 2;
}


.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 50%;
  max-height: 80%;
  overflow-y: auto;
}

.close {
  float: right;
  font-size: 2em;
  cursor: pointer;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th, td {
  padding: 8px 12px;
  border: 1px solid #A91D3A;
  text-align: center;
}

th{
  background-color: #A91D3A;
  color:white;
}

.pagination {
  margin-top: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

 button {
  margin: 0 5px;
  padding: 5px 10px;
  cursor: pointer;
  color: #A91D3A;
  border: 1px solid #A91D3A;
}

 button.active {
  font-weight: bold;
  text-decoration: underline;
}

.delete-btn {
  padding: 5px 10px;
  background-color: #A91D3A;
  color: white;
  border: none;
  cursor: pointer;
}

.update-btn {
  padding: 5px 10px;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
