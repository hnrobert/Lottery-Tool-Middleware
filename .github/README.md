# GitHub Actions CI/CD 配置指南

本项目包含完整的 GitHub Actions CI/CD 工作流，用于自动化构建、测试和发布 Docker 镜像。

## 📋 工作流概览

### 1. CI 测试和质量检查 (`ci-tests.yml`)

- **触发条件**: 推送到 main/develop 分支、创建 PR
- **功能**:
  - Python 代码质量检查 (Black, isort, Flake8)
  - 单元测试运行
  - Docker 镜像构建测试
  - 容器健康检查

### 2. Docker 构建和推送 (`docker-build-and-push.yml`)

- **触发条件**: 推送到 main 分支、创建标签、手动触发
- **功能**:
  - 多平台 Docker 镜像构建 (linux/amd64, linux/arm64)
  - 自动推送到 Docker Hub 和 GitHub Container Registry
  - 安全漏洞扫描 (Trivy)
  - 智能标签管理

### 3. 版本发布 (`release.yml`)

- **触发条件**: 创建 GitHub Release、手动触发
- **功能**:
  - 版本化镜像构建
  - 自动生成部署文件
  - 创建发布资产

## 🔧 配置要求

### GitHub Token 配置

- `GITHUB_TOKEN` 会自动提供，无需手动配置
- 用于认证 GitHub Container Registry

### 镜像仓库配置

工作流会自动推送到 GitHub Container Registry：

- **GitHub Container Registry**: `ghcr.io/hnrobert/lottery-tool-middleware`

如需修改镜像名称，请编辑工作流文件中的环境变量：

```yaml
env:
  GHCR_IMAGE_NAME: your-username/your-image-name
```

## 🚀 使用方法

### 自动触发

1. **推送代码到 main 分支**:

   ```bash
   git push origin main
   ```

   - 触发完整的 CI/CD 流程
   - 自动构建并推送 `latest` 标签

2. **创建版本标签**:

   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

   - 触发版本发布流程
   - 创建多个版本标签 (`v1.0.0`, `1.0.0`, `1.0`, `1`)

3. **创建 GitHub Release**:
   - 在 GitHub 网页上创建 Release
   - 自动触发发布工作流

### 手动触发

1. **在 GitHub Actions 页面**:

   - 选择对应的工作流
   - 点击 "Run workflow" 按钮
   - 填写必要参数（如自定义标签）

2. **手动发布版本**:

   ```bash
   # 通过 GitHub CLI
   gh workflow run release.yml -f version=v1.0.0 -f create_release=true
   ```

## 📦 镜像标签策略

### 自动标签规则

- `latest`: 最新的 main 分支构建
- `main`: main 分支最新构建
- `pr-123`: Pull Request #123 的构建
- `v1.0.0`, `1.0.0`, `1.0`, `1`: 版本标签构建

### 使用示例

```bash
# 拉取最新版本
docker pull ghcr.io/hnrobert/lottery-tool-middleware:latest

# 拉取特定版本
docker pull ghcr.io/hnrobert/lottery-tool-middleware:v1.0.0
```

## 🔍 质量检查

### 代码质量工具

1. **Black**: Python 代码格式化
2. **isort**: 导入语句排序
3. **Flake8**: 代码风格检查
4. **MyPy**: 类型检查（可选）

### 安全扫描

- **Trivy**: 容器镜像漏洞扫描
- 结果自动上传到 GitHub Security 面板

## 🐛 故障排除

### 常见问题

1. **镜像推送失败**:

   - 检查 `GITHUB_TOKEN` 权限设置
   - 确认 GitHub Container Registry 权限正确

2. **代码质量检查失败**:

   ```bash
   # 本地运行检查
   black --check src/
   isort --check-only src/
   flake8 src/
   ```

3. **Docker 构建失败**:
   - 检查 Dockerfile 语法
   - 确认所有依赖文件存在

### 查看日志

1. **GitHub Actions 日志**:

   - 访问仓库的 Actions 页面
   - 点击具体的工作流运行查看详细日志

2. **容器日志**:

   ```bash
   docker logs container-name
   ```

## 📈 监控和通知

### 构建状态徽章

在 README.md 中添加状态徽章：

```markdown
![CI Tests](https://github.com/your-username/lottery-tool-middleware/workflows/CI%20Tests%20and%20Quality%20Checks/badge.svg)
![Docker Build](https://github.com/your-username/lottery-tool-middleware/workflows/Docker%20Build%20and%20Push/badge.svg)
[![GHCR](https://img.shields.io/badge/ghcr.io-your--username%2Flottery--tool--middleware-blue)](https://github.com/your-username/lottery-tool-middleware/pkgs/container/lottery-tool-middleware)
```

### 通知设置

可以在工作流中添加通知步骤：

- Slack 通知
- 邮件通知
- 钉钉/企业微信通知

## 🔄 自定义工作流

### 修改触发条件

```yaml
on:
  push:
    branches: [main, develop, feature/*]
  schedule:
    - cron: "0 2 * * 1" # 每周一凌晨2点
```

### 添加环境变量

```yaml
env:
  CUSTOM_ENV: value
  REGISTRY_URL: ${{ secrets.CUSTOM_REGISTRY }}
```

### 条件执行

```yaml
- name: 生产环境部署
  if: github.ref == 'refs/heads/main'
  run: echo "部署到生产环境"
```

## 📚 参考资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
