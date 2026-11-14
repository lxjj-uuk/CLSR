package com.example.libraryseat.mapper;

import com.example.libraryseat.entity.TimeSlot;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface TimeSlotMapper {
    @Select("SELECT * FROM time_slot WHERE status = 0 ORDER BY id")
    List<TimeSlot> findAllEnabled();
}
