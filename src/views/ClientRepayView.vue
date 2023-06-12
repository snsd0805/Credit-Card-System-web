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
      log: [],
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

    var borrow = await this.token.getPastEvents("Borrow", { fromBlock: 0, toBlock: 'latest', filter: { client: this.clientAddr, bank: this.BankAddress } })
    for (let i of borrow) {
      let result = i.returnValues
      let obj = {
        bank: result['bank'],
        shop: result['shop'],
        id: result['id'],
        amount: result['amount'],
        repay: false
      }
      this.log.push(obj)
    }

    var repay = await this.token.getPastEvents("Repay", { fromBlock: 0, toBlock: 'latest', filter: { client: this.clientAddr, bank: this.BankAddress } })
    for (let i of repay) {
      let result = i.returnValues
      for (let j of this.log) {
        if ((result['bank'] == j.bank) && (result['id'] == j.id)) {
          j.repay = true
        }
      }
    }
    console.log(this.log)

  },
  computed: {
    amountWei() {
      if (!this.web3) {
        return 0
      }
      var ans = 0
      for (let item of this.log) {
        if (item.repay == false){
          ans += parseInt(item['amount'])
        }
      }
      return ans
    },
    amount() {
      if (!this.web3) {
        return 0
      }

      return this.web3.utils.fromWei(this.amountWei.toString())
    }
  },
  methods: {
    async repay() {
      this.isWaiting = true
      await this.bank.methods.repay().send({
        from: this.clientAddr,
        value: this.amountWei
      })
      try {
        this.msg = "還款成功！"
        this.successModalStatus = true
      } catch (error) {
        this.msg = "匯款失敗"
        this.warningModalStatus = true
      }
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
          <ClientNav path="repay"></ClientNav>
          <template v-if="this.$cookies.get('isShop') == 'true'">
            <ShopNav path="repay"></ShopNav>
          </template>
        </div>
        <div class="column">
          <div class="container">
            <div class="block">
              <PageTitle title="還款" subtitle="向本銀行償還帳款"></PageTitle>
            </div>
            <div class="block">
              <table class="table is-fullwidth">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>銀行帳款編號</th>
                    <th>商店</th>
                    <th>金額</th>
                    <th>詳細資訊</th>
                  </tr>
                </thead>

                <tbody>
                  <template v-for="(item, index) in log">
                    <template v-if="item.repay == false">
                      <tr>
                        <td>{{ index }}</td>
                        <td>#{{ item.id }}</td>
                        <td>{{ item.shop }}</td>
                        <td>{{ this.web3.utils.fromWei(item.amount) }} ETH</td>
                        <td>
                          <RouterLink :to="'/order/' + item.id" class="button is-info is-outlined">查詢
                          </RouterLink>
                        </td>
                      </tr>

                    </template>
                  </template>
                  <tr>
                    <td colspan="3"></td>
                    <td><strong>共計 {{ amount }} ETH</strong></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="block">
              <div class="column is-2 is-offset-5">
                <template v-if="!isWaiting">
                  <button class="button is-info is-outlined is-large" @click="repay">還款</button>
                </template>
                <template v-else>
                  <button class="button is-info is-outlined is-large is-loading"></button>
                </template>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </section>
  <WarningModal :active="warningModalStatus" :errorMsg="msg" @closeModal="warningModalStatus = false"></WarningModal>
  <SuccessModal :active="successModalStatus" :successMsg="msg" @closeModal="successModalStatus = false"
    :link="`/client/info`" btnName="繼續"></SuccessModal>
</template>
