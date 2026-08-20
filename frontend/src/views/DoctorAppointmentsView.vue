<template>
  <div class="card">
    <h2 class="page-title">设备预约</h2>
    <el-form :inline="true" :model="form" class="toolbar">
      <el-form-item label="设备">
        <el-select v-model="form.device_id" placeholder="选择在线设备" style="width: 220px">
          <el-option v-for="d in onlineDevices" :key="d.id" :label="`${d.name}（${d.location || '未定位'}）`" :value="d.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="开始时间">
        <el-date-picker v-model="form.start_time" type="datetime" placeholder="选择开始时间" value-format="YYYY-MM-DD HH:mm:ss" />
      </el-form-item>
      <el-form-item label="结束时间">
        <el-date-picker v-model="form.end_time" type="datetime" placeholder="选择结束时间" value-format="YYYY-MM-DD HH:mm:ss" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :loading="submitting" @click="submit">提交预约</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="appointments" v-loading="loading" stripe>
      <el-table-column prop="id" label="预约ID" width="90" />
      <el-table-column prop="device_name" label="设备名称" />
      <el-table-column prop="start_time" label="开始时间" width="180" />
      <el-table-column prop="end_time" label="结束时间" width="180" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag size="small" :type="row.status === 'booked' ? 'success' : 'info'">
            {{ row.status === 'booked' ? '已预约' : row.status }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getDevices } from '../api/devices'
import { createAppointment, getMyAppointments } from '../api/appointments'

const devices = ref([])
const appointments = ref([])
const loading = ref(false)
const submitting = ref(false)
const form = reactive({ device_id: null, start_time: '', end_time: '' })

const onlineDevices = computed(() => devices.value.filter((d) => d.status === 'online'))

async function load() {
  loading.value = true
  try {
    const [deviceRes, apptRes] = await Promise.all([getDevices(), getMyAppointments()])
    devices.value = deviceRes.data
    appointments.value = apptRes.data
  } finally {
    loading.value = false
  }
}

async function submit() {
  if (!form.device_id || !form.start_time || !form.end_time) {
    ElMessage.warning('请完整填写设备与时间')
    return
  }
  submitting.value = true
  try {
    await createAppointment({ ...form })
    ElMessage.success('预约成功')
    Object.assign(form, { device_id: null, start_time: '', end_time: '' })
    await load()
  } finally {
    submitting.value = false
  }
}

onMounted(load)
</script>
