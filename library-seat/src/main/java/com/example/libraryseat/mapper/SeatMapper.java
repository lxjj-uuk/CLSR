package com.example.libraryseat.mapper;

import com.example.libraryseat.entity.Seat;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface SeatMapper {
    @Select("SELECT * FROM seat WHERE room_id = #{roomId} AND status = 0 ORDER BY seat_row, seat_col")
    List<Seat> findNormalByRoom(@Param("roomId") Integer roomId);

    @Select("SELECT * FROM seat WHERE id = #{id}")
    Seat findById(@Param("id") Integer id);
}
