<template>
  <div class="login-page">
    <aside class="login-story">
      <div class="story-brand">
        <span class="story-mark" aria-hidden="true">
          <el-icon><Reading /></el-icon>
        </span>
        <span>
          <strong>校园图书馆</strong>
          <small>座位预约</small>
        </span>
      </div>

      <div class="story-copy">
        <p class="story-path">入口 / 阅览室 / 座位</p>
        <h1>找到你的位置，<br />再把时间<br />交给阅读。</h1>
        <p class="story-note">
          查看实时座位状态，选择合适时段，用一次清晰的预约开启今天的学习。
        </p>
      </div>

      <div class="floor-plan" aria-hidden="true">
        <div class="plan-head">
          <span>三层 · 阅览区</span>
          <span>座位示意</span>
        </div>
        <div class="plan-grid">
          <i v-for="seat in planSeats" :key="seat.id" :class="seat.state"></i>
        </div>
        <div class="plan-foot">
          <span><i></i>可选</span>
          <span><i></i>已约</span>
          <span>服务台</span>
        </div>
      </div>

      <p class="story-foot">日间开放 · 在线预约 · 到馆签到</p>
    </aside>

    <main class="login-main">
      <section class="login-panel">
        <div class="login-heading">
          <p>账号登录</p>
          <h2>继续你的预约</h2>
          <span>使用学号或管理员账号进入系统。</span>
        </div>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-position="top"
          size="large"
          @submit.prevent="handleLogin"
        >
          <el-form-item label="账号" prop="username">
            <el-input
              v-model="form.username"
              name="username"
              autocomplete="username"
              placeholder="学号或管理员账号"
              :prefix-icon="User"
            />
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input
              v-model="form.password"
              name="password"
              type="password"
              autocomplete="current-password"
              show-password
              placeholder="不少于 6 位"
              :prefix-icon="Lock"
            />
          </el-form-item>

          <button class="login-action" type="submit" :disabled="loading">
            <span>{{ loading ? '正在进入…' : '登录系统' }}</span>
            <el-icon><Right /></el-icon>
          </button>
        </el-form>

        <div class="demo-area">
          <span>演示账号</span>
          <button type="button" @click="fillDemo('student')">
            学生 2024001
          </button>
          <button type="button" @click="fillDemo('admin')">
            管理员 admin
          </button>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Lock, Reading, Right, User } from '@element-plus/icons-vue'
import { login } from '../api'
import { useUserStore } from '../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)
const form = reactive({ username: '', password: '' })

const planSeats = [
  { id: 1, state: 'available' },
  { id: 2, state: 'available' },
  { id: 3, state: 'reserved' },
  { id: 4, state: 'available' },
  { id: 5, state: 'reserved' },
  { id: 6, state: 'available' },
  { id: 7, state: 'available' },
  { id: 8, state: 'available' },
  { id: 9, state: 'reserved' },
  { id: 10, state: 'available' },
  { id: 11, state: 'available' },
  { id: 12, state: 'reserved' }
]

const rules = {
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不少于 6 位', trigger: 'blur' }
  ]
}

function fillDemo(type) {
  if (type === 'admin') {
    form.username = 'admin'
  } else {
    form.username = '2024001'
  }
  form.password = '123456'
}

function handleLogin() {
  if (!formRef.value) return
  formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      const response = await login({
        username: form.username,
        password: form.password
      })
      userStore.setAuth(response.data)
      ElMessage.success(`欢迎，${response.data.realName}`)
      router.push(route.query.redirect || '/home')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.login-page {
  display: grid;
  grid-template-columns: minmax(440px, 0.95fr) minmax(480px, 1.05fr);
  min-height: 100vh;
  background: var(--paper);
}

.login-story {
  position: relative;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow: hidden;
  padding: 38px clamp(36px, 5vw, 76px);
  border-radius: 0 44px 44px 0;
  background: var(--ink);
  color: #fff;
  animation: story-enter 620ms cubic-bezier(0.22, 1, 0.36, 1) both;
}

.login-story::before {
  position: absolute;
  top: 21%;
  right: -130px;
  width: 340px;
  height: 340px;
  border: 1px solid rgba(215, 232, 143, 0.14);
  border-radius: 50%;
  content: "";
}

.login-story::after {
  position: absolute;
  top: 26%;
  right: -160px;
  width: 440px;
  height: 440px;
  border: 1px solid rgba(215, 232, 143, 0.07);
  border-radius: 50%;
  content: "";
}

.story-brand {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}

.story-mark {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 13px 13px 3px 13px;
  background: var(--lime);
  color: var(--ink);
  font-size: 23px;
}

.story-brand > span:last-child {
  display: grid;
  gap: 2px;
}

.story-brand strong {
  font-size: 15px;
  letter-spacing: 0.03em;
}

.story-brand small {
  color: rgba(255, 255, 255, 0.48);
  font-size: 10px;
  letter-spacing: 0.16em;
}

.story-copy {
  position: relative;
  z-index: 1;
  max-width: 570px;
  margin: auto 0;
  padding: 70px 0 50px;
}

.story-path {
  margin-bottom: 25px;
  color: var(--lime);
  font-size: 11px;
  font-weight: 650;
  letter-spacing: 0.08em;
}

.story-copy h1 {
  margin-bottom: 26px;
  font-size: clamp(44px, 5.2vw, 74px);
  font-weight: 760;
  letter-spacing: -0.065em;
  line-height: 1.1;
}

.story-note {
  max-width: 440px;
  margin-bottom: 0;
  color: rgba(255, 255, 255, 0.58);
  font-size: 14px;
  line-height: 1.9;
  text-wrap: pretty;
}

.floor-plan {
  position: relative;
  z-index: 1;
  width: min(100%, 490px);
  padding: 18px 20px 16px;
  border: 1px solid rgba(255, 255, 255, 0.13);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.035);
  backdrop-filter: blur(4px);
}

