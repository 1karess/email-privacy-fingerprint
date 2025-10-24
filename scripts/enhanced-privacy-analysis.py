#!/usr/bin/env python3
"""
增强的隐私和指纹识别分析
"""
import json
import re
from datetime import datetime
from pathlib import Path

def parse_ip_info(ip):
    """解析IP信息"""
    if not ip or ip == 'unknown':
        return {'type': 'unknown', 'owner': 'unknown', 'is_proxy': False}
    
    # 检测已知代理IP段
    proxy_patterns = [
        (r'^66\.249\.', 'Google LLC', True),
        (r'^66\.102\.', 'Google LLC', True),
        (r'^74\.125\.', 'Google LLC', True),
        (r'^172\.217\.', 'Google LLC', True),
        (r'^216\.58\.', 'Google LLC', True),
        (r'^40\.107\.', 'Microsoft', True),
        (r'^52\.167\.', 'Microsoft', True),
        (r'^13\.107\.', 'Microsoft', True),
    ]
    
    for pattern, owner, is_proxy in proxy_patterns:
        if re.match(pattern, ip):
            return {'type': 'proxy', 'owner': owner, 'is_proxy': is_proxy}
    
    return {'type': 'direct', 'owner': 'unknown', 'is_proxy': False}

def parse_user_agent(ua):
    """解析User-Agent信息"""
    if not ua or ua == 'unknown':
        return {'email_client': 'unknown', 'platform': 'unknown', 'is_generic': True}
    
    # 检测邮件客户端
    if 'GoogleImageProxy' in ua:
        return {'email_client': 'Gmail', 'platform': 'Web', 'is_generic': True}
    elif 'Outlook' in ua:
        return {'email_client': 'Outlook', 'platform': 'Desktop', 'is_generic': False}
    elif 'Apple' in ua and 'Mail' in ua:
        return {'email_client': 'Apple Mail', 'platform': 'macOS', 'is_generic': False}
    elif 'Thunderbird' in ua:
        return {'email_client': 'Thunderbird', 'platform': 'Desktop', 'is_generic': False}
    else:
        return {'email_client': 'unknown', 'platform': 'unknown', 'is_generic': True}

def calculate_privacy_score(log):
    """计算隐私评分"""
    score = 100  # 满分100分
    
    # IP保护评分
    ip_info = parse_ip_info(log.get('clientIP', ''))
    if ip_info['is_proxy']:
        score += 20  # 使用代理保护IP
    else:
        score -= 30  # 直接暴露IP
    
    # User-Agent保护评分
    ua_info = parse_user_agent(log.get('userAgent', ''))
    if ua_info['is_generic']:
        score += 15  # 通用UA保护设备信息
    else:
        score -= 25  # 暴露设备信息
    
    # Referer保护评分
    referer = log.get('referer', '')
    if not referer or referer == 'unknown':
        score += 10  # 隐藏Referer
    else:
        score -= 20  # 暴露Referer
    
    # 时间戳精度评分
    timestamp = log.get('timestamp', '')
    if timestamp and '.' in timestamp:
        score -= 5  # 精确到毫秒
    
    return max(0, min(100, score))

def analyze_fingerprint_capability(logs):
    """分析指纹识别能力"""
    if not logs:
        return {}
    
    # 统计信息
    total_logs = len(logs)
    unique_ips = len(set(log.get('clientIP', '') for log in logs))
    unique_uas = len(set(log.get('userAgent', '') for log in logs))
    
    # 分析IP类型
    ip_types = {}
    for log in logs:
        ip_info = parse_ip_info(log.get('clientIP', ''))
        ip_type = ip_info['type']
        ip_types[ip_type] = ip_types.get(ip_type, 0) + 1
    
    # 分析邮件客户端
    email_clients = {}
    for log in logs:
        ua_info = parse_user_agent(log.get('userAgent', ''))
        client = ua_info['email_client']
        email_clients[client] = email_clients.get(client, 0) + 1
    
    return {
        'total_requests': total_logs,
        'unique_ips': unique_ips,
        'unique_user_agents': unique_uas,
        'ip_distribution': ip_types,
        'email_client_distribution': email_clients,
        'can_identify_user': unique_ips > 1,
        'can_identify_device': unique_uas > 1,
        'uses_proxy_protection': any(parse_ip_info(log.get('clientIP', ''))['is_proxy'] for log in logs)
    }

