<template>
    <div >
      <Campaign />
    </div>
</template>
  

<script>
import Campaign from '@/components/Campaign/Campaign.vue'
import Headers from '@/components/Headers/Headers.vue'

export default {
    name:"Dashboard",
    components:{
      Campaign,
      Headers,
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
    },
    methods: {
        addCampaign(){
            console.log('working')
            this.$router.push('/addcapmaign')
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