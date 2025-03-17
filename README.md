
# 实验室仪器管理系统

[![Python 3.9.7](https://img.shields.io/badge/Python-3.9.7-blue.svg)](https://www.python.org/)
[![Flask 2.0](https://img.shields.io/badge/Flask-2.0-green.svg)](https://flask.palletsprojects.com/)
[![License MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)

> 基于Flask框架开发的实验室仪器管理系统，实现设备追踪、预约管理等功能

## 📌 目录
- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [部署指南](#部署指南)
- [系统截图](#系统截图)
- [开发文档](#开发文档)
- [许可协议](#许可协议)

## ✨ 功能特性
| 模块         | 功能描述                          |
|--------------|---------------------------------|
| 设备管理      | CRUD操作/状态标记/增添删除        |
| 借出系统      | 申请-归还日期/日历视图            |
| 权限控制      | 角色管理(管理员/用户)    |

## 🚀 快速开始
### 环境要求
- Python 3.8+
- SQLite 3.32+
- Chrome/Firefox 最新版

### 安装步骤
```bash
# 克隆仓库
git clone https://github.com/zhoayan21/lab-device-system.git
cd lab-device-system

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 配置系统
1. 复制环境文件
```bash
cp .env.example .env
```
2. 编辑`.env`文件：
```ini
FLASK_APP=run.py
FLASK_ENV=production  # 生产环境改为production
SECRET_KEY=your-secret-key
DATABASE_URI=sqlite:///lab.db
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
```

### 初始化数据库
```bash
flask init-db
```

### 启动服务
```bash
flask run --host=0.0.0.0 --port=5000
```
访问 http://localhost:5000


## 📦 部署指南
### 开发模式
```bash
# 调试模式运行
FLASK_DEBUG=1 flask run --port 5000
```

### 生产部署
推荐使用Gunicorn + Nginx：
```bash
# 安装生产服务器
pip install gunicorn

# 启动服务
gunicorn --bind 0.0.0.0:8000 -w 4 "run:create_app()"

# Nginx配置示例
location / {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### Docker部署
```bash
# 构建镜像
docker build -t lab-system .

# 运行容器
docker run -d -p 5000:5000 --name lab-system lab-system
```

## 📜 许可协议
本项目采用 [MIT License](LICENSE)