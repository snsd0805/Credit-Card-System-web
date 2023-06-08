<script>
import Web3 from 'web3';
import SBT from '@/assets/SBT.json'
import WarningModal from '../components/WarningModal.vue'
import SuccessModal from '../components/SuccessModal.vue'
import { useClientStore } from '../stores/Client.js'


export default {
  components: { WarningModal, SuccessModal },
  name: 'PageFooter',
  data () {
    return {
      SBTAddress: import.meta.env.VITE_SBT_ADDR,
      number: '',
      warningModalStatus: false,
      successModalStatus: false,
      msg: '',
    }
  },
  methods: {
    async check () {
      console.log(this.SBTAddress)
      const web3 = new Web3(window.ethereum)
      const clientAddr = (await web3.eth.getAccounts())[0]
      var token = new web3.eth.Contract(SBT, this.SBTAddress)
      var returnNumber = await token.methods.getAccountNumber(clientAddr).call()
      if (returnNumber != 0 && returnNumber == number) {
        this.successModalStatus = true
        this.msg = 'Success: '+returnNumber
      } else {
        this.warningModalStatus = true
        this.msg = 'Fail: '+returnNumber
      }
    }
  }
}

</script>

<template>
<button class='button is-info is-large'>mint</button>
<hr>
<form>
  number: <input type='text' v-model='number'>
  <input type='submit' class='button is-success'>
</form>
<button class='button is-info is-large' @click='check'>check</button>

<WarningModal :active="warningModalStatus" :errorMsg="msg" @closeModal="warningModalStatus=false"></WarningModal>
<SuccessModal :active="successModalStatus" :successMsg="msg" @closeModal="successModalStatus=false" link="/signup/linksbt" btnName="繼續"></SuccessModal>

</template>
