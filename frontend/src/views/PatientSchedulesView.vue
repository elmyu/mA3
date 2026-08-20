<template>
  <div class="card">
    <h2 class="page-title">医生时间查看</h2>
    <el-table :data="schedules" v-loading="loading" stripe>
      <el-table-column prop="doctor_name" label="医生" width="140" />
      <el-table-column prop="schedule_date" label="日期" width="140" />
      <el-table-column prop="start_time" label="开始时间" width="120" />
      <el-table-column prop="end_time" label="结束时间" width="120" />
      <el-table-column label="状态" width="100">
        <template #default>
          <el-tag type="success" size="small">出诊</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getDoctorSchedules } from '../api/patients'

const schedules = ref([])
const loading = ref(false)

async function load() {
  loading.value = true
  try {
    const res = await getDoctorSchedules()
    schedules.value = res.data
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
