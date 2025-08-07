<template>
    <div class="profile-page">
      <h1>{{ user.company_name }}'s Profile</h1>
      <p><strong>Company Name:</strong> {{ user.company_name }}</p>
      <p><strong>Individual Name:</strong> {{ user.individual_name }}</p>
      <p><strong>Industry:</strong> {{ user.industry }}</p>
      <p><strong>Budget:</strong> {{ user.budget }}</p>
      <button @click="editProfile" class="edit-button">Edit Profile</button>
    </div>
  </template>
  
  <script>
  export default {
    name: "SponsorProfile",
    data() {
      return {
        user: {} // Sponsor data will be fetched from API
      };
    },
    mounted() {
      // Fetch sponsor data on component mount
      this.fetchUserData();
    },
    methods: {
      async fetchUserData() {
        const userId = localStorage.getItem('userId'); // Get userId from localStorage
        const authToken = localStorage.getItem('authToken'); // Get authToken from localStorage
  
        if (!userId || !authToken) {
          console.error('No userId or authToken found in localStorage');
          return;
        }
  
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/sponsor/profile`, {
            headers: {
              'Authorization': `${authToken}` // Add Authorization header
            }
          });
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          console.log('Sponsor data fetched:', data); // Debug: Check the fetched data
          this.user = data.data[0];
        } catch (error) {
          console.error('Failed to fetch sponsor data:', error);
        }
      },
      editProfile() {
        // Redirect to edit profile page
        this.$router.push('/sponUpdatePro');
      }
    }
  }
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
  