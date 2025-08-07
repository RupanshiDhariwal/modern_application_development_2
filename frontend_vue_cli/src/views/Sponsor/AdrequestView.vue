<template>
  <div>
    <Headers />
    <h1>Sponsor Dashboard</h1>

    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Campaign ID</th>
          <th>Influencer ID</th>
          <th>Messages</th>
          <th>Requirements</th>
          <th>Payment Amount</th>
          <th>Status</th>
          <th>Created By</th>
          <th>Updated By</th>
          <th>Created At</th>
          <th>Updated At</th>
          <th>Campaign Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in adRequests" :key="row.id">
          <td>{{ row.id }}</td>
          <td>{{ row.campaign_id }}</td>
          <td>{{ row.influencer_id }}</td>
          <td>{{ row.messages }}</td>
          <td>{{ row.requirements }}</td>
          <td>{{ row.payment_amount }}</td>
          <td>{{ row.status }}</td>
          <td>{{ row.created_by }}</td>
          <td>{{ row.updated_by }}</td>
          <td>{{ row.created_at }}</td>
          <td>{{ row.updated_at }}</td>
          <td>{{ row.campaign }}</td>
          <td>
            <router-link :to="{ name: 'editRequest', params: { adRequestId: row.id } }" class="nav-link">Edit</router-link> |
            <a class="nav-link delete" @click="deleteAdRequest(row.id)">Delete</a> |
            <router-link :to="{ name: 'detailsRequest', params: { adRequestId: row.id } }" class="nav-link">Show</router-link>
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
  name: 'AdRequestView',
  components: {
    Headers
  },
  data() {
    return {
      adRequests: [], // Rename if needed to reflect ad requests
      var12: null,
      token: null
    };
  },
  created() {
    this.token = localStorage.getItem('authToken');
    if (!this.token) {
      this.$router.push('/login');
    } else {
      this.getAdRequests();
    }
  },
  methods: {
    addAdRequest() {
      this.$router.push('/addrequest');
    },
    getAdRequests() {
      axios
        .get(`http://localhost:5000/api/adrequest`, {
          headers: { Authorization: `${this.token}` }
        })
        .then(response => {
          if (response.status === 200) {
            this.var12 = response.data;
            this.adRequests = response.data.data; // Adjust if needed
          }
        })
        .catch(error => {
          console.error('Error fetching ad requests:', error);
        });
    },
    deleteAdRequest(id) {
      axios
        .delete(`http://localhost:5000/api/adrequest/${id}`, {
          headers: { Authorization: `${this.token}` }
        })
        .then(response => {
          if (response.status === 201) { // Use the appropriate status code
            alert('AdRequest deleted successfully!')
            this.getAdRequests();
          }
        })
        .catch(error => {
          console.error('Error deleting ad request:', error);
        });
    }
  }
};
</script>

<style>
  
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