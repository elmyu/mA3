# Sealos 公网部署指南

本项目已配置 GitHub Actions：每次推送到 `main` 分支会自动把前后端构建成镜像并推送到 GitHub 容器仓库（GHCR），无需本地安装 Docker。

## 镜像地址

| 应用 | 镜像 |
|---|---|
| 后端（Flask） | `ghcr.io/elmyu/ma3/backend:latest` |
| 前端（Nginx） | `ghcr.io/elmyu/ma3/frontend:latest` |

构建进度可在 GitHub 仓库的 **Actions** 页面查看，绿勾即构建完成。

## 一、部署后端

1. 打开你的 Sealos 控制台（https://hzh.sealos.run/ ）并登录，进入一个工作空间。
2. 点击 **应用管理（App Launchpad）** → **创建新应用**。
3. 选择 **通过 Docker 镜像部署**，填入：
   - 镜像：`ghcr.io/elmyu/ma3/backend:latest`
   - 容器端口：`5000`
4. 环境变量（点击“添加环境变量”）：
   - `SECRET_KEY`：随意填一串字符（如 `minibmehub-sealos-secret`）
   - `JWT_SECRET_KEY`：随意填一串较长字符（至少 32 位）
5. 存储卷（必须配置，否则 SQLite 与上传文件重启会丢）：
   - 新建卷 A → 挂载路径 `/app/instance`（数据库）
   - 新建卷 B → 挂载路径 `/app/uploads`（CSV 上传文件）
6. 网络：选择 **内部访问**（不勾选外网），保存并启动。
7. 等待状态变为运行中后，在应用详情页复制它的 **内部地址/服务名**（形如 `backend-xxxxx.default.svc.cluster.local:5000`），下一步要用。

## 二、部署前端

1. 再次进入 **应用管理** → **创建新应用**。
2. 填入：
   - 镜像：`ghcr.io/elmyu/ma3/frontend:latest`
   - 容器端口：`80`
3. 环境变量：
   - `BACKEND_URL`：填上一步复制的后端内部地址，格式必须带协议：`http://backend-xxxxx.default.svc.cluster.local:5000`
4. 网络：勾选 **外网访问（公网）**，协议选 **HTTPS**，系统会自动分配一个 `*.sealos.run` 域名并签发证书。
5. 保存并启动，等待运行中。
6. 点击公网地址即可访问系统，用演示账号登录验证全流程。

## 三、更新到最新版本

推送新代码到 `main` 后，GitHub Actions 会自动更新 `latest` 镜像；到 Sealos 两个应用的详情页点 **更新（拉取最新镜像并重启）** 即可。

## 常见问题

**镜像拉取失败 / ImagePullBackOff**

`ghcr.io` 镜像默认跟随仓库可见性。若仓库是私有的，需要在 Sealos 里配置镜像仓库密钥：

1. 打开 GitHub → 头像 → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token。
2. 勾选 `read:packages`，生成后复制 token（只显示一次，立即保存）。
3. 在 Sealos 应用管理的镜像配置里选择“私有镜像仓库”，填写：
   - 仓库地址：`ghcr.io`
   - 用户名：你的 GitHub 用户名（`elmyu`）
   - 密码：刚生成的 token
4. 重新创建/更新应用。

若仓库是公开的，无需任何密钥即可拉取。

**前端能打开但接口报错**

检查前端的 `BACKEND_URL` 是否填了后端**内部地址**且带 `http://` 前缀，并确认后端已运行。

**上传 CSV 后重启数据丢失**

确认后端两个存储卷的挂载路径与上面一致（`/app/instance`、`/app/uploads`）。
