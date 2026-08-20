<template>
  <div class="card">
    <h2 class="page-title">设备台账看板</h2>
    <el-table :data="devices" v-loading="loading" stripe>
      <el-table-column prop="id" label="设备ID" width="90" />
      <el-table-column prop="name" label="设备名称" />
      <el-table-column label="当前状态" width="110">
        <template #default="{ row }">
          <el-tag :type="statusType[row.status]" size="small">{{ statusText[row.status] }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="last_calibration_date" label="上次校准日期" width="140" />
      <el-table-column prop="location" label="所在位置" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button size="small" type="primary" plain @click="openStatus(row)">修改状态</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="statusVisible" title="修改设备状态" width="420px">
      <template v-if="current">
        <p class="device-name">{{ current.name }}</p>
        <el-select v-model="newStatus" style="width: 100%">
          <el-option label="在线" value="online" />
          <el-option label="故障" value="fault" />
          <el-option label="校准中" value="calibrating" />
        </el-select>
      </template>
      <template #footer>
        <el-button @click="statusVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="saveStatus">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getDevices, updateDeviceStatus } from '../api/devices'

const devices = ref([])
const loading = ref(false)
const statusVisible = ref(false)
const current = ref(null)
const newStatus = ref('online')
const saving = ref(false)

const statusText = { online: '在线', fault: '故障', calibrating: '校准中' }
const statusType = { online: 'success', fault: 'danger', calibrating: 'warning' }

async function load() {
  loading.value = true
  try {
    const res = await getDevices()
    devices.value = res.data
  } finally {
    loading.value = false
  }
}

function openStatus(row) {
  current.value = row
  newStatus.value = row.status
  statusVisible.value = true
}

async function saveStatus() {
  saving.value = true
  try {
    await updateDeviceStatus(current.value.id, newStatus.value)
    ElMessage.success('状态已更新')
    statusVisible.value = false
    await load()
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.device-name {
  margin: 0 0 12px;
  font-weight: 600;
}
</style>
