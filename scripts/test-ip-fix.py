#!/usr/bin/env python3
"""
测试IP获取修复
"""
import json
import urllib.request
import urllib.parse
from datetime import datetime

def test_ip_fix():
    """测试IP获取修复"""
    
    print("🔍 测试IP获取修复")
    print("=" * 50)
    
    # 测试webhook端点
    base_url = "https://email-privacy-fingerprint.vercel.app"
    test_url = f"{base_url}/api/webhook/phase1/html-001-basic.gif"
    
    # 添加测试参数
    params = {
        'run': 'ip-test-fix',
        'uid': 'test-ip-fix-001'
    }
    
    print(f"测试URL: {test_url}")
    print(f"参数: {params}")
    print(f"时间: {datetime.now().isoformat()}")
    print("-" * 50)
    
    try:
        # 构建完整URL
        full_url = f"{test_url}?{urllib.parse.urlencode(params)}"
        
        # 发送GET请求
        with urllib.request.urlopen(full_url, timeout=10) as response:
            print(f"状态码: {response.status}")
            print(f"响应头: {dict(response.headers)}")
            
            content = response.read()
            print(f"响应内容长度: {len(content)}")
            
            if response.status == 200:
                print("✅ Webhook响应正常")
                print(f"Content-Type: {response.headers.get('content-type')}")
                print(f"Content-Length: {response.headers.get('content-length')}")
            else:
                print(f"❌ Webhook响应异常: {response.status}")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print("-" * 50)
    print("💡 请检查Vercel日志中的IP地址:")
    print("1. 登录Vercel控制台")
    print("2. 查看Functions日志")
    print("3. 查找 'EMAIL TRACKING PIXEL HIT' 日志")
    print("4. 检查 'Client IP' 字段")
    print("5. 应该显示Google的代理IP (66.249.x.x 或类似)")

if __name__ == "__main__":
    test_ip_fix()
