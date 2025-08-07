<template>
    <h1>Admin-Dashboard</h1>
    <AdmCampaign />
</template>
  

<script>
import AdmCampaign from '@/components/AdminComp/AdmCampaign.vue';

export default {
    name:"AdminDashboard",
    components:{
        AdmCampaign
    },
    data() {
        return {
            token: null
        }
    },
    created(){
        this.token = localStorage.getItem('authToken')
        if (!this.token) {
            this.$router.push('/login')
        }
    }
}
</script>

<style>
.heading{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 50px;
}
</style>