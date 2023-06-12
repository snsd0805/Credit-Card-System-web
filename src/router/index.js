import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import LinkSBTView from '../views/LinkSBTView.vue'
import CreditView from '../views/CreditView.vue'
import ClientMainView from '../views/ClientMainView.vue'
import ClientInfoView from '../views/ClientInfoView.vue'
import ClientCreditView from '../views/ClientCreditView.vue'
import ClientPayView from '../views/ClientPayView.vue'
import PaymentView from '../views/PaymentView.vue'
import ShopPayView from '../views/ShopPayView.vue'
import ShopPayQRcodeView from '../views/ShopPayQRcodeView.vue'
import ShopLogView from '../views/ShopLogView.vue'
import OrderView from '../views/OrderView.vue'
import ClientLogView from '../views/ClientLogView.vue'
import ClientRepayView from '../views/ClientRepayView.vue'
import ShopManageView from '../views/ShopManageView.vue'

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
    {
      path: '/client/pay/:id',
      name: 'clientpayment',
      component: PaymentView
    },
    {
      path: '/shop/pay',
      name: 'shoppay',
      component: ShopPayView
    },
    {
      path: '/shop/pay/:id',
      name: 'shopayqrcode',
      component: ShopPayQRcodeView
    },
    {
      path: '/shop/log',
      name: 'shopaylog',
      component: ShopLogView
    },
    {
      path: '/order/:id',
      name: 'order',
      component: OrderView
    },
    {
      path: '/client/log',
      name: 'log',
      component: ClientLogView
    },
    {
      path: '/client/repay',
      name: 'repay',
      component: ClientRepayView
    },
    {
      path: '/shop/manage',
      name: 'shopmanage',
      component: ShopManageView
    },
  ]
})

export default router
