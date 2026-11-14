# 校园图书馆座位预约系统 · 前端

基于 **Vue3 + Vite + Element Plus + Pinia + Vue Router + Axios** 的学生端单页应用。

## 功能

- 登录 / 退出（JWT，登录态本地持久化，路由守卫拦截未登录）
- 选座预约：选择阅览室、日期、时段，按座位分布图选座并预约
- 我的预约：查看预约记录，按状态进行 签到 / 签退 / 取消
- 馆内公告：公告列表与公告详情

## 运行步骤

1. 先确保后端（Spring Boot，端口 **8080**）已启动。
2. 解压本工程后进入目录：

   ```bash
   cd library-seat-frontend
   ```

3. 安装依赖：

   ```bash
   npm install
   ```

4. 启动开发服务器：

   ```bash
   npm run dev
   ```

   也可以在 VS Code 中按 `F5`，选择“启动前端并打开浏览器”。

5. 浏览器访问：<http://localhost:5175>

> 前端开发服务器已配置代理：`/api` → `http://localhost:8080`，无需额外跨域设置。

## 测试账号

| 角色 | 账号 | 密码 |
| --- | --- | --- |
| 学生 | `2024001` | `123456` |
| 管理员 | `admin` | `123456` |

## 构建生产版本

```bash
npm run build
```

构建产物默认输出到 `dist/`。

## 目录结构

```
library-seat-frontend
├── index.html
├── package.json
├── vite.config.js          # 端口 5173，/api 代理到 8080
└── src
    ├── main.js             # 入口，注册 Pinia / Router / Element Plus
    ├── App.vue
    ├── api
    │   ├── request.js      # axios 实例与拦截器（自动带 Bearer、统一错误处理）
    │   └── index.js        # 接口函数
    ├── router/index.js     # 路由与登录守卫
    ├── stores/user.js      # 用户登录态（Pinia + localStorage）
    ├── layout/MainLayout.vue
    ├── styles/index.css
    └── views
        ├── Login.vue
        ├── Home.vue
        ├── MyReservations.vue
        ├── Notices.vue
        └── NoticeDetail.vue
```
