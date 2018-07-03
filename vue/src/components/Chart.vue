<template>
  <div class="panel rounded-bottom">
    <chart-base
      :chart-data="transformedData"
      :options="chartOptions"
      :width="100"
      :height="50"
    />
  </div>
</template>

<script>
import ChartBase from '@/components/ChartBase'

export default {
  name: 'Overview',
  components: { ChartBase },
  props: ['chartData', 'symbol'],
  computed: {
    transformedData () {
      const decimals = this.symbol === 'XRP' ? 6 : 2
      return {
        labels: this.chartData,
        datasets: [
          {
            data: this.chartData.map(x => x.toFixed(decimals)),
            borderWidth: 2,
            borderColor: 'rgba(0, 188, 212, 1)',
            backgroundColor: 'rgba(0, 188, 212, 0.2)',
            pointBackgroundColor: 'rgba(0, 0, 0, 0)',
            pointBorderColor: 'rgba(0, 0, 0, 0)',
            pointHoverBackgroundColor: 'rgba(0, 188, 212, 1)',
            pointHoverRadius: 3
          }
        ]
      }
    },
    chartOptions () {
      return {
        events: ['mousemove', 'mouseout', 'touchmove', 'touchend'],
        animation: {
          duration: 0,
          easing: 'easeOutQuart'
        },
        responsive: true,
        maintainAspectRatio: true,
        hover: { intersect: false },
        tooltips: {
          intersect: false,
          mode: 'index',
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          caretSize: 0,
          cornerRadius: 3,
          displayColors: false,
          caretPadding: 20,
          callbacks: {
            label: (tooltipItem, data) => {
              const value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]
              return 'Close: ' + value
            },
            title: () => ''
          }
        },
        legend: { display: false },
        scales: {
          yAxes: [{ gridLines: { display: false, drawTicks: false }, ticks: { display: false } }],
          xAxes: [{ gridLines: { display: false, drawTicks: false }, ticks: { display: false } }]
        }
      }
    }
  }
}
</script>
