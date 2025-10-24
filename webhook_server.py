import csv
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Dict, Tuple
from urllib.parse import ParseResult, parse_qs, urlparse

LOG_PATH = Path("webhook_log.csv")
LOG_HEADERS = [
    "timestamp",
    "method",
    "client_ip",
    "path",
    "query",
    "TestID",
    "RunSetID",
    "UserAgent",
    "Referer",
    "Headers",
]


def ensure_log_file() -> None:
    if not LOG_PATH.exists():
        with LOG_PATH.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(LOG_HEADERS)


class WebhookRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self) -> None:  # noqa: N802
        self._log_request()
        self.send_response(200)
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        self._handle_request()

    def do_POST(self) -> None:  # noqa: N802
        self._handle_request()

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        """
        禁用默认的 stdout 日志，让输出更干净。
        """
        return

    def _handle_request(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length > 0 else b""
        parsed, query_single = self._log_request(body)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def _log_request(self, body: bytes = b"") -> Tuple[ParseResult, Dict[str, object]]:
        ensure_log_file()

        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        query_single = {k: v[0] if len(v) == 1 else v for k, v in query.items()}

        client_ip = self.headers.get("X-Forwarded-For", self.client_address[0])
        record = [
            datetime.now(timezone.utc).isoformat(),
            self.command,
            client_ip,
            parsed.path.lstrip("/"),
            json.dumps(query_single, ensure_ascii=False),
            query_single.get("tid") or parsed.path.rsplit("/", 1)[-1],
            query_single.get("run"),
            self.headers.get("User-Agent"),
            self.headers.get("Referer"),
            json.dumps({k: v for k, v in self.headers.items()}, ensure_ascii=False),
        ]

        with LOG_PATH.open("a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(record)

        if body:
            body_path = Path("webhook_bodies")
            body_path.mkdir(exist_ok=True)
            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            file_name = f"{ts}_{parsed.path.lstrip('/').replace('/', '_') or 'root'}.bin"
            (body_path / file_name).write_bytes(body)

        return parsed, query_single


def run_server(port: int = 8000) -> None:
    ensure_log_file()
    server = HTTPServer(("0.0.0.0", port), WebhookRequestHandler)
    print(f"Webhook 服务器运行中: http://127.0.0.1:{port}")
    print("按 Ctrl+C 停止。")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止。")
        server.server_close()


if __name__ == "__main__":
    run_server()
