<script>
import Web3 from 'web3';
import SBT from '@/assets/SBT.json'
import Bank from '@/assets/Bank.json'
import PageTitle from '../components/PageTitle.vue'
import WarningModal from '../components/WarningModal.vue'
import SuccessModal from '../components/SuccessModal.vue'
import ClientNav from '../components/ClientNav.vue'

// To use Html5QrcodeScanner (more info below)
import { Html5QrcodeScanner } from "html5-qrcode";


export default {
  components: { PageTitle, WarningModal, SuccessModal, ClientNav },
  data() {
    return {
      SBTAddress: import.meta.env.VITE_SBT_ADDR,
      BankAddress: import.meta.env.VITE_BANK_ADDR,
      clientAddr: '',
      web3: null,
      token: null,
      bank: null,
      picName: '',
      pic: '',
      credit: '',
      arrear: '',
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
    this.credit = await this.web3.utils.fromWei(this.credit, 'ether')

    // get arrear
    this.arrear = await this.bank.methods.getArrear(this.clientAddr).call()
    this.arrear = await this.web3.utils.fromWei(this.arrear, 'ether')

  },
  methods: {
    onScanSuccess(decodedText, decodedResult) {
      // handle the scanned code as you like, for example:
      console.log(`Code matched = ${decodedText}`, decodedResult);
      var last_id = decodedText.split('/').pop()
      this.scanner.clear()
      this.$router.push('/client/pay/'+last_id)
    },
    scan() {
      this.scanner = new Html5QrcodeScanner(
        "reader",
        { fps: 10, qrbox: { width: 250, height: 250 } },
        /* verbose= */ false);
      this.scanner.render(this.onScanSuccess);
    }
  }
}
</script>

<template>
  <section class="blog-posts">
    <div class="container">
      <div class="columns">
        <div class="column is-2">
          <ClientNav path="pay"></ClientNav>
        </div>
        <div class="column">
          <div class="container">
            <div class="block">
              <PageTitle title="掃描支付" subtitle="掃描店家給的訂單 QRcode 進行支付"></PageTitle>
            </div>
            <div class="block">
              <p class="block">使用地址：{{ this.clientAddr }}</p>
              <p class="block">剩餘額度：{{ this.credit-this.arrear }} ETH (總額度 {{ this.credit }} ETH )</p>
              
            </div>
            <div class="block">
              <button class="button is-success is-outlined is-large" @click="scan">Pay</button>
              <div id="reader" width="300px"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <WarningModal :active="warningModalStatus" :errorMsg="msg" @closeModal="warningModalStatus = false"></WarningModal>
  <SuccessModal :active="successModalStatus" :successMsg="msg" @closeModal="successModalStatus = false"
    link="/signup/linksbt" btnName="繼續"></SuccessModal>
</template>
