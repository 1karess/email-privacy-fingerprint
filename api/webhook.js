// Vercel Function for webhook monitoring
export default function handler(req, res) {
  // 设置CORS头
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  // 处理OPTIONS请求
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  
  // 记录请求信息
  const timestamp = new Date().toISOString();
  const clientIP = req.headers['x-forwarded-for'] || req.headers['x-real-ip'] || req.connection.remoteAddress;
  const userAgent = req.headers['user-agent'];
  const referer = req.headers['referer'];
  
  // 解析URL路径和查询参数
  const url = new URL(req.url, `https://${req.headers.host}`);
  const path = url.pathname;
  const query = Object.fromEntries(url.searchParams);
  
  // 构建日志记录
  const logEntry = {
    timestamp,
    method: req.method,
    client_ip: clientIP,
    path: path.replace(/^\//, ''),
    query: JSON.stringify(query),
    TestID: query.tid || path.split('/').pop(),
    RunSetID: query.run,
    UserAgent: userAgent,
    Referer: referer,
    Headers: JSON.stringify(req.headers)
  };
  
  // 输出到控制台（Vercel会显示在实时日志中）
  console.log('=== WEBHOOK REQUEST ===');
  console.log('Timestamp:', logEntry.timestamp);
  console.log('Method:', logEntry.method);
  console.log('Client IP:', logEntry.client_ip);
  console.log('Path:', logEntry.path);
  console.log('Query:', logEntry.query);
  console.log('Test ID:', logEntry.TestID);
  console.log('Run Set ID:', logEntry.RunSetID);
  console.log('User Agent:', logEntry.UserAgent);
  console.log('Referer:', logEntry.Referer);
  console.log('Headers:', logEntry.Headers);
  console.log('========================');
  
  // 返回成功响应
  res.status(200).json({ 
    success: true, 
    message: 'Webhook received',
    timestamp: logEntry.timestamp,
    testId: logEntry.TestID,
    runId: logEntry.RunSetID
  });
}
