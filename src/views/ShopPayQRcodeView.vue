<script>
import PageTitle from '../components/PageTitle.vue'
import ClientNav from '../components/ClientNav.vue'
import ShopNav from '../components/ShopNav.vue'
import QRCode from 'qrcode';

export default {
  components: { PageTitle, ClientNav, ShopNav },
  data() {
    return {
      size: 300,
      value: "www.google.com"
    }
  },
  async mounted() {
    const qrcodeCanvas = this.$refs.qrcodeCanvas;
    const qrCodeUrl = import.meta.env.VITE_FRONTEND_PREFIX+"/client/pay/"+this.$route.params.id

    QRCode.toCanvas(qrcodeCanvas, qrCodeUrl, (error) => {
      if (error) {
        console.error(error);
      }
    });
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
          <ClientNav path="shoppay"></ClientNav>
          <ShopNav path="shoppay"></ShopNav>
        </div>
        <div class="column">
          <div class="container">
            <div class="block">
              <PageTitle title="店家收款 QRcode" subtitle="提供顧客掃描以進行支付"></PageTitle>
            </div>
            <div class="block">
              <canvas id="canvas" ref="qrcodeCanvas"></canvas>
            </div>
            <div class="block">
              <RouterLink to="/shop/pay" class="button is-info is-outlined is-large" @click="send">繼續下一訂單</RouterLink>
            </div>
          </div>

        </div>
      </div>
    </div>
  </section>
</template>
