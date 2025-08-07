<template>
    <div class="profile-page">
      <h1>{{ user.name }}'s Profile</h1>
      <p><strong>Name:</strong> {{ user.name }}</p>
      <p><strong>Category:</strong> {{ user.category }}</p>
      <p><strong>Niche:</strong> {{ user.niche }}</p>
      <p><strong>Reach:</strong> {{ user.reach }}</p>
      <button @click="editProfile" class="edit-button">Edit Profile</button>
    </div>
  </template>
  
  <script>
  export default {
    name: "InflueProfile",
    data() {
      return {
        user: {} // User data will be fetched from API
      };
    },
    mounted() {
      // Fetch user data on component mount
      this.fetchUserData();
    },
    methods: {
      async fetchUserData() {
        const userId = localStorage.getItem('userId'); // Get userId from localStorage
        if (!userId) {
          console.error('No userId found in localStorage');
          return;
        }
  
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/influencer/profile/${userId}`);
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          console.log('User data fetched:', data); // Debug: Check the fetched data
          this.user = data.data;
        } catch (error) {
          console.error('Failed to fetch user data:', error);
        }
      },
      editProfile() {
        // Redirect to edit profile page
        this.$router.push('/influeUpdateProfie');
      }
    }
  };
  </script>
  
  <style>
  .profile-page {
    padding: 20px;
    background-color: #f9f9f9;
  }
  
  .profile-page h1 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .profile-page p {
    font-size: 18px;
  }
  
  .edit-button {
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 16px;
    color: white;
    background-color: #007bff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .edit-button:hover {
    background-color: #0056b3;
  }
  </style>
  