<template>
  <div id="app">
    <navbar></navbar>
    <router-view/>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar'

export default {
  name: 'Sigma',
  components: { Navbar }
}
</script>

<style lang="scss">
@import './styles/theme.scss';
@import '../node_modules/bootstrap/scss/bootstrap.scss';
</style>
