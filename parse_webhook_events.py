import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import parse_qs, urlparse

WEBHOOK_BASE_PATTERN = re.compile(r"(phase1/[^/?#]+)")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_headers(raw_headers: Any) -> Dict[str, str]:
    """
    将多种格式的 header 数据统一为 {key: value} 形式。
    """
    if isinstance(raw_headers, dict):
        return {str(k): str(v) for k, v in raw_headers.items()}
    if isinstance(raw_headers, list):
        # webhook.site 导出的 headers 可能是 [{"name": "...", "value": "..."}]
        headers = {}
        for item in raw_headers:
            if isinstance(item, dict):
                name = item.get("name") or item.get("key")
                value = item.get("value")
                if name and value:
                    headers[str(name)] = str(value)
        return headers
    return {}


def extract_url_candidate(event: Dict[str, Any]) -> Optional[str]:
    """
    尽可能从不同结构中找出 URL。
    """
    candidates = [
        event.get("url"),
        event.get("request_url"),
        event.get("raw_url"),
        event.get("target_url"),
    ]
    request = event.get("request") or {}
    candidates.extend(
        [
            request.get("url"),
            request.get("raw_url"),
            request.get("target_url"),
        ]
    )

    for url in candidates:
        if isinstance(url, str) and url:
            return url
    return None


def normalize_event(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    url = extract_url_candidate(event)
    if not url:
        return None

    parsed = urlparse(url)
    query_dict = {k: v if len(v) > 1 else v[0] for k, v in parse_qs(parsed.query).items()}

    headers = normalize_headers(
        event.get("headers")
        or event.get("request_headers")
        or (event.get("request") or {}).get("headers")
    )

    raw_path = parsed.path.lstrip("/")
    probe_match = WEBHOOK_BASE_PATTERN.search(raw_path)
    probe_path = probe_match.group(1) if probe_match else None

    return {
        "url": url,
        "raw_path": raw_path,
        "probe_path": probe_path,
        "query": query_dict,
        "timestamp": event.get("time")
        or event.get("timestamp")
        or event.get("date")
        or event.get("created_at"),
        "ip": event.get("ip") or (event.get("request") or {}).get("remote_ip"),
        "user_agent": headers.get("User-Agent")
        or headers.get("user-agent")
        or headers.get("user_agent"),
        "headers": headers,
        "raw": event,
    }


def load_events(path: Path) -> List[Dict[str, Any]]:
    raw = load_json(path)
    if isinstance(raw, dict):
        for key in ("data", "requests", "items", "entries"):
            if key in raw and isinstance(raw[key], list):
                raw = raw[key]
                break
    if not isinstance(raw, list):
        raise ValueError(f"无法解析事件文件格式: {path}")

    events = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        normalized = normalize_event(item)
        if normalized:
            events.append(normalized)
    return events


def load_test_map(path: Path) -> Dict[str, Dict[str, Any]]:
    data = load_json(path)
    result = {}
    for entry in data:
        probe_paths = entry.get("probe_paths") or []
        for probe in probe_paths:
            result[probe] = entry
    return result


def summarize_results(
    events: Iterable[Dict[str, Any]],
    test_map: Dict[str, Dict[str, Any]],
    run_id: str,
) -> Dict[str, Any]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for event in events:
        if not event["probe_path"]:
            continue
        query = event["query"]
        if query.get("run") != run_id:
            continue
        grouped[event["probe_path"]].append(event)

    summaries = []
    for probe_path, meta in test_map.items():
        hits = grouped.get(probe_path, [])
        summaries.append(
            {
                "test_id": meta["test_id"],
                "category": meta.get("category"),
                "description": meta.get("description"),
                "probe_path": probe_path,
                "triggered": bool(hits),
                "hit_count": len(hits),
                "hits": [
                    {
                        "url": hit["url"],
                        "timestamp": hit["timestamp"],
                        "ip": hit["ip"],
                        "user_agent": hit["user_agent"],
                        "headers": hit["headers"],
                    }
                    for hit in hits
                ],
            }
        )

    totals = {
        "total_tests": len(test_map),
        "triggered": sum(1 for item in summaries if item["triggered"]),
        "not_triggered": sum(1 for item in summaries if not item["triggered"]),
    }

    return {
        "run_id": run_id,
        "totals": totals,
        "results": summaries,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="根据 webhook.site 导出数据，生成 Phase 1 测试结果摘要。"
    )
    parser.add_argument("--manifest", required=True, type=Path, help="发送脚本生成的 manifest JSON。")
    parser.add_argument("--map", required=True, type=Path, help="测试 ID 与 webhook 路径映射。")
    parser.add_argument("--events", required=True, type=Path, help="webhook 导出的事件数据 JSON。")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("phase1-webhook-results.json"),
        help="输出结果 JSON 文件路径。",
    )
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    run_id = manifest.get("run_id")
    if not run_id:
        raise ValueError("manifest 中缺少 run_id。")

    test_map = load_test_map(args.map)
    events = load_events(args.events)
    summary = summarize_results(events, test_map, run_id)

    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"结果已写入 {args.output}。")
    print(
        f"共 {summary['totals']['total_tests']} 项测试，命中 {summary['totals']['triggered']}，未命中 {summary['totals']['not_triggered']}。"
    )


if __name__ == "__main__":
    main()
