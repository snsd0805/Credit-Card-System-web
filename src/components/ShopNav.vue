<script>
export default {
  name: 'ShopNav',
  props: ['path'],
  mounted() {
    if (this.path in this.navCSS) {
      this.navCSS[this.path] += ' is-active'
    }
  },
  data() {
    return {
      navCSS: {
        shoppay: 'panel-block',
        shoplog: 'panel-block',
        shopproducts: 'panel-block',
      }
    }
  }
}

</script>

<template>
  <nav class="panel">
    <p class="panel-heading">
      店家選項
    </p>
    <RouterLink to="/shop/pay" :class="this.navCSS['shoppay']">
      <span class="panel-icon">
        <i class="fas fa-book" aria-hidden="true"></i>
      </span>
      <template v-if="this.path == 'shoppay'">
        <strong>店家結帳</strong>
      </template>
      <template v-else>
        <p>店家結帳</p>
      </template>
    </RouterLink>
    <RouterLink to="/shop/log" :class="this.navCSS['shoplog']">
      <span class="panel-icon">
        <i class="fas fa-book" aria-hidden="true"></i>
      </span>
      <template v-if="this.path == 'shoplog'">
        <strong>店家收款紀錄</strong>
      </template>
      <template v-else>
        <p>店家收款紀錄</p>
      </template>
    </RouterLink>
    <RouterLink to="/shop/products" :class="this.navCSS['shopproducts']">
      <span class="panel-icon">
        <i class="fas fa-book" aria-hidden="true"></i>
      </span>
      <template v-if="this.path == 'shopproducts'">
        <strong>店家商品管理</strong>
      </template>
      <template v-else>
        <p>店家商品管理</p>
      </template>
    </RouterLink>
  </nav>
</template>
