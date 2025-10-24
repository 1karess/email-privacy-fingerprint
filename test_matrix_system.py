#!/usr/bin/env python3
"""
邮件客户端安全测试矩阵系统
按照完整的测试表格进行系统化测试
"""
import json
import smtplib
import time
import uuid
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# 配置
SENDER = "yuqizheng325@gmail.com"
PASSWORD = "cyqszyoonzwhtdoi"
RECEIVER = "nicai51213@gmail.com"

class EmailSecurityTestMatrix:
    """邮件客户端安全测试矩阵"""
    
    def __init__(self, webhook_base):
        self.webhook_base = webhook_base
        self.run_id = str(uuid.uuid4())
        self.test_results = []
        
    def create_test_html(self, test_category, test_cases):
        """创建测试HTML"""
        html = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>{test_category} - 邮件客户端安全测试</title>
            <style>
                body {{ font-family: system-ui, sans-serif; line-height: 1.6; padding: 16px; }}
                .test-section {{ background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; padding: 16px; margin: 16px 0; }}
                .test-id {{ font-weight: bold; color: #0066cc; }}
                .description {{ color: #666; font-size: 0.9em; }}
                img {{ border: 1px solid #ddd; margin: 4px; }}
            </style>
        </head>
        <body>
            <h1>📧 {test_category} 安全测试</h1>
            <p><strong>测试时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Run ID:</strong> {self.run_id}</p>
            <p><strong>测试类别:</strong> {test_category}</p>
        """
        
        for test_case in test_cases:
            html += f"""
            <div class="test-section">
                <div class="test-id">{test_case['test_id']}</div>
                <div class="description">{test_case['description']}</div>
                <div class="test-content">{test_case['html']}</div>
            </div>
            """
        
        html += """
            <div class="test-section">
                <h3>📊 测试说明</h3>
                <p>本邮件包含多个追踪测试向量，用于检测邮件客户端的隐私保护行为。</p>
                <p>如果webhook收到请求，说明该客户端允许了追踪；如果没有收到，说明隐私保护生效。</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_test_email(self, test_category, test_cases):
        """发送测试邮件"""
        html_content = self.create_test_html(test_category, test_cases)
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'🔍 {test_category} - 邮件安全测试'
        msg['From'] = SENDER
        msg['To'] = RECEIVER
        msg['X-Test-Run-ID'] = self.run_id
        msg['X-Test-Category'] = test_category
        msg.attach(MIMEText(html_content, 'html'))
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER, PASSWORD)
            server.send_message(msg)
        
        print(f"✅ 已发送 {test_category} 测试邮件")
        return self.run_id

# 测试用例定义
def get_html_img_tests(webhook_base, run_id):
    """HTML IMG标签测试 (HTML-001 ~ HTML-020)"""
    return [
        {
            'test_id': 'HTML-001',
            'description': '标准 <img> 标签应立即加载',
            'html': f'<img src="{webhook_base}/html-001-basic.gif?run={run_id}" width="1" height="1" alt="">'
        },
        {
            'test_id': 'HTML-002', 
            'description': '<img /> 自闭合写法',
            'html': f'<img src="{webhook_base}/html-002-self-close.gif?run={run_id}" width="1" height="1" alt="" />'
        },
        {
            'test_id': 'HTML-003',
            'description': '<IMG> 大写标签写法',
            'html': f'<IMG SRC="{webhook_base}/html-003-uppercase.gif?run={run_id}" WIDTH="1" HEIGHT="1">'
        },
        {
            'test_id': 'HTML-004',
            'description': '单引号属性值',
            'html': f'<img src=\'{webhook_base}/html-004-single-quote.gif?run={run_id}\' width="1" height="1" alt="">'
        },
        {
            'test_id': 'HTML-005',
            'description': '无引号属性值',
            'html': f'<img src={webhook_base}/html-005-no-quote.gif?run={run_id} width=1 height=1 alt="">'
        },
        {
            'test_id': 'HTML-006',
            'description': '带尺寸属性的图片',
            'html': f'<img src="{webhook_base}/html-006-dimension.gif?run={run_id}" width="48" height="32" alt="尺寸测试">'
        },
        {
            'test_id': 'HTML-007',
            'description': 'style=display:none 隐藏图片',
            'html': f'<img src="{webhook_base}/html-007-display-none.gif?run={run_id}" style="display:none" alt="">'
        },
        {
            'test_id': 'HTML-008',
            'description': 'hidden 属性隐藏图片',
            'html': f'<img src="{webhook_base}/html-008-hidden-attr.gif?run={run_id}" hidden alt="">'
        },
        {
            'test_id': 'HTML-009',
            'description': 'loading="lazy" 懒加载',
            'html': f'<img src="{webhook_base}/html-009-loading-lazy.gif?run={run_id}" loading="lazy" width="1" height="1" alt="">'
        },
        {
            'test_id': 'HTML-010',
            'description': 'loading="eager" 急切加载',
            'html': f'<img src="{webhook_base}/html-010-loading-eager.gif?run={run_id}" loading="eager" width="1" height="1" alt="">'
        },
        {
            'test_id': 'HTML-011',
            'description': 'decoding="async" 解码提示',
            'html': f'<img src="{webhook_base}/html-011-decoding-async.gif?run={run_id}" decoding="async" width="1" height="1" alt="">'
        },
        {
            'test_id': 'HTML-012',
            'description': 'decoding="sync" 解码提示',
            'html': f'<img src="{webhook_base}/html-012-decoding-sync.gif?run={run_id}" decoding="sync" width="1" height="1" alt="">'
        },
        {
            'test_id': 'HTML-013',
            'description': 'importance="high" 优先级提示',
            'html': f'<img src="{webhook_base}/html-013-importance-high.gif?run={run_id}" importance="high" width="1" height="1" alt="">'
        },
        {
            'test_id': 'HTML-014',
            'description': 'fetchpriority="high" 资源优先级',
            'html': f'<img src="{webhook_base}/html-014-fetchpriority-high.gif?run={run_id}" fetchpriority="high" width="1" height="1" alt="">'
        },
        {
            'test_id': 'HTML-015',
            'description': 'srcset 密度感知加载',
            'html': f'<img srcset="{webhook_base}/html-015-srcset-1x.gif?run={run_id} 1x, {webhook_base}/html-015-srcset-2x.gif?run={run_id} 2x" src="{webhook_base}/html-015-srcset-default.gif?run={run_id}" width="1" height="1" alt="">'
        },
        {
            'test_id': 'HTML-016',
            'description': 'srcset + sizes 宽度响应式加载',
            'html': f'<img srcset="{webhook_base}/html-016-srcset-320.gif?run={run_id} 320w, {webhook_base}/html-016-srcset-640.gif?run={run_id} 640w" sizes="(max-width: 480px) 320px, 640px" src="{webhook_base}/html-016-srcset-default.gif?run={run_id}" width="1" height="1" alt="">'
        },
        {
            'test_id': 'HTML-017',
            'description': 'crossorigin="anonymous" CORS 行为',
            'html': f'<img src="{webhook_base}/html-017-crossorigin-anon.gif?run={run_id}" crossorigin="anonymous" width="1" height="1" alt="">'
        },
        {
            'test_id': 'HTML-018',
            'description': 'referrerpolicy="no-referrer"',
            'html': f'<img src="{webhook_base}/html-018-referrerpolicy-noref.gif?run={run_id}" referrerpolicy="no-referrer" width="1" height="1" alt="">'
        },
        {
            'test_id': 'HTML-019',
            'description': '空 alt 属性',
            'html': f'<img src="{webhook_base}/html-019-alt-empty.gif?run={run_id}" alt="">'
        },
        {
            'test_id': 'HTML-020',
            'description': '带 title 属性',
            'html': f'<img src="{webhook_base}/html-020-title.gif?run={run_id}" title="HTML-020 带 title 属性" width="1" height="1" alt="HTML-020 带 title 属性">'
        }
    ]

def get_css_background_tests(webhook_base, run_id):
    """CSS背景追踪测试 (CSS-BG-001 ~ CSS-BG-010)"""
    return [
        {
            'test_id': 'CSS-BG-001',
            'description': 'background-image 基础背景',
            'html': f'<div style="background-image:url(\'{webhook_base}/css-bg-001-basic.gif?run={run_id}\');width:1px;height:1px;"></div>'
        },
        {
            'test_id': 'CSS-BG-002',
            'description': 'background 简写',
            'html': f'<div style="background:url(\'{webhook_base}/css-bg-002-shorthand.gif?run={run_id}\');width:1px;height:1px;"></div>'
        },
        {
            'test_id': 'CSS-BG-003',
            'description': '多背景图片',
            'html': f'<div style="background-image:url(\'{webhook_base}/css-bg-003-multi-1.gif?run={run_id}\'),url(\'{webhook_base}/css-bg-003-multi-2.gif?run={run_id}\');width:1px;height:1px;"></div>'
        },
        {
            'test_id': 'CSS-BG-004',
            'description': '渐变+图片组合',
            'html': f'<div style="background-image:linear-gradient(red,blue),url(\'{webhook_base}/css-bg-004-gradient.gif?run={run_id}\');width:1px;height:1px;"></div>'
        },
        {
            'test_id': 'CSS-BG-005',
            'description': 'border-image 边框图片',
            'html': f'<div style="border-image:url(\'{webhook_base}/css-bg-005-border.gif?run={run_id}\') 30;border-width:1px;border-style:solid;width:1px;height:1px;"></div>'
        },
        {
            'test_id': 'CSS-BG-006',
            'description': 'border-image-source 分离属性',
            'html': f'<div style="border-image-source:url(\'{webhook_base}/css-bg-006-border-source.gif?run={run_id}\');border-width:1px;border-style:solid;width:1px;height:1px;"></div>'
        },
        {
            'test_id': 'CSS-BG-007',
            'description': 'list-style-image 列表图标',
            'html': f'<ul style="list-style-image:url(\'{webhook_base}/css-bg-007-list.gif?run={run_id}\');"><li>Test</li></ul>'
        },
        {
            'test_id': 'CSS-BG-008',
            'description': 'list-style 简写',
            'html': f'<ul style="list-style:url(\'{webhook_base}/css-bg-008-list-shorthand.gif?run={run_id}\');"><li>Test</li></ul>'
        },
        {
            'test_id': 'CSS-BG-009',
            'description': 'content 替换内容',
            'html': f'<div style="content:url(\'{webhook_base}/css-bg-009-content.gif?run={run_id}\');"></div>'
        },
        {
            'test_id': 'CSS-BG-010',
            'description': 'cursor 光标图片',
            'html': f'<div style="cursor:url(\'{webhook_base}/css-bg-010-cursor.gif?run={run_id}\'),auto;width:100px;height:20px;border:1px solid #ccc;">Hover me</div>'
        }
    ]

def main():
    """主测试流程"""
    # 读取webhook配置
    webhook_base = Path("webhook_base.txt").read_text().strip()
    print(f"🌐 Webhook地址: {webhook_base}")
    
    # 创建测试矩阵
    test_matrix = EmailSecurityTestMatrix(webhook_base)
    
    print("🚀 开始邮件客户端安全测试矩阵")
    print(f"📊 Run ID: {test_matrix.run_id}")
    print()
    
    # 测试1: HTML IMG标签测试
    print("📧 发送测试1: HTML IMG标签测试 (HTML-001~HTML-020)")
    html_tests = get_html_img_tests(webhook_base, test_matrix.run_id)
    test_matrix.send_test_email("HTML IMG标签测试", html_tests)
    time.sleep(5)
    
    # 测试2: CSS背景追踪测试
    print("📧 发送测试2: CSS背景追踪测试 (CSS-BG-001~CSS-BG-010)")
    css_tests = get_css_background_tests(webhook_base, test_matrix.run_id)
    test_matrix.send_test_email("CSS背景追踪测试", css_tests)
    
    print()
    print("📋 测试完成！请检查：")
    print("1. 邮件是否到达收件箱")
    print("2. webhook_log.csv 中的请求记录")
    print("3. 不同测试向量的触发情况")
    print(f"4. Run ID: {test_matrix.run_id}")

if __name__ == "__main__":
    main()
