<template>
  <div class="page-shell reservations-page">
    <header class="page-heading">
      <div>
        <h1>我的预约</h1>
        <p>查看预约进度，按时签到或签退。</p>
      </div>
      <button class="refresh-action" type="button" :disabled="loading" @click="loadList">
        <el-icon :class="{ spinning: loading }"><Refresh /></el-icon>
        <span>{{ loading ? '正在更新' : '更新记录' }}</span>
      </button>
    </header>

    <section class="reservation-board surface">
      <div class="filter-bar" role="tablist" aria-label="按预约状态筛选">
        <button
          v-for="filter in filters"
          :key="filter.key"
          type="button"
          role="tab"
          :aria-selected="activeFilter === filter.key"
          :class="{ active: activeFilter === filter.key }"
          @click="activeFilter = filter.key"
        >
          <span>{{ filter.label }}</span>
          <strong>{{ filter.count }}</strong>
        </button>
      </div>

      <div class="record-head" aria-hidden="true">
        <span>预约编号</span>
        <span>位置</span>
        <span>使用时段</span>
        <span>状态</span>
        <span>操作</span>
      </div>

      <div v-loading="loading" class="record-list">
        <article
          v-for="(item, index) in filteredList"
          :key="item.id"
          class="record-row"
          :style="{ '--record-index': index }"
        >
          <div class="record-number">
            <strong>{{ String(index + 1).padStart(2, '0') }}</strong>
            <span>{{ item.reserveNo || `#${item.id}` }}</span>
          </div>

          <div class="record-where">
            <strong>{{ item.roomName || '阅览室' }}</strong>
            <span>{{ item.seatNo || '—' }} 号座位</span>
          </div>

          <div class="record-when">
            <strong>{{ formatDate(item.reserveDate || item.date) }}</strong>
            <span>
              {{ item.slotName || '—' }}
              <template v-if="item.startTime"> · {{ item.startTime }}—{{ item.endTime }}</template>
            </span>
          </div>

          <div class="record-status">
            <span class="status-pill" :class="`status-${item.status}`">
              <i aria-hidden="true"></i>
              {{ statusText(item.status) }}
            </span>
          </div>

          <div class="record-actions">
            <template v-if="item.status === 0">
              <button class="action-primary" type="button" @click="onCheckin(item)">签到</button>
              <button class="action-quiet" type="button" @click="onCancel(item)">取消</button>
            </template>
            <button
              v-else-if="item.status === 1"
              class="action-primary"
              type="button"
              @click="onCheckout(item)"
            >
              签退
            </button>
            <span v-else class="action-empty">—</span>
          </div>
        </article>

        <div v-if="!loading && !filteredList.length" class="records-empty">
          <span class="empty-symbol" aria-hidden="true">
            <el-icon><Tickets /></el-icon>
          </span>
          <h2>{{ list.length ? '这个分类下暂无记录' : '还没有预约记录' }}</h2>
          <p>{{ list.length ? '切换其他状态看看。' : '从选座页挑一个座位，预约会显示在这里。' }}</p>
          <router-link v-if="!list.length" to="/home">去选座</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Tickets } from '@element-plus/icons-vue'
import {
  cancelReservation,
  checkin,
  checkout,
  getMyReservations
} from '../api'

const list = ref([])
const loading = ref(false)
const activeFilter = ref('all')

const statusMap = {
  0: { text: '待签到', type: 'pending' },
  1: { text: '使用中', type: 'active' },
  2: { text: '已完成', type: 'done' },
  3: { text: '已取消', type: 'cancelled' },
  4: { text: '违约', type: 'violated' }
}

const filters = computed(() => [
  { key: 'all', label: '全部', count: list.value.length },
  {
    key: 'pending',
    label: '待签到',
    count: list.value.filter((item) => item.status === 0).length
  },
  {
    key: 'active',
    label: '使用中',
    count: list.value.filter((item) => item.status === 1).length
  },
  {
    key: 'history',
    label: '历史记录',
    count: list.value.filter((item) => [2, 3, 4].includes(item.status)).length
  }
])

