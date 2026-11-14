import axios from 'axios'
import { ElMessage } from 'element-plus'
import { STORAGE_KEY } from '../stores/user'

// 创建 axios 实例：统一走 /api，由 Vite 代理到后端 8080
const service = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器：自动附加 Authorization: Bearer <token>
service.interceptors.request.use(
  (config) => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY)
      if (raw) {
        const { token } = JSON.parse(raw)
        if (token) {
          config.headers['Authorization'] = `Bearer ${token}`
        }
      }
    } catch (e) {
      // 忽略读取异常
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 清理登录态并跳转登录页
function handleUnauthorized() {
  localStorage.removeItem(STORAGE_KEY)
  ElMessage.error('登录状态已过期，请重新登录')
  // 避免在登录页重复跳转
  if (window.location.pathname !== '/login') {
    window.location.href = '/login'
  }
}

// 响应拦截器：统一处理返回结构 { code, msg, data }
service.interceptors.response.use(
  (response) => {
    const res = response.data
    // 非标准结构（理论上后端统一返回 Result），直接透传
    if (res === null || typeof res === 'undefined' || typeof res !== 'object' || !('code' in res)) {
      return res
    }
    if (res.code === 200) {
      return res
    }
    // 业务失败
    if (res.code === 401) {
      handleUnauthorized()
    } else {
      ElMessage.error(res.msg || '请求失败')
    }
    return Promise.reject(new Error(res.msg || 'Error'))
  },
  (error) => {
    const status = error.response?.status
    if (status === 401) {
      handleUnauthorized()
    } else {
      const msg = error.response?.data?.msg || error.message || '网络异常，请稍后重试'
      ElMessage.error(msg)
    }
    return Promise.reject(error)
  }
)

export default service
