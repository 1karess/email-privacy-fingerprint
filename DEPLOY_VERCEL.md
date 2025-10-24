# 部署到Vercel - 免费webhook监控

## 🚀 快速部署步骤

### 1. 注册Vercel账号
- 访问 https://vercel.com
- 点击 "Sign Up" 注册账号（免费）
- 选择 "Continue with GitHub" 使用GitHub账号登录

### 2. 创建GitHub仓库
```bash
# 在您的项目目录中
git init
git add .
git commit -m "Initial commit: Email client privacy fingerprint framework"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/email-privacy-fingerprint.git
git push -u origin main
```

### 3. 连接Vercel
- 登录Vercel后，点击 "New Project"
- 选择 "Import Git Repository"
- 选择您的GitHub仓库
- 点击 "Deploy"

### 4. 获取webhook URL
部署完成后，您会获得一个URL，例如：
`https://your-project-name.vercel.app`

您的webhook端点将是：
`https://your-project-name.vercel.app/api/webhook`

### 5. 更新测试配置
将 `webhook_base.txt` 更新为您的Vercel URL：
```
https://your-project-name.vercel.app
```

## 📊 实时监控

### 查看实时日志
1. 登录Vercel控制台
2. 选择您的项目
3. 点击 "Functions" 标签
4. 点击 "View Function Logs" 查看实时日志

### 日志格式
每个webhook请求都会在控制台显示：
```
=== WEBHOOK REQUEST ===
Timestamp: 2025-10-23T23:31:25.000Z
Method: GET
Client IP: 74.125.209.3
Path: phase1/html-001-basic.gif
Query: {"run":"abc123","uid":"def456"}
Test ID: html-001-basic.gif
Run Set ID: abc123
User Agent: Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11...
Referer: 
Headers: {"host":"your-project.vercel.app",...}
========================
```

## ✅ 优势
- **完全免费** - 无隐藏费用
- **实时监控** - 支持实时日志查看
- **24/7运行** - 比ngrok更稳定
- **全球CDN** - 访问速度快
- **自动HTTPS** - 安全连接

## 🔧 故障排除
如果部署遇到问题：
1. 检查GitHub仓库是否公开
2. 确保所有文件都已提交
3. 查看Vercel部署日志
4. 重新部署项目
