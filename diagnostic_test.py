#!/usr/bin/env python3
"""
邮件客户端安全测试诊断工具
全面测试webhook系统的各个组件
"""
import json
import smtplib
import time
import uuid
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import subprocess
import urllib.request
import urllib.parse

class DiagnosticTest:
    """诊断测试类"""
    
    def __init__(self):
        self.webhook_base = Path("webhook_base.txt").read_text().strip()
        self.run_id = str(uuid.uuid4())
        self.test_results = []
        
    def test_1_webhook_server(self):
        """测试1: 本地webhook服务器"""
        print("🔍 测试1: 本地webhook服务器")
        try:
            req = urllib.request.Request("http://127.0.0.1:8000/test-local")
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    print("   ✅ 本地webhook服务器正常")
                    return True
                else:
                    print(f"   ❌ 本地webhook服务器响应异常: {response.status}")
                    return False
        except Exception as e:
            print(f"   ❌ 本地webhook服务器连接失败: {e}")
            return False
    
    def test_2_ngrok_tunnel(self):
        """测试2: ngrok隧道"""
        print("🔍 测试2: ngrok隧道")
        try:
            # 检查ngrok API
            response = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('tunnels'):
                    tunnel = data['tunnels'][0]
                    public_url = tunnel['public_url']
                    print(f"   ✅ ngrok隧道正常: {public_url}")
                    
                    # 测试公网访问
                    test_response = requests.get(f"{public_url}/test-ngrok", timeout=10)
                    if test_response.status_code == 200:
                        print("   ✅ 公网访问正常")
                        return True
                    else:
                        print(f"   ❌ 公网访问异常: {test_response.status_code}")
                        return False
                else:
                    print("   ❌ 没有活动的ngrok隧道")
                    return False
            else:
                print(f"   ❌ ngrok API异常: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ ngrok隧道测试失败: {e}")
            return False
    
    def test_3_webhook_logging(self):
        """测试3: webhook日志记录"""
        print("🔍 测试3: webhook日志记录")
        try:
            # 发送测试请求
            test_url = f"{self.webhook_base}/test-logging?run={self.run_id}&test=diagnostic"
            response = requests.get(test_url, timeout=10)
            
            if response.status_code == 200:
                # 检查日志文件
                log_file = Path("webhook_log.csv")
                if log_file.exists():
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        if len(lines) > 1:  # 有数据行
                            last_line = lines[-1]
                            if self.run_id in last_line:
                                print("   ✅ webhook日志记录正常")
                                return True
                            else:
                                print("   ❌ 日志中没有找到测试记录")
                                return False
                        else:
                            print("   ❌ 日志文件为空")
                            return False
                else:
                    print("   ❌ 日志文件不存在")
                    return False
            else:
                print(f"   ❌ 测试请求失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ webhook日志测试失败: {e}")
            return False
    
    def test_4_email_sending(self):
        """测试4: 邮件发送"""
        print("🔍 测试4: 邮件发送")
        try:
            # 创建简单测试邮件
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head><title>诊断测试邮件</title></head>
            <body>
                <h1>🔍 诊断测试邮件</h1>
                <p>测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Run ID: {self.run_id}</p>
                
                <h2>基础图片测试</h2>
                <img src="{self.webhook_base}/diagnostic-basic.gif?run={self.run_id}&test=basic" width="1" height="1" alt="">
                
                <h2>隐藏图片测试</h2>
                <img src="{self.webhook_base}/diagnostic-hidden.gif?run={self.run_id}&test=hidden" style="display:none" alt="">
                
                <h2>CSS背景测试</h2>
                <div style="background-image:url('{self.webhook_base}/diagnostic-css.gif?run={self.run_id}&test=css');width:1px;height:1px;"></div>
                
                <p><strong>说明:</strong> 如果您看到此邮件，请检查webhook日志中是否有对应的请求记录。</p>
            </body>
            </html>
            """
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'🔍 诊断测试邮件 - {self.run_id[:8]}'
            msg['From'] = "yuqizheng325@gmail.com"
            msg['To'] = "nicai51213@gmail.com"
            msg['X-Test-Run-ID'] = self.run_id
            msg['X-Test-Type'] = 'diagnostic'
            msg.attach(MIMEText(html_content, 'html'))
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login("yuqizheng325@gmail.com", "cyqszyoonzwhtdoi")
                server.send_message(msg)
            
            print("   ✅ 邮件发送成功")
            return True
            
        except Exception as e:
            print(f"   ❌ 邮件发送失败: {e}")
            return False
    
    def test_5_different_user_agents(self):
        """测试5: 不同User-Agent"""
        print("🔍 测试5: 不同User-Agent模拟")
        
        user_agents = [
            "Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
        ]
        
        success_count = 0
        for i, ua in enumerate(user_agents, 1):
            try:
                headers = {'User-Agent': ua}
                test_url = f"{self.webhook_base}/test-ua-{i}?run={self.run_id}&ua={i}"
                response = requests.get(test_url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    print(f"   ✅ User-Agent {i}: {ua[:50]}...")
                    success_count += 1
                else:
                    print(f"   ❌ User-Agent {i}: HTTP {response.status_code}")
            except Exception as e:
                print(f"   ❌ User-Agent {i}: {e}")
        
        if success_count == len(user_agents):
            print("   ✅ 所有User-Agent测试通过")
            return True
        else:
            print(f"   ⚠️  {success_count}/{len(user_agents)} User-Agent测试通过")
            return False
    
    def test_6_image_formats(self):
        """测试6: 不同图片格式"""
        print("🔍 测试6: 不同图片格式")
        
        formats = ['gif', 'png', 'jpg', 'webp', 'svg']
        success_count = 0
        
        for fmt in formats:
            try:
                test_url = f"{self.webhook_base}/test-{fmt}.{fmt}?run={self.run_id}&format={fmt}"
                response = requests.get(test_url, timeout=5)
                
                if response.status_code == 200:
                    print(f"   ✅ {fmt.upper()}格式: 正常")
                    success_count += 1
                else:
                    print(f"   ❌ {fmt.upper()}格式: HTTP {response.status_code}")
            except Exception as e:
                print(f"   ❌ {fmt.upper()}格式: {e}")
        
        if success_count == len(formats):
            print("   ✅ 所有图片格式测试通过")
            return True
        else:
            print(f"   ⚠️  {success_count}/{len(formats)} 图片格式测试通过")
            return False
    
    def test_7_webhook_analysis(self):
        """测试7: webhook日志分析"""
        print("🔍 测试7: webhook日志分析")
        
        try:
            log_file = Path("webhook_log.csv")
            if not log_file.exists():
                print("   ❌ 日志文件不存在")
                return False
            
            with open(log_file, 'r') as f:
                lines = f.readlines()
            
            if len(lines) <= 1:
                print("   ❌ 日志文件为空或只有标题行")
                return False
            
            # 分析日志
            total_requests = len(lines) - 1  # 减去标题行
            diagnostic_requests = 0
            email_client_requests = 0
            
            for line in lines[1:]:  # 跳过标题行
                if self.run_id in line:
                    diagnostic_requests += 1
                
                # 检查是否有邮件客户端的User-Agent
                ua = line.split(',')[8] if len(line.split(',')) > 8 else ''
                if any(client in ua.lower() for client in ['gmail', 'outlook', 'apple', 'yahoo', 'thunderbird']):
                    email_client_requests += 1
            
            print(f"   📊 总请求数: {total_requests}")
            print(f"   📊 诊断请求数: {diagnostic_requests}")
            print(f"   📊 邮件客户端请求数: {email_client_requests}")
            
            if diagnostic_requests > 0:
                print("   ✅ 诊断请求记录正常")
                return True
            else:
                print("   ❌ 没有找到诊断请求记录")
                return False
                
        except Exception as e:
            print(f"   ❌ 日志分析失败: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有诊断测试"""
        print("🚀 开始邮件客户端安全测试诊断")
        print("=" * 60)
        print(f"📊 Run ID: {self.run_id}")
        print(f"🌐 Webhook地址: {self.webhook_base}")
        print("=" * 60)
        
        tests = [
            ("本地webhook服务器", self.test_1_webhook_server),
            ("ngrok隧道", self.test_2_ngrok_tunnel),
            ("webhook日志记录", self.test_3_webhook_logging),
            ("邮件发送", self.test_4_email_sending),
            ("不同User-Agent", self.test_5_different_user_agents),
            ("不同图片格式", self.test_6_image_formats),
            ("webhook日志分析", self.test_7_webhook_analysis)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"   ❌ 测试异常: {e}")
                results.append((test_name, False))
            time.sleep(1)  # 避免请求过快
        
        # 总结结果
        print("\n" + "=" * 60)
        print("📋 诊断测试总结")
        print("=" * 60)
        
        passed = 0
        for test_name, result in results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{test_name:20} {status}")
            if result:
                passed += 1
        
        print(f"\n📊 测试结果: {passed}/{len(results)} 通过")
        
        if passed == len(results):
            print("🎉 所有测试通过！系统完全正常。")
        elif passed >= len(results) * 0.8:
            print("⚠️  大部分测试通过，系统基本正常。")
        else:
            print("❌ 多个测试失败，系统存在问题。")
        
        return results

def main():
    """主函数"""
    diagnostic = DiagnosticTest()
    results = diagnostic.run_all_tests()
    
    print(f"\n📧 请检查邮件是否到达收件箱")
    print(f"📊 请检查webhook_log.csv中的请求记录")
    print(f"🔍 Run ID: {diagnostic.run_id}")

if __name__ == "__main__":
    main()
