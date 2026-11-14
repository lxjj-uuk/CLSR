import { defineStore } from 'pinia'

// 本地持久化 key
const STORAGE_KEY = 'library_seat_user'

// 角色映射：0 学生，1 管理员
export const ROLE_MAP = {
  0: '学生',
  1: '管理员'
}

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch (e) {
    return null
  }
}

export const useUserStore = defineStore('user', {
  state: () => {
    const saved = loadFromStorage()
    return {
      token: saved?.token || '',
      username: saved?.username || '',
      realName: saved?.realName || '',
      role: saved?.role ?? null
    }
  },
  getters: {
    isLoggedIn: (state) => !!state.token,
    roleText: (state) =>
      state.role === null || state.role === undefined
        ? ''
        : ROLE_MAP[state.role] || '未知'
  },
  actions: {
    // 登录成功后保存
    setAuth(data) {
      this.token = data.token
      this.username = data.username
      this.realName = data.realName
      this.role = data.role
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.$state))
    },
    // 退出 / 401 时清除
    logout() {
      this.token = ''
      this.username = ''
      this.realName = ''
      this.role = null
      localStorage.removeItem(STORAGE_KEY)
    }
  }
})

export { STORAGE_KEY }
