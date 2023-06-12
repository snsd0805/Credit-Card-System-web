<script>
export default {
  name: 'ClientNav',
  props: ['path'],
  mounted() {
    if (this.path in this.navCSS) {
      this.navCSS[this.path] += ' is-active'
    }
  },
  data() {
    return {
      navCSS: {
        main: 'panel-block',
        pay: 'panel-block',
        credit: 'panel-block',
        info: 'panel-block',
        log: 'panel-block'
      }
    }
  }
}

</script>

<template>
  <nav class="panel">
    <p class="panel-heading">
      使用者選項
    </p>
    <RouterLink to="/client" :class="this.navCSS['main']">
      <span class="panel-icon">
        <i class="fas fa-book" aria-hidden="true"></i>
      </span>
      <template v-if="this.path == 'main'">
        <strong>主選單</strong>
      </template>
      <template v-else>
        <p>主選單</p>
      </template>
    </RouterLink>
    <RouterLink to="/client/info" :class="this.navCSS['info']">
      <span class="panel-icon">
        <i class="fas fa-book" aria-hidden="true"></i>
      </span>
      <template v-if="this.path == 'info'">
        <strong>個人資料</strong>
      </template>
      <template v-else>
        <p>個人資料</p>
      </template>
    </RouterLink>
    <RouterLink to="/client/pay" :class="this.navCSS['pay']">
      <span class="panel-icon">
        <i class="fas fa-book" aria-hidden="true"></i>
      </span>
      <template v-if="this.path == 'pay'">
        <strong>掃描支付</strong>
      </template>
      <template v-else>
        <p>掃描支付</p>
      </template>
    </RouterLink>
    <RouterLink to="/client/log" :class="this.navCSS['log']">
      <span class="panel-icon">
        <i class="fas fa-book" aria-hidden="true"></i>
      </span>
      <template v-if="this.path == 'log'">
        <strong>借款紀錄</strong>
      </template>
      <template v-else>
        <p>借款紀錄</p>
      </template>
    </RouterLink>
    <RouterLink to="/client/credit" :class="this.navCSS['credit']">
      <span class="panel-icon">
        <i class="fas fa-book" aria-hidden="true"></i>
      </span>
      <template v-if="this.path == 'credit'">
        <strong>SBT信用紀錄</strong>
      </template>
      <template v-else>
        <p>SBT信用紀錄</p>
      </template>
    </RouterLink>
  </nav>
</template>