const filteredList = computed(() => {
  if (activeFilter.value === 'all') return list.value
  if (activeFilter.value === 'pending') {
    return list.value.filter((item) => item.status === 0)
  }
  if (activeFilter.value === 'active') {
    return list.value.filter((item) => item.status === 1)
  }
  return list.value.filter((item) => [2, 3, 4].includes(item.status))
})

function statusText(status) {
  return statusMap[status]?.text || '未知'
}

function formatDate(value) {
  if (!value) return '—'
  return String(value).slice(0, 10).replaceAll('-', '.')
}

async function loadList() {
  loading.value = true
  try {
    const response = await getMyReservations()
    if (response?.code === 200) {
      list.value = response.data || []
    }
  } finally {
    loading.value = false
  }
}

async function confirmAction(message, title, confirmButtonText) {
  try {
    await ElMessageBox.confirm(message, title, {
      confirmButtonText,
      cancelButtonText: '取消',
      type: 'warning'
    })
    return true
  } catch {
    return false
  }
}

async function onCheckin(item) {
  const confirmed = await confirmAction(
    `确认在 ${item.roomName} ${item.seatNo} 号座位签到吗？`,
    '签到确认',
    '确定签到'
  )
  if (!confirmed) return

  const response = await checkin(item.id)
  if (response?.code === 200) {
    ElMessage.success(response.data || '签到成功')
    await loadList()
  }
}

async function onCheckout(item) {
  const confirmed = await confirmAction(
    `确认结束 ${item.roomName} ${item.seatNo} 号座位的使用吗？`,
    '签退确认',
    '确定签退'
  )
  if (!confirmed) return

  const response = await checkout(item.id)
  if (response?.code === 200) {
    ElMessage.success(response.data || '签退成功')
    await loadList()
  }
}

async function onCancel(item) {
  const confirmed = await confirmAction(
    `确认取消 ${item.roomName} ${item.seatNo} 号座位的预约吗？取消后不可恢复。`,
    '取消预约',
    '确定取消'
  )
  if (!confirmed) return

  const response = await cancelReservation(item.id)
  if (response?.code === 200) {
    ElMessage.success(response.data || '取消成功')
    await loadList()
  }
}

onMounted(loadList)
</script>

<style scoped>
.reservations-page {
  animation: page-enter 520ms cubic-bezier(0.22, 1, 0.36, 1) both;
}

.refresh-action {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 10px 14px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: transparent;
  color: var(--ink);
  cursor: pointer;
  font: inherit;
  font-size: 12px;
  font-weight: 650;
  transition: border-color 160ms ease, background-color 160ms ease;
}

.refresh-action:hover:not(:disabled) {
  border-color: #aab9b1;
  background: var(--surface);
}

.refresh-action:disabled {
  cursor: wait;
  opacity: 0.65;
}

.spinning {
  animation: spin 900ms linear infinite;
}

.reservation-board {
  overflow: hidden;
  border-radius: 22px;
  box-shadow: var(--shadow);
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 17px 24px;
  border-bottom: 1px solid var(--line);
  background: #f0f2ec;
}

.filter-bar button {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 8px 11px;
  border: 0;
  border-radius: 9px;
  background: transparent;
  color: var(--muted);
  cursor: pointer;
  font: inherit;
  font-size: 12px;
  transition: color 160ms ease, background-color 160ms ease;
}

.filter-bar button strong {
  min-width: 18px;
  padding: 1px 5px;
  border-radius: 6px;
  background: rgba(23, 63, 58, 0.06);
  font-size: 10px;
  font-variant-numeric: tabular-nums;
}

.filter-bar button:hover {
  color: var(--ink);
}

.filter-bar button.active {
  background: var(--surface);
  color: var(--ink);
  box-shadow: 0 3px 10px rgba(23, 63, 58, 0.06);
  font-weight: 700;
}

.record-head,
.record-row {
  display: grid;
  grid-template-columns: minmax(150px, 1.15fr) minmax(135px, 1fr) minmax(210px, 1.5fr) 100px 150px;
  align-items: center;
  gap: 18px;
}

.record-head {
  padding: 13px 28px;
  border-bottom: 1px solid var(--line);
  color: #98a19c;
  font-size: 10px;
  letter-spacing: 0.05em;
}

