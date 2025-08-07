<template>
<div>
    <Headers />
<h1>Sponsor Dashboard </h1>

<table class="table">
    <thead>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Description</th>
        <th>Start Date</th>
        <th>End Date</th>
        <th>Budget</th>
        <th>Status</th>
        <th>Visibility</th>
        <th>Goals</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
        
        <tr v-for="row in campaigns" :key="row.id">

            <td>{{ row.id }}</td>
            <td>{{ row.name }}</td>
            <td>{{ row.description }}</td>
            <td>{{ row.start_date }}</td>
            <td>{{ row.end_date }}</td>
            <td>{{ row.budget }}</td>
            <td>{{ row.status }}</td>
            <td>{{ row.Visibility }}</td>
            <td>{{ row.goals }}</td>
            
            <td><router-link :to="{name: 'editCampaign', params: {campaignId: row.id}}"  class="nav-link " >edit</router-link>|
                <a class="nav-link delete"  @click="deleteCampaign(row.id)"> delete</a>|
                <router-link :to="{name: 'campDetailsView', params: {campaignId: row.id}}"  class="nav-link " >show</router-link> 
            </td>
        </tr>
       
    </tbody>
</table>
</div>
</template>



  
<script>
import axios from 'axios';
import Headers from '@/components/Headers/Headers.vue';

  export default {
    name: 'Campaign',
    components: {
       Headers
    },
    data() {
        return {
            campaigns: [],
            var12: null,
            token: null
        }
    },
    created() {
    this.token = localStorage.getItem('authToken');
    if (!this.token) {
      this.$router.push('/login');
    } else {
      this.getCampaignfn();
    }
  },
    methods:{
        addCampaign(){
            console.log('working')
            this.$router.push('/addcapmaign')
        },
        getCampaignfn(){
        console.log('working')
        axios
            .get(`http://localhost:5000/api/campaign/`,
            {headers: {Authorization: `${this.token}`}})
            .then(response => {
                console.log("response block", response)
                if (response.status == 200) {
                    this.var12 = response.data
                    this.campaigns = response.data.data
                }
            })
            .catch(error => {
                console.log("error block", error)
            })
        },
    deleteCampaign(id){
        axios
            .delete(`http://localhost:5000/api/campaign/${id}`,
            {headers: {Authorization: `${this.token}`}})
            .then(response => {
                console.log("response block", response)
                if (response.status == 201) {
                    this.getCampaignfn()
                }
            })
            .catch(error => {
                console.log("error block", error)
            })
    }
    }
  }
</script>






  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  
  .heading{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 50px;
}
h1,h2{
    text-align: center;
}
.linkBox{
    display: flex;
    width: 150px;
    justify-content: space-between;
}
.linkBox a.active-link{
    color:red;
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

.delete {
    color: #c60000;
}

</style>
  