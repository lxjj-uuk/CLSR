package com.example.libraryseat.entity;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class Violation {
    private Integer id;
    private Integer userId;
    private Integer reservationId;
    private Integer type;       // 0未签到 1提前离开 2其他
    private String description;
    private LocalDateTime createTime;
}
