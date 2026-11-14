package com.example.libraryseat.service;

import com.example.libraryseat.entity.Notice;
import com.example.libraryseat.mapper.NoticeMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NoticeService {
    @Autowired
    private NoticeMapper noticeMapper;

    public List<Notice> list() {
        return noticeMapper.findPublished();
    }

    public Notice detail(Integer id) {
        return noticeMapper.findById(id);
    }
}
