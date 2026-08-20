<template>
  <div class="login-page">
    <el-card class="login-card">
      <h2 class="login-title">Mini BME-Hub</h2>
      <p class="login-sub">医疗设备管理平台</p>
      <el-form :model="form" @keyup.enter="handleLogin">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" clearable />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码" show-password />
        </el-form-item>
        <el-button type="primary" class="login-btn" :loading="loading" @click="handleLogin">
          登 录
        </el-button>
      </el-form>
      <div class="demo-tips">
        <el-button size="small" @click="fill('admin', 'admin123')">管理员 admin</el-button>
        <el-button size="small" @click="fill('doctor1', '123456')">医生 doctor1</el-button>
        <el-button size="small" @click="fill('patient1', '123456')">患者 patient1</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'

const router = useRouter()
const store = useUserStore()
const loading = ref(false)
const form = reactive({ username: '', password: '' })

const roleHome = { patient: '/patient/signals', doctor: '/doctor/devices', admin: '/admin/users' }

function fill(username, password) {
  form.username = username
  form.password = password
}

async function handleLogin() {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    await store.login(form.username, form.password)
    ElMessage.success('登录成功')
    router.push(roleHome[store.user.role] || '/')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(160deg, #e6f7ec 0%, #f4f7f4 100%);
}
.login-card {
  width: 360px;
  padding: 12px 8px;
}
.login-title {
  margin: 0;
  text-align: center;
  color: #16a34a;
  font-size: 24px;
}
.login-sub {
  text-align: center;
  color: #6b7280;
  margin: 6px 0 22px;
}
.login-btn {
  width: 100%;
}
.demo-tips {
  margin-top: 18px;
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}
</style>
