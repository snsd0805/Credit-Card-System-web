<script>
import Web3 from 'web3';
import SBT from '@/assets/SBT.json'
import Bank from '@/assets/Bank.json'
import PageTitle from '../components/PageTitle.vue'
import WarningModal from '../components/WarningModal.vue'
import SuccessModal from '../components/SuccessModal.vue'
import ClientNav from '../components/ClientNav.vue'
import ShopNav from '../components/ShopNav.vue'

// To use Html5QrcodeScanner (more info below)
import { Html5QrcodeScanner } from "html5-qrcode";


export default {
  components: { PageTitle, WarningModal, SuccessModal, ClientNav, ShopNav },
  data() {
    return {
      SBTAddress: import.meta.env.VITE_SBT_ADDR,
      BankAddress: import.meta.env.VITE_BANK_ADDR,
      clientAddr: '',
      web3: null,
      token: null,
      bank: null,
      warningModalStatus: false,
      successModalStatus: false,
      msg: '',
      isWaiting: false,
      products: {},
      productCar: [],
      orderId: '0'
    }
  },
  async mounted() {
    this.web3 = new Web3(window.ethereum)
    if (this.$cookies.isKey('address')) {
      this.clientAddr = this.$cookies.get('address')
    } else {
      console.log("Use default address")
      this.clientAddr = import.meta.env.VITE_DEFAULT_SHOP
    }
    this.web3.eth.defaultAccount = this.clientAddr
    this.token = new this.web3.eth.Contract(SBT, this.SBTAddress)
    this.bank = new this.web3.eth.Contract(Bank, this.BankAddress)

    var result = await fetch(import.meta.env.VITE_BACKEND_PREFIX + "/shop/" + this.clientAddr + "/products")
    var data = await result.json()
    for (let product in data['products']) {
      this.products[product] = data['products'][product]
    }
  },
  computed: {
    amount() {
      if (!this.web3) {
        return 0
      }
      var ans = 0
      for (let product of this.productCar) {
        ans += Number(product['price']) * product['count']
      }
      return this.web3.utils.fromWei(ans.toString())
    }
  },
  methods: {
    onScanSuccess(decodedText, decodedResult) {
      // handle the scanned code as you like, for example:
      console.log(`Code matched = ${decodedText}`, decodedResult);
      var product = this.products[decodedText]
      this.productCar.push({
        'name': product['name'],
        'id': product['id'],
        'price': product['price'],
        'count': 1
      })
      this.scanner.clear()
    },
    scan() {
      this.scanner = new Html5QrcodeScanner(
        "reader",
        { fps: 10, qrbox: { width: 250, height: 250 } },
        /* verbose= */ false);
      this.scanner.render(this.onScanSuccess);
    },
    async send() {
      this.isWaiting = true

      var data = {}
      data['from'] = this.clientAddr
      data['products'] = []
      for (let product of this.productCar) {
        data['products'].push({
          'product_id': product['id'],
          'count': product['count']
        })
      }
      try {
        var result = await fetch(import.meta.env.VITE_BACKEND_PREFIX+"/order", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })
        this.orderId = await result.json()
        this.msg = '完成'
        this.successModalStatus = true
      } catch (error) {
        this.msg = '錯誤'
        this.warningModalStatus = true
      }
      this.productCar = []
      this.isWaiting = false
    }
  }
}
</script>

<template>
  <section class="blog-posts">
    <div class="container">
      <div class="columns">
        <div class="column is-2">
          <ClientNav path="shoppay"></ClientNav>
          <ShopNav path="shoppay"></ShopNav>
        </div>
        <div class="column">
          <div class="container">
            <div class="block">
              <PageTitle title="店家收款" subtitle="掃描商品條碼以加入收款單"></PageTitle>
            </div>
            <div class="block">
              <button class="button is-success is-outlined is-large" @click="scan">掃描商品條碼</button>
              <div id="reader" width="300px"></div>
            </div>
            <div class="block">
              <table class="table is-fullwidth">
                <tbody>
                  <tr>
                    <th colspan="4" style="text-align: center;">商品清單</th>
                  </tr>
                  <template v-for="product in productCar">
                    <tr>
                      <td>{{ product['name'] }}</td>
                      <td>{{ this.web3.utils.fromWei(product['price']) }} ETH</td>
                      <td><input class="input is-info" type="number" v-model="product['count']">個</td>
                    </tr>
                  </template>
                  <tr>
                    <td colspan="3">共計 {{ amount }} ETH</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="block">
              <template v-if="!isWaiting">
                <button class="button is-info is-outlined is-large" @click="send">確認以上訂單</button>
              </template>
              <template v-else>
                <button class="button is-info is-outlined is-large is-loading"></button>
              </template>
            </div>
          </div>

        </div>
      </div>
    </div>
  </section>
  <WarningModal :active="warningModalStatus" :errorMsg="msg" @closeModal="warningModalStatus = false"></WarningModal>
  <SuccessModal :active="successModalStatus" :successMsg="msg" @closeModal="successModalStatus = false"
    :link="`/shop/pay/${this.orderId}`" btnName="繼續"></SuccessModal>
</template>
