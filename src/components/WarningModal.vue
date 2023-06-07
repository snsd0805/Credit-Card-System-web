<script>
export default {
  name: 'WarningModal',
  props: ['active', 'errorMsg'],
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
        <p class="modal-card-title">Warning</p>
        <button class="delete" aria-label="close" @click="$emit('closeModal')"></button>
      </header>
      <section class="modal-card-body">
        <!-- Content ... -->
        <p>{{ errorMsg }}</p>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-danger" @click="$emit('closeModal')">OK</button>
      </footer>
    </div>
  </div>
</template>
