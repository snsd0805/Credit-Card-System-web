<script>
import Web3 from 'web3';
import SBT from '@/assets/SBT.json'
import PageTitle from '../components/PageTitle.vue'
import ClientNav from '../components/ClientNav.vue'
import ShopNav from '../components/ShopNav.vue'

export default {
  components: { PageTitle, ClientNav, ShopNav },
  data() {
    return {
      SBTAddress: import.meta.env.VITE_SBT_ADDR,
      clientAddr: '',
      web3: null,
      token: null,
      log: [],
    }
  },
  async mounted() {
    this.web3 = new Web3(window.ethereum)
    this.clientAddr = this.$cookies.get('address')
    this.web3.eth.defaultAccount = this.clientAddr
    this.token = new this.web3.eth.Contract(SBT, this.SBTAddress)

    var borrow = await this.token.getPastEvents("Borrow", { fromBlock: 0, toBlock: 'latest', filter: { shop: this.clientAddr } })
    console.log(borrow)
    for (let i of borrow) {
      let result = i.returnValues
      let obj = {
        bank: result['bank'],
        shop: result['shop'],
        client: result['client'],
        id: result['id'],
        amount: this.web3.utils.fromWei(result['amount'], 'ether'),
      }
      this.log.push(obj)
    }
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
          <ClientNav path="shoplog"></ClientNav>
          <template v-if="this.$cookies.get('isShop') == 'true'">
            <ShopNav path="shoplog"></ShopNav>
          </template>

        </div>
        <div class="column">
          <div class="container">
            <div class="block">
              <PageTitle title="店家收款紀錄" subtitle="查詢客戶付款狀況"></PageTitle>
            </div>
            <div class="block">
              <h1 class="title is-4">收款紀錄</h1>
              <table class="table is-fullwidth is-striped is-hoverable">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>客戶</th>
                    <th>銀行</th>
                    <th>帳款編號</th>
                    <th>金額</th>
                    <th>詳細訂單狀況</th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(value, index) of log">
                    <tr>
                      <th>{{ index }}</th>
                      <td>{{ value.client }}</td>
                      <td>{{ value.bank }}</td>
                      <td>#{{ value.id }}</td>
                      <td>{{ value.amount }} ETH</td>
                      <td><RouterLink :to="'/order/'+value.id" class="button is-info is-outlined">查詢</RouterLink></td>
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
</template>
