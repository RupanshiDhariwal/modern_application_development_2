<template>
  <div>
    <h1>Create New Ad Request</h1>
    <form @submit.prevent="submitForm" method="POST" class="form">
      <div class="form-group">
        <label for="campaign_id" class="form-label">Campaign ID:</label>
        <input 
          v-model="searchQuery" 
          @input="searchCampaigns" 
          @focus="showCampaigns = true" 
          @blur="hideCampaigns"
          type="text" 
          id="campaign_id" 
          name="campaign_id" 
          class="form-control input-field" 
          placeholder="Search for a campaign..." 
          required
        >
        <ul v-if="showCampaigns && campaigns.length" class="autocomplete-results">
          <li 
            v-for="campaign in campaigns" 
            :key="campaign.id" 
            @mousedown.prevent="selectCampaign(campaign)"
            class="autocomplete-item"
          >
            {{ campaign.name }} (ID: {{ campaign.id }})
          </li>
        </ul>
      </div>

      <div class="form-group">
        <label for="influencer_id" class="form-label">Influencer ID:</label>
        <input 
          v-model="influencerSearchQuery" 
          @input="searchInfluencers" 
          @focus="showInfluencers = true" 
          @blur="hideInfluencers"
          type="text" 
          id="influencer_id" 
          name="influencer_id" 
          class="form-control input-field" 
          placeholder="Search for an influencer..." 
          
        >
        <ul v-if="showInfluencers && influencers.length" class="autocomplete-results">
          <li 
            v-for="influencer in influencers" 
            :key="influencer.id" 
            @mousedown.prevent="selectInfluencer(influencer)"
            class="autocomplete-item"
          >
            {{ influencer.name }} (ID: {{ influencer.id }})
          </li>
        </ul>
      </div>

      <div class="form-group">
        <label for="messages" class="form-label">Messages:</label>
        <textarea v-model="form.messages" id="messages" name="messages" class="form-control textarea-field" required></textarea>
      </div>

      <div class="form-group">
        <label for="requirements" class="form-label">Requirements:</label>
        <textarea v-model="form.requirements" id="requirements" name="requirements" class="form-control textarea-field" required></textarea>
      </div>

      <div class="form-group">
        <label for="payment_amount" class="form-label">Payment Amount:</label>
        <input v-model="form.payment_amount" type="number" id="payment_amount" name="payment_amount" class="form-control input-field" required>
      </div>

      <div class="form-group">
        <button type="submit" class="btn-submit">Create Ad Request</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AddRequest',
  data() {
    return {
      form: {
        campaign_id: '',
        influencer_id: '',
        messages: '',
        requirements: '',
        payment_amount: ''
      },
      token: null,
      searchQuery: '',
      influencerSearchQuery: '',
      campaigns: [],
      influencers: [],
      showCampaigns: false,
      showInfluencers: false
    };
  },
  created() {
    this.token = localStorage.getItem('authToken');
    if (!this.token) {
      this.$router.push('/login');
    }
  },
  methods: {
    searchCampaigns() {
      let params = {};
      if (this.searchQuery.length > 0) {
        params.query = this.searchQuery;
      }
      axios.get('http://127.0.0.1:5000/api/campaign/user/specific/', {
        params,
        headers: { Authorization: `${this.token}` }
      })
      .then(response => {
        this.campaigns = response.data.data;
      })
      .catch(error => {
        console.error('Error fetching campaigns:', error);
      });
    },
    selectCampaign(campaign) {
      this.form.campaign_id = campaign.id;
      this.searchQuery = campaign.name; // Optional: Set the search query to the selected campaign name
      this.showCampaigns = false; // Hide the list
    },
    hideCampaigns() {
      setTimeout(() => {
        this.showCampaigns = false;
      }, 200);
    },
    searchInfluencers() {
      let params = {};
      if (this.influencerSearchQuery.length > 0) {
        params.query = this.influencerSearchQuery;
      }
      axios.get('http://127.0.0.1:5000/api/influencer/search/list', {
        params,
        headers: { Authorization: `${this.token}` }
      })
      .then(response => {
        this.influencers = response.data.data;
      })
      .catch(error => {
        console.error('Error fetching influencers:', error);
      });
    },
    selectInfluencer(influencer) {
      this.form.influencer_id = influencer.id;
      this.influencerSearchQuery = influencer.name; // Optional: Set the search query to the selected influencer name
      this.showInfluencers = false; // Hide the list
    },
    hideInfluencers() {
      setTimeout(() => {
        this.showInfluencers = false;
      }, 200);
    },
    submitForm() {
      axios.post('http://127.0.0.1:5000/api/adrequest', this.form,
      { headers: { Authorization: `${this.token}` } })
      .then(response => {
        if (response.status === 201) {
          alert('Ad Request created successfully!');
          this.resetForm();
          this.$router.push('/addrequest'); // Redirect to the page where you show all ad requests or any other page
        }
      })
      .catch(error => {
        alert('Error occurred while creating ad request.');
        console.error('Error creating ad request:', error);
      });
    },
    resetForm() {
      this.form = {
        campaign_id: '',
        influencer_id: '',
        messages: '',
        requirements: '',
        payment_amount: ''
      };
      this.searchQuery = ''; // Clear the search query
      this.influencerSearchQuery = ''; // Clear the influencer search query
    }
  }
};
</script>

<style>
/* Reuse the existing styles for form elements */
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

.form-group {
  margin-bottom: 15px;
  width: 100%;
  position: relative; /* Add this to position the autocomplete list correctly */
}

.form-label {
  margin-bottom: 5px;
  font-weight: bold;
}

.input-field, .textarea-field, .select-field {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.textarea-field {
  height: 100px;
}

.btn-submit {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-submit:hover {
  background-color: #45a049;
}

.autocomplete-results {
  border: 1px solid #ccc;
  border-radius: 4px;
  max-height: 150px;
  overflow-y: auto;
  margin-top: 5px;
  padding: 0;
  position: absolute;
  background-color: #fff;
  width: calc(100% - 16px); /* Ensure it matches the input width minus padding/border */
  z-index: 1000;
}

.autocomplete-item {
  padding: 8px;
  cursor: pointer;
}

.autocomplete-item:hover {
  background-color: #f0f0f0;
}
</style>
