<template>
  <div class="heading">
    <div class="linkBox">
      <router-link to="/campaign" class="nav-link" active-class="active-link">Campaign</router-link> |
      <router-link to="/adrequest" class="nav-link" active-class="active-link">Ad_Request</router-link> |
      <router-link to="/spoNegotiation" class="nav-link" active-class="active-link">Negotiation</router-link> |
      <router-link to="/sponsorProfile" class="nav-link" active-class="active-link">profile</router-link> 
    </div>

    <a class="btn btn-success" @click="handleAdd">
      <i class="fas fa-plus fa-xs"></i>
      Add
    </a>
    <a class="btn btn-success" @click="handleCSV">
      <i class="fas fa-plus fa-xs"></i>
      Export campaign CSV
    </a>
  </div>
</template>
  
<script>
import axios from 'axios';

export default {
  name: "Header",
  data() {
        return {
            token: null
        }
    },
    created(){
        console.log(localStorage.getItem('authToken'))
        this.token = localStorage.getItem('authToken')
        if (!this.token) {
            this.$router.push('/login')
        }
    },
  methods: {
    handleAdd() {
      const currentRoute = this.$route.name;

      if (currentRoute === 'campaign' || currentRoute === 'dashboard') {
        this.$router.push('/campAdd');
      } else if (currentRoute === 'adrequest') {
        this.$router.push('/addrequest');
      } else {
        console.error('Unknown route:', currentRoute);
      }
    },
    async handleCSV() {
    try {
      // Call the API with headers passed as the second argument
      await axios.post('http://127.0.0.1:5000/api/sponsor/exportcsv', {}, {
        headers: {
          'Authorization': `${this.token}`  // Make sure to use the 'Bearer' scheme if your backend expects it
        }
      });
      
      // Show alert message
      alert('Export process started. You will receive an email once done.');
    } catch (error) {
      console.error('Error starting export process:', error);
      alert('There was an error starting the export process. Please try again.');
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
