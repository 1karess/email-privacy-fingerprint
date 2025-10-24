# 📁 项目文件结构

## 🎯 核心功能 (core/)
```
core/
├── api/
│   └── webhook.js          # Vercel Functions webhook处理
```

## 🧪 测试相关 (tests/)
```
tests/
├── phase1/
│   ├── html-img-tests.html # 20个HTML图片追踪测试用例
│   └── test-map.json       # 测试映射配置
```

## 📊 数据和分析 (data/ & analysis/)
```
data/
├── webhook-logs.json       # 实时webhook日志数据
├── analysis-report.json    # 分析报告数据
├── test-record.xlsx        # 测试记录Excel文件
└── logs/                   # 日志文件目录

analysis/
├── dashboard.html          # 实时可视化仪表板
├── realtime-monitor.py     # 实时监控脚本
└── generate-report.py      # 分析报告生成器
```

## 🔧 脚本和工具 (scripts/)
```
scripts/
├── send_tests.py           # 邮件发送脚本
├── analyze_results.py      # 结果分析工具
├── parse_webhook_events.py # webhook事件解析器
└── start-monitoring.sh     # 一键启动监控脚本
```

## ⚙️ 配置文件 (config/)
```
config/
├── package.json            # Node.js项目配置
├── vercel.json            # Vercel部署配置
└── webhook_base.txt       # webhook基础URL配置
```

## 📚 文档 (docs/)
```
docs/
├── README.md              # 项目说明文档
└── PROJECT_STRUCTURE.md  # 项目结构说明
```

## 🚀 快速开始

### 1. 发送测试邮件
```bash
python scripts/send_tests.py
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

## 📋 文件分类说明

- **core/**: 核心功能代码，包括API端点
- **tests/**: 测试用例和测试配置
- **data/**: 数据存储目录
- **analysis/**: 数据分析和可视化工具
- **scripts/**: 自动化脚本和工具
- **config/**: 项目配置文件
- **docs/**: 项目文档

## 🔄 数据流

```
用户访问测试邮件
→ 邮件客户端加载图片
→ 触发 core/api/webhook.js
→ 数据保存到 data/webhook-logs.json
→ analysis/ 工具实时分析
→ 生成可视化仪表板和报告
```
