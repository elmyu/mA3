<template>
  <div class="card">
    <h2 class="page-title">我的健康档案</h2>
    <div class="toolbar">
      <CsvUpload @success="load" />
    </div>
    <el-table :data="records" v-loading="loading" stripe>
      <el-table-column prop="id" label="记录ID" width="90" />
      <el-table-column prop="signal_type" label="信号类型" width="110" />
      <el-table-column prop="sample_rate" label="采样率(Hz)" width="110" />
      <el-table-column prop="recorded_at" label="记录时间" />
      <el-table-column prop="file_path" label="数据文件" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button size="small" type="primary" plain @click="openDetail(row)">查看波形</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="dialogVisible" title="波形详情" width="720px">
      <template v-if="current">
        <el-descriptions :column="3" border>
          <el-descriptions-item label="信号类型">{{ current.signal_type }}</el-descriptions-item>
          <el-descriptions-item label="采样率">{{ current.sample_rate }} Hz</el-descriptions-item>
          <el-descriptions-item label="记录时间">{{ current.recorded_at }}</el-descriptions-item>
        </el-descriptions>
        <EChartWave :values="current.values || []" :sample-rate="current.sample_rate" />
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import CsvUpload from '../components/CsvUpload.vue'
import EChartWave from '../components/EChartWave.vue'
import { getMySignals, getWaveform } from '../api/signals'

const records = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const current = ref(null)

async function load() {
  loading.value = true
  try {
    const res = await getMySignals()
    records.value = res.data
  } finally {
    loading.value = false
  }
}

async function openDetail(row) {
  const res = await getWaveform(row.id)
  current.value = res.data
  dialogVisible.value = true
}

onMounted(load)
</script>
