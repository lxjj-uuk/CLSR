# CLSR 校园图书馆座位预约系统

基于 Spring Boot、MyBatis、MySQL、Vue 3 和 Element Plus 的图书馆座位预约系统，包含座位查询、预约、签到、签退、取消、公告查看和 JWT 鉴权等功能。

## 项目结构

```text
CLSR/
├── library-seat/                 # Spring Boot 后端
├── library-seat-frontend/        # Vue 3 前端
├── database/                     # MySQL 建表与演示数据
├── docs/                         # 课程设计报告与图表
├── docker-compose.yml            # 本地 MySQL
├── .env.example                  # 环境变量模板
└── README.md
```

## 环境要求

| 组件 | 版本 |
| --- | --- |
| JDK | 17 |
| Maven | 3.8+ |
| Node.js | 18+ |
| npm | 9+ |
| MySQL | 8.0 |
| Docker（可选） | 20+，用于快速启动 MySQL |

后端依赖版本由 `library-seat/pom.xml` 锁定，前端依赖由 `library-seat-frontend/package-lock.json` 锁定。

## 快速启动

### 1. 配置环境变量

复制模板并填写自己的值：

```powershell
Copy-Item .env.example .env
```

至少需要修改以下变量：

- `DB_URL`：MySQL JDBC 连接地址
- `DB_USERNAME`：数据库用户名
- `DB_PASSWORD`：数据库密码
- `JWT_SECRET`：至少 32 字节的随机签名密钥

Docker 方式还会使用 `MYSQL_DATABASE`、`MYSQL_USER`、`MYSQL_PASSWORD` 和 `MYSQL_ROOT_PASSWORD`。`.env` 已被 Git 忽略，不要提交真实凭据。

### 2. 启动 MySQL

使用 Docker：

```powershell
docker compose up -d
```

容器首次创建时会自动执行 `database/01-schema.sql`、`02-seed.sql` 和 `03-demo-reservations.sql`。如果数据卷已存在，初始化脚本不会再次执行。

也可以使用本机 MySQL，依次导入：

```powershell
mysql -u root -p < database/01-schema.sql
mysql -u root -p < database/02-seed.sql
mysql -u root -p < database/03-demo-reservations.sql
```

### 3. 启动后端

在 PowerShell 中先将 `.env` 中的值设置为当前进程环境变量，再运行 Maven：

```powershell
$env:DB_URL="jdbc:mysql://localhost:3306/library_seat?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai&useSSL=false&allowPublicKeyRetrieval=true"
$env:DB_USERNAME="library_seat"
$env:DB_PASSWORD="你的数据库密码"
$env:JWT_SECRET="至少32字节的随机字符串"

Set-Location library-seat
mvn spring-boot:run
```

后端默认地址为 <http://localhost:8080>，接口统一以 `/api` 开头。

### 4. 启动前端

另开一个终端：

```powershell
Set-Location library-seat-frontend
npm install
npm run dev
```

浏览器访问 <http://localhost:5175>。Vite 开发服务器会把 `/api` 代理到 `http://localhost:8080`。

## 演示账号

| 角色 | 账号 | 密码 |
| --- | --- | --- |
| 学生 | `2024001` | `123456` |
| 管理员 | `admin` | `123456` |

这些账号仅用于本地课程演示。正式部署前应更换密码、移除演示数据，并将数据库中的明文密码迁移为 BCrypt 等安全哈希。

## 构建

```powershell
Set-Location library-seat
mvn clean package

Set-Location ..\library-seat-frontend
npm ci
npm run build
```

后端产物位于 `library-seat/target/library-seat-0.0.1-SNAPSHOT.jar`，前端产物位于 `library-seat-frontend/dist/`。

## 配置说明

后端读取以下环境变量：

| 变量 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `DB_URL` | 否 | 本地 `library_seat` JDBC 地址 | MySQL 连接串 |
| `DB_USERNAME` | 否 | `root` | MySQL 用户名 |
| `DB_PASSWORD` | 是 | 无 | MySQL 密码 |
| `JWT_SECRET` | 是 | 无 | JWT HS256 密钥，至少 32 字节 |
| `SERVER_PORT` | 否 | `8080` | 后端端口 |

## 安全提示

- 不要把 `.env`、IDE 数据源配置或真实 Token 提交到 GitHub。
- 生产环境应使用独立数据库账户、TLS、密钥管理服务和强密码。
- 当前课程版本按明文密码校验登录；生产化前需要升级密码哈希、登录限流和审计日志。

## 课程设计报告

项目根目录包含课程设计报告 PDF 和 DOCX，图表源文件位于 `docs/diagrams/`。
