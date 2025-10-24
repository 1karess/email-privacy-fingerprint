# 邮件客户端安全测试框架

## 🎯 项目概述

这是一个系统化的邮件客户端安全测试框架，用于研究不同邮件客户端对追踪技术的隐私保护行为。

## 📁 项目结构

```
邮件/
├── webhook_server.py          # Webhook服务器
├── test_matrix_system.py      # 主测试系统
├── analyze_results.py         # 结果分析工具
├── parse_webhook_events.py    # 数据解析工具
├── webhook_base.txt          # Webhook地址配置
├── webhook_log.csv           # 测试日志
└── phase1/                   # 测试用例目录
    ├── html-img-tests.html   # HTML测试用例
    └── test-map.json         # 测试映射
```

## 🚀 快速开始

### 1. 启动Webhook服务器
```bash
python3 webhook_server.py
```

### 2. 启动ngrok隧道（新终端）
```bash
ngrok http 8000
```

### 3. 更新webhook地址
将ngrok提供的公网地址写入 `webhook_base.txt`

### 4. 运行测试
```bash
python3 test_matrix_system.py
```

### 5. 分析结果
```bash
python3 analyze_results.py
```

## 📊 测试矩阵

### 当前支持的测试类别

1. **HTML IMG标签测试** (HTML-001 ~ HTML-020)
   - 标准img标签
   - 属性变体
   - 加载策略
   - 响应式图片

2. **CSS背景追踪测试** (CSS-BG-001 ~ CSS-BG-010)
   - background-image
   - 多背景图片
   - border-image
   - list-style-image

### 扩展测试类别

系统支持扩展更多测试类别：
- 输入类型图片测试
- 链接标签测试
- 媒体标签测试
- SVG相关测试
- 字体加载测试
- 等等...

## 🔍 结果分析

### 日志格式
测试结果记录在 `webhook_log.csv` 中，包含：
- 时间戳
- 请求方法
- 客户端IP
- 请求路径
- 查询参数
- User-Agent
- 请求头

### 分析指标
- 测试触发率
- 客户端类型识别
- 隐私保护行为
- 时序分析

## 📋 使用说明

### 配置邮件发送
编辑 `test_matrix_system.py` 中的配置：
```python
SENDER = "your-email@gmail.com"
PASSWORD = "your-app-password"
RECEIVER = "target-email@gmail.com"
```

### 添加新测试用例
在 `test_matrix_system.py` 中添加新的测试函数：
```python
def get_new_test_category(webhook_base, run_id):
    return [
        {
            'test_id': 'NEW-001',
            'description': '测试描述',
            'html': f'<img src="{webhook_base}/new-test.gif?run={run_id}">'
        }
    ]
```

## 🎯 研究目标

1. **发现漏洞** - 识别邮件客户端的追踪向量
2. **证明风险** - 展示隐私保护不足的情况
3. **提出防护建议** - 基于测试结果提出改进方案
4. **推动标准改进** - 为邮件安全标准提供数据支持

## 📈 预期成果

- 发现新的追踪向量（CVE）
- 证明隐私保护不足
- 提出改进方案
- 发表学术论文

## 🔧 技术栈

- Python 3.x
- SMTP邮件发送
- HTTP Webhook服务器
- ngrok公网隧道
- CSV数据记录
- JSON结果分析

## 📝 注意事项

1. 确保webhook服务器和ngrok隧道正常运行
2. 使用应用专用密码而非账户密码
3. 遵守相关法律法规和道德准则
4. 仅用于学术研究和安全测试目的
