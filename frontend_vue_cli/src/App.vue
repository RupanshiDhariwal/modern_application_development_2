<template>
  <nav>
    <router-link to="/">Home</router-link> 
    <!-- Conditionally render Register and Login links based on authentication -->
    <template v-if="!isAuthenticated">
    | <router-link to="/register">Register</router-link> 
    |  <router-link to="/login">Login</router-link> 
    </template>
    <!-- Render Sponsor and Influencer links based on roles -->
    <template v-if="roles.includes('sponsor')">
      | <router-link to="/dashboard">Sponsor</router-link> 
    </template>
    <template v-if="roles.includes('admin')">
      | <router-link to="/admin-dashboard">Admin</router-link> 
    </template>
    <template v-if="roles.includes('influencer')">
      | <router-link to="/influencer-dashboard">Influencer</router-link>
    </template>
    <!-- Render Logout button if user is authenticated -->
    <button v-if="isAuthenticated" @click="logout">Logout</button>
  </nav>
  <router-view/>
</template>

<script>
export default {
  data() {
    return {
      userId: JSON.parse(localStorage.getItem('userId')) || '',
      roles: JSON.parse(localStorage.getItem('role')) || [],
      isAuthenticated: localStorage.getItem('authToken') !== null
    };
  },
  methods: {
    logout() {
      // Clear local storage
      localStorage.removeItem('authToken');
      localStorage.removeItem('role');
      localStorage.removeItem('userId');
      // Update the data properties
      this.isAuthenticated = false;
      this.roles = [];
      // Redirect to login page
      this.$router.push('/login');
    }
  },
  // Update the component data when the route changes
  watch: {
    $route(to, from) {
      // Update authentication state based on local storage
      this.isAuthenticated = localStorage.getItem('authToken') !== null;
      this.roles = JSON.parse(localStorage.getItem('role')) || [];
      this.userId = JSON.parse(localStorage.getItem('userId')) || '';
    }
  },
  mounted() {
    // Initialize authentication state and roles on mount
    this.isAuthenticated = localStorage.getItem('authToken') !== null;
    this.roles = JSON.parse(localStorage.getItem('role')) || [];
    this.userId = JSON.parse(localStorage.getItem('userId')) || '';

  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

button {
  margin-left: 20px; /* Pushes the button to the rightmost side */
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background-color: #358a6b;
}

</style>
