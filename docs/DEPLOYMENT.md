# 🚀 部署说明

## Vercel 部署要求

### 重要：API 文件位置
Vercel 要求 API 文件必须放在 `api/` 目录下，不能放在其他子目录中。

### 正确的文件结构
```
邮件/
├── api/                    # ✅ Vercel API 目录（必须）
│   └── webhook.js         # ✅ webhook 处理文件
├── core/                  # 核心功能（开发用）
│   └── api/
│       └── webhook.js     # 开发版本
├── tests/                 # 测试文件
├── data/                  # 数据文件
├── analysis/              # 分析工具
├── scripts/               # 脚本文件
├── config/                # 配置文件
└── docs/                  # 文档
```

## 部署步骤

### 1. 确保 API 文件在正确位置
```bash
# 检查 api/webhook.js 是否存在
ls -la api/webhook.js
```

### 2. 部署到 Vercel
```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录 Vercel
vercel login

# 部署项目
vercel --prod
```

### 3. 配置 webhook 地址
部署完成后，更新 `config/webhook_base.txt`：
```
https://your-project.vercel.app/api/webhook
```

## 文件说明

- **`api/webhook.js`**: Vercel Functions 处理文件（生产环境）
- **`core/api/webhook.js`**: 开发版本，用于本地测试
- **空目录**: 已清理，不再需要

## 注意事项

1. **API 路径**: Vercel 只识别 `api/` 目录下的文件
2. **文件同步**: 修改 `core/api/webhook.js` 后，需要同步到 `api/webhook.js`
3. **部署检查**: 部署后检查 Vercel 控制台确认 API 正常工作
