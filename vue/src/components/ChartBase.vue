<script>
import { Line, mixins } from 'vue-chartjs'

export default {
  name: 'ChartBase',
  extends: Line,
  mixins: [mixins.reactiveProp],
  props: ['chartData', 'options'],
  mounted () {
    const self = this
    this.addPlugin({
      id: 'vertical-line',
      afterDraw: function (chart) {
        if (chart.tooltip._active && chart.tooltip._active.length) {
          const activePoint = chart.tooltip._active[0]
          const ctx = chart.ctx
          const x = activePoint.tooltipPosition().x
          ctx.save()
          ctx.beginPath()
          ctx.moveTo(x, chart.scales['y-axis-0'].top)
          ctx.lineTo(x, chart.scales['y-axis-0'].bottom)
          ctx.lineWidth = 2
          ctx.strokeStyle = self.$store.getters.getColors.$blue
          ctx.stroke()
          ctx.restore()
        }
      }
    })
    this.renderChart(this.chartData, this.options)
  }
}
</script>
