<template>
  <el-container class="layout">
    <el-aside width="210px" class="aside">
      <div class="logo">Mini BME-Hub</div>
      <el-menu :default-active="$route.path" router class="menu">
        <el-menu-item v-for="item in menus" :key="item.path" :index="item.path">
          {{ item.title }}
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span>{{ user?.real_name || user?.username }}（{{ roleText }}）</span>
        <el-button size="small" type="primary" plain @click="handleLogout">退出登录</el-button>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const store = useUserStore()
const user = computed(() => store.user)

const roleText = computed(() => ({ patient: '患者', doctor: '医生', admin: '管理员' })[user.value?.role] || '')

const menus = computed(() => {
  const map = {
    patient: [
      { path: '/patient/signals', title: '我的健康档案' },
      { path: '/patient/schedules', title: '医生时间查看' },
    ],
    doctor: [
      { path: '/doctor/patients', title: '患者信息调阅' },
      { path: '/doctor/devices', title: '设备台账看板' },
      { path: '/doctor/appointments', title: '设备预约' },
    ],
    admin: [
      { path: '/admin/users', title: '用户管理' },
      { path: '/admin/devices', title: '设备维护' },
    ],
  }
  return map[user.value?.role] || []
})

function handleLogout() {
  store.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout {
  height: 100%;
}
.aside {
  background: #fff;
  border-right: 1px solid #e5e7eb;
}
.logo {
  height: 56px;
  line-height: 56px;
  text-align: center;
  font-weight: 700;
  color: #16a34a;
  border-bottom: 1px solid #e5e7eb;
}
.menu {
  border-right: none;
}
.header {
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.main {
  padding: 20px;
}
</style>
