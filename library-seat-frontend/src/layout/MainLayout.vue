<template>
  <el-container class="layout">
    <header class="topbar">
      <div class="topbar-inner">
        <button class="brand" type="button" aria-label="返回选座首页" @click="router.push('/home')">
          <span class="brand-mark" aria-hidden="true">
            <el-icon><Reading /></el-icon>
          </span>
          <span class="brand-copy">
            <span class="brand-name">校园图书馆</span>
            <span class="brand-sub">座位预约</span>
          </span>
        </button>

        <nav class="nav" aria-label="主导航">
          <router-link
            v-for="item in menus"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <el-icon><component :is="item.icon" /></el-icon>
            <span>{{ item.label }}</span>
          </router-link>
        </nav>

        <div class="user-area">
          <span class="user-avatar" aria-hidden="true">{{ userInitial }}</span>
          <span class="user-copy">
            <span class="user-name">{{ userStore.realName || userStore.username }}</span>
            <span class="user-role">{{ userStore.roleText }}</span>
          </span>
          <button class="logout-btn" type="button" aria-label="退出登录" @click="handleLogout">
            <el-icon><SwitchButton /></el-icon>
            <span>退出</span>
          </button>
        </div>
      </div>
    </header>

    <el-main class="main">
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>

    <footer class="footer">
      <span>校园图书馆座位预约</span>
      <span aria-hidden="true">/</span>
      <span>教学演示系统</span>
    </footer>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import {
  Reading,
  Grid,
  Tickets,
  Bell,
  SwitchButton
} from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const menus = [
  { path: '/home', label: '选座预约', icon: Grid },
  { path: '/my', label: '我的预约', icon: Tickets },
  { path: '/notices', label: '馆内公告', icon: Bell }
]

const userInitial = computed(() => {
  const name = userStore.realName || userStore.username || '读'
  return name.slice(0, 1)
})

function isActive(path) {
  if (path === '/notices') {
    return route.path.startsWith('/notices')
  }
  return route.path === path
}

async function handleLogout() {
  try {
    await ElMessageBox.confirm('退出后需要重新登录才能预约座位。', '退出登录', {
      confirmButtonText: '退出',
      cancelButtonText: '取消',
      type: 'warning'
    })
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
.layout {
  min-height: 100%;
  flex-direction: column;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--ink);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.topbar-inner {
  width: min(1240px, calc(100% - 48px));
  min-height: 76px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 36px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 11px;
  flex-shrink: 0;
  padding: 0;
  border: 0;
  color: #fff;
  background: transparent;
  cursor: pointer;
  font: inherit;
  text-align: left;
}

.brand-mark {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 12px 12px 3px 12px;
  background: var(--lime);
  color: var(--ink);
  font-size: 21px;
}

.brand-copy {
  display: grid;
  gap: 1px;
}

.brand-name {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.brand-sub {
  color: rgba(255, 255, 255, 0.55);
  font-size: 11px;
  letter-spacing: 0.16em;
}

.nav {
  display: flex;
  align-items: stretch;
  align-self: stretch;
  gap: 4px;
}

.nav-item {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 0 16px;
  color: rgba(255, 255, 255, 0.62);
  text-decoration: none;
  font-size: 14px;
  transition: color 160ms ease;
}

.nav-item::after {
  position: absolute;
  right: 16px;
  bottom: 0;
  left: 16px;
  height: 3px;
  border-radius: 3px 3px 0 0;
  background: var(--lime);
  content: "";
  opacity: 0;
  transform: scaleX(0.4);
  transition: opacity 160ms ease, transform 160ms ease;
}

.nav-item:hover {
  color: #fff;
}

.nav-item.active {
  color: #fff;
  font-weight: 650;
}

.nav-item.active::after {
  opacity: 1;
  transform: scaleX(1);
}

.user-area {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: auto;
  color: #fff;
}

.user-avatar {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  font-size: 13px;
  font-weight: 700;
}

.user-copy {
  display: grid;
  gap: 1px;
}

.user-name {
  max-width: 110px;
  overflow: hidden;
  font-size: 13px;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-role {
  color: rgba(255, 255, 255, 0.48);
  font-size: 10px;
}

.logout-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  margin-left: 6px;
  padding: 7px 9px;
  border: 0;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.6);
  background: transparent;
  cursor: pointer;
  font: inherit;
  font-size: 12px;
  transition: color 160ms ease, background-color 160ms ease;
}

.logout-btn:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.08);
}

.main {
  width: 100%;
  min-height: calc(100vh - 76px - 54px);
  padding: 0;
}

.footer {
  display: flex;
  justify-content: center;
  gap: 8px;
  padding: 18px 24px;
  color: #84908a;
  font-size: 11px;
  letter-spacing: 0.05em;
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 220ms ease;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
}

@media (max-width: 880px) {
  .topbar-inner {
    width: min(100% - 32px, 720px);
    flex-wrap: wrap;
    gap: 0 20px;
    padding: 12px 0 0;
  }

  .brand {
    padding-bottom: 12px;
  }

  .user-area {
    padding-bottom: 12px;
  }

  .nav {
    order: 3;
    width: 100%;
    height: 48px;
    overflow-x: auto;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    scrollbar-width: none;
  }

  .nav::-webkit-scrollbar {
    display: none;
  }

  .nav-item {
    flex: 1;
    justify-content: center;
    min-width: 110px;
    padding: 0 10px;
  }

  .nav-item::after {
    right: 20px;
    left: 20px;
  }

  .main {
    min-height: calc(100vh - 133px - 54px);
  }
}

@media (max-width: 560px) {
  .topbar-inner {
    width: calc(100% - 28px);
  }

  .brand-mark {
    width: 36px;
    height: 36px;
  }

  .brand-name {
    font-size: 14px;
  }

  .user-copy,
  .logout-btn span {
    display: none;
  }

  .logout-btn {
    margin-left: 0;
    padding: 8px;
  }

  .footer {
    padding: 16px;
  }
}
</style>
