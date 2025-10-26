#!/usr/bin/env python3
"""
发送 input vs img 对比测试邮件
验证 <input type="image"> 在邮件中是否会自动加载图片
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import uuid

# 配置
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "yuqizheng325@gmail.com"
SENDER_PASSWORD = "zdrd tbzz msjq bgia"  # Gmail应用密码
RECEIVER_EMAIL = "nicai51213@gmail.com"

# Webhook配置
WEBHOOK_BASE = "https://email-privacy-fingerprint.vercel.app"

def read_html_template(file_path):
    """读取HTML测试模板"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误: 找不到测试HTML文件 {file_path}")
        return None

def send_test_email(html_file, subject, description):
    """发送测试邮件"""
    
    # 读取HTML内容
    html_content = read_html_template(html_file)
    if not html_content:
        return False
    
    # 创建邮件
    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    
    # 添加纯文本版本
    text_content = f"""
{description}

请打开HTML版本查看完整测试。
"""
    
    # 添加HTML版本
    msg.attach(MIMEText(text_content, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    
    try:
        # 连接SMTP服务器
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            # 发送邮件
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            print(f"✅ {subject} 发送成功！")
            return True
            
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    print("🧪 Input vs Img 精确对比测试")
    print("=" * 50)
    print("分别测试 <input type='image'> 和 <img> 标签的追踪能力")
    print()
    
    # 检查应用密码
    if SENDER_PASSWORD == "your_app_password_here":
        print("❌ 请先设置Gmail应用密码")
        print("   1. 打开Google账户设置")
        print("   2. 安全 → 两步验证 → 应用密码")
        print("   3. 生成应用密码并替换脚本中的SENDER_PASSWORD")
        return
    
    # 发送两个独立的测试邮件
    print("📧 发送测试邮件...")
    print()
    
    # 测试1: 传统img标签
    print("1️⃣ 发送传统IMG标签测试...")
    success1 = send_test_email(
        "../../tests/phase2/img-only-test.html",
        "Phase2-IMG标签追踪测试",
        "测试传统<img>标签在邮件中的追踪能力"
    )
    
    if success1:
        print("   📋 检查: img-track.gif 是否被触发")
        print()
    
    # 测试2: input type="image"
    print("2️⃣ 发送Input标签测试...")
    success2 = send_test_email(
        "../../tests/phase2/input-only-test.html", 
        "Phase2-Input标签追踪测试",
        "测试<input type='image'>在邮件中的追踪能力"
    )
    
    if success2:
        print("   📋 检查: input-track.gif 是否被触发")
        print()
    
    # 测试3: input formaction
    print("3️⃣ 发送Input FormAction测试...")
    success3 = send_test_email(
        "../../tests/phase2/input-formaction-test.html", 
        "Phase2-Input FormAction追踪测试",
        "测试<input type='image' formaction>在邮件中的追踪能力"
    )
    
    if success3:
        print("   📋 检查: formaction-track.gif 是否被触发")
        print()
    
    # 测试4: button type="image"
    print("4️⃣ 发送Button Image测试...")
    success4 = send_test_email(
        "../../tests/phase2/button-image-test.html", 
        "Phase2-Button Image追踪测试",
        "测试<button type='image'>在邮件中的追踪能力"
    )
    
    if success4:
        print("   📋 检查: button-track.gif 是否被触发")
        print()
    
    if success1 and success2 and success3 and success4:
        print("✅ 四个测试邮件都发送成功！")
        print("\n🔍 下一步：")
        print("   1. 检查Gmail收件箱中的四个邮件")
        print("   2. 分别打开四个邮件（HTML版本）")
        print("   3. 检查Vercel日志：")
        print(f"      {WEBHOOK_BASE}/api/webhook/input-vs-img/")
        print("   4. 对比分析四个测试的结果")
        print("\n📊 关键对比：")
        print("   - img-track.gif: 传统<img>标签")
        print("   - input-track.gif: <input type='image'>")
        print("   - formaction-track.gif: <input formaction>")
        print("   - button-track.gif: <button type='image'>")
        print("\n🎯 测试目标：")
        print("   - 验证哪些INPUT变体可以用于邮件追踪")
        print("   - 发现新的追踪向量")
    else:
        print("❌ 部分测试邮件发送失败")

if __name__ == "__main__":
    main()
