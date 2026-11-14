package com.example.libraryseat.mapper;

import com.example.libraryseat.dto.ReservationVO;
import com.example.libraryseat.entity.Reservation;
import org.apache.ibatis.annotations.*;
import java.time.LocalDate;
import java.util.List;

@Mapper
public interface ReservationMapper {

    @Insert("INSERT INTO reservation(reserve_no,user_id,seat_id,room_id,slot_id,reserve_date,status) " +
            "VALUES(#{reserveNo},#{userId},#{seatId},#{roomId},#{slotId},#{reserveDate},0)")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(Reservation r);

    // 该座位该日期该时段是否已有有效预约
    @Select("SELECT COUNT(*) FROM reservation " +
            "WHERE seat_id = #{seatId} AND reserve_date = #{date} AND slot_id = #{slotId} AND status IN (0,1)")
    int countSeatReserved(@Param("seatId") Integer seatId,
                          @Param("date") LocalDate date,
                          @Param("slotId") Integer slotId);

    // 该用户该日期该时段是否已有预约（防同时段重复约）
    @Select("SELECT COUNT(*) FROM reservation " +
            "WHERE user_id = #{userId} AND reserve_date = #{date} AND slot_id = #{slotId} AND status IN (0,1)")
    int countUserSlot(@Param("userId") Integer userId,
                      @Param("date") LocalDate date,
                      @Param("slotId") Integer slotId);

    // 我的预约（联表带座位号/阅览室/时段名）
    @Select("SELECT r.id, r.reserve_no, s.seat_no, rm.room_name, t.slot_name, " +
            "r.reserve_date, t.start_time, t.end_time, r.status, r.check_in_time, r.check_out_time " +
            "FROM reservation r " +
            "JOIN seat s ON r.seat_id = s.id " +
            "JOIN reading_room rm ON r.room_id = rm.id " +
            "JOIN time_slot t ON r.slot_id = t.id " +
            "WHERE r.user_id = #{userId} ORDER BY r.reserve_date DESC, r.id DESC")
    List<ReservationVO> findVOByUser(@Param("userId") Integer userId);

    @Select("SELECT * FROM reservation WHERE id = #{id}")
    Reservation findById(@Param("id") Integer id);

    @Update("UPDATE reservation SET status = 3, cancel_time = NOW() " +
            "WHERE id = #{id} AND user_id = #{userId} AND status = 0")
    int cancel(@Param("id") Integer id, @Param("userId") Integer userId);

    @Update("UPDATE reservation SET status = 1, check_in_time = NOW() " +
            "WHERE id = #{id} AND user_id = #{userId} AND status = 0")
    int checkIn(@Param("id") Integer id, @Param("userId") Integer userId);

    @Update("UPDATE reservation SET status = 2, check_out_time = NOW() " +
            "WHERE id = #{id} AND user_id = #{userId} AND status = 1")
    int checkOut(@Param("id") Integer id, @Param("userId") Integer userId);
}
