import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import LinkSBTView from '../views/LinkSBTView.vue'
import CreditView from '../views/CreditView.vue'
import ClientMainView from '../views/ClientMainView.vue'
import ClientInfoView from '../views/ClientInfoView.vue'
import ClientCreditView from '../views/ClientCreditView.vue'
import ClientPayView from '../views/ClientPayView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/signup/linksbt',
      name: 'linksbt',
      component: LinkSBTView
    },
    {
      path: '/signup/credit',
      name: 'startcredit',
      component: CreditView
    },
    {
      path: '/client',
      name: 'clientmain',
      component: ClientMainView
    },
    {
      path: '/client/info',
      name: 'clientinfo',
      component: ClientInfoView
    },
    {
      path: '/client/credit',
      name: 'clientcredit',
      component: ClientCreditView
    },
    {
      path: '/client/pay',
      name: 'clientpay',
      component: ClientPayView
    },
  ]
})

export default router
