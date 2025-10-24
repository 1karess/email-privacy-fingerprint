#!/usr/bin/env python3
"""
生成详细的测试分析报告
"""
import json
from datetime import datetime
from pathlib import Path

def generate_markdown_report():
    """生成Markdown格式的分析报告"""
    
    # 读取分析数据
    analysis_file = Path("data/analysis-report.json")
    if not analysis_file.exists():
        print("❌ 没有找到分析数据，请先运行测试")
        return
    
    with open(analysis_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    analysis = data['analysis']
    
    # 生成报告
    report = f"""# 📊 邮件隐私指纹测试分析报告

## 📈 测试概览

- **测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **总日志数**: {analysis['total_logs']}
- **触发测试数**: {analysis['triggered_tests']}/20
- **阻止测试数**: {analysis['blocked_tests']}/20
- **成功率**: {analysis['success_rate']}%

## 🎯 测试结果详情

### ✅ 成功触发的测试

"""
    
    # 添加成功触发的测试
    triggered_tests = [test_id for test_id, result in analysis['test_results'].items() if result['triggered']]
    if triggered_tests:
        for test_id in sorted(triggered_tests):
            result = analysis['test_results'][test_id]
            report += f"- **{test_id}**: 触发 {result['hit_count']} 次\n"
    else:
        report += "无测试被触发\n"
    
    report += "\n### ❌ 被阻止的测试\n\n"
    
    # 添加被阻止的测试
    all_tests = [f"html-{i:03d}-" for i in range(1, 21)]
    blocked_tests = [test for test in all_tests if test not in triggered_tests]
    if blocked_tests:
        for test_id in blocked_tests:
            report += f"- **{test_id}**: 被邮件客户端阻止\n"
    else:
        report += "所有测试都被触发\n"
    
    report += f"""
## 💡 分析建议

"""
    
    # 添加建议
    for rec in data['recommendations']:
        report += f"- {rec}\n"
    
    report += f"""
## 📊 详细统计

### 测试分布
- 总测试数: 20
- 触发测试: {analysis['triggered_tests']}
- 阻止测试: {analysis['blocked_tests']}
- 成功率: {analysis['success_rate']}%

### 用户代理分析
"""
    
    # 分析用户代理
    user_agents = set()
    for result in analysis['test_results'].values():
        user_agents.update(result.get('user_agents', []))
    
    if user_agents:
        for ua in sorted(user_agents):
            report += f"- {ua}\n"
    else:
        report += "- 无用户代理信息\n"
    
    report += f"""
## 🔍 结论

根据测试结果，邮件客户端的隐私保护行为如下：

1. **隐私保护强度**: {'强' if analysis['success_rate'] < 50 else '中等' if analysis['success_rate'] < 80 else '弱'}
2. **追踪阻止率**: {100 - analysis['success_rate']}%
3. **建议**: {'建议启用更强的隐私保护设置' if analysis['success_rate'] > 50 else '当前隐私保护设置良好'}

---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # 保存报告
    report_file = Path("analysis/test-report.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📄 报告已生成: {report_file}")
    return report_file

if __name__ == "__main__":
    generate_markdown_report()
