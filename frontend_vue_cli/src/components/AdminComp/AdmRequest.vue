<template>
    <div>
      <AdminHeader />
  
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Campaign ID</th>
            <th>Influencer ID</th>
            <th>Messages</th>
            <th>Requirements</th>
            <th>Payment Amount</th>
            <th>Status</th>
            <th>Created By</th>
            <th>Updated By</th>
            <th>Created At</th>
            <th>Updated At</th>
            <th>Campaign</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in adRequests" :key="row.id">
            <td>{{ row.id }}</td>
            <td>{{ row.campaign_id }}</td>
            <td>{{ row.influencer_id }}</td>
            <td>{{ row.messages }}</td>
            <td>{{ row.requirements }}</td>
            <td>{{ row.payment_amount }}</td>
            <td>{{ row.status }}</td>
            <td>{{ row.created_by }}</td>
            <td>{{ row.updated_by }}</td>
            <td>{{ row.created_at }}</td>
            <td>{{ row.update_at }}</td>
            <td>{{ row.campaign }}</td>
            <td>
              <a
                class="nav-link delete"
                :class="{ disabled: row.status === 'deleted' }"
                @click="deleteAdRequest(row.id)"
                :disabled="row.status === 'deleted'"
              >
                delete
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import AdminHeader from '../Headers/AdminHeader.vue';
  
  export default {
    name: 'AdmRequest',
    components: {
      AdminHeader
    },
    data() {
      return {
        adRequests: [],
        token: null
      }
    },
    created() {
      this.token = localStorage.getItem('authToken');
      if (!this.token) {
        this.$router.push('/login');
      } else {
        this.getAdRequests();
      }
    },
    methods: {
      async getAdRequests() {
        console.log('Fetching ad requests');
        try {
          const response = await axios.get('http://localhost:5000/api/adrequest/all', {
            headers: { Authorization: `${this.token}` }
          });
          console.log('API response:', response);
          if (response.status === 200) {
            this.adRequests = response.data.data;
            console.log('Ad Requests data:', this.adRequests);
          }
        } catch (error) {
          console.error('Error fetching ad requests:', error);
        }
      },
      async deleteAdRequest(id) {
        axios
          .delete(`http://localhost:5000/api/adrequest/${id}`, {
            headers: { Authorization: `${this.token}` }
          })
          .then(response => {
            console.log('response block', response);
            if (response.status == 201) {
              this.getAdRequests();
            }
          })
          .catch(error => {
            console.log('error block', error);
          });
      }
    }
  };
  </script>
  
  <style scoped>
.heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 50px;
}

h1, h2 {
  text-align: center;
}

.linkBox {
  display: flex;
  width: 150px;
  justify-content: space-between;
}

.linkBox a.active-link {
  color: red;
}

.nav-link {
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
  cursor: pointer;
}

.nav-link:hover {
  color: #0056b3;
  text-decoration: underline;
}

.delete {
  color: #c60000;
}

.disabled {
  color: grey;
  cursor: not-allowed;
  pointer-events: none;
}

/* Table Styles */
.table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

.table th, .table td {
  padding: 12px;
  text-align: left;
  border: 1px solid #ddd;
}

.table th {
  background-color: #f4f4f4;
}

/* Responsive Styles */
@media (max-width: 768px) {
  .table, .table thead, .table tbody, .table th, .table td, .table tr {
    display: block;
  }
  
  .table th {
    display: none;
  }
  
  .table tr {
    margin-bottom: 15px;
    border-bottom: 1px solid #ddd;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  
  .table td {
    display: flex;
    justify-content: space-between;
    position: relative;
    padding-left: 50%;
    text-align: right;
  }
  
  .table td::before {
    content: attr(data-label);
    position: absolute;
    left: 0;
    width: 50%;
    padding-left: 10px;
    font-weight: bold;
    text-align: left;
  }
}
</style>

  