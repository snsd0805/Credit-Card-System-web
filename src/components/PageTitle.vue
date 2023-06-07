<script>
export default {
  name: 'PageTitle',
  props: [
    'title', 'subtitle'
  ]
}
</script>

<template>
  <div class="block">
    <h1 class="title is-1">{{  title }}</h1>
    <h1 class="subtitle is-6">{{ subtitle }}</h1>
  </div>
</template>
