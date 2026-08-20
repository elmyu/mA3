# Mini BME-Hub 医疗设备管理平台

集病人生理数据查看、医疗设备状态管理、设备预约/维护于一体的简易 Web 全栈平台，模拟医院中患者、医生、管理员三类角色的日常业务交互。

## 功能特性

- 三角色登录（患者 / 医生 / 管理员），JWT 鉴权 + 前端路由守卫 + 后端角色校验双层隔离
- 患者端：我的健康档案（生理信号历史）、医生出诊/空闲时间查看
- 医生端：患者信息调阅、设备台账看板（在线 / 故障 / 校准中）、设备预约
- 管理员端：用户增删改查、设备物资维护
- 加分项：ECG 波形可视化（ECharts）、CSV 生理数据上传、Docker 容器化、GitHub Actions 自动构建镜像、Sealos 公网部署

## 技术栈

- 前端：Vue3 + Vite + Element Plus + Pinia + Vue Router + Axios + ECharts
- 后端：Python + Flask（三层架构 `api` / `services` / `models`）+ Flask-SQLAlchemy + Flask-JWT-Extended + Flasgger
- 数据库：SQLite

## 目录结构

```
aiT2/
├─ backend/            # Flask 后端（app/api、app/services、app/models.py、seed.py）
├─ frontend/           # Vue3 前端（src/api、src/router、src/stores、src/views、src/components）
├─ docker/             # Dockerfile.backend / Dockerfile.frontend / nginx 模板 / docker-compose.yml
├─ .github/workflows/  # GitHub Actions：自动构建并推送 GHCR 镜像
├─ docs/               # 设计简报、Sealos 部署指南、API 截图、演示截图
└─ README.md
```

## 本地运行

### 1. 后端（端口 5000）

```powershell
cd D:\AISpace\ProjectALL\majorAssignment\TRY\aiT2\backend
python -m venv venv
.\venv\Scripts\Activate.ps1          # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python seed.py                        # 初始化数据库与演示数据（可重复运行）
python run.py                         # http://127.0.0.1:5000
```

### 2. 前端（端口 5173）

```powershell
cd D:\AISpace\ProjectALL\majorAssignment\TRY\aiT2\frontend
pnpm install
pnpm dev                              # http://localhost:5173
```

打开 http://localhost:5173 ，用下方账号登录。

## 演示账号

| 角色 | 用户名 | 密码 |
|---|---|---|
| 患者 | `patient1` | `123456` |
| 医生 | `doctor1` | `123456` |
| 管理员 | `admin` | `admin123` |

## Docker 本地运行（可选）

```powershell
cd D:\AISpace\ProjectALL\majorAssignment\TRY\aiT2
docker compose -f docker/docker-compose.yml up --build
```

访问 http://localhost:8080 。停止：`Ctrl+C`；彻底关闭：`docker compose -f docker/docker-compose.yml down`。

## 公网部署（Sealos，加分项）

每次推送到 `main` 分支，GitHub Actions 会自动构建镜像到 GHCR：

- 后端：`ghcr.io/elmyu/ma3/backend:latest`
- 前端：`ghcr.io/elmyu/ma3/frontend:latest`

部署步骤见 [docs/Sealos部署指南.md](docs/Sealos部署指南.md)，全程在网页控制台操作，无需本地安装 Docker。

## API 文档

后端启动后访问 http://127.0.0.1:5000/apidocs 查看 Swagger 接口文档（提交清单中的“API 接口清单”截图见 `docs/api-截图/`）。
