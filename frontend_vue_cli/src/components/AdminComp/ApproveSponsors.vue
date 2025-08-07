<template>
    <div>
      <AdminHeader />
    
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Username</th>
            <th>Company Name</th>
            <th>Individual Name</th>
            <th>Industry</th>
            <th>Budget</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.username || 'N/A' }}</td>
            <td>{{ user.company_name || 'N/A' }}</td>
            <td>{{ user.individual_name || 'N/A' }}</td>
            <td>{{ user.industry || 'N/A' }}</td>
            <td>{{ user.budget !== null ? user.budget : 'N/A' }}</td>
            <td>
              <button
                class="approve-button"
                :class="{ disabled: user.active }"
                @click="activateUser(user.id)"
                :disabled="user.active"
              >
                Approve
              </button>
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
    name: 'ApproveSponsors',
    components: {
      AdminHeader
    },
    data() {
      return {
        users: [],
        token: null
      }
    },
    created() {
      this.token = localStorage.getItem('authToken');
      if (!this.token) {
        this.$router.push('/login');
      } else {
        this.getUsers();
      }
    },
    methods: {
      async getUsers() {
        console.log('Fetching deactivated users');
        try {
          const response = await axios.get('http://localhost:5000/api/deactiveted/sponsors', {
            headers: { Authorization: `${this.token}` }
          });
          console.log('API response:', response);
          if (response.status === 200) {
            this.users = response.data.data;
            console.log('Users data:', this.users);
          }
        } catch (error) {
          console.error('Error fetching users:', error);
        }
      },
      async activateUser(id) {
        try {
          const response = await axios.post(`http://localhost:5000/api/activate/${id}`, {}, {
            headers: { Authorization: `${this.token}` }
          });
          console.log('Activation response:', response);
          if (response.status === 200) {
            this.getUsers(); // Refresh user list after activation
          }
        } catch (error) {
          console.error('Error activating user:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
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
  
  /* Button Styles */
  .approve-button {
    color: white;
    background-color: #28a745;
    border: none;
    padding: 8px 16px;
    cursor: pointer;
  }
  
  .approve-button:hover {
    background-color: #218838;
  }
  
  .approve-button.disabled {
    background-color: grey;
    cursor: not-allowed;
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
  