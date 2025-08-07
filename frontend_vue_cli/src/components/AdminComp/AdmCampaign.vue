<template>
    <div>
      <AdminHeader />
  
      <!-- Display Campaign Summary -->
      <div class="summary">
        <h2>Campaign Summary</h2>
        <p>Total Active Campaigns: {{ statusCounts.active }}</p>
        <p>Total Deleted Campaigns: {{ statusCounts.deleted }}</p>
        <p>Total Inactive Campaigns: {{ statusCounts.inactive }}</p>
        <p>Total Public Campaigns: {{ visibilityCounts.public }}</p>
        <p>Total Private Campaigns: {{ visibilityCounts.private }}</p>
      </div>
  
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Budget</th>
            <th>Status</th>
            <th>Visibility</th>
            <th>Goals</th>
            <th>Total Ad Requests</th> <!-- Added Column -->
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in campaigns" :key="row.id">
            <td>{{ row.id }}</td>
            <td>{{ row.name }}</td>
            <td>{{ row.description }}</td>
            <td>{{ row.start_date }}</td>
            <td>{{ row.end_date }}</td>
            <td>{{ row.budget }}</td>
            <td>{{ row.status }}</td>
            <td>{{ row.visibility }}</td>
            <td>{{ row.goals }}</td>
            <td>{{ row.total_ad_requests || 0 }}</td> <!-- Display Total Ad Requests -->
            <td>
              <a
                class="nav-link delete"
                :class="{ disabled: row.status === 'deleted' }"
                @click="deleteCampaign(row.id)"
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
    name: 'AdmCampaign',
    components: {
      AdminHeader
    },
    data() {
      return {
        campaigns: [],
        statusCounts: {
          active: 0,
          deleted: 0,
          inactive: 0
        },
        visibilityCounts: {
          public: 0,
          private: 0
        },
        token: null
      }
    },
    created() {
      this.token = localStorage.getItem('authToken');
      if (!this.token) {
        this.$router.push('/login');
      } else {
        this.getCampaignfn();
      }
    },
    methods: {
      async getCampaignfn() {
        console.log('Fetching campaigns');
        try {
          const response = await axios.get('http://localhost:5000/api/campaign/all', {
            headers: { Authorization: `${this.token}` }
          });
          console.log('API response:', response);
          if (response.status === 200) {
            this.campaigns = response.data.data.map(campaign => ({
              ...campaign,
              total_ad_requests: campaign.ad_requests.length // Assuming `ad_requests` is an array
            }));
            this.statusCounts = response.data.status_counts;
            this.visibilityCounts = response.data.visibility_counts;
            console.log('Campaigns data:', this.campaigns);
          }
        } catch (error) {
          console.error('Error fetching campaigns:', error);
        }
      },
      async deleteCampaign(id) {
        axios
          .delete(`http://localhost:5000/api/campaign/${id}`, {
            headers: { Authorization: `${this.token}` }
          })
          .then(response => {
            console.log('response block', response);
            if (response.status === 201) {
              this.getCampaignfn();
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
  