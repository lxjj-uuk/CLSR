package com.example.libraryseat.mapper;

import com.example.libraryseat.entity.Notice;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface NoticeMapper {
    @Select("SELECT * FROM notice WHERE status = 0 ORDER BY publish_time DESC")
    List<Notice> findPublished();

    @Select("SELECT * FROM notice WHERE id = #{id}")
    Notice findById(@Param("id") Integer id);
}
