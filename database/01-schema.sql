DROP DATABASE IF EXISTS library_seat;
CREATE DATABASE library_seat DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE library_seat;

CREATE TABLE user (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(32) NOT NULL UNIQUE,
  password VARCHAR(64) NOT NULL,
  name VARCHAR(32) NOT NULL,
  role TINYINT NOT NULL DEFAULT 0 COMMENT '0学生 1管理员',
  phone VARCHAR(20) DEFAULT NULL,
  status TINYINT NOT NULL DEFAULT 0 COMMENT '0正常 1禁用',
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE reading_room (
  id INT PRIMARY KEY AUTO_INCREMENT,
  room_name VARCHAR(64) NOT NULL,
  floor VARCHAR(16) DEFAULT NULL,
  capacity INT DEFAULT 0,
  open_time TIME NOT NULL,
  close_time TIME NOT NULL,
  description VARCHAR(255) DEFAULT NULL,
  status TINYINT NOT NULL DEFAULT 0 COMMENT '0开放 1关闭',
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE seat (
  id INT PRIMARY KEY AUTO_INCREMENT,
  room_id INT NOT NULL,
  seat_no VARCHAR(16) NOT NULL,
  seat_row INT NOT NULL,
  seat_col INT NOT NULL,
  zone TINYINT NOT NULL DEFAULT 0 COMMENT '0普通 1靠窗 2静音 3讨论',
  has_power TINYINT NOT NULL DEFAULT 0,
  status TINYINT NOT NULL DEFAULT 0 COMMENT '0正常 1维修 2停用',
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_room (room_id)
) ENGINE=InnoDB;

CREATE TABLE time_slot (
  id INT PRIMARY KEY AUTO_INCREMENT,
  slot_name VARCHAR(32) NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  status TINYINT NOT NULL DEFAULT 0
) ENGINE=InnoDB;

CREATE TABLE reservation (
  id INT PRIMARY KEY AUTO_INCREMENT,
  reserve_no VARCHAR(32) NOT NULL UNIQUE,
  user_id INT NOT NULL,
  seat_id INT NOT NULL,
  room_id INT NOT NULL,
  slot_id INT NOT NULL,
  reserve_date DATE NOT NULL,
  status TINYINT NOT NULL DEFAULT 0 COMMENT '0已预约 1已签到 2已完成 3已取消 4违约',
  check_in_time DATETIME DEFAULT NULL,
  check_out_time DATETIME DEFAULT NULL,
  cancel_time DATETIME DEFAULT NULL,
  remark VARCHAR(255) DEFAULT NULL,
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_seat_slot (seat_id, reserve_date, slot_id),
  KEY idx_user (user_id)
) ENGINE=InnoDB;

CREATE TABLE notice (
  id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(128) NOT NULL,
  content TEXT,
  admin_id INT DEFAULT NULL,
  view_count INT NOT NULL DEFAULT 0,
  status TINYINT NOT NULL DEFAULT 0 COMMENT '0已发布 1草稿',
  publish_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE violation (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  reservation_id INT DEFAULT NULL,
  type TINYINT NOT NULL DEFAULT 0 COMMENT '0未签到 1提前离开 2其他',
  description VARCHAR(255) DEFAULT NULL,
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE blacklist (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  reason VARCHAR(255) DEFAULT NULL,
  start_time DATETIME NOT NULL,
  end_time DATETIME DEFAULT NULL,
  status TINYINT NOT NULL DEFAULT 0 COMMENT '0生效中 1已解除',
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

INSERT INTO user(username,password,name,role,phone) VALUES
('admin','123456','李明','1','13800000001'),
('2024001','123456','张涵','0','13800000002'),
('2024002','123456','王雪','0','13800000003');

INSERT INTO reading_room(room_name,floor,capacity,open_time,close_time,description) VALUES
('一楼综合阅览室','一楼',40,'08:00:00','22:00:00','靠近入口，配备自助借还机'),
('三楼自然科学阅览室','三楼',30,'08:30:00','21:30:00','安静区域，可查阅期刊');

INSERT INTO time_slot(slot_name,start_time,end_time) VALUES
('上午场','08:00:00','10:00:00'),
('中午场','10:00:00','12:00:00'),
('下午场','14:00:00','16:00:00'),
('晚间场','18:00:00','20:00:00');

INSERT INTO notice(title,content,admin_id,view_count,status,publish_time) VALUES
('关于阅览室座位预约规则调整的通知','为提升座位资源利用率，自本周起预约保留时长由 30 分钟调整为 20 分钟，请读者按时签到，逾期未签到将记入违约记录。','1',128,0,'2026-10-08 09:00:00'),
('国庆假期阅览室开放安排','10 月 1 日至 10 月 3 日一楼综合阅览室正常开放（08:00-18:00），三楼自然科学阅览室闭馆检修。','1',96,0,'2026-09-27 16:30:00'),
('座位预约系统上线试运行公告','校园图书馆座位预约系统已上线试运行，读者可通过网页端查询实时座位状态并完成预约。','1',215,0,'2026-09-15 10:20:00');
