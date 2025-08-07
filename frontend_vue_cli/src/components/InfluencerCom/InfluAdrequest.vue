<template>
  <div class="container">
    <InfluencerHeader />
    <h1>Ad Requests</h1>
    <div class="table-responsive">
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
            <th>Campaign</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in adRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.campaign_id }}</td>
            <td>{{ request.influencer_id }}</td>
            <td>{{ request.messages }}</td>
            <td>{{ request.requirements }}</td>
            <td>{{ request.payment_amount }}</td>
            <td>{{ request.status }}</td>
            <td>{{ request.created_by }}</td>
            <td>{{ request.updated_by }}</td>
            <td>{{ request.created_at }}</td>
            <td>{{ request.updated_at }}</td>
            <td>{{ request.campaign }}</td>
            <td>
              <a class="nav-link " @click="acceptRequest(request.id)">Accept</a> |
              <a class="nav-link delete" @click="rejectRequest(request.id)">Reject</a> |
              <router-link :to="{ name: 'infAddNegotiation', params: { adRequestId: request.id } }" class="nav-link">Negotiation</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import InfluencerHeader from '../Headers/InfluencerHeader.vue';

export default {
  name: 'InfluAdrequest',
  components: {
    InfluencerHeader
  },
  data() {
    return {
      adRequests: []
    };
  },
  created() {
    this.checkLoginStatus();
  },
  methods: {
    async checkLoginStatus() {
      const token = localStorage.getItem('authToken');
      if (!token) {
        this.$router.push('/login');
      } else {
        this.fetchAdRequests();
      }
    },
    async fetchAdRequests() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/adrequest', {
          headers: { Authorization: `${localStorage.getItem('authToken')}` }
        });
        if (response.status === 200) {
          this.adRequests = response.data.data;
        }
      } catch (error) {
        console.error("Error fetching ad requests:", error);
      }
    },
    async acceptRequest(id) {
      try {
        const response = await axios.put(`http://127.0.0.1:5000/api/adrequest/accept/${id}`, {}, {
          headers: { Authorization: `${localStorage.getItem('authToken')}` }
        });
        if (response.status === 200) {
          alert('Request accepted successfully!');
          this.fetchAdRequests(); // Refresh the list of ad requests
        }
      } catch (error) {
        alert('Error accepting request: ' + error.message);
      }
    },
    async rejectRequest(id) {
      try {
        const response = await axios.put(`http://127.0.0.1:5000/api/adrequest/reject/${id}`, {}, {
          headers: { Authorization: `${localStorage.getItem('authToken')}` }
        });
        if (response.status === 200) {
          alert('Request rejected successfully!');
          this.fetchAdRequests(); // Refresh the list of ad requests
        }
      } catch (error) {
        alert('Error rejecting request: ' + error.message);
      }
    }
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.table-responsive {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th, .table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.table th {
  background-color: #f2f2f2;
  text-align: left;
}

.table tr:nth-child(even) {
  background-color: #f9f9f9;
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

@media (max-width: 768px) {
  .table th, .table td {
    padding: 12px;
    font-size: 12px;
  }

  .nav-link {
    font-size: 12px;
  }
}
</style>
