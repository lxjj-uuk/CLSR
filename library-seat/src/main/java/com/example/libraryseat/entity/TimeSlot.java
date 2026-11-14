package com.example.libraryseat.entity;

import lombok.Data;
import java.time.LocalTime;

@Data
public class TimeSlot {
    private Integer id;
    private String slotName;
    private LocalTime startTime;
    private LocalTime endTime;
    private Integer status;
}
