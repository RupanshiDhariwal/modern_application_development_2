<template>
    <div>
      <AdminHeader />
    
      <!-- Display total influencers and sponsors -->
      <div class="summary">
        <p>Total Influencers: {{ totalInfluencers }}</p>
        <p>Total Sponsors: {{ totalSponsors }}</p>
      </div>
    
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
                class="deactivate-button"
                :class="{ disabled: !user.active }"
                @click="deactivateUser(user.id)"
                :disabled="!user.active"
              >
                Deactivate
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
    name: 'AdmUsers',
    components: {
      AdminHeader
    },
    data() {
      return {
        users: [],
        token: null,
        totalInfluencers: 0,
        totalSponsors: 0
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
        console.log('Fetching users');
        try {
          const response = await axios.get('http://localhost:5000/api/user/all', {
            headers: { Authorization: `${this.token}` }
          });
          console.log('API response:', response);
          if (response.status === 200) {
            this.users = response.data.data;
            this.totalInfluencers = response.data.total_influencers;
            this.totalSponsors = response.data.total_sponsors;
            console.log('Users data:', this.users);
          }
        } catch (error) {
          console.error('Error fetching users:', error);
        }
      },
      async deactivateUser(id) {
        try {
          const response = await axios.post(`http://localhost:5000/api/deactiveUser/${id}`, {}, {
            headers: { Authorization: `${this.token}` }
          });
          console.log('Deactivation response:', response);
          if (response.status === 200) {
            this.getUsers(); // Refresh user list after deactivation
          }
        } catch (error) {
          console.error('Error deactivating user:', error);
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
  .deactivate-button {
    color: white;
    background-color: #dc3545;
    border: none;
    padding: 8px 16px;
    cursor: pointer;
  }
  
  .deactivate-button:hover {
    background-color: #c82333;
  }
  
  .deactivate-button.disabled {
    background-color: grey;
    cursor: not-allowed;
  }
  
  /* Summary Styles */
  .summary {
    margin: 20px 0;
  }
  
  .summary p {
    font-weight: bold;
    margin: 5px 0;
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
  