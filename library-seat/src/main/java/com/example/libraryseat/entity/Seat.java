package com.example.libraryseat.entity;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class Seat {
    private Integer id;
    private Integer roomId;
    private String seatNo;
    private Integer seatRow;
    private Integer seatCol;
    private Integer zone;       // 0普通 1靠窗 2静音 3讨论
    private Integer hasPower;   // 0否 1是
    private Integer status;     // 0正常 1维修 2停用
    private LocalDateTime createTime;
}
