<template>
    <div class="ad-request-details">
        <h2>Ad Request Details (ID: {{ id }})</h2>
        
        <div class="button-group">
            <button  class="btn-action">Accept</button>
            <button  class="btn-action">Reject</button>
        </div>

        <div class="detail-group">
            <label class="detail-label">Campaign ID:</label>
            <p class="detail-value">{{ adRequest.campaign_id }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Influencer ID:</label>
            <p class="detail-value">{{ adRequest.influencer_id }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Messages:</label>
            <p class="detail-value">{{ adRequest.messages }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Requirements:</label>
            <p class="detail-value">{{ adRequest.requirements }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Payment Amount:</label>
            <p class="detail-value">{{ adRequest.payment_amount }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Status:</label>
            <p class="detail-value">{{ adRequest.status }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Created By:</label>
            <p class="detail-value">{{ adRequest.created_by }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Updated By:</label>
            <p class="detail-value">{{ adRequest.updated_by }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Created At:</label>
            <p class="detail-value">{{ formatDate(adRequest.created_at) }}</p>
        </div>
        <div class="detail-group">
            <label class="detail-label">Updated At:</label>
            <p class="detail-value">{{ formatDate(adRequest.updated_at) }}</p>
        </div>

        
    </div>
</template>
<script>
import axios from 'axios';
import Headers from '@/components/Headers/Headers.vue';

export default {
    name: 'InfDetailAdReq',
    components: {
       Headers
    },
    data() {
        return {
            adRequest: {
                campaign_id: null,
                influencer_id: null,
                messages: null,
                requirements: null,
                payment_amount: null,
                status: null,
                created_by: null,
                updated_by: null,
                created_at: null,
                updated_at: null,
            },
            responseMessage: null,
            token: null,
            id: null
        };
    },
    created() {
        this.token = localStorage.getItem('authToken');
        this.id = this.$route.params.adRequestId;
        if (!this.token) {
            this.$router.push('/login');
        }
        this.getAdRequestDetails();
    },
    methods: {
        getAdRequestDetails() {
            axios
                .get(`http://localhost:5000/api/adrequest/${this.id}`, {
                    headers: { Authorization: `${this.token}` }
                })
                .then(response => {
                    if (response.status === 200) {
                        const data = response.data.data;
                        this.adRequest = data;
                    }
                })
                .catch(error => {
                    console.log("Error fetching ad request details", error);
                });
        },
        formatDate(dateString) {
            const date = new Date(dateString);
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        }
    }
};
</script>
<style>
.ad-request-details {
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
