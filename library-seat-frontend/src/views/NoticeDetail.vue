<template>
  <div class="page-shell detail-page">
    <button class="back-action" type="button" @click="goBack">
      <el-icon><ArrowLeft /></el-icon>
      <span>返回公告列表</span>
    </button>

    <article v-loading="loading" class="notice-article surface">
      <template v-if="notice">
        <header class="article-head">
          <p class="article-meta">
            馆内公告
            <span aria-hidden="true">/</span>
            {{ formatDate(notice.createTime || notice.publishTime) }}
          </p>
          <h1>{{ notice.title }}</h1>
        </header>

        <div class="article-rule" aria-hidden="true">
          <span></span>
        </div>

        <div class="article-content">{{ notice.content }}</div>
      </template>

      <div v-else-if="!loading" class="article-empty">
        <span class="empty-symbol" aria-hidden="true">
          <el-icon><Document /></el-icon>
        </span>
        <h1>没有找到这条公告</h1>
        <p>公告可能已被移除或链接不完整。</p>
        <button type="button" @click="goBack">返回公告列表</button>
      </div>
    </article>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Document } from '@element-plus/icons-vue'
import { getNoticeDetail } from '../api'

const route = useRoute()
const router = useRouter()
const notice = ref(null)
const loading = ref(false)

function formatDate(value) {
  if (!value) return '未注明日期'
  const date = new Date(String(value).replace(' ', 'T'))
  if (Number.isNaN(date.getTime())) return String(value)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
}

async function loadDetail() {
  loading.value = true
  try {
    const response = await getNoticeDetail(route.params.id)
    if (response?.code === 200) {
      notice.value = response.data || null
    }
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.push('/notices')
}

onMounted(loadDetail)
</script>

<style scoped>
.detail-page {
  width: min(960px, calc(100% - 48px));
  animation: page-enter 520ms cubic-bezier(0.22, 1, 0.36, 1) both;
}

.back-action {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 20px;
  padding: 5px 0;
  border: 0;
  background: transparent;
  color: var(--muted);
  cursor: pointer;
  font: inherit;
  font-size: 12px;
  transition: color 160ms ease, transform 160ms ease;
}

.back-action:hover {
  color: var(--ink);
  transform: translateX(-2px);
}

.notice-article {
  min-height: 460px;
  padding: clamp(34px, 7vw, 76px);
  border-radius: 24px;
  box-shadow: var(--shadow);
}

.article-head {
  max-width: 720px;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 24px;
  color: var(--teal);
  font-size: 11px;
  font-weight: 650;
  letter-spacing: 0.06em;
}

.article-meta span {
  color: #b6beb9;
}

.article-head h1 {
  margin-bottom: 0;
  font-size: clamp(30px, 5vw, 50px);
  font-weight: 760;
  letter-spacing: -0.055em;
  line-height: 1.2;
  text-wrap: balance;
}

.article-rule {
  position: relative;
  height: 1px;
  margin: 38px 0;
  background: var(--line);
}

.article-rule span {
  position: absolute;
  top: -1px;
  left: 0;
  width: 48px;
  height: 3px;
  background: var(--gold);
}

.article-content {
  max-width: 720px;
  color: #344b45;
  font-size: 15px;
  line-height: 2;
  white-space: pre-wrap;
  word-break: break-word;
}

.article-empty {
  display: grid;
  justify-items: center;
  padding: 80px 0;
  text-align: center;
}

.empty-symbol {
  width: 54px;
  height: 54px;
  display: grid;
  place-items: center;
  margin-bottom: 18px;
  border-radius: 16px 16px 4px 16px;
  background: var(--teal-soft);
  color: var(--teal);
  font-size: 24px;
}

.article-empty h1 {
  margin-bottom: 8px;
  font-size: 24px;
}

.article-empty p {
  margin-bottom: 20px;
  color: var(--muted);
  font-size: 13px;
}

.article-empty button {
  padding: 9px 14px;
  border: 0;
  border-radius: 9px;
  background: var(--ink);
  color: #fff;
  cursor: pointer;
  font: inherit;
  font-size: 12px;
  font-weight: 650;
}

@keyframes page-enter {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 760px) {
  .detail-page {
    width: calc(100% - 28px);
  }

  .notice-article {
    padding: 30px 24px 42px;
    border-radius: 18px;
  }

  .article-rule {
    margin: 28px 0;
  }

  .article-content {
    font-size: 14px;
    line-height: 1.95;
  }
}
</style>
