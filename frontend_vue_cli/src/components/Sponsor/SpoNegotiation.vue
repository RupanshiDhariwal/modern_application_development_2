<template>
    <div class="container">
      <Headers />
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
                  :disabled="!negotiation.should_nego_status_change_sponsor"
                  @click="acceptNegotiation(negotiation.id)">Accept</button>
                <button 
                  :disabled="!negotiation.should_nego_status_change_sponsor"
                  @click="rejectNegotiation(negotiation.id)">Reject</button>
                <button 
                  :disabled="!negotiation.should_nego_status_change_sponsor"
                  @click="editNegotiation(negotiation.id)">Edit</button>
                <!-- <router-link 
                  :to="{ name: 'sponsorDetailAdReq', params: { adRequestId: negotiation.ad_request_id } }"
                  class="nav-link">View Request</router-link> -->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Headers from '../Headers/Headers.vue';
  
  export default {
    name: 'SpoNegotiation',
    components: {
        Headers
    },
    data() {
      return {
        negotiations: [],
        token: null
      };
    },
    created() {
    this.token = localStorage.getItem('authToken');
    if (!this.token) {
      this.$router.push('/login');
    } else {
      this.fetchNegotiations();
    }
  },
    methods: {
      async fetchNegotiations() {
        try {
          console.log('working')
          console.log(localStorage.getItem('userId'))
          const response = await axios.get(`http://127.0.0.1:5000/api/adrequest/get/sponsor/negotiation`, {
            headers: { Authorization: `${localStorage.getItem('authToken')}` }
          });
          if (response.status === 200) {
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
  /* Styles remain the same */
  </style>
  