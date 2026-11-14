package com.example.libraryseat.controller;

import com.example.libraryseat.common.Result;
import com.example.libraryseat.dto.ReservationVO;
import com.example.libraryseat.dto.SeatVO;
import com.example.libraryseat.entity.Notice;
import com.example.libraryseat.entity.ReadingRoom;
import com.example.libraryseat.entity.TimeSlot;
import com.example.libraryseat.entity.User;
import com.example.libraryseat.service.NoticeService;
import com.example.libraryseat.service.ReservationService;
import com.example.libraryseat.service.SeatService;
import com.example.libraryseat.service.UserService;
import com.example.libraryseat.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class ApiController {

    @Autowired
    private UserService userService;

    @Autowired
    private SeatService seatService;

    @Autowired
    private ReservationService reservationService;

    @Autowired
    private NoticeService noticeService;

    @Autowired
    private JwtUtil jwtUtil;

    // 登录（不拦截）
    @PostMapping("/login")
    public Result<Map<String, Object>> login(@RequestBody Map<String, String> body) {
        User user = userService.login(body.get("username"), body.get("password"));
        if (user == null) {
            return Result.error("账号或密码错误");
        }
        String token = jwtUtil.create(user.getId(), user.getUsername(), user.getRole());

        Map<String, Object> data = new HashMap<>();
        data.put("token", token);
        data.put("username", user.getUsername());
        data.put("realName", user.getName());
        data.put("role", user.getRole());
        return Result.success(data);
    }

    // 阅览室列表
    @GetMapping("/rooms")
    public Result<List<ReadingRoom>> rooms() {
        return Result.success(seatService.rooms());
    }

    // 时段列表
    @GetMapping("/slots")
    public Result<List<TimeSlot>> slots() {
        return Result.success(seatService.slots());
    }

    // 座位列表：/api/seats?roomId=1&date=2026-10-11&slotId=1
    @GetMapping("/seats")
    public Result<List<SeatVO>> seats(@RequestParam Integer roomId,
                                      @RequestParam String date,
                                      @RequestParam Integer slotId) {
        return Result.success(seatService.seats(roomId, LocalDate.parse(date), slotId));
    }

    // 预约
    @PostMapping("/reserve")
    public Result<String> reserve(@RequestBody Map<String, Object> body, HttpServletRequest request) {
        Integer userId = (Integer) request.getAttribute("userId");
        Integer seatId = ((Number) body.get("seatId")).intValue();
        Integer slotId = ((Number) body.get("slotId")).intValue();
        LocalDate date = LocalDate.parse((String) body.get("date"));

        String r = reservationService.reserve(userId, seatId, slotId, date);
        return "success".equals(r) ? Result.success("预约成功") : Result.error(r);
    }

    // 我的预约
    @GetMapping("/my/reservations")
    public Result<List<ReservationVO>> myReservations(HttpServletRequest request) {
        Integer userId = (Integer) request.getAttribute("userId");
        return Result.success(reservationService.myReserves(userId));
    }

    // 取消预约
    @PostMapping("/cancel/{id}")
    public Result<String> cancel(@PathVariable Integer id, HttpServletRequest request) {
        Integer userId = (Integer) request.getAttribute("userId");
        String r = reservationService.cancel(id, userId);
        return "success".equals(r) ? Result.success("取消成功") : Result.error(r);
    }

    // 签到
    @PostMapping("/checkin/{id}")
    public Result<String> checkin(@PathVariable Integer id, HttpServletRequest request) {
        Integer userId = (Integer) request.getAttribute("userId");
        String r = reservationService.checkIn(id, userId);
        return "success".equals(r) ? Result.success("签到成功") : Result.error(r);
    }

    // 签退
    @PostMapping("/checkout/{id}")
    public Result<String> checkout(@PathVariable Integer id, HttpServletRequest request) {
        Integer userId = (Integer) request.getAttribute("userId");
        String r = reservationService.checkOut(id, userId);
        return "success".equals(r) ? Result.success("签退成功") : Result.error(r);
    }

    // 公告列表
    @GetMapping("/notices")
    public Result<List<Notice>> notices() {
        return Result.success(noticeService.list());
    }

    // 公告详情
    @GetMapping("/notices/{id}")
    public Result<Notice> noticeDetail(@PathVariable Integer id) {
        return Result.success(noticeService.detail(id));
    }
}
