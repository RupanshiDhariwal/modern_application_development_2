<template>
  <form class="form" @submit.prevent="loginfunc">
      <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input type="email" v-model="email" class="form-control input-field" id="email" placeholder="name@example.com">
      </div>
      <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" v-model="password" class="form-control input-field" id="password" placeholder="password">
      </div>
     
      <button type="submit" class="btn btn-primary btn-submit">Submit</button>
  </form>
  <a class="register-link" @click="registerPage">click here to register</a>
  <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginView',
  data() {
    return {
      email: null,
      password: null,
      errorMessage: null
    };
  },
  methods: {
    printonconsole() {
      console.log("email: ", this.email);
      console.log("password: ", this.password);
    },
    loginfunc() {
      console.log('working');
      axios
        .post('http://localhost:5000/api/login', {
          email: this.email,
          password: this.password
        })
        .then(response => {
          console.log("response block", response);
          
          if (response.status === 200) {
            // Store authToken and roles in localStorage
            localStorage.setItem('authToken', response.data.authToken);
            localStorage.setItem('role', JSON.stringify(response.data.roles)); // Save roles as a JSON string
            localStorage.setItem('userId', JSON.stringify(response.data.userId));
            this.email = null;
            this.password = null;
            this.errorMessage = null;
            this.routeBasedOnRole(response.data.roles);
          }
        })
        .catch(error => {
          console.log("error block", error);
          
          if (error.response) {
            // Check status code and set error message accordingly
            if (error.response.status === 403) {
              this.errorMessage = "You are not approved by admin yet.";
            } else if (error.response.status === 401) {
              this.errorMessage = "Check your credentials.";
            } else {
              this.errorMessage = "An unexpected error occurred.";
            }
          } else {
            this.errorMessage = "Network error or server not reachable.";
          }
        });
    },
    routeBasedOnRole(roles) {
      if (roles.includes('influencer')) {
        this.$router.push('/influencer-dashboard');
      } else if (roles.includes('sponsor')) {
        this.$router.push('/dashboard');
      } else if (roles.includes('admin')) {
        this.$router.push('/admin-dashboard');
      } else {
        console.log('Role not recognized');
        // Optionally handle unrecognized roles
      }
    },
    registerPage() {
      this.$router.push('/register');
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

.input-field {
  width: 100%;
}

.btn-submit {
  margin-top: 20px;
}

.register-link {
  display: block;
  margin-top: 20px;
  cursor: pointer;
  color: blue;
  text-decoration: underline;
}

.error-message {
  color: red;
  margin-top: 20px;
}
</style>
