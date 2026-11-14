package com.example.libraryseat.mapper;

import com.example.libraryseat.entity.ReadingRoom;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface ReadingRoomMapper {
    @Select("SELECT * FROM reading_room WHERE status = 0 ORDER BY id")
    List<ReadingRoom> findAllOpen();

    @Select("SELECT * FROM reading_room WHERE id = #{id}")
    ReadingRoom findById(@Param("id") Integer id);
}
