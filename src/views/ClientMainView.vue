<script>
import Web3 from 'web3';
import SBT from '@/assets/SBT.json'
import PageTitle from '../components/PageTitle.vue'
import detectEthereumProvider from '@metamask/detect-provider'
import WarningModal from '../components/WarningModal.vue'
import SuccessModal from '../components/SuccessModal.vue'
import { useClientStore } from '../stores/Client.js'
import ClientNav from '../components/ClientNav.vue'

// To use Html5QrcodeScanner (more info below)
import { Html5QrcodeScanner } from "html5-qrcode";

// To use Html5Qrcode (more info below)
import { Html5Qrcode } from "html5-qrcode";



export default {
  components: { PageTitle, WarningModal, SuccessModal, ClientNav },
  data() {
    return {
      SBTAddress: import.meta.env.VITE_SBT_ADDR,
      number: 0,
      warningModalStatus: false,
      successModalStatus: false,
      msg: '',
      clientAddr: '',
      web3: null,
      token: null,
      isWaiting: false,
      log: [],
      scanner: null
    }
  },
  async mounted() {
    if (!this.$cookies.isKey('linked')) {
      this.$router.push('/')
    }
    this.web3 = new Web3(window.ethereum)
    this.clientAddr = (await this.web3.eth.getAccounts())[0]
    this.web3.eth.defaultAccount = this.clientAddr
  },
  methods: {
    onScanSuccess(decodedText, decodedResult) {
      // handle the scanned code as you like, for example:
      console.log(`Code matched = ${decodedText}`, decodedResult);
      this.scanner.clear()
    },
    scan () {
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
          <!-- <ClientNav path="main"></ClientNav> -->
        </div>
        <div class="column">
          <div class="container">
            <div class="block">
              <PageTitle title="Set Credit Limit" subtitle="根據 SBT 信用紀錄設定額度"></PageTitle>
            </div>
            <div class="block">

              <div class="tile is-ancestor">
                <div class="tile is-vertical is-8">
                  <div class="tile">
                    <div class="tile is-parent is-vertical">


                      <RouterLink to="/client/info" class="tile is-child notification is-info">
                        <article>
                          <p class="title"><i class="fas fa-user"></i> 個人資料</p>
                          <!-- <p class="subtitle">Top tile</p> -->
                        </article>
                      </RouterLink>
                      <RouterLink to="/client/pay" class="tile is-child notification is-info">
                        <article>
                          <p class="title"><i class="fas fa-credit-card"></i> 掃描支付</p>
                          <!-- <p class="subtitle">Top tile</p> -->
                        </article>
                      </RouterLink>
                      <RouterLink to="/client/credit" class="tile is-child notification is-info">
                        <article>
                          <p class="title"><i class="fas fa-history"></i> 信用紀錄</p>
                          <!-- <p class="subtitle">Top tile</p> -->
                        </article>
                      </RouterLink>
                    </div>
                  </div>
                </div>
              </div>


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
