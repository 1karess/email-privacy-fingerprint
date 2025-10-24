#!/usr/bin/env python3
"""
分析webhook测试结果
"""
import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

def analyze_webhook_log():
    """分析webhook日志"""
    log_file = Path("webhook_log.csv")
    
    if not log_file.exists():
        print("❌ webhook_log.csv 不存在")
        return
    
    # 读取日志
    with open(log_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        records = list(reader)
    
    print(f"📊 总记录数: {len(records)}")
    
    if len(records) == 0:
        print("📝 没有webhook请求记录")
        return
    
    # 按测试ID分组
    test_groups = defaultdict(list)
    for record in records:
        test_id = record.get('TestID', 'unknown')
        if test_id and test_id != 'unknown':
            test_groups[test_id].append(record)
    
    print(f"🔍 检测到的测试ID: {list(test_groups.keys())}")
    
    # 分析每个测试
    for test_id, hits in test_groups.items():
        print(f"\n📋 {test_id}:")
        print(f"   触发次数: {len(hits)}")
        
        for hit in hits:
            timestamp = hit.get('timestamp', 'unknown')
            user_agent = hit.get('UserAgent', 'unknown')
            ip = hit.get('client_ip', 'unknown')
            
            print(f"   ⏰ 时间: {timestamp}")
            print(f"   🌐 IP: {ip}")
            print(f"   🔍 User-Agent: {user_agent[:50]}...")
    
    # 检查是否有邮件客户端的请求
    email_clients = []
    for record in records:
        ua = record.get('UserAgent', '').lower()
        if any(client in ua for client in ['gmail', 'outlook', 'apple', 'yahoo', 'thunderbird']):
            email_clients.append(record)
    
    if email_clients:
        print(f"\n✅ 检测到邮件客户端请求: {len(email_clients)} 个")
        for client in email_clients:
            print(f"   📧 {client.get('UserAgent', 'unknown')}")
    else:
        print("\n❌ 没有检测到邮件客户端请求")
        print("   这可能表示:")
        print("   1. 邮件客户端的隐私保护机制生效")
        print("   2. 邮件还在传输中")
        print("   3. 需要手动启用图片加载")

def export_results():
    """导出测试结果"""
    log_file = Path("webhook_log.csv")
    results_file = Path("test_results.json")
    
    if not log_file.exists():
        print("❌ 没有测试数据可导出")
        return
    
    # 读取并分析数据
    with open(log_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        records = list(reader)
    
    # 按测试ID分组
    test_results = defaultdict(lambda: {
        'test_id': '',
        'triggered': False,
        'hit_count': 0,
        'hits': [],
        'first_trigger': None,
        'last_trigger': None
    })
    
    for record in records:
        test_id = record.get('TestID', 'unknown')
        if test_id and test_id != 'unknown':
            test_results[test_id]['test_id'] = test_id
            test_results[test_id]['triggered'] = True
            test_results[test_id]['hit_count'] += 1
            test_results[test_id]['hits'].append({
                'timestamp': record.get('timestamp'),
                'ip': record.get('client_ip'),
                'user_agent': record.get('UserAgent'),
                'path': record.get('path')
            })
            
            # 记录时间
            timestamp = record.get('timestamp')
            if timestamp:
                if not test_results[test_id]['first_trigger']:
                    test_results[test_id]['first_trigger'] = timestamp
                test_results[test_id]['last_trigger'] = timestamp
    
    # 导出结果
    results = {
        'analysis_time': datetime.now().isoformat(),
        'total_records': len(records),
        'test_results': dict(test_results),
        'summary': {
            'total_tests': len(test_results),
            'triggered_tests': sum(1 for r in test_results.values() if r['triggered']),
            'blocked_tests': sum(1 for r in test_results.values() if not r['triggered'])
        }
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"📄 结果已导出到: {results_file}")
    print(f"📊 测试总结:")
    print(f"   总测试数: {results['summary']['total_tests']}")
    print(f"   触发测试: {results['summary']['triggered_tests']}")
    print(f"   阻止测试: {results['summary']['blocked_tests']}")

def main():
    """主函数"""
    print("🔍 分析webhook测试结果")
    print("=" * 50)
    
    analyze_webhook_log()
    print("\n" + "=" * 50)
    export_results()

if __name__ == "__main__":
    main()
