<template>
    <div>
      <h2>Edit Ad Request with ID: {{ id }}</h2>
      <form @submit.prevent="updateAdRequest" class="form">
        <div class="form-group">
          <label for="campaign_id" class="form-label">Campaign ID:</label>
          <input type="text" id="campaign_id" v-model="form.campaign_id" class="form-control input-field" required>
        </div>
        <div class="form-group">
          <label for="influencer_id" class="form-label">Influencer ID:</label>
          <input type="text" id="influencer_id" v-model="form.influencer_id" class="form-control input-field" >
        </div>
        <div class="form-group">
          <label for="messages" class="form-label">Messages:</label>
          <textarea id="messages" v-model="form.messages" class="form-control textarea-field" required></textarea>
        </div>
        <div class="form-group">
          <label for="requirements" class="form-label">Requirements:</label>
          <textarea id="requirements" v-model="form.requirements" class="form-control textarea-field" required></textarea>
        </div>
        <div class="form-group">
          <label for="payment_amount" class="form-label">Payment Amount:</label>
          <input type="number" id="payment_amount" v-model="form.payment_amount" class="form-control input-field" required>
        </div>
        <div class="form-group">
          <button type="submit" class="btn-submit">Update Ad Request</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'EditAdRequest',
    data() {
      return {
        form: {
          campaign_id: '',
          influencer_id: '',
          messages: '',
          requirements: '',
          payment_amount: ''
        },
        token: null,
        id: null
      }
    },
    created() {
      this.token = localStorage.getItem('authToken');
      this.id = this.$route.params.adRequestId;
      if (!this.token) {
        this.$router.push('/login');
      } else {
        this.getAdRequestDetails();
      }
    },
    methods: {
      async getAdRequestDetails() {
        try {
          const response = await axios.get(`http://localhost:5000/api/adrequest/${this.id}`, 
          { headers: { Authorization: `${this.token}` } });
          if (response.status === 200) {
            const data = response.data.data;
            this.form = {
              campaign_id: data.campaign_id,
              influencer_id: data.influencer_id,
              messages: data.messages,
              requirements: data.requirements,
              payment_amount: data.payment_amount
            };
          }
        } catch (error) {
          console.error('Error fetching ad request details:', error);
        }
      },
      async updateAdRequest() {
        try {
          const response = await axios.put(`http://localhost:5000/api/adrequest/${this.id}`, this.form, 
          { headers: { Authorization: `${this.token}` } });
          if (response.status === 200) {
            alert("Ad request updated successfully!");
            this.$router.push(`/editRequest/${this.id}`);
          }
        } catch (error) {
          console.error('Error updating ad request:', error);
          alert("Failed to update ad request.");
        }
      }
    }
  }
  </script>
  
  <style>
  .form {
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
  
  .form-group {
    margin-bottom: 15px;
    width: 100%;
  }
  
  .form-label {
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .input-field, .textarea-field, .select-field {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .textarea-field {
    height: 100px;
  }
  
  .btn-submit {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-submit:hover {
    background-color: #45a049;
  }
  </style>
  