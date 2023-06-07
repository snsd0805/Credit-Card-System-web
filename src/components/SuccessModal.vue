<script>
export default {
  name: 'SuccessModal',
  props: ['active', 'successMsg', 'link', 'btnName'],
  computed: {
    modalStatus () {
      if (this.active) {
        return 'modal is-active'
      } else {
        return 'modal'
      }
    }
  }
}
</script>

<template>
  <div :class="modalStatus">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Success</p>
        <button class="delete" aria-label="close" @click="$emit('closeModal')"></button>
      </header>
      <section class="modal-card-body">
        <!-- Content ... -->
        <p>{{ successMsg }}</p>
      </section>
      <footer class="modal-card-foot">
        <RouterLink :to="link" class="button is-success" @click="$emit('closeModal')">{{ btnName }}</RouterLink>
        <button class="button" @click="$emit('closeModal')">Cancel</button>
      </footer>
    </div>
  </div>
</template>
