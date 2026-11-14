<template>
  <div class="page-shell home-page">
    <section class="booking-hero">
      <div class="hero-copy">
        <p class="hero-date">{{ dateDisplay }}</p>
        <h1>今天，<br />坐在哪里读书？</h1>
        <p class="hero-note">
          选定阅览室、日期和时段，再从座位图里挑一个合适的位置。
        </p>

        <div v-if="currentRoom" class="room-facts">
          <span>
            <el-icon><Location /></el-icon>
            {{ currentRoom.floor }}
          </span>
          <span>
            <el-icon><Clock /></el-icon>
            {{ currentRoom.openTime }}—{{ currentRoom.closeTime }}
          </span>
        </div>
      </div>

      <form class="booking-panel" @submit.prevent="querySeats">
        <div class="field field-room">
          <label for="room-select">阅览室</label>
          <el-select
            id="room-select"
            v-model="roomId"
            placeholder="请选择阅览室"
          >
            <el-option
              v-for="room in rooms"
              :key="room.id"
              :label="`${room.roomName}（${room.floor}）`"
              :value="room.id"
            />
          </el-select>
        </div>

        <div class="field">
          <label for="date-select">日期</label>
          <el-date-picker
            id="date-select"
            v-model="date"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
            :disabled-date="disabledBeforeToday"
            :clearable="false"
          />
        </div>

        <div class="field">
          <label for="slot-select">时段</label>
          <el-select id="slot-select" v-model="slotId" placeholder="请选择时段">
            <el-option
              v-for="slot in slots"
              :key="slot.id"
              :label="`${slot.slotName}（${slot.startTime}-${slot.endTime}）`"
              :value="slot.id"
            />
          </el-select>
        </div>

        <button class="search-action" type="submit">
          <el-icon><Search /></el-icon>
          <span>查询座位</span>
        </button>

        <p v-if="currentRoom?.description" class="room-note">
          {{ currentRoom.description }}
        </p>
      </form>
    </section>

    <section v-loading="loading" class="seat-stage surface">
      <header class="seat-stage-head">
        <div>
          <p class="stage-kicker">座位分布</p>
          <h2>{{ currentRoom?.roomName || '阅览室座位' }}</h2>
        </div>

        <div v-if="seats.length" class="availability">
          <div class="availability-count">
            <strong>{{ availableCount }}</strong>
            <span>/ {{ seats.length }} 个座位可选</span>
          </div>
          <div class="availability-track" aria-hidden="true">
            <span :style="{ width: `${availabilityRate}%` }"></span>
          </div>
        </div>
      </header>

      <div class="seat-toolbar">
        <p>点选绿色座位完成预约；横向滑动可查看整排座位。</p>
        <div class="legend" aria-label="座位状态图例">
          <span class="legend-item">
            <i class="legend-seat is-available"></i>
            可选
          </span>
          <span class="legend-item">
            <i class="legend-seat is-reserved"></i>
            已预约
          </span>
          <span class="legend-item">
            <i class="legend-seat is-off"></i>
            停用 / 维修
          </span>
          <span class="legend-item">
            <el-icon><Lightning /></el-icon>
            带电源
          </span>
        </div>
      </div>

      <el-empty
        v-if="!loading && !seats.length"
        description="当前条件下没有座位，试试更换日期或时段"
      />

      <div v-else class="seat-map">
        <div
          v-for="(row, rowIdx) in seatRows"
          :key="`${roomId}-${slotId}-${date}-${rowIdx}`"
          class="seat-row"
          :style="{ '--row-index': rowIdx }"
        >
          <div class="row-label">
            <span>第</span>
            <strong>{{ rowIdx + 1 }}</strong>
            <span>排</span>
          </div>
          <div class="row-seats">
            <button
              v-for="seat in row"
              :key="seat.id"
              type="button"
              class="seat"
              :class="seatClass(seat)"
              :disabled="!seatAvailable(seat)"
              :title="seatTitle(seat)"
              :aria-label="seatTitle(seat)"
              @click="onSeatClick(seat)"
            >
              <el-icon v-if="seat.hasPower === 1" class="power-icon">
                <Lightning />
              </el-icon>
              <span class="seat-no">{{ seat.seatNo }}</span>
              <span class="seat-state">{{ seatStateText(seat) }}</span>
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, h, onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Clock,
  Lightning,
  Location,
  Search
} from '@element-plus/icons-vue'
import { getRooms, getSlots, getSeats, reserve } from '../api'

const rooms = ref([])
const slots = ref([])
const seats = ref([])
const roomId = ref(null)
const slotId = ref(null)
const date = ref('')
const loading = ref(false)

const ZONE_MAP = { 0: '普通区', 1: '靠窗区', 2: '静音区', 3: '讨论区' }
const WEEKDAYS = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']

