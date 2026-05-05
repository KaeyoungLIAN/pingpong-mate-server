# 🏓 乒乓搭子 PingPong Mate

> 帮乒乓球爱好者快速找到水平相近、时间地点合适的球友。**北京地区**约球平台 MVP。

## 功能

### 后端已完成 API

| 模块 | 接口 | 说明 |
|------|------|------|
| **用户系统** | `POST /api/users/login/` | 微信登录（mock 模式） |
| | `GET /api/users/profile/` | 获取个人资料 |
| | `PUT /api/users/profile/` | 更新个人资料 |
| | `GET /api/users/<id>/` | 查看其他用户信息 |
| **约球系统** | `GET /api/matches/` | 约球列表（分页+筛选） |
| | `POST /api/matches/` | 发布约球 |
| | `GET /api/matches/<id>/` | 约球详情 |
| | `DELETE /api/matches/<id>/` | 取消约球 |
| | `POST /api/matches/<id>/apply/` | 报名 |
| | `POST /api/matches/<id>/cancel-apply/` | 取消报名 |
| | `GET /api/matches/my/` | 我的约球（我发起的+我报名的） |

### 前端已完成页面

- **登录页** — 微信一键登录，新用户引导完善资料
- **首页** — 约球列表卡片，按日期/距离/水平筛选
- **发布约球** — 日期、时间、地点（区）、人数、水平要求
- **约球详情** — 完整信息+报名人列表+微信号展示+报名按钮
- **我的约球** — Tab 切换「我发起的」/「我报名的」
- **个人资料编辑** — 性别、年龄、水平、球板、胶皮、自我介绍

## 技术栈

### 后端
- Python 3.9+ / Django 4.2.30
- Django REST Framework 3.16
- Token Authentication（DRF authtoken）
- SQLite（开发环境）
- CORS Headers

### 前端
- 微信小程序原生
- 原生组件库

## 本地运行

### 后端

```bash
# 1. 克隆仓库
git clone https://github.com/KaeyoungLIAN/pingpong-mate-server.git
cd pingpong-mate-server

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install django djangorestframework django-cors-headers

# 4. 迁移数据库
python manage.py migrate

# 5. 启动服务
python manage.py runserver 0.0.0.0:8001
```

后端服务运行在 `http://localhost:8001`

### 前端

```bash
# 1. 克隆仓库
git clone https://github.com/KaeyoungLIAN/pingpong-mate-weapp.git
cd pingpong-mate-weapp

# 2. 用微信开发者工具打开此目录

# 3. 修改 project.config.json 中的 appid 为你的 AppID

# 4. 如需修改后端地址，编辑 utils/api.js 或 app.js 中的 apiBaseUrl
```

## Mock 登录

MVP 阶段后端使用 mock 微信登录：

| code | 对应 openid | 说明 |
|------|-------------|------|
| `test` | `mock_openid_001` | 用户1 |
| `test2` | `mock_openid_002` | 用户2 |
| `test3` | `mock_openid_003` | 用户3 |

接入真实微信登录后，替换 `users/views.py` 中的 `mock_openid_map` 为微信 API 调用。

## 项目结构

```
pingpong-mate-server/
├── config/              # Django 项目配置
│   ├── settings.py      # 主配置
│   └── urls.py          # 根路由
├── users/               # 用户系统 app
│   ├── models.py        # User 模型
│   ├── serializers.py   # 序列化器
│   ├── views.py         # 登录、资料接口
│   └── urls.py          # 路由
├── matches/             # 约球系统 app
│   ├── models.py        # Match, MatchApplication 模型
│   ├── serializers.py   # 序列化器
│   ├── views.py         # 约球 CRUD、报名
│   └── urls.py          # 路由
├── venues/              # 球馆 app（预留）
│   └── models.py        # Venue 模型
└── manage.py
```

## 后续开发方向

1. 接入真实微信登录（替换 mock）
2. 球馆库（北京地区50+主流球馆）
3. 距离筛选（接入腾讯位置服务）
4. 用户评价和鸽子率系统
5. 消息推送（服务通知）
6. 扩展羽毛球、网球等运动类型