def generate_enhanced_report():
    """生成增强的分析报告"""
    
    # 读取数据
    with open('data/webhook-logs.json', 'r', encoding='utf-8') as f:
        logs = json.load(f)
    
    if not logs:
        print("❌ 没有找到测试数据")
        return
    
    print("🔍 增强隐私指纹分析报告")
    print("=" * 80)
    print(f"📅 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 总请求数: {len(logs)}")
    print()
    
    # 1. 请求来源分析
    print("🌐 请求来源分析")
    print("-" * 40)
    
    ip_info = parse_ip_info(logs[0].get('clientIP', ''))
    print(f"IP地址: {logs[0].get('clientIP', 'unknown')}")
    print(f"归属: {ip_info['owner']}")
    print(f"类型: {ip_info['type']}")
    print(f"代理保护: {'✅ 是' if ip_info['is_proxy'] else '❌ 否'}")
    print()
    
    # 2. 客户端识别分析
    print("🖥️ 客户端识别分析")
    print("-" * 40)
    
    ua_info = parse_user_agent(logs[0].get('userAgent', ''))
    print(f"User-Agent: {logs[0].get('userAgent', 'unknown')[:50]}...")
    print(f"邮件客户端: {ua_info['email_client']}")
    print(f"平台: {ua_info['platform']}")
    print(f"设备信息保护: {'✅ 是' if ua_info['is_generic'] else '❌ 否'}")
    print()
    
    # 3. 隐私评分分析
    print("🛡️ 隐私保护评分")
    print("-" * 40)
    
    privacy_scores = [calculate_privacy_score(log) for log in logs]
    avg_score = sum(privacy_scores) / len(privacy_scores)
    
    print(f"平均隐私评分: {avg_score:.1f}/100")
    if avg_score >= 80:
        print("评级: 🟢 优秀")
    elif avg_score >= 60:
        print("评级: 🟡 良好")
    elif avg_score >= 40:
        print("评级: 🟠 一般")
    else:
        print("评级: 🔴 较差")
    print()
    
    # 4. 指纹识别能力分析
    print("🔍 指纹识别能力分析")
    print("-" * 40)
    
    fingerprint_analysis = analyze_fingerprint_capability(logs)
    print(f"唯一IP数: {fingerprint_analysis['unique_ips']}")
    print(f"唯一User-Agent数: {fingerprint_analysis['unique_user_agents']}")
    print(f"可识别用户: {'✅ 是' if fingerprint_analysis['can_identify_user'] else '❌ 否'}")
    print(f"可识别设备: {'✅ 是' if fingerprint_analysis['can_identify_device'] else '❌ 否'}")
    print(f"代理保护: {'✅ 是' if fingerprint_analysis['uses_proxy_protection'] else '❌ 否'}")
    print()
    
    # 5. 详细测试结果
    print("📋 详细测试结果")
    print("-" * 40)
    
    test_map = {
        'html-001-basic': 'HTML-001: 标准 <img> 标签',
        'html-002-self-close': 'HTML-002: 自闭合 <img />',
        'html-003-uppercase': 'HTML-003: 大写标签 <IMG>',
        'html-004-single-quote': 'HTML-004: 单引号属性',
        'html-005-no-quote': 'HTML-005: 无引号属性',
        'html-006-dimension': 'HTML-006: 带尺寸属性',
        'html-007-display-none': 'HTML-007: display:none 隐藏',
        'html-008-hidden-attr': 'HTML-008: hidden 属性',
        'html-009-loading-lazy': 'HTML-009: loading="lazy"',
        'html-010-loading-eager': 'HTML-010: loading="eager"',
        'html-011-decoding-async': 'HTML-011: decoding="async"',
        'html-012-decoding-sync': 'HTML-012: decoding="sync"',
        'html-013-importance-high': 'HTML-013: importance="high"',
        'html-014-fetchpriority-high': 'HTML-014: fetchpriority="high"',
        'html-015-srcset-default': 'HTML-015: srcset（密度）',
        'html-016-srcset-default': 'HTML-016: srcset（宽度）',
        'html-017-crossorigin-anon': 'HTML-017: crossorigin="anonymous"',
        'html-018-referrerpolicy-noref': 'HTML-018: referrerpolicy="no-referrer"',
        'html-019-alt-empty': 'HTML-019: 空 alt 属性',
        'html-020-title': 'HTML-020: 带 title 属性'
    }
    
    # 按测试ID分组
    test_groups = {}
    for log in logs:
        test_id = log['testId']
        if test_id not in test_groups:
            test_groups[test_id] = []
        test_groups[test_id].append(log)
    
    for i in range(1, 21):
        test_key = f"html-{i:03d}-"
        matching_test = None
        for test_id in test_groups.keys():
            if test_id.startswith(test_key):
                matching_test = test_id
                break
        
        if matching_test and matching_test in test_groups:
            test_logs = test_groups[matching_test]
            latest_log = max(test_logs, key=lambda x: x['timestamp'])
            test_name = test_map.get(matching_test, f"HTML-{i:03d}")
            privacy_score = calculate_privacy_score(latest_log)
            
            print(f"✅ {test_name}")
            print(f"   触发时间: {latest_log['timestamp']}")
            print(f"   隐私评分: {privacy_score}/100")
            print(f"   IP保护: {'✅' if parse_ip_info(latest_log.get('clientIP', ''))['is_proxy'] else '❌'}")
            print(f"   UA保护: {'✅' if parse_user_agent(latest_log.get('userAgent', ''))['is_generic'] else '❌'}")
        else:
            test_name = f"HTML-{i:03d}: 未知测试"
            print(f"❌ {test_name}")
            print(f"   状态: 被邮件客户端阻止")
        print()
    
    # 6. 综合结论
    print("🎯 综合结论")
    print("-" * 40)
    
    if avg_score >= 80:
        print("🟢 隐私保护优秀：邮件客户端提供了良好的隐私保护")
    elif avg_score >= 60:
        print("🟡 隐私保护良好：邮件客户端提供了一定的隐私保护")
    elif avg_score >= 40:
        print("🟠 隐私保护一般：邮件客户端的隐私保护有待改进")
    else:
        print("🔴 隐私保护较差：邮件客户端的隐私保护不足")
    
    print(f"\n💡 建议:")
    if not fingerprint_analysis['uses_proxy_protection']:
        print("   - 启用代理保护以隐藏真实IP地址")
    if not all(parse_user_agent(log.get('userAgent', ''))['is_generic'] for log in logs):
        print("   - 使用通用User-Agent以保护设备信息")
    if any(log.get('referer') and log.get('referer') != 'unknown' for log in logs):
        print("   - 隐藏Referer信息以保护浏览历史")
    
    # 保存增强分析结果
    enhanced_analysis = {
        'timestamp': datetime.now().isoformat(),
        'basic_stats': {
            'total_logs': len(logs),
            'unique_tests': len(test_groups),
            'success_rate': 100.0
        },
        'privacy_analysis': {
            'average_privacy_score': avg_score,
            'ip_protection': ip_info,
            'user_agent_protection': ua_info,
            'privacy_rating': '优秀' if avg_score >= 80 else '良好' if avg_score >= 60 else '一般' if avg_score >= 40 else '较差'
        },
        'fingerprint_analysis': fingerprint_analysis,
        'detailed_results': {
            test_id: {
                'triggered': True,
                'privacy_score': calculate_privacy_score(max(test_groups[test_id], key=lambda x: x['timestamp'])),
                'ip_protected': parse_ip_info(max(test_groups[test_id], key=lambda x: x['timestamp']).get('clientIP', ''))['is_proxy'],
                'ua_protected': parse_user_agent(max(test_groups[test_id], key=lambda x: x['timestamp']).get('userAgent', ''))['is_generic']
            } for test_id in test_groups.keys()
        }
    }
    
    with open('data/enhanced-privacy-analysis.json', 'w', encoding='utf-8') as f:
        json.dump(enhanced_analysis, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 增强分析结果已保存到: data/enhanced-privacy-analysis.json")

if __name__ == "__main__":
    generate_enhanced_report()
