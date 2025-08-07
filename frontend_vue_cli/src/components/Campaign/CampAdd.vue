<template>
    <div>
      <form @submit.prevent="submitForm" class="form">
        <div class="form-group">
          <label for="name" class="form-label">Campaign Name:</label>
          <input type="text" id="name" v-model="form.name" class="form-control input-field" required>
        </div>
        <div class="form-group">
          <label for="description" class="form-label">Description:</label>
          <textarea id="description" v-model="form.description" class="form-control input-field" required></textarea>
        </div>
        <div class="form-group">
          <label for="start_date" class="form-label">Start Date (YYYY-MM-DD):</label>
          <input type="date" id="start_date" v-model="form.start_date" class="form-control input-field" required>
        </div>
        <div class="form-group">
          <label for="end_date" class="form-label">End Date (YYYY-MM-DD):</label>
          <input type="date" id="end_date" v-model="form.end_date" class="form-control input-field" required>
        </div>
        <div class="form-group">
          <label for="budget" class="form-label">Budget:</label>
          <input type="number" id="budget" v-model="form.budget" class="form-control input-field" required>
        </div>
        <div class="form-group">
          <label for="visibility" class="form-label">Visibility:</label>
          <select id="visibility" v-model="form.visibility" class="form-control input-field" required>
            <option value="public">Public</option>
            <option value="private">Private</option>
          </select>
        </div>
        <div class="form-group">
          <label for="goals" class="form-label">Goals:</label>
          <input type="text" id="goals" v-model="form.goals" class="form-control input-field" required>
        </div>
        <div class="form-group">
          <button type="submit" class="btn-submit">Create Campaign</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'CampAdd',
    data() {
      return {
        form: {
          name: '',
          description: '',
          start_date: '',
          end_date: '',
          budget: '',
          visibility: 'public',
          goals: ''
        },
        token: null
      }
    },
    created() {
      this.token = localStorage.getItem('authToken')
      if (!this.token) {
        this.$router.push('/login')
      }
    },
    methods: {
        submitForm() {
        axios.post('http://127.0.0.1:5000/api/campaign/', this.form, {
            headers: { Authorization: `${this.token}` } // Added Bearer prefix
        })
        .then(response => {
            console.log(response); // Log the response
            if (response.status === 201) {
            alert('Submitted successfully!');
            this.resetForm(); // Clear all fields
            this.$router.push('/campAdd'); // Redirect to a page where you show all campaigns or any other page
            }
        })
        .catch(error => {
            console.error('Error creating campaign:', error); // Log the error
            alert('Error occurred!');
        });
        
    },
      resetForm() {
        this.form = {
          name: '',
          description: '',
          start_date: '',
          end_date: '',
          budget: '',
          visibility: 'public',
          goals: ''
        };
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
  
  .input-field {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
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
  