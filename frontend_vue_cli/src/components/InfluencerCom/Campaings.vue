<template>
  <div class="container">
    <InfluencerHeader />
    
    <div class="search-container">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search campaigns..."
        class="search-bar"
      />
      <button
        :disabled="!searchQuery"
        @click="searchCampaigns"
        class="search-button"
      >
        Search
      </button>
    </div>
    
    <div class="table-container">
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
            <td>{{ row.visibility }}</td>
            <td>{{ row.goals }}</td>
            <td>
              <router-link :to="{ name: 'campAdrequest', query: { adRequests: JSON.stringify(row.ad_requests) } }" class="nav-link">
                View Ad Requests
              </router-link>
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
  name: 'InfluencerCampaigns',
  components: {
    InfluencerHeader
  },
  data() {
    return {
      campaigns: [],
      token: null,
      searchQuery: ''
    };
  },
  created() {
    this.token = localStorage.getItem('authToken');
    if (!this.token) {
      this.$router.push('/login');
    } else {
      this.getCampaignfn();
    }
  },
  methods: {
    getCampaignfn() {
      axios
        .get(`http://127.0.0.1:5000/api/campaign/influ/search/`, {
          headers: { Authorization: `${this.token}` }
        })
        .then(response => {
          if (response.status === 200) {
            this.campaigns = response.data.data;
          }
        })
        .catch(error => {
          console.log('Error fetching campaigns:', error);
        });
    },
    searchCampaigns() {
      axios
        .get(`http://127.0.0.1:5000/api/campaign/influ/search/`, {
          params: { search: this.searchQuery },
          headers: { Authorization: `${this.token}` }
        })
        .then(response => {
          if (response.status === 200) {
            this.campaigns = response.data.data;
          }
        })
        .catch(error => {
          console.log('Error searching campaigns:', error);
        });
    }
  }
};
</script>

<style scoped>
.container {
  margin: 0 auto;
  padding: 20px;
  max-width: 1200px;
}

.search-container {
  display: flex;
  margin: 20px 0;
  align-items: center;
}

.search-bar {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.search-button {
  margin-left: 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

.search-button:disabled {
  background-color: #c0c0c0;
  cursor: not-allowed;
}

.table-container {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
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

@media (max-width: 768px) {
  .search-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-bar {
    margin-bottom: 10px;
    width: 100%;
  }
  
  .search-button {
    width: 100%;
  }

  .table-container {
    overflow-x: auto;
  }

  .table {
    width: 100%;
  }

  .table th, .table td {
    font-size: 12px;
  }
}
</style>
