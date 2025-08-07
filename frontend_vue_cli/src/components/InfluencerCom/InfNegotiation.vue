<template>
    <div class="container">
      <InfluencerHeader />
      <h1>Negotiations</h1>
      <div class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th>Ad Request ID</th>
              <th>Negotiation ID</th>
              <th>Message</th>
              <th>Payment Amount</th>
              <th>Influencer Negotiation Payment Amount</th>
              <th>Sponsor Negotiation Payment Amount</th>
              <th>Influencer Negotiation Status</th>
              <th>Sponsor Negotiation Status</th>
              <th>Negotiator Role</th>
              <th>Created At</th>
              <th>Updated At</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="negotiation in negotiations" :key="negotiation.id">
              <td>{{ negotiation.ad_request_id }}</td>
              <td>{{ negotiation.id }}</td>
              <td>{{ negotiation.message }}</td>
              <td>{{ negotiation.payment_amount }}</td>
              <td>{{ negotiation.influencer_negotiation_payment_amt }}</td>
              <td>{{ negotiation.sponsor_negotiation_payment_amt }}</td>
              <td>{{ negotiation.influencer_negotiation_status }}</td>
              <td>{{ negotiation.sponsor_negotiation_status }}</td>
              <td>{{ negotiation.negotiator_role }}</td>
              <td>{{ negotiation.created_at }}</td>
              <td>{{ negotiation.updated_at }}</td>
              <td>
                <button 
                  :disabled="!negotiation.should_nego_status_change_influencer"
                  @click="acceptNegotiation(negotiation.id)">Accept</button>
                <button 
                  :disabled="!negotiation.should_nego_status_change_influencer"
                  @click="rejectNegotiation(negotiation.id)">Reject</button>
                <button 
                  :disabled="!negotiation.should_nego_status_change_influencer"
                  @click="editNegotiation(negotiation.id)">Edit</button>
                  <router-link :to="{name: 'infDetailAdReq', params: {adRequestId: negotiation.ad_request_id}}"  class="nav-link " >View Reuest</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import InfluencerHeader from '../Headers/InfluencerHeader.vue';
  
  export default {
    name: 'InfNegotiation',
    components: {
      InfluencerHeader
    },
    data() {
      return {
        negotiations: []
      };
    },
    created() {
      this.checkLoginStatus();
    },
    methods: {
      async checkLoginStatus() {
        const token = localStorage.getItem('authToken');
        if (!token) {
          this.$router.push('/login');
        } else {
          this.fetchNegotiations();
        }
      },
      async fetchNegotiations() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/api/adrequest/get/user/negotiation', {
            headers: { Authorization: `${localStorage.getItem('authToken')}` }
          });
          if (response.status === 200) {
            // Flatten the negotiations array
            this.negotiations = response.data.flatMap(request => request.negotiations);
          }
        } catch (error) {
          console.error("Error fetching negotiations:", error);
        }
      },
      async acceptNegotiation(negotiationId) {
        try {
          const response = await axios.put(`http://127.0.0.1:5000/api/negotiation/accept/${negotiationId}`, {}, {
            headers: { Authorization: `${localStorage.getItem('authToken')}` }
          });
          if (response.status === 200) {
            alert('Negotiation accepted successfully!');
            this.fetchNegotiations(); // Refresh the list of negotiations
          }
        } catch (error) {
          alert('Error accepting negotiation: ' + error.message);
        }
      },
      async rejectNegotiation(negotiationId) {
        try {
          const response = await axios.put(`http://127.0.0.1:5000/api/negotiation/reject/${negotiationId}`, {}, {
            headers: { Authorization: `${localStorage.getItem('authToken')}` }
          });
          if (response.status === 200) {
            alert('Negotiation rejected successfully!');
            this.fetchNegotiations(); // Refresh the list of negotiations
          }
        } catch (error) {
          alert('Error rejecting negotiation: ' + error.message);
        }
      },
      async editNegotiation(negotiationId) {
        // Implement edit negotiation logic here
        console.log('Edit negotiation for:', negotiationId);
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    padding: 20px;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .table-responsive {
    overflow-x: auto;
  }
  
  .table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .table th, .table td {
    border: 1px solid #ddd;
    padding: 8px;
  }
  
  .table th {
    background-color: #f2f2f2;
    text-align: left;
  }
  
  .table tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  
  button {
    margin-right: 5px;
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
  
  @media (max-width: 768px) {
    .table th, .table td {
      padding: 12px;
      font-size: 12px;
    }
  
    .nav-link {
      font-size: 12px;
    }
  }
  </style>
  