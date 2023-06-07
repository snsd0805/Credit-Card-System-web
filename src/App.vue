<script setup>
import { RouterView } from 'vue-router'
import PageNavbar from './components/PageNavbar.vue'
import PageFooter from './components/PageFooter.vue'
</script>

<template>
  <!-- Navbar  -->
  <PageNavbar></PageNavbar>

  <!-- body  -->
  <body>
    <RouterView />
  </body>

  <!-- footer -->
  <PageFooter></PageFooter>
</template>
