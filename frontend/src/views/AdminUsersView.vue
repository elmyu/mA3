<template>
  <div class="card">
    <h2 class="page-title">用户管理</h2>
    <div class="toolbar">
      <el-button type="primary" @click="openCreate">新增用户</el-button>
    </div>
    <el-table :data="users" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="username" label="用户名" width="140" />
      <el-table-column label="角色" width="100">
        <template #default="{ row }">
          <el-tag size="small" :type="roleType[row.role]">{{ roleText[row.role] }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="real_name" label="姓名" width="120" />
      <el-table-column prop="gender" label="性别" width="70" />
      <el-table-column prop="age" label="年龄" width="70" />
      <el-table-column prop="phone" label="联系电话" />
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button size="small" type="primary" plain @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" plain @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑用户' : '新增用户'" width="480px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名"><el-input v-model="form.username" /></el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password :placeholder="form.id ? '留空则不修改' : ''" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="form.role" style="width: 100%">
            <el-option label="患者" value="patient" />
            <el-option label="医生" value="doctor" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.real_name" /></el-form-item>
        <el-form-item label="性别">
          <el-select v-model="form.gender" style="width: 100%">
            <el-option label="男" value="男" />
            <el-option label="女" value="女" />
          </el-select>
        </el-form-item>
        <el-form-item label="年龄"><el-input-number v-model="form.age" :min="0" :max="150" /></el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone" /></el-form-item>
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
import { createUser, deleteUser, getUsers, updateUser } from '../api/users'

const users = ref([])
const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const form = reactive({ id: null, username: '', password: '', role: 'patient', real_name: '', gender: '', age: null, phone: '' })

const roleText = { patient: '患者', doctor: '医生', admin: '管理员' }
const roleType = { patient: 'success', doctor: 'primary', admin: 'warning' }

async function load() {
  loading.value = true
  try {
    const res = await getUsers()
    users.value = res.data
  } finally {
    loading.value = false
  }
}

function resetForm() {
  Object.assign(form, { id: null, username: '', password: '', role: 'patient', real_name: '', gender: '', age: null, phone: '' })
}

function openCreate() {
  resetForm()
  dialogVisible.value = true
}

function openEdit(row) {
  Object.assign(form, row, { password: '' })
  dialogVisible.value = true
}

async function save() {
  if (!form.username || !form.role || (!form.id && !form.password)) {
    ElMessage.warning('用户名、角色必填，新增时必须设置密码')
    return
  }
  saving.value = true
  try {
    if (form.id) {
      await updateUser(form.id, form)
      ElMessage.success('用户已更新')
    } else {
      await createUser(form)
      ElMessage.success('用户已创建')
    }
    dialogVisible.value = false
    await load()
  } finally {
    saving.value = false
  }
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确认删除用户「${row.username}」？`, '删除确认', { type: 'warning' })
  await deleteUser(row.id)
  ElMessage.success('用户已删除')
  await load()
}

onMounted(load)
</script>
