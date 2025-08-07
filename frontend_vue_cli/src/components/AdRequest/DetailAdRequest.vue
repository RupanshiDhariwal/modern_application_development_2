<template>
    <div class="ad-request-details">
      <h2>Ad Request Details (ID: {{ id }})</h2>
      
      <div class="button-group">
        <button @click="editAdRequest" class="btn-action">Edit</button>
        <button @click="deleteAdRequest" class="btn-action">Delete</button>
      </div>
  
      <div class="detail-group">
        <label class="detail-label">Campaign ID:</label>
        <p class="detail-value">{{ campaign_id }}</p>
      </div>
      <div class="detail-group">
        <label class="detail-label">Influencer ID:</label>
        <p class="detail-value">{{ influencer_id }}</p>
      </div>
      <div class="detail-group">
        <label class="detail-label">Messages:</label>
        <p class="detail-value">{{ messages }}</p>
      </div>
      <div class="detail-group">
        <label class="detail-label">Requirements:</label>
        <p class="detail-value">{{ requirements }}</p>
      </div>
      <div class="detail-group">
        <label class="detail-label">Payment Amount:</label>
        <p class="detail-value">{{ payment_amount }}</p>
      </div>
      
      <p>{{ responseMessage }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Headers from '@/components/Headers/Headers.vue';
  
  export default {
    name: 'DetailAdRequest',
    components: {
      Headers
    },
    data() {
      return {
        campaign_id: null,
        influencer_id: null,
        messages: null,
        requirements: null,
        payment_amount: null,
        responseMessage: null,
        token: null,
        id: null
      };
    },
    created() {
      this.token = localStorage.getItem('authToken');
      this.id = this.$route.params.adRequestId;
      if (!this.token) {
        this.$router.push('/login');
      }
      this.getAdRequestDetails();
    },
    methods: {
      getAdRequestDetails() {
        axios
          .get(`http://localhost:5000/api/adrequest/${this.id}`, {
            headers: { Authorization: `${this.token}` }
          })
          .then(response => {
            if (response.status === 200) {
              const data = response.data.data;
              this.campaign_id = data.campaign_id;
              this.influencer_id = data.influencer_id;
              this.messages = data.messages;
              this.requirements = data.requirements;
              this.payment_amount = data.payment_amount;
            }
          })
          .catch(error => {
            console.log("Error fetching ad request details", error);
          });
      },
      editAdRequest() {
        this.$router.push(`/editRequest/${this.id}`);
      },
      deleteAdRequest() {
        axios
          .delete(`http://localhost:5000/api/adrequest/${this.id}`, {
            headers: { Authorization: `${this.token}` }
          })
          .then(response => {
            if (response.status === 201) {
              this.responseMessage = "Ad request deleted successfully!";
              alert('Ad request deleted successfully!')
              this.$router.push('/dashboard');
            }
          })
          .catch(error => {
            console.log("Error deleting ad request", error);
            this.responseMessage = "Failed to delete ad request.";
          });
      }
    }
  };
  </script>
  
  <style>
  .ad-request-details {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 50px auto;
    max-width: 60%;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .detail-group {
    margin-bottom: 15px;
    width: 100%;
  }
  
  .detail-label {
    font-weight: bold;
  }
  
  .detail-value {
    margin-left: 10px;
    padding: 8px;
    background-color: #f9f9f9;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .button-group {
    margin-top: 20px;
    display: flex;
    gap: 10px;
  }
  
  .btn-action {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-action:hover {
    background-color: #45a049;
  }
  </style>
  