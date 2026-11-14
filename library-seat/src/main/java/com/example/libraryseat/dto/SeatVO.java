package com.example.libraryseat.dto;

import com.example.libraryseat.entity.Seat;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class SeatVO extends Seat {
    private String roomName;
    private Boolean reserved;   // 该时段是否已被预约
}
