#!/usr/bin/env python3
"""
实时监控webhook日志并生成分析报告
"""
import json
import time
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

class RealtimeMonitor:
    def __init__(self):
        self.data_dir = Path("data")
        self.logs_file = self.data_dir / "webhook-logs.json"
        self.analysis_file = self.data_dir / "analysis-report.json"
        self.last_check = None
        
    def load_logs(self):
        """加载日志数据"""
        if not self.logs_file.exists():
            return []
        
        try:
            with open(self.logs_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 加载日志失败: {e}")
            return []
    
    def analyze_logs(self, logs):
        """分析日志数据"""
        if not logs:
            return {
                'total_logs': 0,
                'unique_tests': 0,
                'triggered_tests': 0,
                'blocked_tests': 0,
                'test_results': {},
                'summary': '暂无数据'
            }
        
        # 按测试ID分组
        test_groups = defaultdict(list)
        for log in logs:
            test_id = log.get('testId', 'unknown')
            test_groups[test_id].append(log)
        
        # 分析每个测试
        test_results = {}
        for test_id, test_logs in test_groups.items():
            latest_log = max(test_logs, key=lambda x: x.get('timestamp', ''))
            test_results[test_id] = {
                'triggered': True,
                'hit_count': len(test_logs),
                'first_trigger': min(test_logs, key=lambda x: x.get('timestamp', ''))['timestamp'],
                'last_trigger': latest_log['timestamp'],
                'user_agents': list(set(log.get('userAgent', '') for log in test_logs)),
                'ips': list(set(log.get('clientIP', '') for log in test_logs))
            }
        
        # 计算统计信息
        total_logs = len(logs)
        unique_tests = len(test_groups)
        triggered_tests = len([r for r in test_results.values() if r['triggered']])
        
        # 预期的测试数量（HTML-001到HTML-020）
        expected_tests = 20
        blocked_tests = expected_tests - triggered_tests
        
        return {
            'total_logs': total_logs,
            'unique_tests': unique_tests,
            'triggered_tests': triggered_tests,
            'blocked_tests': blocked_tests,
            'success_rate': round((triggered_tests / expected_tests) * 100, 1) if expected_tests > 0 else 0,
            'test_results': test_results,
            'summary': f"总日志: {total_logs}, 触发测试: {triggered_tests}/{expected_tests}, 成功率: {round((triggered_tests / expected_tests) * 100, 1)}%"
        }
    
    def generate_report(self, analysis):
        """生成分析报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'analysis': analysis,
            'recommendations': self.get_recommendations(analysis)
        }
        
        # 保存报告
        with open(self.analysis_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report
    
    def get_recommendations(self, analysis):
        """生成建议"""
        recommendations = []
        
        if analysis['success_rate'] < 50:
            recommendations.append("🔒 邮件客户端隐私保护较强，大部分追踪被阻止")
        elif analysis['success_rate'] < 80:
            recommendations.append("⚠️ 邮件客户端部分隐私保护，部分追踪被阻止")
        else:
            recommendations.append("🚨 邮件客户端隐私保护较弱，大部分追踪未被阻止")
        
        if analysis['blocked_tests'] > 0:
            recommendations.append(f"📊 有 {analysis['blocked_tests']} 个测试被阻止，说明邮件客户端有隐私保护机制")
        
        if analysis['triggered_tests'] > 0:
            recommendations.append(f"✅ 有 {analysis['triggered_tests']} 个测试被触发，说明部分追踪成功")
        
        return recommendations
    
    def print_status(self, analysis):
        """打印状态信息"""
        print(f"\n🔍 实时监控状态 - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 50)
        print(f"📊 总日志数: {analysis['total_logs']}")
        print(f"🎯 触发测试: {analysis['triggered_tests']}/20")
        print(f"🚫 阻止测试: {analysis['blocked_tests']}/20")
        print(f"📈 成功率: {analysis['success_rate']}%")
        print("=" * 50)
        
        if analysis['recommendations']:
            print("💡 建议:")
            for rec in analysis['recommendations']:
                print(f"   {rec}")
    
    def monitor(self, interval=10):
        """开始监控"""
        print("🚀 启动实时监控...")
        print(f"📁 监控文件: {self.logs_file}")
        print(f"⏱️ 检查间隔: {interval}秒")
        print("按 Ctrl+C 停止监控")
        
        try:
            while True:
                logs = self.load_logs()
                analysis = self.analyze_logs(logs)
                report = self.generate_report(analysis)
                self.print_status(report)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n👋 监控已停止")

def main():
    monitor = RealtimeMonitor()
    monitor.monitor(interval=10)

if __name__ == "__main__":
    main()
