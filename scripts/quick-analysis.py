#!/usr/bin/env python3
"""
快速分析webhook数据
"""
import json
from datetime import datetime
from pathlib import Path

def analyze_webhook_data():
    """分析webhook数据"""
    
    # 读取数据
    with open('data/webhook-logs.json', 'r', encoding='utf-8') as f:
        logs = json.load(f)
    
    if not logs:
        print("❌ 没有找到webhook数据")
        return
    
    print("🔍 邮件隐私指纹测试分析报告")
    print("=" * 50)
    print(f"📅 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 总请求数: {len(logs)}")
    print(f"🎯 唯一测试数: {len(set(item['testId'] for item in logs))}")
    print(f"🆔 运行ID: {logs[0]['runId']}")
    print(f"⏰ 时间范围: {logs[0]['timestamp']} 到 {logs[-1]['timestamp']}")
    
    # 分析测试结果
    test_results = {}
    for log in logs:
        test_id = log['testId']
        if test_id not in test_results:
            test_results[test_id] = {
                'triggered': True,
                'hit_count': 0,
                'first_trigger': log['timestamp'],
                'last_trigger': log['timestamp'],
                'user_agents': set(),
                'ips': set()
            }
        
        test_results[test_id]['hit_count'] += 1
        test_results[test_id]['last_trigger'] = log['timestamp']
        test_results[test_id]['user_agents'].add(log['userAgent'])
        test_results[test_id]['ips'].add(log['clientIP'])
    
    # 统计信息
    total_tests = 20  # HTML-001到HTML-020
    triggered_tests = len(test_results)
    blocked_tests = total_tests - triggered_tests
    success_rate = (triggered_tests / total_tests) * 100
    
    print(f"\n📈 测试结果统计:")
    print(f"   总测试数: {total_tests}")
    print(f"   触发测试: {triggered_tests}")
    print(f"   阻止测试: {blocked_tests}")
    print(f"   成功率: {success_rate:.1f}%")
    
    print(f"\n✅ 成功触发的测试:")
    for test_id in sorted(test_results.keys()):
        result = test_results[test_id]
        print(f"   {test_id}: 触发 {result['hit_count']} 次")
    
    if blocked_tests > 0:
        print(f"\n❌ 被阻止的测试:")
        all_tests = [f"html-{i:03d}-" for i in range(1, 21)]
        blocked_tests_list = [test for test in all_tests if test not in test_results]
        for test_id in blocked_tests_list:
            print(f"   {test_id}: 被邮件客户端阻止")
    
    # 用户代理分析
    print(f"\n🌐 用户代理分析:")
    all_user_agents = set()
    for result in test_results.values():
        all_user_agents.update(result['user_agents'])
    
    for ua in sorted(all_user_agents):
        print(f"   {ua}")
    
    # 结论
    print(f"\n🎯 结论:")
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
    
    # 保存分析结果
    analysis_result = {
        'timestamp': datetime.now().isoformat(),
        'total_logs': len(logs),
        'unique_tests': len(test_results),
        'triggered_tests': triggered_tests,
        'blocked_tests': blocked_tests,
        'success_rate': success_rate,
        'test_results': {k: {
            'triggered': v['triggered'],
            'hit_count': v['hit_count'],
            'first_trigger': v['first_trigger'],
            'last_trigger': v['last_trigger'],
            'user_agents': list(v['user_agents']),
            'ips': list(v['ips'])
        } for k, v in test_results.items()},
        'summary': f"总日志: {len(logs)}, 触发测试: {triggered_tests}/{total_tests}, 成功率: {success_rate:.1f}%"
    }
    
    with open('data/analysis-report.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 分析结果已保存到: data/analysis-report.json")

if __name__ == "__main__":
    analyze_webhook_data()
