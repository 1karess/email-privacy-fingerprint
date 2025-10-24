#!/usr/bin/env python3
"""
分析真实的IP地址来源
"""
import json
import re
from datetime import datetime

def analyze_real_ip():
    """分析真实的IP地址"""
    
    # 读取数据
    with open('data/webhook-logs.json', 'r', encoding='utf-8') as f:
        logs = json.load(f)
    
    if not logs:
        print("❌ 没有找到测试数据")
        return
    
    print("🔍 真实IP地址分析")
    print("=" * 60)
    
    # 分析IP地址
    first_log = logs[0]
    client_ip = first_log.get('clientIP', '')
    user_agent = first_log.get('userAgent', '')
    referer = first_log.get('referer', '')
    
    print(f"📊 检测到的IP地址: {client_ip}")
    print(f"📊 User-Agent: {user_agent}")
    print(f"📊 Referer: {referer}")
    print()
    
    # 分析IP类型
    print("🌐 IP地址分析:")
    print("-" * 30)
    
    if client_ip.startswith('192.168.'):
        print("🔍 类型: 私有网络地址 (192.168.x.x)")
        print("⚠️  问题: 这是本地网络IP，不是真实公网IP")
        print("💡 可能原因:")
        print("   1. 邮件客户端使用了本地代理")
        print("   2. 邮件客户端在本地网络环境中")
        print("   3. 测试环境配置问题")
    elif client_ip.startswith('10.'):
        print("🔍 类型: 私有网络地址 (10.x.x.x)")
        print("⚠️  问题: 这是本地网络IP，不是真实公网IP")
    elif client_ip.startswith('172.'):
        print("🔍 类型: 私有网络地址 (172.16-31.x.x)")
        print("⚠️  问题: 这是本地网络IP，不是真实公网IP")
    elif client_ip.startswith('66.249.') or client_ip.startswith('66.102.'):
        print("🔍 类型: Google代理服务器")
        print("✅ 保护: 使用了Google的代理保护")
    elif client_ip.startswith('74.125.'):
        print("🔍 类型: Google代理服务器")
        print("✅ 保护: 使用了Google的代理保护")
    elif client_ip.startswith('172.217.'):
        print("🔍 类型: Google代理服务器")
        print("✅ 保护: 使用了Google的代理保护")
    elif client_ip.startswith('216.58.'):
        print("🔍 类型: Google代理服务器")
        print("✅ 保护: 使用了Google的代理保护")
    else:
        print("🔍 类型: 未知公网IP")
        print("⚠️  风险: 可能是真实公网IP")
    
    print()
    
    # 分析User-Agent
    print("🖥️ User-Agent分析:")
    print("-" * 30)
    
    if 'GoogleImageProxy' in user_agent:
        print("✅ 检测到: Google图片代理")
        print("🛡️ 保护: 使用了Google的代理保护")
    elif 'Outlook' in user_agent:
        print("📧 检测到: Outlook邮件客户端")
    elif 'Apple' in user_agent and 'Mail' in user_agent:
        print("📧 检测到: Apple Mail邮件客户端")
    elif 'Thunderbird' in user_agent:
        print("📧 检测到: Thunderbird邮件客户端")
    else:
        print("❓ 未知: 标准浏览器User-Agent")
        print("⚠️  风险: 可能暴露设备信息")
    
    print()
    
    # 分析Referer
    print("🔗 Referer分析:")
    print("-" * 30)
    
    if referer == 'https://gmail.com':
        print("📧 来源: Gmail网页版")
        print("⚠️  风险: 暴露了邮件客户端类型")
    elif referer == 'unknown' or not referer:
        print("✅ 保护: Referer被隐藏")
    else:
        print(f"📊 来源: {referer}")
        print("⚠️  风险: 暴露了来源信息")
    
    print()
    
    # 综合分析
    print("🎯 综合分析:")
    print("-" * 30)
    
    if client_ip.startswith('192.168.') or client_ip.startswith('10.') or client_ip.startswith('172.'):
        print("🚨 重要发现: 检测到的是私有网络IP，不是真实公网IP！")
        print("💡 这意味着:")
        print("   1. 邮件客户端可能使用了本地代理")
        print("   2. 或者邮件客户端在本地网络环境中运行")
        print("   3. 真实的公网IP被隐藏了")
        print()
        print("🔍 要获取真实IP，需要:")
        print("   1. 检查Vercel日志中的真实请求IP")
        print("   2. 查看x-forwarded-for头信息")
        print("   3. 分析实际的网络请求")
    else:
        print("📊 检测到公网IP，需要进一步分析")
    
    print()
    
    # 建议检查Vercel日志
    print("💡 建议检查Vercel日志:")
    print("-" * 30)
    print("1. 登录Vercel控制台")
    print("2. 查看Functions日志")
    print("3. 寻找真实的x-forwarded-for头信息")
    print("4. 分析实际的网络请求来源")
    
    # 保存分析结果
    analysis_result = {
        'timestamp': datetime.now().isoformat(),
        'detected_ip': client_ip,
        'ip_type': 'private' if client_ip.startswith(('192.168.', '10.', '172.')) else 'public',
        'user_agent': user_agent,
        'referer': referer,
        'analysis': {
            'is_private_ip': client_ip.startswith(('192.168.', '10.', '172.')),
            'is_google_proxy': client_ip.startswith(('66.249.', '66.102.', '74.125.', '172.217.', '216.58.')),
            'is_generic_ua': 'GoogleImageProxy' not in user_agent,
            'referer_exposed': referer and referer != 'unknown'
        }
    }
    
    with open('data/real-ip-analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 分析结果已保存到: data/real-ip-analysis.json")

if __name__ == "__main__":
    analyze_real_ip()
