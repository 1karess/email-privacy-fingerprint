# 邮件测试关键配置

- **Webhook 基础地址**：`https://webhook.site/d76b930f-74bd-402b-b863-5117c1fd8ae4/`
- **发送邮箱 (Gmail)**：`yuqizheng325@gmail.com`
- **接收邮箱 (Gmail)**：`nicai51213@gmail.com`
- **发送邮箱应用专用密码**：`cyqszyoonzwhtdoi`
- **SMTP 设置**：服务器 `smtp.gmail.com`，端口 `587`（TLS）
- **缓存规避策略**：发送脚本会自动为指向 webhook.site 的 URL 追加 `?uid=<UUID>` 查询参数，避免缓存影响测试结果。

以上信息来自 `send_tests.py` 与 `send_security_tests.py`，可在重写 HTML 测试时直接复用。
