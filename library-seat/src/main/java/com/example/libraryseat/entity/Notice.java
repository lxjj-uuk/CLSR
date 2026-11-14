package com.example.libraryseat.entity;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class Notice {
    private Integer id;
    private String title;
    private String content;
    private Integer adminId;
    private Integer viewCount;
    private Integer status;
    private LocalDateTime publishTime;
}
