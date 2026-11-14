<template>
  <div class="page-shell notices-page">
    <header class="page-heading">
      <div>
        <h1>馆内公告</h1>
        <p>开放安排、服务调整和座位使用提醒。</p>
      </div>
      <span class="notice-count">{{ list.length }} 条公告</span>
    </header>

    <section class="notice-ledger surface">
      <div class="ledger-head" aria-hidden="true">
        <span>发布日期</span>
        <span>公告内容</span>
        <span>查看</span>
      </div>

      <div v-loading="loading" class="notice-list">
        <button
          v-for="(item, index) in list"
          :key="item.id"
          type="button"
          class="notice-row"
          :style="{ '--notice-index': index }"
          @click="goDetail(item.id)"
        >
          <span class="notice-date">
            <strong>{{ dateParts(item.createTime || item.publishTime).day }}</strong>
            <small>{{ dateParts(item.createTime || item.publishTime).month }}</small>
          </span>

          <span class="notice-main">
            <strong>{{ item.title }}</strong>
            <span>{{ item.content || '打开公告查看详情。' }}</span>
          </span>

          <span class="notice-open">
            <span>阅读</span>
            <el-icon><ArrowRight /></el-icon>
          </span>
        </button>

        <div v-if="!loading && !list.length" class="notice-empty">
          <span class="empty-symbol" aria-hidden="true">
            <el-icon><Bell /></el-icon>
          </span>
          <h2>暂无可查看的公告</h2>
          <p>新的开放安排会在这里发布。</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowRight, Bell } from '@element-plus/icons-vue'
import { getNotices } from '../api'

const router = useRouter()
const list = ref([])
const loading = ref(false)

function dateParts(value) {
  if (!value) return { day: '—', month: '公告' }
  const date = new Date(String(value).replace(' ', 'T'))
  if (Number.isNaN(date.getTime())) {
    return { day: String(value).slice(8, 10) || '—', month: '日期' }
  }
  return {
    day: String(date.getDate()).padStart(2, '0'),
    month: `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}`
  }
}

async function loadList() {
  loading.value = true
  try {
    const response = await getNotices()
    if (response?.code === 200) {
      list.value = response.data || []
    }
  } finally {
    loading.value = false
  }
}

function goDetail(id) {
  router.push(`/notices/${id}`)
}

onMounted(loadList)
</script>

<style scoped>
.notices-page {
  animation: page-enter 520ms cubic-bezier(0.22, 1, 0.36, 1) both;
}

.notice-count {
  color: var(--muted);
  font-size: 12px;
  font-variant-numeric: tabular-nums;
}

.notice-ledger {
  overflow: hidden;
  border-radius: 22px;
  box-shadow: var(--shadow);
}

.ledger-head {
  display: grid;
  grid-template-columns: 104px minmax(0, 1fr) 70px;
  gap: 24px;
  padding: 14px 30px;
  border-bottom: 1px solid var(--line);
  background: #f0f2ec;
  color: #98a19c;
  font-size: 10px;
  letter-spacing: 0.06em;
}

.ledger-head span:last-child {
  text-align: right;
}

.notice-list {
  min-height: 240px;
}

.notice-row {
  display: grid;
  grid-template-columns: 104px minmax(0, 1fr) 70px;
  align-items: center;
  gap: 24px;
  width: 100%;
  min-height: 108px;
  padding: 20px 30px;
  border: 0;
  border-bottom: 1px solid #edf0eb;
  background: transparent;
  color: inherit;
  cursor: pointer;
  font: inherit;
  text-align: left;
  transition: background-color 170ms ease;
  animation: notice-in 420ms calc(80ms + var(--notice-index) * 45ms)
    cubic-bezier(0.22, 1, 0.36, 1) both;
}

.notice-row:last-of-type {
  border-bottom: 0;
}

.notice-row:hover {
  background: #fbfcf8;
}

.notice-date {
  display: grid;
  justify-items: start;
  gap: 4px;
  padding-left: 14px;
  border-left: 2px solid var(--line);
  transition: border-color 170ms ease;
}

.notice-row:hover .notice-date {
  border-color: var(--gold);
}

.notice-date strong {
  color: var(--ink);
  font-size: 26px;
  font-variant-numeric: tabular-nums;
  font-weight: 650;
  letter-spacing: -0.04em;
  line-height: 1;
}

.notice-date small {
  color: var(--muted);
  font-size: 9px;
  letter-spacing: 0.04em;
}

.notice-main {
  display: grid;
  gap: 8px;
  min-width: 0;
}

.notice-main strong {
  overflow: hidden;
  color: var(--ink);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.015em;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notice-main > span {
  display: -webkit-box;
  overflow: hidden;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.7;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.notice-open {
  display: inline-flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
  color: #99a39d;
  font-size: 10px;
  transition: color 170ms ease, transform 170ms ease;
}

.notice-row:hover .notice-open {
  color: var(--teal);
  transform: translateX(3px);
}

.notice-empty {
  display: grid;
  justify-items: center;
  padding: 70px 24px 78px;
  text-align: center;
}

.empty-symbol {
  width: 52px;
  height: 52px;
  display: grid;
  place-items: center;
  margin-bottom: 16px;
  border-radius: 15px 15px 4px 15px;
  background: var(--teal-soft);
  color: var(--teal);
  font-size: 23px;
}

.notice-empty h2 {
  margin-bottom: 7px;
  font-size: 18px;
}

.notice-empty p {
  margin: 0;
  color: var(--muted);
  font-size: 12px;
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

@keyframes notice-in {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 680px) {
  .ledger-head {
    display: none;
  }

  .notice-row {
    grid-template-columns: 62px minmax(0, 1fr);
    gap: 16px;
    min-height: 104px;
    padding: 18px 16px;
  }

  .notice-date {
    padding-left: 10px;
  }

  .notice-date strong {
    font-size: 23px;
  }

  .notice-open {
    display: none;
  }

  .notice-main strong {
    white-space: normal;
  }
}
</style>
