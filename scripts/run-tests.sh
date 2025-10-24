#!/bin/bash

echo "🚀 邮件隐私指纹测试系统"
echo "========================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python"
    exit 1
fi

# 检查配置文件
if [ ! -f "config/webhook_base.txt" ]; then
    echo "❌ 错误: 未找到webhook配置，请先配置config/webhook_base.txt"
    exit 1
fi

# 创建必要目录
mkdir -p data logs

echo "📧 发送测试邮件..."
python3 scripts/send_tests.py

echo ""
echo "✅ 测试邮件已发送！"
echo "💡 现在可以："
echo "   1. 运行 ./scripts/start-monitoring.sh 开始实时监控"
echo "   2. 打开 analysis/dashboard.html 查看仪表板"
echo "   3. 运行 python analysis/generate-report.py 生成报告"
