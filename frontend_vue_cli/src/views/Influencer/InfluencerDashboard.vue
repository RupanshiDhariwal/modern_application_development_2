<template>
    <h1>Influencer-Dashboard</h1>
    <Campaings />
</template>
  

<script>
import Campaings from '@/components/InfluencerCom/Campaings.vue';
export default {
    name:"InfluencerDashboard",
    components:{
        Campaings
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