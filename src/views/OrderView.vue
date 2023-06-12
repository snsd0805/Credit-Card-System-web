<script>

import Web3 from 'web3';
import SBT from '@/assets/SBT.json'
import WarningModal from '../components/WarningModal.vue'
import SuccessModal from '../components/SuccessModal.vue'
import PageTitle from '../components/PageTitle.vue'
import Bank from '@/assets/Bank.json'


export default {
  components: { PageTitle },
  data() {
    return {
      SBTAddress: import.meta.env.VITE_SBT_ADDR,
      BankAddress: import.meta.env.VITE_BANK_ADDR,
      clientAddr: '',
      web3: null,
      token: null,
      bank: null,
      link: '',
      orderId: '',
      products: [],
      amount: "0",
      amountWei: "0",
      client: '',
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

    // get order
    this.orderId = this.$route.params.id
    console.log("id: ", this.orderId)
    const response = await fetch(`${import.meta.env.VITE_BACKEND_PREFIX}/order/${this.orderId}`);
    var orderData = await response.json();
    console.log(orderData)
    this.products = orderData.products
    this.amountWei = orderData.amount
    this.client = orderData.client
    this.amount = this.web3.utils.fromWei(orderData.amount, 'ether')
    this.shop = orderData.shop
  },
}

</script>

<template>
  <section class="blog-posts">
    <div class="container">
      <div class="block">
        <PageTitle title="訂單資訊" subtitle=""></PageTitle>
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
              <td colspan="3">{{ this.client }}</td>
            </tr>
            <tr>
              <th>店家地址：</th>
              <td colspan="3">{{ this.shop.address }} ( {{ this.shop.name }} )</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="block">
        <div class="columns">
          <div class="column is-2 is-offset-5">
              <button @click="this.$router.go(-1)" class="button is-danger is-fullwidth is-medium is-outlined">返回</button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
