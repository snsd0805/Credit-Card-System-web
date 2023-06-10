<script>
import Web3 from 'web3';
import SBT from '@/assets/SBT.json'
import Bank from '@/assets/Bank.json'
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
      BankAddress: import.meta.env.VITE_BANK_ADDR,
      clientAddr: '',
      web3: null,
      token: null,
      bank: null,
      picName: '',
      pic: '',
      credit: '',
      arrear: '',
      borrowNum: 0,
      repayNum: 0,
      warningNum: 0
    }
  },
  async mounted() {
    if (!this.$cookies.isKey('linked')) {
      this.$router.push('/')
    }
    this.web3 = new Web3(window.ethereum)
    this.clientAddr = this.$cookies.get('address')
    this.web3.eth.defaultAccount = this.clientAddr
    this.token = new this.web3.eth.Contract(SBT, this.SBTAddress)
    this.bank = new this.web3.eth.Contract(Bank, this.BankAddress)

    // get svg image
    var base64Data = await this.token.methods.tokenURI(this.$cookies.get('SBTNumber')).call()
    const commaIndex = base64Data.indexOf(',');
    if (commaIndex !== -1) {
      base64Data = base64Data.substr(commaIndex + 1);
    }
    const decodedData = JSON.parse(atob(base64Data));
    this.picName = decodedData.name
    this.pic = decodedData.image_data
    this.pic = this.pic.replace('<svg', '<svg class="svg-container"')

    // get credit
    this.credit = await this.bank.methods.getCredit(this.clientAddr).call()
    this.credit = await this.web3.utils.fromWei(this.credit, 'ether')

    // get arrear
    this.arrear = await this.bank.methods.getArrear(this.clientAddr).call()
    this.arrear = await this.web3.utils.fromWei(this.arrear, 'ether')

    var borrow = await this.token.getPastEvents("Borrow", { fromBlock: 0, toBlock: 'latest', filter: { client: this.clientAddr, bank: this.BankAddress } })
    var repay = await this.token.getPastEvents("Repay", { fromBlock: 0, toBlock: 'latest', filter: { client: this.clientAddr, bank: this.BankAddress } })
    var warning = await this.token.getPastEvents("Warning", { fromBlock: 0, toBlock: 'latest', filter: { client: this.clientAddr, bank: this.BankAddress } })
    this.borrowNum = borrow.length
    this.repayNum = repay.length
    this.warningNum = warning.length
  },
  methods: {
  }
}
</script>

<template>
  <section class="blog-posts">
    <div class="container">
      <div class="columns">
        <div class="column is-2">
          <ClientNav path="info"></ClientNav>
        </div>
        <div class="column">
          <div class="container">
            <div class="block">
              <PageTitle title="個人資料" subtitle="紀錄在區塊鏈上的相關資料"></PageTitle>
            </div>
            <div class="block">
              <table class="table is-fullwidth">
                <tbody>
                  <tr>
                    <th>地址：</th>
                    <td>{{ this.clientAddr }}</td>
                    <!-- <td>{{ this.clientAddr.slice(0, 8)+"..."+this.clientAddr.slice(33, 42) }}</td> -->
                  </tr>
                  <tr>
                    <th>目前信用額度：</th>
                    <td>{{ this.credit }} ETH (尚可使用 {{ this.credit-this.arrear }} ETH)</td>
                    <!-- <td>{{ this.clientAddr.slice(0, 8)+"..."+this.clientAddr.slice(33, 42) }}</td> -->
                  </tr>
                  <tr>
                    <th>目前欠款：</th>
                    <td>{{ this.arrear }} ETH</td>
                    <!-- <td>{{ this.clientAddr.slice(0, 8)+"..."+this.clientAddr.slice(33, 42) }}</td> -->
                  </tr>
                  <tr>
                    <th>本銀行借款紀錄簡覽</th>
                    <td>共計借款 {{ this.borrowNum }} 項，已還款 {{ this.repayNum }} 項。被本銀行預警 {{ this.warningNum }} 次</td>
                  </tr>
                  <tr>
                    <th>Soulbound Token 號碼：</th>
                    <td>{{ this.$cookies.get('SBTNumber') }}</td>
                  </tr>
                  <tr>
                    <th>Soulbound Token NFT 證書：</th>
                    <td>{{ picName }}<div class="block is-fullwidth" v-html="pic"></div></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
