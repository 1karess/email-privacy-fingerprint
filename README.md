# 🔍 邮件客户端隐私指纹检测框架

## 📁 项目结构

```
邮件/
├── core/                   # 核心功能
│   └── api/
│       └── webhook.js     # Vercel Functions webhook处理
├── tests/                  # 测试相关
│   └── phase1/
│       ├── html-img-tests.html  # 20个HTML图片追踪测试用例
│       └── test-map.json        # 测试映射配置
├── data/                   # 数据存储
│   ├── webhook-logs.json       # 实时webhook日志数据
│   ├── analysis-report.json    # 分析报告数据
│   ├── test-record.xlsx        # 测试记录Excel文件
│   └── logs/                   # 日志文件目录
├── analysis/               # 数据分析和可视化
│   ├── dashboard.html          # 实时可视化仪表板
│   ├── realtime-monitor.py     # 实时监控脚本
│   └── generate-report.py      # 分析报告生成器
├── scripts/                # 脚本和工具
│   ├── send_tests.py           # 邮件发送脚本
│   ├── analyze_results.py      # 结果分析工具
│   ├── parse_webhook_events.py # webhook事件解析器
│   ├── start-monitoring.sh     # 一键启动监控脚本
│   └── run-tests.sh            # 一键运行测试脚本
├── config/                 # 配置文件
│   ├── package.json            # Node.js项目配置
│   ├── vercel.json          # Vercel部署配置
│   └── webhook_base.txt       # webhook基础URL配置
└── docs/                   # 项目文档
    ├── README.md              # 项目说明文档
    └── PROJECT_STRUCTURE.md   # 项目结构说明
```

## 🚀 快速开始

### 1. 一键运行测试
```bash
./scripts/run-tests.sh
```

### 2. 启动实时监控
```bash
./scripts/start-monitoring.sh
```

### 3. 查看仪表板
```bash
open analysis/dashboard.html
```

### 4. 生成分析报告
```bash
python analysis/generate-report.py
```

## 📊 功能特性

- **实时数据同步**: 测试数据自动保存到本地文件
- **可视化仪表板**: 实时显示测试结果和分析
- **自动监控**: 实时监控webhook请求并分析
- **报告生成**: 自动生成详细的Markdown分析报告
- **分类管理**: 按功能分类组织项目文件

## 🔧 配置说明

### webhook配置
编辑 `config/webhook_base.txt` 文件，设置你的Vercel webhook地址：
```
https://your-project.vercel.app/api/webhook
```

### 邮件配置
编辑 `scripts/send_tests.py` 文件中的邮件设置：
```python
SENDER = "your-email@gmail.com"
PASSWORD = "your-app-password"
RECEIVER = "target-email@gmail.com"
```

## 📈 数据流

```
用户访问测试邮件
→ 邮件客户端加载图片
→ 触发 core/api/webhook.js
→ 数据保存到 data/webhook-logs.json
→ analysis/ 工具实时分析
→ 生成可视化仪表板和报告
```

## 🎯 测试用例

项目包含20个HTML追踪向量测试：

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

## 📝 注意事项

1. **隐私保护** - 本框架仅用于安全研究和教育目的
2. **合法使用** - 请确保在合法范围内使用本框架
3. **数据安全** - 测试数据请妥善保管，避免泄露
4. **持续更新** - 邮件客户端会不断更新隐私保护机制

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进本项目。

## 📄 许可证

MIT License
