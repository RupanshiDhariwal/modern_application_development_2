<template>
    <div class="campaign-details">
        <h2>Campaign Details (ID: {{ id }})</h2>
        
        <div class="button-group">
            <button @click="addRequest" class="btn-action">Add Request</button>
            <button @click="editCampaign" class="btn-action">Edit</button>
            <button @click="deleteCampaign" class="btn-action">Delete</button>
            <button @click="viewAllRequests" class="btn-action">See All Requests</button>
        </div>

        <div class="detail-group">
            <label class="detail-label">Campaign Name:</label>
            <p class="detail-value">{{ name }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Description:</label>
            <p class="detail-value">{{ description }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Start Date:</label>
            <p class="detail-value">{{ start_date }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">End Date:</label>
            <p class="detail-value">{{ end_date }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Budget:</label>
            <p class="detail-value">{{ budget }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Visibility:</label>
            <p class="detail-value">{{ visibility }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Goals:</label>
            <p class="detail-value">{{ goals }}</p>
        </div>
        
        <p>{{ responseMessage }}</p>
    </div>
</template>

<script>
import axios from 'axios';
import Headers from '@/components/Headers/Headers.vue';

export default {
    name: 'CampDetailsView',
    components: {
       Headers
    },
    data() {
        return {
            name: null,
            description: null,
            start_date: null,
            end_date: null,
            budget: null,
            visibility: null,
            goals: null,
            responseMessage: null,
            token: null,
            id: null
        };
    },
    created() {
        this.token = localStorage.getItem('authToken');
        this.id = this.$route.params.campaignId;
        if (!this.token) {
            this.$router.push('/login');
        }
        this.getCampaignDetails();
    },
    methods: {
        getCampaignDetails() {
            axios
                .get(`http://localhost:5000/api/campaign/${this.id}`, {
                    headers: { Authorization: `${this.token}` }
                })
                .then(response => {
                    if (response.status === 200) {
                        const data = response.data.data;
                        this.name = data.name;
                        this.description = data.description;
                        this.start_date = this.formatDate(data.start_date);
                        this.end_date = this.formatDate(data.end_date);
                        this.budget = data.budget;
                        this.visibility = data.visibility;
                        this.goals = data.goals;
                    }
                })
                .catch(error => {
                    console.log("Error fetching campaign details", error);
                });
        },
        formatDate(dateString) {
            const date = new Date(dateString);
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        },
        addRequest() {
            // Logic to handle add request
        },
        editCampaign() {
            this.$router.push(`/editCampaign/${this.id}`);
        },
        deleteCampaign() {
            axios
                .delete(`http://localhost:5000/api/campaign/${this.id}`, {
                    headers: { Authorization: `${this.token}` }
                })
                .then(response => {
                    if (response.status === 201) {
                        this.responseMessage = "Campaign deleted successfully!";
                        alert('campaign deleted successfully !')
                        this.$router.push('/dashboard');
                    }
                })
                .catch(error => {
                    console.log("Error deleting campaign", error);
                    this.responseMessage = "Failed to delete campaign.";
                });
        },
        viewAllRequests() {
            // this.$router.push(`/campaign/${this.id}/requests`);
        }
    }
};
</script>

<style>
.campaign-details {
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

.detail-group {
    margin-bottom: 15px;
    width: 100%;
}

.detail-label {
    font-weight: bold;
}

.detail-value {
    margin-left: 10px;
    padding: 8px;
    background-color: #f9f9f9;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.button-group {
    margin-top: 20px;
    display: flex;
    gap: 10px;
}

.btn-action {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.btn-action:hover {
    background-color: #45a049;
}
</style>
