# 邮件客户端隐私指纹检测框架

## 项目概述

本项目专注于检测邮件客户端对20个HTML追踪向量的隐私保护行为，通过系统性的测试来研究不同邮件客户端的隐私保护机制。

## 项目结构

```
邮件/
├── phase1/
│   ├── html-img-tests.html   # 20个HTML图片追踪测试用例
│   └── test-map.json         # 测试映射配置
├── api/
│   └── webhook.js            # Vercel Functions webhook处理
├── send_tests.py            # 测试邮件发送脚本
├── analyze_results.py       # 结果分析工具
├── parse_webhook_events.py  # webhook事件解析器
├── vercel.json              # Vercel部署配置
├── package.json             # Node.js项目配置
└── README.md                # 项目说明文档
```

## 20个HTML追踪向量测试

### HTML-001 ~ HTML-020 测试用例

1. **HTML-001** - 标准 `<img>` 标签
2. **HTML-002** - 自闭合 `<img />` 标签
3. **HTML-003** - 大写标签 `<IMG>`
4. **HTML-004** - 单引号属性
5. **HTML-005** - 无引号属性
6. **HTML-006** - 带尺寸属性
7. **HTML-007** - `display:none` 隐藏
8. **HTML-008** - `hidden` 属性
9. **HTML-009** - `loading="lazy"`
10. **HTML-010** - `loading="eager"`
11. **HTML-011** - `decoding="async"`
12. **HTML-012** - `decoding="sync"`
13. **HTML-013** - `importance="high"`
14. **HTML-014** - `fetchpriority="high"`
15. **HTML-015** - `srcset`（密度）
16. **HTML-016** - `srcset`（宽度）
17. **HTML-017** - `crossorigin="anonymous"`
18. **HTML-018** - `referrerpolicy="no-referrer"`
19. **HTML-019** - 空 `alt` 属性
20. **HTML-020** - 带 `title` 属性

## 快速开始

### 1. 部署到Vercel

```bash
# 安装Vercel CLI
npm i -g vercel

# 登录Vercel
vercel login

# 部署项目
vercel --prod
```

### 2. 配置webhook地址

部署完成后，Vercel会提供一个URL，例如：
```
https://your-project.vercel.app
```

您的webhook端点将是：
```
https://your-project.vercel.app/api/webhook
```

### 3. 更新测试配置

创建 `webhook_base.txt` 文件，设置您的Vercel webhook地址：

```
https://your-project.vercel.app
```

### 4. 运行测试

```bash
# 发送测试邮件
python send_tests.py

# 分析结果
python analyze_results.py
```

## 使用方法

### 发送测试邮件

```python
from send_tests import send_test_email

# 发送HTML图片追踪测试
send_test_email("phase1/html-img-tests.html")
```

### 分析测试结果

```python
from analyze_results import analyze_webhook_log

# 分析webhook日志
results = analyze_webhook_log("webhook_log.csv")
print(results)
```

## 注意事项

1. **隐私保护** - 本框架仅用于安全研究和教育目的
2. **合法使用** - 请确保在合法范围内使用本框架
3. **数据安全** - 测试数据请妥善保管，避免泄露
4. **持续更新** - 邮件客户端会不断更新隐私保护机制

## 贡献指南

欢迎提交Issue和Pull Request来改进本项目。

## 许可证

MIT License