---
author: admin@pldz1.com
category: 2h2g-playbook
csdn: ''
date: '2026-04-12'
gitee: ''
github: ''
juejin: ''
serialNo: 1
status: publish
summary: 了解云服务器的防火墙端口, 才能保证你的网络服务能够正常访问.
tags:
- cloud
- cloud server
- fireware
- network
thumbnail: /api/v1/website/image/2h2g-playbook/cloud-fireware-thumbnail.jpg
title: ⚠️ 云服务器防火墙 / 安全组放行端口
---

# ⚠️ 云服务器防火墙 / 安全组放行端口

> **如果你在腾讯云、阿里云、华为云等云平台上部署，光启动服务是不够的 —— 还必须在控制台和系统两侧都放行端口/出入站规则，否则浏览器访问不通。**
### 第一步：云控制台安全组放行
登录你的云平台控制台，找到对应实例的**安全组 / 防火墙规则**，添加一条**入站规则**：
| 方向 | 协议 | 端口 | 来源 |
|------|------|------|------|
| 入站 | TCP | `7689` | `0.0.0.0/0`（所有IP）或你的固定IP |
> 各平台入口：
> - 腾讯云：控制台 → 云服务器 → 安全组 → 入站规则
> - 阿里云：控制台 → ECS → 安全组 → 手动添加
> - 华为云：控制台 → ECS → 安全组 → 入方向规则
### 第二步：系统级防火墙放行（ufw / firewalld 二选一）
**Ubuntu / Debian（使用 ufw）：**
```bash
sudo ufw allow 7689/tcp
sudo ufw reload
sudo ufw status  # 确认规则已生效
```
**CentOS / RHEL（使用 firewalld）：**
```bash
sudo firewall-cmd --permanent --add-port=7689/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports  # 确认规则已生效
```
> 💡 两步都要做：**云控制台安全组** 是云平台层面的网络隔离，**系统防火墙** 是操作系统层面的过滤，缺任何一步都可能导致连不上。
---
## ⚙️ 说明
* 每个 demo 目录包含 **README.md**，提供部署及操作指南
* 项目按时间或折腾顺序更新，便于追踪实验结果
* 主要面向 **自学、运维实验、工具集成**