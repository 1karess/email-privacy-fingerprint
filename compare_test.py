#!/usr/bin/env python3
"""
对比测试：webhook.site vs 我们的ngrok
"""
import smtplib
import time
import uuid
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_comparison_test():
    """发送对比测试邮件"""
    
    # 配置
    webhook_site = "https://webhook.site/d76b930f-74bd-402b-b863-5117c1fd8ae4"
    our_ngrok = "https://raylene-noncircuited-unfeasibly.ngrok-free.dev"
    run_id = str(uuid.uuid4())
    
    # 创建对比测试HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>对比测试：webhook.site vs ngrok</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            .test-section {{ 
                border: 1px solid #ddd; 
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 5px;
            }}
            .webhook-site {{ background-color: #e8f5e8; }}
            .our-ngrok {{ background-color: #e8f0ff; }}
            img {{ border: 1px solid #ccc; margin: 5px; }}
        </style>
    </head>
    <body>
        <h1>🔍 对比测试：webhook.site vs ngrok</h1>
        <p><strong>测试时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Run ID:</strong> {run_id}</p>
        
        <div class="test-section webhook-site">
            <h2>🟢 webhook.site 测试</h2>
            <p>这些图片指向webhook.site，应该能够被加载：</p>
            
            <h3>基础图片测试</h3>
            <img src="{webhook_site}/compare-basic.gif?run={run_id}&service=webhook-site" width="1" height="1" alt="">
            
            <h3>隐藏图片测试</h3>
            <img src="{webhook_site}/compare-hidden.gif?run={run_id}&service=webhook-site" style="display:none" alt="">
            
            <h3>CSS背景测试</h3>
            <div style="background-image:url('{webhook_site}/compare-css.gif?run={run_id}&service=webhook-site');width:1px;height:1px;"></div>
        </div>
        
        <div class="test-section our-ngrok">
            <h2>🔵 我们的ngrok 测试</h2>
            <p>这些图片指向我们的ngrok隧道，测试是否能被加载：</p>
            
            <h3>基础图片测试</h3>
            <img src="{our_ngrok}/compare-basic.gif?run={run_id}&service=our-ngrok" width="1" height="1" alt="">
            
            <h3>隐藏图片测试</h3>
            <img src="{our_ngrok}/compare-hidden.gif?run={run_id}&service=our-ngrok" style="display:none" alt="">
            
            <h3>CSS背景测试</h3>
            <div style="background-image:url('{our_ngrok}/compare-css.gif?run={run_id}&service=our-ngrok');width:1px;height:1px;"></div>
        </div>
        
        <div class="test-section">
            <h2>📊 测试说明</h2>
            <p><strong>预期结果：</strong></p>
            <ul>
                <li>🟢 webhook.site 应该收到所有请求（6个图片）</li>
                <li>🔵 我们的ngrok 可能收到0-6个请求</li>
            </ul>
            <p><strong>对比分析：</strong></p>
            <ul>
                <li>如果webhook.site收到请求，说明Gmail允许图片加载</li>
                <li>如果我们的ngrok没收到请求，说明问题在我们的配置</li>
                <li>如果两个都没收到请求，说明Gmail完全阻止了图片</li>
            </ul>
        </div>
    </body>
    </html>
    """
    
    # 发送邮件
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'🔍 对比测试：webhook.site vs ngrok - {run_id[:8]}'
    msg['From'] = "yuqizheng325@gmail.com"
    msg['To'] = "nicai51213@gmail.com"
    msg['X-Test-Run-ID'] = run_id
    msg['X-Test-Type'] = 'comparison'
    msg.attach(MIMEText(html_content, 'html'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("yuqizheng325@gmail.com", "cyqszyoonzwhtdoi")
        server.send_message(msg)
    
    print(f"✅ 对比测试邮件已发送")
    print(f"📊 Run ID: {run_id}")
    print(f"🟢 webhook.site: {webhook_site}")
    print(f"🔵 我们的ngrok: {our_ngrok}")
    print()
    print("📋 请检查：")
    print("1. webhook.site 是否收到请求")
    print("2. 我们的webhook_log.csv 是否收到请求")
    print("3. 对比两者的差异")

if __name__ == "__main__":
    send_comparison_test()
