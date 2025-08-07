<template>
   
      <div class="linkBox">
        <router-link to="/influencerCampaigns" class="nav-link" active-class="active-link">Campaign</router-link> |
        <router-link to="/influAdrequest" class="nav-link" active-class="active-link">Ad_Request</router-link> |
        <router-link to="/infNegotiation" class="nav-link" active-class="active-link">Negotiation</router-link> |
        <router-link to="/influeProfile" class="nav-link" active-class="active-link">Profile</router-link>
      </div>
    
  </template>
    
    <script>
  export default {
    name: "Header",
    methods: {
      handleAdd() {
        const currentRoute = this.$route.name;
  
        if (currentRoute === 'campaign') {
          this.$router.push('/addcampaign');
        } else if (currentRoute === 'adrequest') {
          this.$router.push('/addrequest');
        } else {
          console.error('Unknown route:', currentRoute);
        }
      }
    }
  }
  </script>
    
    <style>
    .heading {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 50px;
    }
    
    .linkBox {
      display: flex;
      width: 150px;
      justify-content: space-between;
    }
    
    .linkBox a.active-link {
      color: red;
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
    </style>
    