const currentRoom = computed(
  () => rooms.value.find((room) => room.id === roomId.value)
)

const currentSlot = computed(
  () => slots.value.find((slot) => slot.id === slotId.value)
)

const dateDisplay = computed(() => {
  const value = date.value || todayStr()
  const parsed = new Date(`${value}T00:00:00`)
  if (Number.isNaN(parsed.getTime())) return '选择日期'
  return `${parsed.getMonth() + 1}月${parsed.getDate()}日 · ${WEEKDAYS[parsed.getDay()]}`
})

const seatRows = computed(() => {
  const rowMap = new Map()
  for (const seat of seats.value) {
    if (!rowMap.has(seat.seatRow)) rowMap.set(seat.seatRow, [])
    rowMap.get(seat.seatRow).push(seat)
  }
  return [...rowMap.entries()]
    .sort(([rowA], [rowB]) => rowA - rowB)
    .map(([, row]) => row.sort((seatA, seatB) => seatA.seatCol - seatB.seatCol))
})

const availableCount = computed(
  () => seats.value.filter((seat) => seatAvailable(seat)).length
)

const availabilityRate = computed(() => {
  if (!seats.value.length) return 0
  return Math.round((availableCount.value / seats.value.length) * 100)
})

function todayStr() {
  const now = new Date()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  return `${now.getFullYear()}-${month}-${day}`
}

function disabledBeforeToday(value) {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return value.getTime() < today.getTime()
}

function seatAvailable(seat) {
  return !seat.reserved && seat.status === 0
}

function seatClass(seat) {
  if (seat.reserved) return 'is-reserved'
  if (seat.status !== 0) return 'is-off'
  return 'is-available'
}

function seatStateText(seat) {
  if (seat.reserved) return '已预约'
  if (seat.status === 1) return '维修'
  if (seat.status === 2) return '停用'
  return '可选'
}

function seatTitle(seat) {
  const zone = ZONE_MAP[seat.zone] || '普通区'
  const details = [`${seat.seatNo} 号座位`, zone]
  if (seat.hasPower === 1) details.push('带电源')
  if (seat.reserved) details.push('已被预约')
  if (seat.status === 1) details.push('维修中')
  if (seat.status === 2) details.push('已停用')
  return details.join('，')
}

async function querySeats() {
  if (!roomId.value || !slotId.value || !date.value) {
    ElMessage.warning('请先选择阅览室、日期与时段')
    return
  }

  loading.value = true
  try {
    const response = await getSeats({
      roomId: roomId.value,
      date: date.value,
      slotId: slotId.value
    })
    seats.value = response.data || []
  } finally {
    loading.value = false
  }
}

async function onSeatClick(seat) {
  if (!seatAvailable(seat)) return

  const slotText = currentSlot.value
    ? `${currentSlot.value.slotName}（${currentSlot.value.startTime}-${currentSlot.value.endTime}）`
    : '—'

  const summary = h(
    'div',
    { style: 'display:grid;gap:7px;line-height:1.65;color:#41534d' },
    [
      h('span', `阅览室：${currentRoom.value?.roomName || '—'}`),
      h('strong', { style: 'font-size:19px;color:#173f3a' }, `${seat.seatNo} 号座位`),
      h('span', `日期：${date.value}`),
      h('span', `时段：${slotText}`)
    ]
  )

  try {
    await ElMessageBox.confirm(summary, '确认这次预约？', {
      confirmButtonText: '确认预约',
      cancelButtonText: '再看看',
      type: 'info'
    })
  } catch {
    return
  }

  const response = await reserve({
    seatId: seat.id,
    slotId: slotId.value,
    date: date.value
  })
  ElMessage.success(response.data || '预约成功')
  await querySeats()
}

onMounted(async () => {
  date.value = todayStr()
  const [roomResponse, slotResponse] = await Promise.all([getRooms(), getSlots()])
  rooms.value = roomResponse.data || []
  slots.value = slotResponse.data || []
  if (rooms.value.length) roomId.value = rooms.value[0].id
  if (slots.value.length) slotId.value = slots.value[0].id
  await querySeats()
})
</script>

<style scoped>
.home-page {
  display: grid;
  gap: 24px;
}

.booking-hero {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 0.88fr) minmax(460px, 1.12fr);
  min-height: 330px;
  overflow: hidden;
  border-radius: 28px 28px 28px 8px;
  background: var(--ink);
  box-shadow: 0 28px 70px rgba(23, 63, 58, 0.16);
  animation: hero-enter 600ms cubic-bezier(0.22, 1, 0.36, 1) both;
}

.booking-hero::after {
  position: absolute;
  top: 0;
  left: 42%;
  width: 1px;
  height: 100%;
  background: rgba(255, 255, 255, 0.08);
  content: "";
  pointer-events: none;
}

