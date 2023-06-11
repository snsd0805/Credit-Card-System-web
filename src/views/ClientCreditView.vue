<script>
import Web3 from 'web3';
import SBT from '@/assets/SBT.json'
import PageTitle from '../components/PageTitle.vue'
import detectEthereumProvider from '@metamask/detect-provider'
import WarningModal from '../components/WarningModal.vue'
import SuccessModal from '../components/SuccessModal.vue'
import { useClientStore } from '../stores/Client.js'
import ClientNav from '../components/ClientNav.vue'
import ShopNav from '../components/ShopNav.vue'

// To use Html5QrcodeScanner (more info below)
import { Html5QrcodeScanner } from "html5-qrcode";

// To use Html5Qrcode (more info below)
import { Html5Qrcode } from "html5-qrcode";



export default {
  components: { PageTitle, WarningModal, SuccessModal, ClientNav, ShopNav },
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
      warningLog: [],
      scanner: null
    }
  },
  async mounted() {
    this.web3 = new Web3(window.ethereum)
    this.clientAddr = this.$cookies.get('address')
    this.web3.eth.defaultAccount = this.clientAddr
    this.token = new this.web3.eth.Contract(SBT, this.SBTAddress)

    var borrow = await this.token.getPastEvents("Borrow", { fromBlock: 0, toBlock: 'latest', filter: { client: this.clientAddr } })
    for (let i of borrow) {
      let result = i.returnValues
      let obj = {
        bank: result['bank'],
        shop: result['shop'],
        id: result['id'],
        amount: this.web3.utils.fromWei(result['amount'], 'ether'),
        repay: false
      }
      this.log.push(obj)
    }

    var repay = await this.token.getPastEvents("Repay", { fromBlock: 0, toBlock: 'latest', filter: { client: this.clientAddr } })
    for (let i of repay) {
      let result = i.returnValues
      for (let j of this.log) {
        if ((result['bank'] == j.bank) && (result['id'] == j.id)) {
          j.repay = true
        }
      }
    }
    console.log(this.log)

    var warning = await this.token.getPastEvents("Warning", { fromBlock: 0, toBlock: 'latest', filter: { client: this.clientAddr } })
    for (let i of warning) {
      let result = i.returnValues
      this.warningLog.push(result.bank)
    }
    console.log(this.warningLog)
  },
  methods: {
    onScanSuccess(decodedText, decodedResult) {
      // handle the scanned code as you like, for example:
      console.log(`Code matched = ${decodedText}`, decodedResult);
      this.scanner.clear()
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
          <ClientNav path="credit"></ClientNav>
          <template v-if="this.$cookies.get('isShop') == 'true'">
            <ShopNav path="credit"></ShopNav>
          </template>

        </div>
        <div class="column">
          <div class="container">
            <div class="block">
              <PageTitle title="SBT 信用紀錄" subtitle="根據 SBT 信用紀錄設定額度"></PageTitle>
            </div>
            <div class="block">
              <div class="box">
                <div class="content">
                  <h5 class="title is-5">說明</h5>
                  <ul>
                    <li>我們會根據您提供的 SBT 查詢相關信用紀錄，我們會根據紀錄設定給予的每月額度</li>
                    <li>若擁有新的 SBT，代表您不曾擁有過信用紀錄，下表為空。</li>
                    <li>若您不曾擁有過信用交易紀錄，我們提供最低額度 1 ETH/1 month。</li>
                    <li>請確認下表紀錄，我們將依照該紀錄表計算。</li>
                  </ul>
                </div>
              </div>
            </div>
            <br>
            <div class="block">
              <h1 class="title is-4">支付紀錄</h1>
              <table class="table is-fullwidth is-striped is-hoverable">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>銀行</th>
                    <th>銀行帳款編號</th>
                    <th>商店</th>
                    <th>金額</th>
                    <th>已結清帳款</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(value, index) of log">
                    <tr>
                      <th>{{ index }}</th>
                      <td>{{ value.bank }}</td>
                      <td>#{{ value.id }}</td>
                      <td>{{ value.shop }}</td>
                      <td>{{ value.amount }} ETH</td>
                      <td v-if="value.repay">
                        <span class="icon has-text-success">
                          <i class="fas fa-check-square"></i>
                        </span>
                      </td>
                      <td v-else>
                      </td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </div>
            <div class="block">
              <h1 class="title is-4">警告紀錄</h1>
              <table class="table is-fullwidth is-striped is-hoverable">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>發起預警之銀行</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(value, index) of warningLog">
                    <tr>
                      <th>{{ index }}</th>
                      <td>{{ value }}</td>
                    </tr>
                  </template>
                </tbody>
              </table>
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
