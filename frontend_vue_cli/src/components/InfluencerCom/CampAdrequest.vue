<template>
    <div>
      <h2>Ad Requests</h2>
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
            <td>{{ request.update_at }}</td>
            <td>{{ request.campaign }}</td>
            <td>
                <router-link :to="{name: 'infDetailAdReq', params: {adRequestId: request.id}}"  class="nav-link " >View</router-link> 
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    name: 'campAdrequest',
    data() {
      return {
        adRequests: []
      };
    },
    created() {
  try {
    const adRequests = this.$route.query.adRequests;
    if (adRequests) {
      this.adRequests = JSON.parse(adRequests);
    }
  } catch (error) {
    console.error("Failed to parse adRequests:", error);
    this.adRequests = [];
  }
}
  };
  </script>
  
  <style scoped>
  /* Add styles as needed */
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
  </style>
  