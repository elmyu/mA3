<template>
  <div class="card">
    <h2 class="page-title">设备维护</h2>
    <div class="toolbar">
      <el-button type="primary" @click="openCreate">新增设备</el-button>
    </div>
    <el-table :data="devices" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="name" label="设备名称" />
      <el-table-column label="状态" width="110">
        <template #default="{ row }">
          <el-tag size="small" :type="statusType[row.status]">{{ statusText[row.status] }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="last_calibration_date" label="上次校准日期" width="140" />
      <el-table-column prop="location" label="所在位置" />
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button size="small" type="primary" plain @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" plain @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑设备' : '新增设备'" width="480px">
      <el-form :model="form" label-width="110px">
        <el-form-item label="设备名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="在线" value="online" />
            <el-option label="故障" value="fault" />
            <el-option label="校准中" value="calibrating" />
          </el-select>
        </el-form-item>
        <el-form-item label="上次校准日期">
          <el-date-picker v-model="form.last_calibration_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="所在位置"><el-input v-model="form.location" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { createDevice, deleteDevice, getDevices, updateDevice } from '../api/devices'

const devices = ref([])
const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const form = reactive({ id: null, name: '', status: 'online', last_calibration_date: null, location: '' })

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

function resetForm() {
  Object.assign(form, { id: null, name: '', status: 'online', last_calibration_date: null, location: '' })
}

function openCreate() {
  resetForm()
  dialogVisible.value = true
}

function openEdit(row) {
  Object.assign(form, row)
  dialogVisible.value = true
}

async function save() {
  if (!form.name) {
    ElMessage.warning('设备名称不能为空')
    return
  }
  saving.value = true
  try {
    if (form.id) {
      await updateDevice(form.id, form)
      ElMessage.success('设备已更新')
    } else {
      await createDevice(form)
      ElMessage.success('设备已创建')
    }
    dialogVisible.value = false
    await load()
  } finally {
    saving.value = false
  }
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确认删除设备「${row.name}」？`, '删除确认', { type: 'warning' })
  await deleteDevice(row.id)
  ElMessage.success('设备已删除')
  await load()
}

onMounted(load)
</script>
