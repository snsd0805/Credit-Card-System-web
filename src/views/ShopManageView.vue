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
      clientAddr: '',
      warningModalStatus: false,
      successModalStatus: false,
      web3: null,
      msg: '',
      isWaiting: false,
      products: {},
      name: "",
      price: 0.01,
      code: "",
    }
  },
  async mounted() {
    this.web3 = new Web3(window.ethereum)
    this.clientAddr = this.$cookies.get('address')
    this.update()
  },
  methods: {
    async update() {
      var result = await fetch(import.meta.env.VITE_BACKEND_PREFIX + "/shop/" + this.clientAddr + "/products")
      var data = await result.json()
      for (let product in data['products']) {
        this.products[product] = data['products'][product]
      }

    },
    onScanSuccess(decodedText, decodedResult) {
      // handle the scanned code as you like, for example:
      console.log(`Code matched = ${decodedText}`, decodedResult);
      this.code = decodedText
      this.scanner.clear()
    },
    scan() {
      this.scanner = new Html5QrcodeScanner(
        "reader",
        { fps: 10, qrbox: { width: 400, height: 400 } },
        /* verbose= */ false);
      this.scanner.render(this.onScanSuccess);
    },
    async send() {
      try {
        await fetch(import.meta.env.VITE_BACKEND_PREFIX + "/shop/" + this.clientAddr + "/products", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            'product': {
              'name': this.name,
              'code': this.code,
              'price': this.web3.utils.toWei(this.price.toString())
            }
          })
        })
        this.name = ''
        this.code = ''
        this.price = 0.01
        this.msg = "新增成功"
        this.successModalStatus = true
      } catch (error) {
        this.msg = "新增失敗"
        this.warningModalStatus = true
      }
      this.update()
    }
  }
}
</script>

<template>
  <section class="blog-posts">
    <div class="container">
      <div class="columns">
        <div class="column is-2">
          <ClientNav path="shopproducts"></ClientNav>
          <ShopNav path="shopproducts"></ShopNav>
        </div>
        <div class="column">
          <div class="container">
            <div class="block">
              <PageTitle title="商品管理" subtitle="加入新商品"></PageTitle>
            </div>
            <div class="block">
              <div id="reader" width="200px"></div>
            </div>
            <div class="block">
              <article class="message is-info">
                <div class="message-header">
                  <p>新增商品</p>
                  <button class="delete" aria-label="delete"></button>
                </div>
                <div class="message-body">
                  <div class="field is-horizontal">
                    <div class="field-label is-normal">
                      <label class="label">名稱</label>
                    </div>
                    <div class="field-body">
                      <div class="field">
                        <p class="control">
                          <input class="input" type="text" v-model="name">
                        </p>
                      </div>
                    </div>
                    <div class="field-label is-normal">
                      <label class="label"></label>
                    </div>
                  </div>
                  <div class="field is-horizontal">
                    <div class="field-label is-normal">
                      <label class="label">價格</label>
                    </div>
                    <div class="field-body">
                      <div class="field">
                        <p class="control">
                          <input class="input" type="number" v-model="price">
                        </p>
                      </div>
                    </div>
                    <div class="field-label is-normal">
                      <label class="label">ETH</label>
                    </div>
                  </div>
                  <div class="field is-horizontal">
                    <div class="field-label is-normal">
                      <label class="label">條碼</label>
                    </div>
                    <div class="field-body">
                      <div class="field">
                        <p class="control">
                          <input class="input" type="text" placeholder="手打 or 使用鏡頭掃描商品條碼" v-model="code">
                        </p>
                      </div>
                    </div>
                    <div class="field-label is-normal">
                      <button class="button is-success is-outlined" @click="scan">掃描</button>
                    </div>
                  </div>
                  <div class="column is-2 is-offset-5">
                    <button class="button is-info is-outlined is-large" @click="send">新增</button>
                  </div>
                </div>
              </article>
            </div>

            <div class="block">
              <table class="table is-fullwidth">
                <thead>
                  <tr>
                    <th colspan="3" style="text-align: center;"><strong>商品清單</strong></th>
                  </tr>
                  <tr>
                    <th>商品名稱</th>
                    <th>價格</th>
                    <th>條碼編號</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(product, index) in products">
                    <tr>
                      <td>{{ product['name'] }}</td>
                      <td>{{ this.web3.utils.fromWei(product['price']) }} ETH</td>
                      <td>{{ index }} </td>
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
    :link="`/shop/manage`" btnName="繼續"></SuccessModal>
</template>
