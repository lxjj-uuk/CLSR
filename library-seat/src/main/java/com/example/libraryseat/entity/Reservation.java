package com.example.libraryseat.entity;

import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
public class Reservation {
    private Integer id;
    private String reserveNo;
    private Integer userId;
    private Integer seatId;
    private Integer roomId;
    private Integer slotId;
    private LocalDate reserveDate;
    private Integer status;     // 0已预约 1已签到 2已完成 3已取消 4违约
    private LocalDateTime checkInTime;
    private LocalDateTime checkOutTime;
    private LocalDateTime cancelTime;
    private String remark;
    private LocalDateTime createTime;
}
