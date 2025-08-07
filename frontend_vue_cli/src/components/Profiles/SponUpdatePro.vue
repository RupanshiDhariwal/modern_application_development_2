<template>
    <div class="update-profile-page">
      <h1>Update Profile</h1>
      <form @submit.prevent="updateProfile">
        <div class="form-group">
          <label for="companyName">Company Name:</label>
          <input v-model="user.company_name" type="text" id="companyName" />
        </div>
        <div class="form-group">
          <label for="industry">Industry:</label>
          <input v-model="user.industry" type="text" id="industry" />
        </div>
        <div class="form-group">
          <label for="budget">Budget:</label>
          <input v-model="user.budget" type="number" id="budget"  />
        </div>
        <div class="form-group">
          <label for="individualName">Individual Name:</label>
          <input v-model="user.individual_name" type="text" id="individualName"  />
        </div>
        <button type="submit" class="submit-button">Update Profile</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: "SponUpdatePro",
    data() {
      return {
        user: {
          company_name: '',
          industry: '',
          budget: '',
          individual_name: ''
        },
        loading: true // Add a loading state
      };
    },
    mounted() {
      this.fetchUserData();
    },
    methods: {
      async fetchUserData() {
        const userId = localStorage.getItem('userId');
        const authToken = localStorage.getItem('authToken'); // Retrieve token from localStorage
  
        if (!userId || !authToken) {
          console.error('No userId or authToken found in localStorage');
          return;
        }
  
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/sponsor/profile/${userId}`, {
            headers: {
              'Authorization': `${authToken}` // Add Authorization header
            }
          });
          if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
          }
          const data = await response.json();
          this.user = data.data;
          this.loading = false; // Set loading to false once data is fetched
        } catch (error) {
          console.error('Failed to fetch user data:', error);
        }
      },
      async updateProfile() {
        const userId = localStorage.getItem('userId');
        const authToken = localStorage.getItem('authToken'); // Retrieve token from localStorage
  
        if (!userId || !authToken) {
          console.error('No userId or authToken found in localStorage');
          return;
        }
  
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/sponsor/profile/${userId}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `${authToken}` // Add Authorization header
            },
            body: JSON.stringify(this.user)
          });
          if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
          }
          alert('Profile updated successfully');
        } catch (error) {
          console.error('Failed to update user data:', error);
        }
      }
    }
  }
  </script>
  
  <style>
  .update-profile-page {
    padding: 20px;
    background-color: #f9f9f9;
  }
  
  .update-profile-page h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    font-weight: bold;
  }
  
  .form-group input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .submit-button {
    padding: 10px 20px;
    font-size: 16px;
    color: white;
    background-color: #007bff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .submit-button:hover {
    background-color: #0056b3;
  }
  </style>
  