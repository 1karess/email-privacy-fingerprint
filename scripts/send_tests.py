import datetime as dt
import json
import re
import smtplib
import time
import uuid
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Iterable, List

SENDER = "yuqizheng325@gmail.com"
PASSWORD = "cyqszyoonzwhtdoi"
RECEIVER = "nicai51213@gmail.com"

RUN_ID = uuid.uuid4().hex
WEBHOOK_BASE = Path("config/webhook_base.txt").read_text(encoding="utf-8").strip().rstrip("/")


@dataclass(frozen=True)
class TestCase:
    path: str
    subject: str
    category: str


def load_html(path: str) -> str:
    html = Path(path).read_text(encoding="utf-8")
    return html.replace("__WEBHOOK_BASE__", WEBHOOK_BASE)


def append_cache_buster(html: str) -> str:
    """
    为 webhook.site 的请求追加随机查询参数，避免缓存影响测试结果。
    """

    base_pattern = re.escape(f"{WEBHOOK_BASE}/")

    def repl(match: re.Match) -> str:
        base_url = match.group(1)
        return f"{base_url}?run={RUN_ID}&uid={uuid.uuid4().hex}"

    pattern = rf"({base_pattern}[^\"')\s]+)"
    return re.sub(pattern, repl, html)


def send_test(case: TestCase) -> None:
    html_content = append_cache_buster(load_html(case.path))
    msg = MIMEMultipart("alternative")
    msg["Subject"] = case.subject
    msg["From"] = SENDER
    msg["To"] = RECEIVER
    msg["X-Test-Run-Id"] = RUN_ID
    msg["X-Test-Category"] = case.category
    msg["X-Test-File"] = case.path
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.send_message(msg)
    print(f"已发送: {case.subject}")


def load_phase1_tests() -> List[TestCase]:
    """
    返回 Phase 1 Gmail→Gmail 基础测试用例。
    """
    config = [
        {
            "path": "tests/phase1/html-img-tests.html",
            "subject": "Phase1-HTML IMG 标签测试 (HTML-001~HTML-020)",
            "category": "HTML-IMG",
        }
    ]
    return [TestCase(**item) for item in config]


def export_manifest(cases: Iterable[TestCase]) -> None:
    """
    导出本次测试的元信息，方便记录。
    """
    manifest = {
        "run_id": RUN_ID,
        "timestamp": dt.datetime.utcnow().isoformat() + "Z",
        "sender": SENDER,
        "receiver": RECEIVER,
        "tests": [case.__dict__ for case in cases],
    }
    Path("data/phase1-run-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"已写入 run manifest: data/phase1-run-manifest.json（run_id={RUN_ID}）")


if __name__ == "__main__":
    cases = load_phase1_tests()
    export_manifest(cases)

    for case in cases:
        send_test(case)
        time.sleep(10)
