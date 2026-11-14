package com.example.libraryseat.mapper;

import org.apache.ibatis.annotations.*;

@Mapper
public interface BlacklistMapper {
    @Select("SELECT COUNT(*) FROM blacklist " +
            "WHERE user_id = #{userId} AND status = 0 " +
            "AND start_time <= NOW() AND (end_time IS NULL OR end_time > NOW())")
    int countActive(@Param("userId") Integer userId);
}
