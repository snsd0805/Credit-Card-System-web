<script>

import Web3 from 'web3';
import SBT from '@/assets/SBT.json'
import WarningModal from '../components/WarningModal.vue'
import SuccessModal from '../components/SuccessModal.vue'
import PageTitle from '../components/PageTitle.vue'
import Bank from '@/assets/Bank.json'


export default {
  components: { WarningModal, SuccessModal, PageTitle },
  data() {
    return {
      SBTAddress: import.meta.env.VITE_SBT_ADDR,
      BankAddress: import.meta.env.VITE_BANK_ADDR,
      warningModalStatus: false,
      successModalStatus: false,
      clientAddr: '',
      web3: null,
      token: null,
      bank: null,
      link: '',
      msg: '',
      credit: '',
      arrear: '',
      orderId: '',
      products: [],
      amount: "0",
      amountWei: "0",
      creditWei: "0",
      arrearWei: "0",
      shop: {
        'address': '',
        'name': '',
      },
      waiting: false
    }
  },
  async mounted() {
    // if (!this.$cookies.isKey('linked')) {
    //   this.$router.push('/')
    // }
    this.web3 = new Web3(window.ethereum)
    this.clientAddr = this.$cookies.get('address')
    this.web3.eth.defaultAccount = this.clientAddr
    this.token = new this.web3.eth.Contract(SBT, this.SBTAddress)
    this.bank = new this.web3.eth.Contract(Bank, this.BankAddress)

    // get credit
    this.credit = await this.bank.methods.getCredit(this.clientAddr).call()
    this.creditWei = this.credit
    this.credit = await this.web3.utils.fromWei(this.credit, 'ether')

    // get arrear
    this.arrear = await this.bank.methods.getArrear(this.clientAddr).call()
    this.arrearWei = this.arrear
    this.arrear = await this.web3.utils.fromWei(this.arrear, 'ether')

    // get order
    this.orderId = this.$route.params.id
    console.log("id: ", this.orderId)
    const response = await fetch(`${import.meta.env.VITE_BACKEND_PREFIX}/order/${this.orderId}`);
    var orderData = await response.json();
    this.products = orderData.products
    this.amountWei = orderData.amount
    this.amount = this.web3.utils.fromWei(orderData.amount, 'ether')
    this.shop = orderData.shop
    console.log(this.products)
    console.log(this.amount)
    console.log(this.shop)
  },
  methods: {
    async pay () {
      this.waiting = true
      // await this.bank.methods.pay(this.number, this.shop.address, this.amountWei).send({ from: this.clientAddr })
      try {
        await this.bank.methods.pay(this.orderId, this.shop.address, this.amountWei).send({ from: this.clientAddr })
        this.link = '/client/info'
        this.msg = '支付成功！<br>已經支付'+this.amount+" ETH 給"+this.shop.name+" ("+this.shop.address+")"
        this.successModalStatus = true
      } catch (error) {
        this.msg = '支付失敗'
        this.warningModalStatus = true
      }
      this.waiting = false
    }
  }
}

</script>

<template>
  <section class="blog-posts">
    <div class="container">
      <div class="block">
        <PageTitle title="確認付款資訊" subtitle="確認後由銀行先向店家支付 ETH"></PageTitle>
      </div>
      <div class="block">
        <table class="table is-fullwidth">
          <tbody>
            <tr>
              <th colspan="4" style="text-align: center;">商品清單</th>
            </tr>
            <template v-for="product in products">
              <tr>
                <td><b>{{ product.name }}</b></td>
                <td>{{ web3.utils.fromWei(product.price, 'ether') }} ETH/個</td>
                <td> * {{ product.count }} 個</td>
                <td> 合計 {{ web3.utils.fromWei(product.price, 'ether') * product.count }} ETH</td>
              </tr>
            </template>
            <tr>
              <td colspan="3"></td>
              <td>共計 {{ amount }} ETH</td>
            </tr>
          </tbody>
        </table>
        <table class="table is-fullwidth">
          <tbody>

            <tr>
              <th>支付地址：</th>
              <td colspan="3">{{ this.clientAddr }}</td>
            </tr>
            <tr>
              <th>店家地址：</th>
              <td colspan="3">{{ this.shop.address }} ( {{ this.shop.name }} )</td>
            </tr>
            <tr>
              <th>目前信用額度：</th>
              <td colspan="4">{{ this.credit }} ETH (尚可使用 {{ this.credit - this.arrear }} ETH)</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="block">
        <div class="columns">
          <div class="column is-2 is-offset-5">
            <template v-if="(this.creditWei - this.arrearWei) >= this.amountWei">
              <template v-if="!waiting">
                <button @click="pay" class="button is-primary is-fullwidth is-medium is-outlined">支付</button>
              </template>
              <template v-else>
                <button class="button is-primary is-fullwidth is-medium is-outlined is-loading">支付</button>
              </template>
            </template>
            <template v-else>
              <RouterLink to="/client" class="button is-danger is-fullwidth is-medium is-outlined">額度不足，取消</RouterLink>
            </template>
          </div>
        </div>
      </div>
    </div>
  </section>
  <WarningModal :active="warningModalStatus" :errorMsg="msg" @closeModal="warningModalStatus = false"></WarningModal>
  <SuccessModal :active="successModalStatus" :successMsg="msg" @closeModal="successModalStatus = false" :link="link"
    btnName="繼續"></SuccessModal>
</template>
