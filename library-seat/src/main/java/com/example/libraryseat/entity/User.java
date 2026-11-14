package com.example.libraryseat.entity;

import lombok.Data;

@Data
public class User {
    private Integer id;
    private String username;
    private String password;
    private String name;
    private Integer role;
    private String phone;
}
