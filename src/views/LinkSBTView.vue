<script>

import Web3 from 'web3';
import SBT from '@/assets/SBT.json'
import WarningModal from '../components/WarningModal.vue'
import SuccessModal from '../components/SuccessModal.vue'
import PageTitle from '../components/PageTitle.vue'
import { useClientStore } from '../stores/Client.js'


export default {
  components: { WarningModal, SuccessModal, PageTitle },
  name: 'PageFooter',
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
      isWaiting: false
    }
  },
  async mounted() {
    this.web3 = new Web3(window.ethereum)
    this.clientAddr = (await this.web3.eth.getAccounts())[0]
    this.web3.eth.defaultAccount = this.clientAddr
    this.token = new this.web3.eth.Contract(SBT, this.SBTAddress)
  },
  methods: {
    async check() {
      var returnNumber = await this.token.methods.getAccountNumber(this.clientAddr).call()
      if (returnNumber != 0 && returnNumber == this.number) {
        this.successModalStatus = true
        this.msg = '驗證成功！'
      } else {
        this.warningModalStatus = true
        this.msg = '連接失敗，這並不是你的 SBT number'
      }
    },
    async mint() {
      this.isWaiting = true
      try {
        var result = await this.token.methods.mint(this.clientAddr).send({ from: this.clientAddr })
        this.successModalStatus = true
        var returnNumber = await this.token.methods.getAccountNumber(this.clientAddr).call()
        this.msg = 'mint 成功！ <a href="https://sepolia.etherscan.io/tx/' + result.transactionHash + '">etherscan</a><br>您的 SBT number 是 ' + returnNumber
      } catch (error) {
        this.warningModalStatus = true
        this.msg = 'mint 失敗，您可能已經持有 SBT，請在左方輸入 SBT number 進行驗證'
      }
      this.isWaiting = false
    }
  }
}

</script>

<template>
  <section class="blog-posts">
    <div class="container">
      <div class="block">
        <PageTitle title="Set up Soulbound Token(SBT)" subtitle="Mint SBT 紀錄個人信用並作為身份驗證憑證"></PageTitle>
      </div>
      <div class="block">
        <div class="columns">
          <div class="column is-6">
            <div class="box is-fullwidth">
              <div class="block">
                <h1 class="title is-4">您已經擁有 SBT</h1>
              </div>
              <div class="block">
                請輸入您的 SBT 相關資訊
              </div>
              <div class="block">
                <div class="field">
                  <label class="label">SBT address</label>
                  <div class="control">
                    <input class="input is-info is-rounded" type="text" :value="SBTAddress" disabled>
                  </div>
                </div>
                <div class="field">
                  <label class="label">Username</label>
                  <div class="control has-icons-left has-icons-right">
                    <input class="input is-info is-rounded" type="number" placeholder="Token number" v-model="number">
                    <span class="icon is-small is-left">
                      <i class="fas fa-user"></i>
                    </span>
                    <span class="icon is-small is-right">
                      <!-- <i class="fas fa-check"></i> -->
                    </span>
                  </div>
                  <!-- <p class="help is-success">This username is available</p> -->
                </div>
                <div class="column is-2 is-offset-5">
                  <button class="button is-info is-outlined" @click="check">驗證</button>
                </div>
              </div>
            </div>
          </div>
          <div class="column is-6">
            <div class="box is-fullwidth">
              <div class="block">
                <h1 class="title is-4">您還沒有 SBT</h1>
              </div>
              <div class="block">
                向下方 SBT 智能合約地址請求 Mint 一個 Soulbound Token 到你的地址

              </div>
              <div class="block">
                <div class="field">
                  <label class="label">SBT address</label>
                  <div class="control">
                    <input class="input is-info is-rounded" type="text" :value="SBTAddress" disabled>
                  </div>
                </div>
                <div class="column is-2 is-offset-5">
                  <template v-if="!isWaiting">
                    <button class="button is-info is-outlined" @click="mint">MINT</button>
                  </template>
                  <template v-else>
                    <button class="button is-info is-outlined is-loading"></button>
                  </template>
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
    link="/signup/credit" btnName="繼續"></SuccessModal>
</template>
