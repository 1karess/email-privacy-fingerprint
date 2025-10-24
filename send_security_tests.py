import re
import smtplib
import time
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

SENDER = "yuqizheng325@gmail.com"
PASSWORD = "cyqszyoonzwhtdoi"
RECEIVER = "nicai51213@gmail.com"


def load_html(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def append_cache_buster(html: str) -> str:
    """
    为 webhook.site 的请求追加随机查询参数，避免缓存影响测试结果。
    """

    def repl(match: re.Match) -> str:
        base_url = match.group(1)
        return f"{base_url}?uid={uuid.uuid4().hex}"

    pattern = r"(https://webhook\.site/d76b930f-74bd-402b-b863-5117c1fd8ae4/[^\"')\s]+)"
    return re.sub(pattern, repl, html)


def send_test(html_path: str, subject: str) -> None:
    html_content = append_cache_buster(load_html(html_path))
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = RECEIVER
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.send_message(msg)
    print(f"已发送: {subject}")


if __name__ == "__main__":
    tests = [
        ("test-security-protocol.html", "安全测试A-协议探测"),
        ("test-security-svg.html", "安全测试B-SVG探测"),
        ("test-security-timing.html", "安全测试C-时序探测"),
        ("test-security-layout.html", "安全测试D-布局特性"),
        ("test-security-effects.html", "安全测试E-视觉特性"),
        ("test-security-font.html", "安全测试F-字体指纹"),
    ]

    for path, subject in tests:
        send_test(path, subject)
        time.sleep(10)
