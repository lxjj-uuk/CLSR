package com.example.libraryseat.entity;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class Blacklist {
    private Integer id;
    private Integer userId;
    private String reason;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private Integer status;     // 0生效中 1已解除
    private LocalDateTime createTime;
}
