<template>
  <div v-html="svg" @click="$emit('click')"></div>
</template>

<script>
import feather from 'feather-icons'

export default {
  name: 'Icon',
  props: ['name', 'color', 'size'],
  data () {
    return {
      svg: ''
    }
  },
  mounted () {
    this.svg = feather.icons[this.name].toSvg({
      color: this.color,
      width: this.size,
      height: this.size
    })
  }
}
</script>
