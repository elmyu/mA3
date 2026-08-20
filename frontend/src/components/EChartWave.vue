<template>
  <div ref="chartRef" class="wave-chart"></div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  values: { type: Array, default: () => [] },
  sampleRate: { type: Number, default: 250 },
})

const chartRef = ref(null)
let chart = null

function render() {
  if (!chart) return
  chart.setOption({
    animation: false,
    grid: { left: 44, right: 16, top: 16, bottom: 30 },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      name: '时间(s)',
      data: props.values.map((_, i) => (i / props.sampleRate).toFixed(2)),
    },
    yAxis: { type: 'value', name: '幅值(mV)' },
    series: [
      {
        type: 'line',
        data: props.values,
        showSymbol: false,
        lineStyle: { color: '#16a34a', width: 1.5 },
      },
    ],
  })
}

onMounted(() => {
  chart = echarts.init(chartRef.value)
  render()
})

watch(() => props.values, render)

onBeforeUnmount(() => {
  chart?.dispose()
})
</script>

<style scoped>
.wave-chart {
  width: 100%;
  height: 320px;
}
</style>
