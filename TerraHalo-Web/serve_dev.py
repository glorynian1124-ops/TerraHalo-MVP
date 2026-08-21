#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TerraHalo-Web 开发服务器（禁用缓存，便于前端迭代实时生效）

用法:
    python serve_dev.py            # 启动于 http://localhost:8000
"""
import os
import sys
import http.server

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 禁用缓存：每次请求都返回最新文件，避免前端迭代时看到旧页面
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write('[web] %s\n' % (fmt % args))


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = http.server.ThreadingHTTPServer(('0.0.0.0', port), NoCacheHandler)
    print('TerraHalo-Web serving on http://localhost:%d (no-cache)' % port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
