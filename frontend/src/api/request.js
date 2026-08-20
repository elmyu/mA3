import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({ baseURL: '/api', timeout: 10000 })

request.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

request.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const status = err.response?.status
    const message = err.response?.data?.message || err.response?.data?.msg || '请求失败'
    if (status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      if (location.pathname !== '/login') location.href = '/login'
    } else {
      ElMessage.error(message)
    }
    return Promise.reject(err)
  }
)

export default request