.hero-copy {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 46px 48px;
  color: #fff;
}

.hero-date {
  margin-bottom: 20px;
  color: var(--lime);
  font-size: 13px;
  font-variant-numeric: tabular-nums;
  font-weight: 650;
  letter-spacing: 0.05em;
}

.hero-copy h1 {
  max-width: 420px;
  margin-bottom: 20px;
  font-size: clamp(38px, 4.4vw, 58px);
  font-weight: 760;
  letter-spacing: -0.055em;
  line-height: 1.08;
}

.hero-note {
  max-width: 360px;
  margin-bottom: 34px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  line-height: 1.8;
}

.room-facts {
  display: flex;
  flex-wrap: wrap;
  gap: 9px 20px;
  color: rgba(255, 255, 255, 0.78);
  font-size: 12px;
}

.room-facts span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.room-facts .el-icon {
  color: var(--lime);
}

.booking-panel {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-content: center;
  gap: 18px 14px;
  margin: 18px;
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 19px;
  background: var(--surface);
  box-shadow: 0 18px 46px rgba(6, 37, 33, 0.18);
}

.field {
  display: grid;
  gap: 8px;
  min-width: 0;
}

.field-room {
  grid-column: 1 / -1;
}

.field label {
  color: var(--ink);
  font-size: 12px;
  font-weight: 700;
}

.field :deep(.el-select),
.field :deep(.el-date-editor) {
  width: 100%;
}

.field :deep(.el-date-editor .el-input__wrapper) {
  width: 100%;
}

.search-action {
  grid-column: 1 / -1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 48px;
  margin-top: 3px;
  border: 0;
  border-radius: 11px;
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

.search-action:hover {
  background: var(--teal);
  box-shadow: 0 9px 22px rgba(44, 117, 104, 0.2);
  transform: translateY(-1px);
}

.search-action:active {
  transform: translateY(0) scale(0.99);
}

.room-note {
  grid-column: 1 / -1;
  margin: -4px 0 0;
  color: var(--muted);
  font-size: 11px;
  line-height: 1.6;
  text-align: center;
}

.seat-stage {
  position: relative;
  overflow: hidden;
  min-height: 300px;
  padding: 30px 32px 36px;
  border-radius: 22px;
  box-shadow: var(--shadow);
  animation: surface-enter 650ms 90ms cubic-bezier(0.22, 1, 0.36, 1) both;
}

.seat-stage-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--line);
}

.stage-kicker {
  margin-bottom: 6px;
  color: var(--teal);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
}

.seat-stage-head h2 {
  margin-bottom: 0;
  font-size: 26px;
  font-weight: 750;
  letter-spacing: -0.035em;
}

.availability {
  width: 190px;
  flex-shrink: 0;
  padding-top: 5px;
}

.availability-count {
  display: flex;
  align-items: baseline;
  justify-content: flex-end;
  gap: 5px;
  font-variant-numeric: tabular-nums;
}

.availability-count strong {
  font-size: 22px;
  line-height: 1;
}

.availability-count span {
  color: var(--muted);
  font-size: 11px;
}

.availability-track {
  height: 4px;
  margin-top: 9px;
  overflow: hidden;
  border-radius: 4px;
  background: var(--mist);
}

.availability-track span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: var(--teal);
  transition: width 500ms cubic-bezier(0.22, 1, 0.36, 1);
}

.seat-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 18px 0 8px;
}

.seat-toolbar p {
  margin: 0;
  color: var(--muted);
  font-size: 12px;
}

.legend {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 8px 15px;
  color: var(--muted);
  font-size: 11px;
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  white-space: nowrap;
}

.legend-seat {
  width: 17px;
  height: 14px;
  border: 1px solid transparent;
  border-radius: 5px 5px 3px 3px;
}

.legend-seat.is-available {
  border-color: #90b9a4;
  background: #e1efe5;
}