.plan-head,
.plan-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: rgba(255, 255, 255, 0.38);
  font-size: 9px;
  letter-spacing: 0.08em;
}

.plan-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
  margin: 16px 0;
}

.plan-grid i {
  height: 24px;
  border: 1px solid rgba(215, 232, 143, 0.45);
  border-radius: 4px 4px 8px 8px;
  background: rgba(215, 232, 143, 0.12);
}

.plan-grid i.reserved {
  border-color: rgba(255, 255, 255, 0.1);
  background:
    repeating-linear-gradient(
      -45deg,
      rgba(255, 255, 255, 0.06) 0 3px,
      rgba(255, 255, 255, 0.01) 3px 6px
    );
}

.plan-foot {
  justify-content: flex-start;
  gap: 16px;
}

.plan-foot span {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.plan-foot i {
  width: 8px;
  height: 8px;
  border-radius: 2px;
  background: var(--lime);
}

.plan-foot span:nth-child(2) i {
  background: rgba(255, 255, 255, 0.18);
}

.story-foot {
  position: relative;
  z-index: 1;
  margin: 34px 0 0;
  color: rgba(255, 255, 255, 0.3);
  font-size: 10px;
  letter-spacing: 0.08em;
}

.login-main {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
}

.login-panel {
  width: min(100%, 410px);
  animation: form-enter 620ms 100ms cubic-bezier(0.22, 1, 0.36, 1) both;
}

.login-heading {
  margin-bottom: 34px;
}

.login-heading p {
  margin-bottom: 12px;
  color: var(--teal);
  font-size: 12px;
  font-weight: 700;
}

.login-heading h2 {
  margin-bottom: 12px;
  font-size: 36px;
  font-weight: 760;
  letter-spacing: -0.05em;
}

.login-heading span {
  color: var(--muted);
  font-size: 13px;
}

.login-panel :deep(.el-form-item) {
  margin-bottom: 22px;
}

.login-panel :deep(.el-form-item__label) {
  padding-bottom: 7px;
  color: var(--ink);
  font-size: 12px;
}

.login-panel :deep(.el-input__wrapper) {
  min-height: 50px;
  border-radius: 12px;
  background: #fbfbf7;
}

.login-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  min-height: 52px;
  margin-top: 5px;
  padding: 0 18px 0 22px;
  border: 0;
  border-radius: 12px;
  background: var(--ink);
  color: #fff;
  cursor: pointer;
  font: inherit;
  font-size: 14px;
  font-weight: 700;
  transition:
    background-color 180ms ease,
    box-shadow 180ms ease,
    transform 180ms cubic-bezier(0.22, 1, 0.36, 1);
}

.login-action:hover:not(:disabled) {
  background: var(--teal);
  box-shadow: 0 12px 30px rgba(23, 63, 58, 0.15);
  transform: translateY(-1px);
}

.login-action:disabled {
  cursor: wait;
  opacity: 0.72;
}

.demo-area {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid var(--line);
}

.demo-area > span {
  width: 100%;
  margin-bottom: 1px;
  color: var(--muted);
  font-size: 10px;
  letter-spacing: 0.08em;
}

.demo-area button {
  padding: 7px 10px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: transparent;
  color: var(--muted);
  cursor: pointer;
  font: inherit;
  font-size: 11px;
  transition: border-color 160ms ease, color 160ms ease;
}

.demo-area button:hover {
  border-color: var(--teal);
  color: var(--teal);
}

@keyframes story-enter {
  from {
    opacity: 0;
    transform: translateX(-18px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes form-enter {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 980px) {
  .login-page {
    grid-template-columns: 1fr;
  }

  .login-story {
    min-height: auto;
    padding: 30px;
    border-radius: 0 0 32px 32px;
  }

  .story-copy {
    margin: 0;
    padding: 66px 0 46px;
  }

  .story-copy h1 {
    font-size: clamp(42px, 9vw, 66px);
  }

  .floor-plan,
  .story-foot {
    display: none;
  }

  .login-main {
    padding: 52px 28px 64px;
  }

  .login-panel {
    width: min(100%, 500px);
  }
}

@media (max-width: 540px) {
  .login-story {
    padding: 24px 22px;
    border-radius: 0 0 24px 24px;
  }

  .story-copy {
    padding: 54px 0 28px;
  }

  .story-copy h1 {
    margin-bottom: 18px;
    font-size: 39px;
  }

  .story-note {
    font-size: 13px;
  }

  .login-main {
    padding: 38px 22px 52px;
  }

  .login-heading h2 {
    font-size: 31px;
  }
}
</style>
