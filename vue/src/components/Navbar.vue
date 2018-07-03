<template>
  <nav class="navbar navbar-dark bg-dark mb-4">
    <router-link to="/" class="navbar-brand mr-0">
      <img class="logo" src="../assets/sigma.png" alt="">
    </router-link>
    <div class="btn-group frequency" role="group">
      <button
        type="button"
        class="btn btn-light d-flex justify-content-center align-items-center frequency-icon"
        v-if="$store.getters.getToken"
      >
        <icon class="icon" name="repeat" size="16"></icon>
      </button>
      <template v-for="(scale, index) in scales">
        <button
          :key="index"
          type="button"
          class="btn btn-light"
          v-if="$store.getters.getToken"
          v-bind:class="{ 'active' : scale === $store.getters.getScale }"
          @click="setScale(index)"
        >{{ scale }}</button>
      </template>
    </div>
    <icon
      class="icon pointer"
      name="log-out"
      size="20"
      v-bind:color="$store.getters.getColors.$cyan"
      @click="$api.logout()"
      v-if="$store.getters.getToken"
    ></icon>
  </nav>
</template>

<script>
import Icon from '@/components/Icon'

export default {
  name: 'Navbar',
  components: { Icon },
  data: () => {
    return {
      scales: ['1h', '6h', '24h', '72h']
    }
  },
  methods: {
    setScale (index) {
      this.$store.dispatch('setScale', this.scales[index]).then(() => {
        this.$api.getTicks()
      })
    }
  }
}
</script>
