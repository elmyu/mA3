import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  { path: '/login', component: () => import('../views/LoginView.vue') },
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: 'patient/signals', component: () => import('../views/PatientSignalsView.vue'), meta: { roles: ['patient'] } },
      { path: 'patient/schedules', component: () => import('../views/PatientSchedulesView.vue'), meta: { roles: ['patient'] } },
      { path: 'doctor/patients', component: () => import('../views/DoctorPatientsView.vue'), meta: { roles: ['doctor'] } },
      { path: 'doctor/devices', component: () => import('../views/DoctorDevicesView.vue'), meta: { roles: ['doctor'] } },
      { path: 'doctor/appointments', component: () => import('../views/DoctorAppointmentsView.vue'), meta: { roles: ['doctor'] } },
      { path: 'admin/users', component: () => import('../views/AdminUsersView.vue'), meta: { roles: ['admin'] } },
      { path: 'admin/devices', component: () => import('../views/AdminDevicesView.vue'), meta: { roles: ['admin'] } },
    ],
  },
  { path: '/:pathMatch(.*)*', redirect: '/login' },
]

const roleHome = {
  patient: '/patient/signals',
  doctor: '/doctor/devices',
  admin: '/admin/users',
}

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to) => {
  const store = useUserStore()
  if (to.meta.requiresAuth && !store.token) return '/login'
  if (to.path === '/login' && store.token) return roleHome[store.user?.role] || '/'
  if (to.meta.roles && !to.meta.roles.includes(store.user?.role)) {
    return roleHome[store.user?.role] || '/login'
  }
  return true
})

export default router
