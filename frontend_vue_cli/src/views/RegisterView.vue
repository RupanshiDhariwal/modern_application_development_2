<template>
    <form class="form" @submit.prevent="registerUser">
        <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input 
                v-model="form.email"
                type="email" 
                class="form-control input-field" 
                id="email" 
                placeholder="name@example.com" 
                required
            >
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input 
                v-model="form.password"
                type="password" 
                class="form-control input-field" 
                id="password" 
                placeholder="password" 
                required
            >
        </div>

        <div class="mb-3">
            <select 
                v-model="form.role"
                class="form-select input-field" 
                aria-label="Default select example"
                required
            >
                <option value="" disabled>Select Role</option>
                <option value="sponsor">Sponsor</option>
                <option value="influencer">Influencer</option>
            </select>
        </div>
        <button type="submit" class="btn btn-primary btn-submit">Submit</button>
    </form>
</template>

<script>
import axios from 'axios';

export default {
    name: 'RegisterView',
    data() {
        return {
            form: {
                email: '',
                password: '',
                role: ''
            }
        };
    },
    methods: {
        async registerUser() {
            try {
                const response = await axios.post('http://127.0.0.1:5000/api/register', this.form);
                
                if(response.status === 200){
                    alert(response.data.message);
                    this.$router.push('/login');
                    this.resetForm();
                }
                
            } catch (error) {
                console.error('Error registering user:', error);
                alert('Error occurred during registration.');
            }
        },
        resetForm() {
            this.form = {
                email: '',
                password: '',
                role: ''
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
    border: 1px solid  #ccc;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.input-field {
    width: 100%;
}

.btn-submit {
    margin-top: 20px;
}
</style>
