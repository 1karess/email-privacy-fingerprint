#!/usr/bin/env python3
"""
简单测试：发送一个包含单个图片的邮件
"""
import smtplib
import time
import uuid
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_simple_test():
    """发送简单测试邮件"""
    
    # 配置
    our_ngrok = "https://raylene-noncircuited-unfeasibly.ngrok-free.dev"
    run_id = str(uuid.uuid4())
    
    # 创建简单测试HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>简单测试</title>
    </head>
    <body>
        <h1>🔍 简单测试</h1>
        <p>测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Run ID: {run_id}</p>
        
        <h2>基础图片测试</h2>
        <img src="{our_ngrok}/simple-test.gif?run={run_id}&test=basic" width="1" height="1" alt="">
        
        <h2>隐藏图片测试</h2>
        <img src="{our_ngrok}/simple-test.gif?run={run_id}&test=hidden" style="display:none" alt="">
        
        <h2>CSS背景测试</h2>
        <div style="background-image:url('{our_ngrok}/simple-test.gif?run={run_id}&test=css');width:1px;height:1px;"></div>
        
        <p>如果我们的ngrok工作正常，应该收到3个请求。</p>
    </body>
    </html>
    """
    
    # 发送邮件
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'🔍 简单测试 - {run_id[:8]}'
    msg['From'] = "yuqizheng325@gmail.com"
    msg['To'] = "nicai51213@gmail.com"
    msg['X-Test-Run-ID'] = run_id
    msg['X-Test-Type'] = 'simple'
    msg.attach(MIMEText(html_content, 'html'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("yuqizheng325@gmail.com", "cyqszyoonzwhtdoi")
        server.send_message(msg)
    
    print(f"✅ 简单测试邮件已发送")
    print(f"📊 Run ID: {run_id}")
    print(f"🔵 我们的ngrok: {our_ngrok}")
    print()
    print("📋 请等待2-3分钟，然后检查webhook_log.csv")

if __name__ == "__main__":
    send_simple_test()
