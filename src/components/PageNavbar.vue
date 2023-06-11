<script>
import detectEthereumProvider from '@metamask/detect-provider'
import WarningModal from '../components/WarningModal.vue'
import SuccessModal from '../components/SuccessModal.vue'
import Web3 from 'web3'
import Bank from '@/assets/Bank.json'

export default {
  components: { WarningModal, SuccessModal },
  name: 'PageNavbar',
  data() {
    return {
      BankAddress: import.meta.env.VITE_BANK_ADDR,
      linked: false,
      address: '',
      msg:'',
      successModalStatus: false,
      warningModalStatus: false,
      web3: null,
    }
  },
  mounted() {
    console.log(this.$cookies.isKey('linked'))
    if (!this.$cookies.isKey('linked')) {
      this.linked = false
    } else {
      this.linked = true
      this.address = this.$cookies.get('address')
    }
  },
  methods: {
    async login() {
      const provider = await detectEthereumProvider()
      if (provider) {
        const chainId = await window.ethereum.request({ method: 'eth_chainId' })
        console.log(chainId)
        if (chainId == import.meta.env.VITE_CHAIN_ID) {
          const account = await window.ethereum.request({ method: 'eth_requestAccounts' })

          // check from bank
          this.web3 = new Web3(window.ethereum)
          var token = new this.web3.eth.Contract(Bank, this.BankAddress)
          var clientAddr = (await this.web3.eth.getAccounts())[0]
          this.web3.eth.defaultAccount = clientAddr
          var returnNumber = await token.methods.getSBTNumber(clientAddr).call({from: clientAddr})
          if (returnNumber != 0){
            var result = await fetch(import.meta.env.VITE_BACKEND_PREFIX+"/shop/check", {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({'address': clientAddr})
            })
            var result = await result.json()
            this.$cookies.set('isShop', result.status)
            this.$cookies.set('address', clientAddr)
            this.$cookies.set('linked', true)
            this.$cookies.set('SBTNumber', returnNumber)
            this.linked = true
            this.address = this.$cookies.get('address')
            this.msg = '成功連接 MetaMask'
            this.successModalStatus = true
          } else {
            this.msg = '您可能還沒有註冊過！'
            this.warningModalStatus = true
          }
        } else {
          this.msg = '你連接的不是 Sepolia 測試網路，目前只接受 Sepolia address'
          this.warningModalStatus = true
        }
      } else {
        this.msg = 'no Metamask'
        this.warningModalStatus = true
      }
    },
    logout () {
      console.log('logout')
      this.linked = false
      this.address = ''
      this.$cookies.remove('linked')
      this.$cookies.remove('address')
      this.$cookies.remove('SBTNumber')
      this.$cookies.remove('shop')
      this.$router.push('/')
    }
  }
}

</script>

<template>
  <section class="hero is-large">
    <div class="hero-head">
      <div class="container">
        <nav class="navbar" role="navigation" aria-label="main navigation">
          <div class="navbar-brand">
            <a class="navbar-item" href="https://bulma.io">
              <img src="@/assets/NCNU_Bank.png" width="112" height="28">
            </a>

            <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false"
              data-target="navbarBasicExample">
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
            </a>
          </div>

          <div id="navbarBasicExample" class="navbar-menu">
            <div class="navbar-start">
              <RouterLink to="/" class="navbar-item">Home</RouterLink>
              <RouterLink to="/document" class="navbar-item">Documentation</RouterLink>
            </div>

            <div class="navbar-end">
              <div class="navbar-item">
                <template v-if="!linked">
                  <div class="buttons">
                    <RouterLink to="/signup" class="button is-primary is-outlined">Sign up</RouterLink>
                    <a class="button is-info is-outlined" @click="login">Log in</a>
                  </div>
                </template>
                <template v-else>
                  <RouterLink to="/client" class="button is-info is-outlined is-small is-rounded">{{ 'Hello! ' + address }}</RouterLink>
                  <button class="button is-danger is-outlined is-small is-rounded" @click="logout">登出</button>
                </template>
              </div>
            </div>
          </div>
        </nav>
      </div>
    </div>
  </section>
  <WarningModal :active="warningModalStatus" :errorMsg="msg" @closeModal="warningModalStatus=false"></WarningModal>
  <SuccessModal :active="successModalStatus" :successMsg="msg" @closeModal="successModalStatus=false" link="/client" btnName="繼續"></SuccessModal>

</template>
