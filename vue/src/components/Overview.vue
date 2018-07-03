<template>
  <div class="container mb-4">
    <div class="row justify-content-center">
      <div class="col-12 col-lg-6 mb-4" v-for="(tick, index) in $store.getters.getTicks" :key="index">
        <div class="panel rounded-top container pt-4 px-4" v-if="tick.data.length">
          <div class="row">
            <div class="col-12 d-flex flex-row justify-content-start align-items-center mb-3">
              <icon
                class="icon"
                name="activity"
                size="20"
                v-bind:color="$store.getters.getColors.$cyan"
              ></icon>
              <h4 class="mb-0 ml-2">{{ tick.symbol }}</h4>
              <h4 class="ml-auto mb-0 d-flex flex-row align-items-center">
                <span class="small">$</span>
                <span>{{ price(tick) }}</span>
              </h4>
            </div>
            <div class="col-12 d-flex flex-row justify-content-start align-items-center">
              <div class="font-weight-bold" v-bind:class="percentageClass(tick)">
                {{ percentage(tick) }}<span class="small">%</span>
              </div>
              <hr class="my-0 ml-3"/>
            </div>
          </div>
        </div>
        <chart :chart-data="tick.data" :symbol="tick.symbol"/>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from '@/components/Chart'
import Icon from '@/components/Icon'

export default {
  name: 'Overview',
  components: { Chart, Icon },
  mounted () {
    this.$api.getTicks()
    setInterval(() => {
      this.$api.getTicks()
    }, 30000)
  },
  methods: {
    price (tick) {
      const decimals = tick.symbol === 'XRP' ? 6 : 2
      return tick.data[tick.data.length - 1].toFixed(decimals)
    },
    percentage (tick) {
      const last = tick.data[tick.data.length - 1]
      const first = tick.data[0]
      const result = (last - first) * 100 / last
      return (result > 0) ? '+' + result.toFixed(2) : result.toFixed(2)
    },
    percentageClass (tick) {
      return {
        'text-success': this.percentage(tick) >= 0,
        'text-danger': this.percentage(tick) < 0
      }
    }
  }
}
</script>
