#!/bin/bash

echo "🔄 同步 webhook 文件到 Vercel 部署目录"
echo "=================================="

# 检查源文件
if [ ! -f "core/api/webhook.js" ]; then
    echo "❌ 错误: 未找到源文件 core/api/webhook.js"
    exit 1
fi

# 确保目标目录存在
mkdir -p api

# 同步文件
echo "📁 从 core/api/webhook.js 同步到 api/webhook.js"
cp core/api/webhook.js api/webhook.js

# 检查文件是否同步成功
if [ -f "api/webhook.js" ]; then
    echo "✅ 同步成功！"
    echo "📊 文件大小: $(wc -c < api/webhook.js) 字节"
    echo "📅 最后修改: $(stat -f "%Sm" api/webhook.js)"
else
    echo "❌ 同步失败！"
    exit 1
fi

echo ""
echo "💡 现在可以部署到 Vercel:"
echo "   vercel --prod"
