package com.example.libraryseat.service;

import com.example.libraryseat.dto.ReservationVO;
import com.example.libraryseat.entity.Reservation;
import com.example.libraryseat.entity.Seat;
import com.example.libraryseat.mapper.BlacklistMapper;
import com.example.libraryseat.mapper.ReservationMapper;
import com.example.libraryseat.mapper.SeatMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;

@Service
public class ReservationService {
    @Autowired private ReservationMapper reservationMapper;
    @Autowired private SeatMapper seatMapper;
    @Autowired private BlacklistMapper blacklistMapper;

    @Transactional
    public String reserve(Integer userId, Integer seatId, Integer slotId, LocalDate date) {
        if (blacklistMapper.countActive(userId) > 0) {
            return "你已被列入黑名单，暂不可预约";
        }
        Seat seat = seatMapper.findById(seatId);
        if (seat == null || seat.getStatus() != 0) {
            return "该座位不可用或正在维修";
        }
        if (date.isBefore(LocalDate.now())) {
            return "不能预约过去的日期";
        }
        if (reservationMapper.countSeatReserved(seatId, date, slotId) > 0) {
            return "该座位此时段已被预约";
        }
        if (reservationMapper.countUserSlot(userId, date, slotId) > 0) {
            return "你在该时段已有预约，不能重复预约";
        }

        Reservation r = new Reservation();
        r.setReserveNo(generateNo());
        r.setUserId(userId);
        r.setSeatId(seatId);
        r.setRoomId(seat.getRoomId());
        r.setSlotId(slotId);
        r.setReserveDate(date);
        reservationMapper.insert(r);
        return "success";
    }

    public List<ReservationVO> myReserves(Integer userId) {
        return reservationMapper.findVOByUser(userId);
    }

    @Transactional
    public String cancel(Integer id, Integer userId) {
        return reservationMapper.cancel(id, userId) > 0 ? "success" : "取消失败";
    }

    @Transactional
    public String checkIn(Integer id, Integer userId) {
        return reservationMapper.checkIn(id, userId) > 0 ? "success" : "签到失败，可能已签到或预约已失效";
    }

    @Transactional
    public String checkOut(Integer id, Integer userId) {
        return reservationMapper.checkOut(id, userId) > 0 ? "success" : "签退失败";
    }

    // 预约单号：RES + 时间戳 + 3位随机
    private String generateNo() {
        String time = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMddHHmmss"));
        int rand = ThreadLocalRandom.current().nextInt(100, 1000);
        return "RES" + time + rand;
    }
}
