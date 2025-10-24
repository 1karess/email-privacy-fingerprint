#!/usr/bin/env python3
"""
显示测试结果的可视化界面
"""
import json
from datetime import datetime
from pathlib import Path

def show_results():
    """显示测试结果"""
    
    # 读取数据
    with open('data/webhook-logs.json', 'r', encoding='utf-8') as f:
        logs = json.load(f)
    
    if not logs:
        print("❌ 没有找到测试数据")
        return
    
    print("🔍 邮件隐私指纹测试结果")
    print("=" * 60)
    
    # 基本统计
    total_tests = 20
    triggered_tests = len(set(log['testId'] for log in logs))
    blocked_tests = total_tests - triggered_tests
    success_rate = (triggered_tests / total_tests) * 100
    
    print(f"📊 测试统计:")
    print(f"   总测试数: {total_tests}")
    print(f"   触发测试: {triggered_tests}")
    print(f"   阻止测试: {blocked_tests}")
    print(f"   成功率: {success_rate:.1f}%")
    print()
    
    # 测试映射
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
    
    print("🎯 详细测试结果:")
    print("-" * 60)
    
    # 显示所有测试结果
    for i in range(1, 21):
        test_key = f"html-{i:03d}-"
        # 找到匹配的测试ID
        matching_test = None
        for test_id in test_groups.keys():
            if test_id.startswith(test_key):
                matching_test = test_id
                break
        
        if matching_test and matching_test in test_groups:
            # 找到对应的测试
            test_logs = test_groups[matching_test]
            latest_log = max(test_logs, key=lambda x: x['timestamp'])
            test_name = test_map.get(matching_test, f"HTML-{i:03d}")
            print(f"✅ {test_name}")
            print(f"   触发时间: {latest_log['timestamp']}")
            print(f"   触发次数: {len(test_logs)}")
        else:
            # 没有找到对应的测试，说明被阻止了
            test_name = f"HTML-{i:03d}: 未知测试"
            print(f"❌ {test_name}")
            print(f"   状态: 被邮件客户端阻止")
        print()
    
    # 结论
    print("🎯 结论:")
    if success_rate == 100:
        print("   🚨 所有追踪向量都被触发！邮件客户端隐私保护较弱。")
        print("   💡 建议: 启用更强的隐私保护设置，如阻止图片加载。")
    elif success_rate >= 80:
        print("   ⚠️ 大部分追踪向量被触发，邮件客户端隐私保护中等。")
        print("   💡 建议: 考虑启用更严格的隐私保护设置。")
    elif success_rate >= 50:
        print("   🔒 部分追踪向量被阻止，邮件客户端有基本隐私保护。")
        print("   💡 建议: 当前设置提供了一定的隐私保护。")
    else:
        print("   ✅ 大部分追踪向量被阻止，邮件客户端隐私保护较强。")
        print("   💡 建议: 当前隐私保护设置良好。")
    
    print()
    print("📁 数据文件:")
    print(f"   webhook日志: data/webhook-logs.json ({len(logs)} 条记录)")
    print(f"   分析报告: data/analysis-report.json")
    print(f"   可视化仪表板: analysis/simple-dashboard.html")

if __name__ == "__main__":
    show_results()
