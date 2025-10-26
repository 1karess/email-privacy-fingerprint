# 阶段二测试 - Input vs Img精确对比测试

## 测试目标
分别验证`<input type="image">`和`<img>`标签在邮件中的追踪能力，进行精确对比。

## 核心假设
**关键假设**: 邮件客户端是否会加载`<input type="image">`的图片？

- 如果验证 → 发现新的追踪方法
- 如果否定 → 邮件客户端正确禁用了表单元素

## 运行测试
```bash
cd scripts/phase2
python send-input-vs-img-test.py
```

## 测试结构
**四个独立的测试邮件**：

### 测试1: IMG标签测试
- **文件**: `img-only-test.html`
- **内容**: 只包含1个`<img>`标签
- **目标**: 验证传统追踪方法
- **检查**: `img-track.gif` 是否被触发

### 测试2: Input标签测试  
- **文件**: `input-only-test.html`
- **内容**: 只包含1个`<input type="image">`标签
- **目标**: 验证新的追踪方法
- **检查**: `input-track.gif` 是否被触发

### 测试3: Input FormAction测试
- **文件**: `input-formaction-test.html`
- **内容**: 只包含1个`<input type="image" formaction>`标签
- **目标**: 验证表单动作追踪
- **检查**: `formaction-track.gif` 是否被触发

### 测试4: Button Image测试
- **文件**: `button-image-test.html`
- **内容**: 只包含1个`<button type="image">`标签
- **目标**: 验证按钮图片追踪
- **检查**: `button-track.gif` 是否被触发

## 🎉 测试结果

### ✅ 成功触发的追踪向量
1. **`img-track.gif`** - 传统`<img>`标签 ✅
2. **`input-track.gif`** - `<input type="image" src="...">` ✅
3. **`formaction-track.gif`** - `<input type="image" formaction="...">` ✅ ⭐ **意外发现！**

### ❌ 未触发的测试
4. **`button-track.gif`** - `<button type="image">` ❌ (邮件客户端不支持)

## 结果分析
- **3个被触发** → 发现新的追踪向量！
- **核心假设验证** → `<input type="image">`确实可以追踪
- **重大安全发现** → 现有隐私保护工具可能无法检测

## 🚨 安全影响

### ⚠️ 重大安全发现
**`<input type="image">`确实可以用于邮件追踪！**

**潜在风险**:
- 绕过某些反追踪工具
- 用户更难发现这种追踪方法
- 邮件安全工具可能不会检测input元素
- 攻击者可以利用此方法进行隐蔽追踪

### 🎯 建议措施
- 更新邮件隐私保护工具以检测input元素
- 用户需要了解这种新的追踪方法
- 邮件客户端应考虑禁用input元素
