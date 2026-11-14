package com.example.libraryseat.mapper;

import com.example.libraryseat.entity.User;
import org.apache.ibatis.annotations.*;

@Mapper
public interface UserMapper {
    @Select("SELECT * FROM `user` WHERE username = #{username} AND password = #{password} AND status = 0")
    User login(@Param("username") String username, @Param("password") String password);

    @Select("SELECT * FROM `user` WHERE id = #{id}")
    User findById(@Param("id") Integer id);
}
