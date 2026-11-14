package com.example.libraryseat.service;

import com.example.libraryseat.dto.SeatVO;
import com.example.libraryseat.entity.ReadingRoom;
import com.example.libraryseat.entity.Seat;
import com.example.libraryseat.entity.TimeSlot;
import com.example.libraryseat.mapper.ReadingRoomMapper;
import com.example.libraryseat.mapper.ReservationMapper;
import com.example.libraryseat.mapper.SeatMapper;
import com.example.libraryseat.mapper.TimeSlotMapper;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Service
public class SeatService {
    @Autowired private ReadingRoomMapper roomMapper;
    @Autowired private TimeSlotMapper slotMapper;
    @Autowired private SeatMapper seatMapper;
    @Autowired private ReservationMapper reservationMapper;

    public List<ReadingRoom> rooms() {
        return roomMapper.findAllOpen();
    }

    public List<TimeSlot> slots() {
        return slotMapper.findAllEnabled();
    }

    public List<SeatVO> seats(Integer roomId, LocalDate date, Integer slotId) {
        List<Seat> seats = seatMapper.findNormalByRoom(roomId);
        ReadingRoom room = roomMapper.findById(roomId);
        List<SeatVO> result = new ArrayList<>();
        for (Seat s : seats) {
            SeatVO vo = new SeatVO();
            BeanUtils.copyProperties(s, vo);
            vo.setRoomName(room != null ? room.getRoomName() : "");
            vo.setReserved(reservationMapper.countSeatReserved(s.getId(), date, slotId) > 0);
            result.add(vo);
        }
        return result;
    }
}
