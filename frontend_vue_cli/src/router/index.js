import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '@/views/RegisterView.vue'
import LoginView from '@/views/LoginView.vue'
import Dashboard from '@/views/Sponsor/Dashboard.vue'
import AdrequestView from '@/views/Sponsor/AdrequestView.vue'
import EditCampView from '@/views/Sponsor/campaign/EditCampView.vue'
import CampDetailsView from '@/views/Sponsor/campaign/CampDetailsView.vue'
import Campaign from '@/components/Campaign/Campaign.vue'
import AddRequest from '@/components/AdRequest/AddRequest.vue'
import EditRequest from '@/components/AdRequest/EditRequest.vue'
import DetailAdRequest from '@/components/AdRequest/DetailAdRequest.vue'
import InfluencerDashboard from '@/views/Influencer/InfluencerDashboard.vue'
import AdminDashboard from '@/views/Admin/AdminDashboard.vue'
import CampAdrequest from '@/components/InfluencerCom/CampAdrequest.vue'
import Campaings from '@/components/InfluencerCom/Campaings.vue'
import InfluAdrequest from '@/components/InfluencerCom/InfluAdrequest.vue'
import InfDetailAdReq from '@/components/InfluencerCom/InfDetailAdReq.vue'
import InfAddNegotiation from '@/components/InfluencerCom/InfAddNegotiation.vue'
import InfNegotiation from '@/components/InfluencerCom/InfNegotiation.vue'
import InflueProfile from '@/components/Profiles/InflueProfile.vue'
import InflueUpdateProfie from '@/components/Profiles/InflueUpdateProfie.vue'
import AdmRequest from '@/components/AdminComp/AdmRequest.vue'
import AdmUsers from '@/components/AdminComp/AdmUsers.vue'
import ApproveSponsors from '@/components/AdminComp/ApproveSponsors.vue'
import CampAdd from '@/components/Campaign/CampAdd.vue'
import SpoNegotiation from '@/components/Sponsor/SpoNegotiation.vue'
import SponsorProfile from '@/components/Profiles/SponsorProfile.vue'
import SponUpdatePro from '@/components/Profiles/SponUpdatePro.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/adrequest',
    name: 'adrequest',
    component: AdrequestView
    
  },
  {
    path: '/addrequest',
    name: 'addrequest',
    component: AddRequest
    
  },
  {
    path:'/register',
    name:'register',
    component: RegisterView

  },
  {
    path: '/login',
    name:'login',
    component:LoginView
  },
  {
    path:'/dashboard',
    name:'dashboard',
    component:Dashboard
  },
  // {
  //   path:'/addcampaign',
  //   name:'addcampaign',
  //   component: AddCampaign
  // },
  {
    path:'/campaign',
    name:'campaign',
    component:Campaign
  },
  {
    path: '/editCampaign/:campaignId',
    name: 'editCampaign',
    component: EditCampView
  },
  {
    path: '/editRequest/:adRequestId',
    name: 'editRequest',
    component: EditRequest
  },
  {
    path: '/detailsCampaign/:campaignId',
    name: 'campDetailsView',
    component: CampDetailsView
  },
  {
    path: '/detailsRequest/::adRequestId',
    name: 'detailsRequest',
    component:  DetailAdRequest
  },
  {
    path: '/influencer-dashboard',
    name: 'influencer-dashboard',
    component:  InfluencerDashboard
  },
  {
    path: '/admin-dashboard',
    name: 'admin-dashboard',
    component:  AdminDashboard
  },
  {
    path: '/campAdrequest',
    name: 'campAdrequest',
    component: CampAdrequest
  },
  {
    path: '/influencerCampaigns',
    name: 'InfluencerCampaigns',
    component: Campaings
  },
  {
    path: '/influAdrequest',
    name: 'InfluAdrequest',
    component: InfluAdrequest
  },
  {
    path: '/infDetailAdReq/:adRequestId',
    name: 'infDetailAdReq',
    component: InfDetailAdReq
  },
  {
    path: '/infAddNegotiation/:adRequestId',
    name: 'infAddNegotiation',
    component: InfAddNegotiation
  },
  {
    path: '/infNegotiation',
    name: 'infNegotiation',
    component: InfNegotiation
  },
  {
    path: '/influeProfile',
    name: 'influeProfile',
    component: InflueProfile
  },
  {
    path: '/influeUpdateProfie',
    name: 'influeUpdateProfie',
    component: InflueUpdateProfie
  },
  {
    path: '/adminDashboard',
    name: 'adminDashboard',
    component: AdminDashboard
  },
  {
    path: '/admRequest',
    name: 'admRequest',
    component: AdmRequest
  },
  {
    path: '/admUsers',
    name: 'admUsers',
    component: AdmUsers
  },
  {
    path: '/approveSponsors',
    name: 'approveSponsors',
    component: ApproveSponsors
  },
  {
    path: '/campAdd',
    name: 'campAdd',
    component: CampAdd
  },
  {
    path: '/spoNegotiation',
    name: 'spoNegotiation',
    component: SpoNegotiation
  },
  {
    path: '/sponsorProfile',
    name: 'sponsorProfile',
    component: SponsorProfile
  },
  {
    path: '/sponUpdatePro',
    name: 'sponUpdatePro',
    component: SponUpdatePro
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Global navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('authToken');
  if (!token && to.name !== 'login' && to.name !== 'register' && to.name !== 'home') {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router