.legend-seat.is-reserved {
  border-color: #d1c8ba;
  background:
    repeating-linear-gradient(-45deg, #e9e3d9 0 3px, #f2eee7 3px 6px);
}

.legend-seat.is-off {
  border-color: #d6d8d3;
  background: #e9ebe7;
}

.seat-map {
  padding-top: 8px;
}

.seat-row {
  display: flex;
  align-items: center;
  min-width: max-content;
  padding: 13px 0;
  border-bottom: 1px dashed #e1e6df;
  animation: row-enter 460ms calc(160ms + var(--row-index) * 45ms)
    cubic-bezier(0.22, 1, 0.36, 1) both;
}

.seat-row:last-child {
  border-bottom: 0;
}

.row-label {
  position: sticky;
  left: 0;
  z-index: 2;
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 3px;
  width: 66px;
  flex: 0 0 66px;
  padding-right: 14px;
  background: var(--surface);
  color: var(--muted);
  font-size: 10px;
}

.row-label strong {
  color: var(--ink);
  font-size: 17px;
  font-variant-numeric: tabular-nums;
  font-weight: 750;
}

.row-seats {
  display: flex;
  flex-wrap: nowrap;
  gap: 10px;
}

.seat {
  position: relative;
  width: 64px;
  height: 54px;
  flex: 0 0 64px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  padding: 0;
  overflow: hidden;
  border: 1px solid #90b9a4;
  border-radius: 8px 8px 14px 14px;
  color: #24563f;
  background: #e1efe5;
  cursor: pointer;
  font: inherit;
  transition:
    background-color 170ms ease,
    border-color 170ms ease,
    box-shadow 170ms ease,
    color 170ms ease,
    transform 170ms cubic-bezier(0.22, 1, 0.36, 1);
}

.seat::after {
  position: absolute;
  right: 7px;
  bottom: 3px;
  left: 7px;
  height: 2px;
  border-radius: 2px;
  background: rgba(36, 86, 63, 0.15);
  content: "";
}

.seat.is-available:hover {
  border-color: var(--ink);
  background: var(--ink);
  color: #fff;
  box-shadow: 0 10px 25px rgba(23, 63, 58, 0.22);
  transform: translateY(-3px);
}

.seat.is-available:hover::after {
  background: rgba(255, 255, 255, 0.2);
}

.seat.is-reserved {
  border-color: #d1c8ba;
  color: #8f877b;
  background:
    repeating-linear-gradient(-45deg, #e9e3d9 0 4px, #f2eee7 4px 8px);
  cursor: not-allowed;
}

.seat.is-off {
  border-color: #d6d8d3;
  color: #9a9f99;
  background: #e9ebe7;
  cursor: not-allowed;
}

.power-icon {
  position: absolute;
  top: 5px;
  right: 6px;
  color: var(--gold);
  font-size: 11px;
}

.seat-no {
  font-size: 13px;
  font-variant-numeric: tabular-nums;
  font-weight: 750;
  line-height: 1;
}

.seat-state {
  font-size: 9px;
  line-height: 1;
  opacity: 0.7;
}

.seat:disabled {
  opacity: 1;
}

.seat-stage :deep(.el-empty) {
  padding: 58px 0 40px;
}

.seat-stage :deep(.el-loading-mask) {
  background: rgba(255, 254, 250, 0.82);
  backdrop-filter: blur(3px);
}

@keyframes hero-enter {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes surface-enter {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes row-enter {
  from {
    opacity: 0;
    transform: translateX(-8px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@media (max-width: 1020px) {
  .booking-hero {
    grid-template-columns: 1fr;
  }

  .booking-hero::after {
    display: none;
  }

  .hero-copy {
    padding: 38px 38px 20px;
  }

  .hero-copy h1 {
    font-size: 46px;
  }

  .booking-panel {
    margin: 12px 18px 18px;
  }
}

@media (max-width: 760px) {
  .home-page {
    gap: 16px;
  }

  .booking-hero {
    border-radius: 22px 22px 22px 7px;
  }

  .hero-copy {
    padding: 30px 24px 14px;
  }

  .hero-copy h1 {
    margin-bottom: 14px;
    font-size: 38px;
  }

  .hero-note {
    margin-bottom: 22px;
    font-size: 13px;
  }

  .booking-panel {
    grid-template-columns: 1fr;
    margin: 10px 12px 12px;
    padding: 22px;
  }

  .field-room {
    grid-column: auto;
  }

  .seat-stage {
    padding: 22px 18px 26px;
    border-radius: 18px;
  }

  .seat-stage-head {
    align-items: flex-end;
  }

  .seat-stage-head h2 {
    font-size: 22px;
  }

  .availability {
    width: 140px;
  }

  .availability-count span {
    font-size: 10px;
  }

  .seat-toolbar {
    align-items: flex-start;
    flex-direction: column;
    gap: 10px;
  }

  .legend {
    justify-content: flex-start;
  }

  .seat-map {
    margin-right: -18px;
    overflow-x: auto;
    scrollbar-color: var(--line) transparent;
  }

  .row-label {
    margin-left: 0;
  }
}

@media (max-width: 430px) {
  .hero-copy h1 {
    font-size: 34px;
  }

  .room-facts {
    align-items: flex-start;
    flex-direction: column;
  }

  .seat-stage-head {
    align-items: flex-start;
    flex-direction: column;
    gap: 14px;
  }

  .availability {
    width: 100%;
  }

  .availability-count {
    justify-content: flex-start;
  }
}
</style>
