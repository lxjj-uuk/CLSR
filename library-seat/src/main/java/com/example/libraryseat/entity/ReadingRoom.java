package com.example.libraryseat.entity;

import lombok.Data;
import java.time.LocalDateTime;
import java.time.LocalTime;

@Data
public class ReadingRoom {
    private Integer id;
    private String roomName;
    private String floor;
    private Integer capacity;
    private LocalTime openTime;
    private LocalTime closeTime;
    private String description;
    private Integer status;     // 0开放 1关闭
    private LocalDateTime createTime;
}
