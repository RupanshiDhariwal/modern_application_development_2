<template>
    <div class="update-profile-page">
      <h1>Update Profile</h1>
      <form @submit.prevent="updateProfile">
        <div class="form-group">
          <label for="name">Name:</label>
          <input v-model="user.name" type="text" id="name" required />
        </div>
        <div class="form-group">
          <label for="category">Category:</label>
          <input v-model="user.category" type="text" id="category" required />
        </div>
        <div class="form-group">
          <label for="niche">Niche:</label>
          <input v-model="user.niche" type="text" id="niche" required />
        </div>
        <div class="form-group">
          <label for="reach">Reach:</label>
          <input v-model="user.reach" type="text" id="reach" required />
        </div>
        <button type="submit" class="submit-button">Update Profile</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: "InflueUpdateProfile",
    data() {
      return {
        user: {
          name: '',
          category: '',
          niche: '',
          reach: ''
        },
        loading: true, // Add a loading state
      };
    },
    mounted() {
      this.fetchUserData();
    },
    methods: {
      async fetchUserData() {
        const userId = localStorage.getItem('userId');
        if (!userId) {
          console.error('No userId found in localStorage');
          return;
        }
  
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/influencer/profile/${userId}`);
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
        if (!userId) {
          console.error('No userId found in localStorage');
          return;
        }
  
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/influencer/profile/${userId}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
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
  };
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
  