.record-head span:last-child {
  text-align: right;
}

.record-list {
  position: relative;
  min-height: 220px;
}

.record-row {
  min-height: 92px;
  padding: 18px 28px;
  border-bottom: 1px solid #edf0eb;
  transition: background-color 170ms ease;
  animation: row-in 420ms calc(var(--record-index) * 45ms)
    cubic-bezier(0.22, 1, 0.36, 1) both;
}

.record-row:last-child {
  border-bottom: 0;
}

.record-row:hover {
  background: #fcfdf9;
}

.record-number,
.record-where,
.record-when {
  display: grid;
  gap: 5px;
  min-width: 0;
}

.record-number {
  grid-template-columns: 28px minmax(0, 1fr);
  align-items: center;
}

.record-number strong {
  color: #b2bbb5;
  font-size: 18px;
  font-variant-numeric: tabular-nums;
  font-weight: 550;
}

.record-number span,
.record-where span,
.record-when span {
  overflow: hidden;
  color: var(--muted);
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.record-where strong,
.record-when strong {
  overflow: hidden;
  color: var(--ink);
  font-size: 14px;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.record-when strong {
  font-variant-numeric: tabular-nums;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  width: fit-content;
  padding: 6px 9px;
  border-radius: 7px;
  font-size: 10px;
  font-weight: 650;
  white-space: nowrap;
}

.status-pill i {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
}

.status-0 {
  background: #f8eed5;
  color: #8c6415;
}

.status-1 {
  background: #dfeee8;
  color: #276454;
}

.status-2 {
  background: #e9eeea;
  color: #66736c;
}

.status-3 {
  background: #eeefec;
  color: #858d87;
}

.status-4 {
  background: #f6e7e4;
  color: var(--danger);
}

.record-actions {
  display: flex;
  justify-content: flex-end;
  gap: 6px;
}

.record-actions button {
  min-width: 48px;
  padding: 7px 10px;
  border-radius: 8px;
  cursor: pointer;
  font: inherit;
  font-size: 11px;
  font-weight: 650;
  transition: background-color 160ms ease, border-color 160ms ease;
}

.action-primary {
  border: 1px solid var(--ink);
  background: var(--ink);
  color: #fff;
}

.action-primary:hover {
  border-color: var(--teal);
  background: var(--teal);
}

.action-quiet {
  border: 1px solid var(--line);
  background: transparent;
  color: var(--muted);
}

.action-quiet:hover {
  border-color: #c7a09c;
  color: var(--danger);
}

.action-empty {
  color: #b0b7b2;
  font-size: 12px;
}

.records-empty {
  display: grid;
  justify-items: center;
  padding: 62px 24px 68px;
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

.records-empty h2 {
  margin-bottom: 7px;
  font-size: 18px;
}

.records-empty p {
  margin-bottom: 18px;
  color: var(--muted);
  font-size: 12px;
}

.records-empty a {
  padding: 8px 13px;
  border-radius: 8px;
  background: var(--ink);
  color: #fff;
  font-size: 11px;
  font-weight: 650;
  text-decoration: none;
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

@keyframes row-in {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 920px) {
  .record-head {
    display: none;
  }

  .record-row {
    grid-template-columns: 1fr auto;
    gap: 16px 18px;
    padding: 22px;
  }

  .record-number {
    grid-column: 1;
    grid-row: 1;
  }

  .record-status {
    grid-column: 2;
    grid-row: 1;
    justify-self: end;
  }

  .record-where {
    grid-column: 1;
    grid-row: 2;
  }

  .record-when {
    grid-column: 1;
    grid-row: 3;
  }

  .record-actions {
    grid-column: 2;
    grid-row: 2 / 4;
    align-self: end;
  }
}

@media (max-width: 640px) {
  .filter-bar {
    overflow-x: auto;
    padding: 13px 14px;
    scrollbar-width: none;
  }

  .filter-bar::-webkit-scrollbar {
    display: none;
  }

  .filter-bar button {
    flex: 0 0 auto;
  }

  .record-row {
    grid-template-columns: 1fr auto;
    padding: 19px 16px;
  }

  .record-when span {
    white-space: normal;
  }
}
</style>
