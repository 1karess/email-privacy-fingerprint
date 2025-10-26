# 邮件隐私追踪测试项目

## 项目概述
本项目用于测试邮件客户端的隐私保护机制，特别是对追踪像素的检测和阻止能力。

## 核心假设
**关键假设**: 邮件客户端是否会加载`<input type="image">`的图片？

- 如果验证 → 发现新的追踪方法
- 如果否定 → 邮件客户端正确禁用了表单元素

## 🎉 测试结果总结

### ✅ 重大发现
**核心假设得到验证！** `<input type="image">`确实可以用于邮件追踪！

### 📊 成功触发的追踪向量
1. **传统方法**: `<img>`标签 ✅
2. **新方法1**: `<input type="image" src="...">` ✅
3. **新方法2**: `<input type="image" formaction="...">` ✅ ⭐ **意外发现！**

### ❌ 未触发的测试
4. **`<button type="image">`** ❌ (邮件客户端不支持)

## 项目结构

### 核心文件
- `api/webhook.js` - 核心webhook处理程序，用于接收和记录追踪请求
- `config/` - 配置文件目录

### 测试结构

#### 阶段一 (Phase 1) - 基础HTML IMG测试
**目录**: `tests/phase1/`, `scripts/phase1/`

**目标**: 测试传统`<img>`标签的各种变体在邮件中的行为

**测试文件**:
- `html-img-tests.html` - 包含HTML-001到HTML-020的20个测试用例
- `send_tests.py` - 发送阶段一测试邮件的脚本

**测试内容**:
- 标准`<img>`标签
- 自闭合标签
- 大写标签
- 不同引号风格
- 隐藏属性测试
- 加载策略测试
- 跨域和引用策略测试

#### 阶段二 (Phase 2) - Input vs Img精确对比测试
**目录**: `tests/phase2/`, `scripts/phase2/`

**目标**: 验证`<input type="image">`在邮件中的追踪能力

**测试文件**:
- `img-only-test.html` - 传统`<img>`标签测试（对照组）
- `input-only-test.html` - `<input type="image" src="...">`测试
- `input-formaction-test.html` - `<input type="image" formaction="...">`测试
- `button-image-test.html` - `<button type="image">`测试
- `send-input-vs-img-test.py` - 发送阶段二测试邮件的脚本

**测试内容**:
- 4个独立的测试邮件，分别测试不同追踪向量
- 1x1像素追踪测试
- 精确对比不同HTML元素的追踪能力

## 使用方法

### 阶段一测试
```bash
cd scripts/phase1
python send_tests.py
```

### 阶段二测试
```bash
cd scripts/phase2
python send-input-vs-img-test.py
```

### 查看结果
1. 检查Vercel项目日志
2. 查看webhook接收到的请求
3. 分析哪些测试用例被触发

## 配置说明

### Webhook配置
- 主webhook: `https://email-privacy-fingerprint.vercel.app/api/webhook/`
- 阶段一测试路径: `/phase1/`
- 阶段二测试路径: `/input-vs-img/`

### 邮件配置
- 发送方: `yuqizheng325@gmail.com`
- 接收方: `nicai51213@gmail.com`
- 使用Gmail应用密码进行认证

## 测试假设

### 阶段一假设
- 传统`<img>`标签应该能够正常追踪
- 各种HTML变体可能有不同的行为
- 隐藏属性可能影响追踪效果

### 阶段二假设
- `<input type="image">`可能被邮件客户端当作表单元素处理
- 如果input能追踪，则发现新的追踪方法
- 如果input不能追踪，则邮件客户端正确禁用了表单元素

## 🚨 安全影响分析

### ⚠️ 重大安全发现
**`<input type="image">`确实可以用于邮件追踪！**

**潜在安全风险**:
- ✅ **绕过某些反追踪工具** - 现有工具可能只检测`<img>`标签
- ✅ **用户更难发现** - 这种追踪方法更隐蔽
- ✅ **邮件安全工具可能不会检测** - input元素可能被忽略
- ✅ **发现新的追踪向量** - 攻击者可以利用此方法

**具体发现**:
1. `<input type="image" src="...">` - 高追踪潜力 ✅
2. `<input type="image" formaction="...">` - 意外发现 ✅
3. `<button type="image">` - 不支持 ❌

### 🎯 建议措施
- 更新邮件隐私保护工具以检测input元素
- 用户需要了解这种新的追踪方法
- 邮件客户端应考虑禁用input元素

## 部署说明

### Vercel部署
1. 确保`api/webhook.js`在正确位置
2. 使用`vercel --prod`部署
3. 更新`config/webhook_base.txt`中的webhook地址

### 注意事项
1. API文件必须放在`api/`目录下
2. 部署后检查Vercel控制台确认API正常工作
3. 使用不同的run_id避免缓存影响

## 注意事项

1. 测试前确保webhook服务正常运行
2. 使用不同的run_id避免缓存影响
3. 记录测试时间和环境信息
4. 分析结果时考虑邮件客户端的差异

## 清理说明

本项目已清理所有历史测试数据和可视化内容，只保留核心测试代码。如需重新开始测试，请直接运行相应阶段的脚本。