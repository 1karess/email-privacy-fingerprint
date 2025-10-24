const PIXEL_BUFFER = Buffer.from(
  'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
  'base64'
);

// 数据存储配置
const DATA_DIR = '/tmp/email-privacy-data';
const LOG_FILE = `${DATA_DIR}/webhook-logs.json`;

// 确保数据目录存在
import fs from 'fs';
import path from 'path';

function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

function saveLogEntry(logData) {
  try {
    ensureDataDir();
    
    // 读取现有日志
    let logs = [];
    if (fs.existsSync(LOG_FILE)) {
      const content = fs.readFileSync(LOG_FILE, 'utf8');
      logs = JSON.parse(content);
    }
    
    // 添加新日志
    logs.push(logData);
    
    // 保存到文件
    fs.writeFileSync(LOG_FILE, JSON.stringify(logs, null, 2));
    
    // 同时保存到项目目录（如果可能）
    try {
      const projectLogFile = './data/webhook-logs.json';
      if (!fs.existsSync('./data')) {
        fs.mkdirSync('./data', { recursive: true });
      }
      fs.writeFileSync(projectLogFile, JSON.stringify(logs, null, 2));
    } catch (e) {
      // 忽略项目目录写入错误
    }
    
  } catch (error) {
    console.error('保存日志失败:', error);
  }
}

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, HEAD, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }

  const timestamp = new Date().toISOString();
  // 获取真实IP地址，优先使用Vercel的代理头
  const forwardedFor = req.headers['x-forwarded-for'];
  const realIP = req.headers['x-real-ip'];
  const cfConnectingIP = req.headers['cf-connecting-ip']; // Cloudflare
  const clientIP = forwardedFor ? forwardedFor.split(',')[0].trim() : 
                   realIP || cfConnectingIP || 
                   req.socket?.remoteAddress || 
                   req.connection?.remoteAddress || 
                   'unknown';
  const userAgent = req.headers['user-agent'] || 'unknown';
  const referer = req.headers['referer'] || 'unknown';

  const url = new URL(req.url, `https://${req.headers.host}`);
  const query = Object.fromEntries(url.searchParams.entries());
  const routedPath = query.path ? String(query.path) : url.pathname.replace(/^\/api\/webhook\/?/, '');
  const normalizedPath = routedPath.replace(/^\//, '');
  const pathFragment = normalizedPath.split('/').pop() || '';
  const derivedTest = pathFragment.replace(/\.[^.]+$/, '');
  const testId = query.test || query.tid || derivedTest || 'unknown';
  const runId = query.run || query.run_id || 'unknown';

  // 构建日志数据
  const logData = {
    timestamp,
    testId,
    runId,
    clientIP,
    userAgent,
    referer,
    method: req.method,
    path: normalizedPath || '/',
    query: url.search || '',
    headers: {
      'user-agent': userAgent,
      'referer': referer,
      'x-forwarded-for': clientIP
    }
  };

  // 保存到文件
  saveLogEntry(logData);

  console.log('=== EMAIL TRACKING PIXEL HIT ===');
  console.log('Timestamp:', timestamp);
  console.log('Test ID:', testId);
  console.log('Run ID:', runId);
  console.log('Client IP:', clientIP);
  console.log('User Agent:', userAgent);
  console.log('Referer:', referer);
  console.log('Method:', req.method);
  console.log('Path:', normalizedPath || '/');
  console.log('Raw Query:', url.search || '');
  console.log('================================');

  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  res.setHeader('Content-Type', 'image/gif');
  res.setHeader('Content-Length', PIXEL_BUFFER.length);

  if (req.method === 'HEAD') {
    res.status(200).end();
    return;
  }

  res.status(200).end(PIXEL_BUFFER);
}