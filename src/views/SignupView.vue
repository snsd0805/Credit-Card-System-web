<script>
import PageTitle from '../components/PageTitle.vue'
import detectEthereumProvider from '@metamask/detect-provider'
import WarningModal from '../components/WarningModal.vue'
import SuccessModal from '../components/SuccessModal.vue'
import { useClientStore } from '../stores/Client.js'

export default {
  components: { PageTitle, WarningModal, SuccessModal },
  data () {
    return {
      warningModalStatus: false,
      successModalStatus: false,
      msg: '',
      client: useClientStore()
    }
  },
  methods: {
    async detect () {
      const provider = await detectEthereumProvider()
      if (provider) {
        const chainId = await window.ethereum.request({ method: 'eth_chainId' })
        console.log(chainId)
        if (chainId == import.meta.env.VITE_CHAIN_ID) {
          const account = await window.ethereum.request({ method: 'eth_requestAccounts' })
          this.client.address = account[0]
          this.client.linked = true
          this.msg = 'Success: 已經成功連接 MetaMask，繼續完成 Soulbound Token 設定'
          this.successModalStatus = true
        } else {
          this.msg = 'ERROR: 你連接的不是 Sepolia 測試網路，目前只接受 Sepolia address'
          this.warningModalStatus = true
        }
      } else {
        this.msg = 'ERROR: no Metamask'
        this.warningModalStatus = true
      }
    }
  }
}
</script>

<template>
  <section class="blog-posts">
    <div class="container">
      <div class="block">
        <PageTitle title="Sign Up" subtitle="連接 MetaMask 錢包並使用 Soulbound Token (SBT) 進行身份驗證"></PageTitle>
      </div>
      <div class="block">
        <div class="box">
          <div class="content">
            <h5 class="title is-5">流程說明</h5>
            <ol>
              <li>連接 MetaMask 個人錢包</li>
              <li>Mint 新的或連接已有的 Soulbound Token(SBT) 以紀錄個人信用並作為身份驗證憑證</li>
              <li>申請信用評分並設定信用額度</li>
              <li>進行消費</li>
            </ol>
          </div>
        </div>
      </div>
      <div class="block">
        <div class="columns">

          <div class="column is-2 is-offset-4">
            <button @click="detect" class="button is-primary is-fullwidth is-medium is-outlined">Link to MetaMask</button>
          </div>
          <div class="column is-2">
            <RouterLink to="/" class="button is-danger is-fullwidth is-medium is-outlined">Cancel</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </section>
  <WarningModal :active="warningModalStatus" :errorMsg="msg" @closeModal="warningModalStatus=false"></WarningModal>
  <SuccessModal :active="successModalStatus" :successMsg="msg" @closeModal="successModalStatus=false" link="/signup/linksbt" btnName="繼續"></SuccessModal>
</template>
