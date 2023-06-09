<script>
export default {
  name: 'PageNavbar',
  data() {
    return {
      linked: false,
      address: '',
      msg: "HELLO"
    }
  },
  mounted() {
    console.log(this.$cookies.isKey('linked'))
    if (!this.$cookies.isKey('linked')) {
      this.linked = false
    } else {
      this.linked = true
      this.address = this.$cookies.get('address')
      console.log(this.address)
      console.log("Addr: "+this.address)
    }
  }
}

</script>

<template>
  <section class="hero is-large">
    <div class="hero-head">
      <div class="container">
        <nav class="navbar" role="navigation" aria-label="main navigation">
          <div class="navbar-brand">
            <a class="navbar-item" href="https://bulma.io">
              <img src="@/assets/NCNU_Bank.png" width="112" height="28">
            </a>

            <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false"
              data-target="navbarBasicExample">
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
            </a>
          </div>

          <div id="navbarBasicExample" class="navbar-menu">
            <div class="navbar-start">
              <RouterLink to="/" class="navbar-item">Home</RouterLink>
              <RouterLink to="/document" class="navbar-item">Documentation</RouterLink>
            </div>

            <div class="navbar-end">
              <div class="navbar-item">
                <template v-if="!linked">
                  <div class="buttons">
                    <RouterLink to="/signup" class="button is-primary is-outlined">Sign up</RouterLink>
                    <RouterLink to="/login" class="button is-info is-outlined">Log in</RouterLink>
                  </div>
                </template>
                <template v-else>
                  <button class="button is-info is-outlined is-small is-rounded">{{ 'Hello! ' + address }}</button>
                </template>
              </div>
            </div>
          </div>
        </nav>
      </div>
    </div>
  </section>
</template>
