<template>
    <div>
      <h1>Initiate New Negotiation</h1>
      <form @submit.prevent="submitForm" method="POST" class="form">
        <div class="form-group">
          <label for="amount" class="form-label">New Payment Amount:</label>
          <input v-model="form.amount" type="number" id="amount" name="amount" class="form-control input-field" required>
        </div>
        <div class="form-group">
          <label for="message" class="form-label">Message:</label>
          <textarea v-model="form.message" id="message" name="message" class="form-control textarea-field"></textarea>
        </div>
        <div class="form-group">
          <button type="submit" class="btn-submit">Initiate Negotiation</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'InfAddNegotiation',
    data() {
      return {
        form: {
          amount: '',
          message: ''
        },
        token: null
      };
    },
    created() {
      this.token = localStorage.getItem('authToken');
      if (!this.token) {
        this.$router.push('/login');
      }
    },
    methods: {
      submitForm() {
        const id = this.$route.params.adRequestId; // Get the id from the route params
        axios.post(`http://127.0.0.1:5000/api/adrequest/add/negotiation/${id}`, this.form,
        { headers: { Authorization: `${this.token}` } })
        .then(response => {
          if (response.status === 200) {
            alert('Negotiation initiated successfully!');
            this.resetForm();
            this.$router.push('/influAdrequest'); 
          }
        })
        .catch(error => {
          alert('Error occurred while initiating negotiation.');
          console.error('Error initiating negotiation:', error);
        });
      },
      resetForm() {
        this.form = {
          amount: '',
          message: ''
        };
      }
    }
  };
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
  