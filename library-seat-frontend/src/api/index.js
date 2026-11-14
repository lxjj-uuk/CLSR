import request from './request'

// 1. 登录
export function login(data) {
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

// 2. 阅览室列表
export function getRooms() {
  return request({ url: '/rooms', method: 'get' })
}

// 3. 时段列表
export function getSlots() {
  return request({ url: '/slots', method: 'get' })
}

// 4. 座位列表 params: { roomId, date: 'yyyy-MM-dd', slotId }
export function getSeats(params) {
  return request({ url: '/seats', method: 'get', params })
}

// 5. 预约 data: { seatId, slotId, date }
export function reserve(data) {
  return request({ url: '/reserve', method: 'post', data })
}

// 6. 我的预约
export function getMyReservations() {
  return request({ url: '/my/reservations', method: 'get' })
}

// 7. 取消预约
export function cancelReservation(id) {
  return request({ url: `/cancel/${id}`, method: 'post' })
}

// 8. 签到
export function checkin(id) {
  return request({ url: `/checkin/${id}`, method: 'post' })
}

// 9. 签退
export function checkout(id) {
  return request({ url: `/checkout/${id}`, method: 'post' })
}

// 10. 公告列表
export function getNotices() {
  return request({ url: '/notices', method: 'get' })
}

// 11. 公告详情
export function getNoticeDetail(id) {
  return request({ url: `/notices/${id}`, method: 'get' })
}
