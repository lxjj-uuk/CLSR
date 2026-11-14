package com.example.libraryseat.dto;

import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

@Data
public class ReservationVO {
    private Integer id;
    private String reserveNo;
    private String seatNo;
    private String roomName;
    private String slotName;
    private LocalDate reserveDate;
    private LocalTime startTime;
    private LocalTime endTime;
    private Integer status;
    private LocalDateTime checkInTime;
    private LocalDateTime checkOutTime;
}
