<template>
  <div class="card">
    <h2 class="page-title">患者信息调阅</h2>
    <el-table :data="patients" v-loading="loading" stripe>
      <el-table-column prop="id" label="患者ID" width="90" />
      <el-table-column prop="real_name" label="姓名" width="120" />
      <el-table-column prop="gender" label="性别" width="80" />
      <el-table-column prop="age" label="年龄" width="80" />
      <el-table-column prop="phone" label="联系电话" />
      <el-table-column label="操作" width="130">
        <template #default="{ row }">
          <el-button size="small" type="primary" plain @click="openSignals(row)">查看信号</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="signalsVisible" title="患者信号记录" width="860px">
      <template v-if="currentPatient">
        <el-descriptions :column="4" border class="patient-info">
          <el-descriptions-item label="姓名">{{ currentPatient.real_name }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ currentPatient.gender }}</el-descriptions-item>
          <el-descriptions-item label="年龄">{{ currentPatient.age }}</el-descriptions-item>
          <el-descriptions-item label="电话">{{ currentPatient.phone }}</el-descriptions-item>
        </el-descriptions>
        <el-table :data="patientSignals" stripe>
          <el-table-column prop="id" label="记录ID" width="90" />
          <el-table-column prop="signal_type" label="信号类型" width="110" />
          <el-table-column prop="sample_rate" label="采样率(Hz)" width="110" />
          <el-table-column prop="recorded_at" label="记录时间" />
        </el-table>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getPatientSignals, getPatients } from '../api/patients'

const patients = ref([])
const loading = ref(false)
const signalsVisible = ref(false)
const currentPatient = ref(null)
const patientSignals = ref([])

async function load() {
  loading.value = true
  try {
    const res = await getPatients()
    patients.value = res.data
  } finally {
    loading.value = false
  }
}

async function openSignals(patient) {
  currentPatient.value = patient
  signalsVisible.value = true
  const res = await getPatientSignals(patient.id)
  patientSignals.value = res.data.records
}

onMounted(load)
</script>

<style scoped>
.patient-info {
  margin-bottom: 16px;
}
</style>
