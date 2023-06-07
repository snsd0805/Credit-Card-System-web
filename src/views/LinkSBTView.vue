<script>
import PageTitle from '../components/PageTitle.vue'
// import detectEthereumProvider from '@metamask/detect-provider'
import WarningModal from '../components/WarningModal.vue'
import SuccessModal from '../components/SuccessModal.vue'
// import { useClientStore } from '../stores/Client.js'

export default {
  components: { PageTitle, WarningModal, SuccessModal },
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
                    <input class="input is-info is-rounded" type="text" value="0x92E72Cc93e465810814F60957e08a8C8D1762Eb6" disabled>
                  </div>
                </div>
                <div class="field">
                  <label class="label">Username</label>
                  <div class="control has-icons-left has-icons-right">
                    <input class="input is-info is-rounded" type="text" placeholder="Text input" value="bulma">
                    <span class="icon is-small is-left">
                      <i class="fas fa-user"></i>
                    </span>
                    <span class="icon is-small is-right">
                      <i class="fas fa-check"></i>
                    </span>
                  </div>
                  <!-- <p class="help is-success">This username is available</p> -->
                </div>
                <div class="column is-2 is-offset-5">
                  <button class="button is-info is-outlined">驗證</button>
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
              確認後會向下方 SBT 智能合約地址請求 Mint 一個 Soulbound Token 到你的地址

            </div>
            <div class="block">
                <div class="field">
                  <label class="label">SBT address</label>
                  <div class="control">
                    <input class="input is-info is-rounded" type="text" value="0x92E72Cc93e465810814F60957e08a8C8D1762Eb6" disabled>
                  </div>
                </div>
                <div class="column is-2 is-offset-5">
                  <button class="button is-info is-outlined">MINT</button>
                </div>

              </div>
          </div>
        </div>
      </div>
      </div>
      <!-- <div class="block">
            <div class="columns">

              <div class="column is-2 is-offset-4">
                <button @click="detect" class="button is-primary is-fullwidth is-medium is-outlined">Link to MetaMask</button>
              </div>
              <div class="column is-2">
                <RouterLink to="/" class="button is-danger is-fullwidth is-medium is-outlined">Cancel</RouterLink>
              </div>
            </div>
          </div> -->
    </div>
  </section>
  <WarningModal :active="warningModalStatus" :errorMsg="msg" @closeModal="warningModalStatus = false"></WarningModal>
  <SuccessModal :active="successModalStatus" :successMsg="msg" @closeModal="successModalStatus = false"
    link="/signup/linksbt" btnName="繼續"></SuccessModal>
</template>
