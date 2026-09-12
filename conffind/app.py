#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ConfFind 会议资料检索站 —— 纯标准库实现，直接运行：python3 app.py"""
import hashlib
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, quote

import importer
import repo
import views
from db import get_db, init_db

BASE = os.path.dirname(os.path.abspath(__file__))
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
SECRET = b'conffind-demo-secret-v1'
TOKEN = hashlib.sha256(SECRET + ADMIN_PASSWORD.encode()).hexdigest()
DEFAULT_IMPORT = os.path.join(BASE, 'data', 'import.json')


# ---------------- 页面处理函数 ----------------

def h_home(ctx, p, b):
    body = views.home(repo.stats(), repo.tracks(), repo.conferences()[:6], repo.hot_terms(8))
    ctx.html(views.layout('首页', body))

def h_conferences(ctx, p, b):
    ctx.html(views.layout('会议库', views.conferences_page(repo.conferences())))

def h_conference(ctx, p, b, cid):
    conf = repo.get_conference(cid)
    if not conf:
        return ctx.html(views.layout('未找到', views.not_found('会议不存在')), 404)
    sessions = repo.conference_sessions(cid)
    files_map = {s['id']: repo.session_files(s['id']) for s in sessions}
    body = views.conference_page(conf, sessions, files_map, repo.conference_type_counts(cid))
    ctx.html(views.layout(conf['name'], body))

def h_search(ctx, p, b):
    q = (p.get('q') or '').strip()
    topic, speaker, ftype = p.get('topic') or '', p.get('speaker') or '', p.get('ftype') or ''
    searched = bool(q or topic or speaker or ftype)
    results = repo.search_files(q, topic, speaker, ftype) if searched else []
    if q:
        repo.log_search(q, len(results))
    body = views.search_page(q, topic, speaker, ftype, repo.tracks(), repo.speakers(), results, searched)
    ctx.html(views.layout('资料检索', body, q=q))

def h_file(ctx, p, b, fid):
    f = repo.get_file(fid)
    if not f:
        return ctx.html(views.layout('未找到', views.not_found('文件不存在')), 404)
    if f['status'] != 'active':
        return ctx.html(views.layout('条目已屏蔽', views.blocked_page(f)), 410)
    siblings = repo.session_files(f['session_id'])
    by_track, by_speaker = repo.related_conferences(f)
    ctx.html(views.layout(f['title'], views.file_page(f, siblings, by_track, by_speaker)))

def h_speaker(ctx, p, b, spid):
    sp, sessions = repo.get_speaker(spid)
    if not sp:
        return ctx.html(views.layout('未找到', views.not_found('讲者不存在')), 404)
    files_map = {s['id']: repo.session_files(s['id']) for s in sessions}
    ctx.html(views.layout(sp['name'], views.speaker_page(sp, sessions, files_map)))

def h_login_page(ctx, p, b):
    ctx.html(views.layout('后台登录', views.login_page(p.get('err') or '')))

def h_login(ctx, p, b):
    if (b.get('password') or '') == ADMIN_PASSWORD:
        ctx.send_response(302)
        ctx.send_header('Location', '/admin')
        ctx.send_header('Set-Cookie', 'cf_admin=%s; HttpOnly; Path=/; SameSite=Lax' % TOKEN)
        ctx.end_headers()
    else:
        ctx.html(views.layout('后台登录', views.login_page('密码错误，请重试')), 403)

def h_logout(ctx, p, b):
    ctx.send_response(302)
    ctx.send_header('Location', '/')
    ctx.send_header('Set-Cookie', 'cf_admin=; HttpOnly; Path=/; Max-Age=0')
    ctx.end_headers()

def h_admin(ctx, p, b):
    body = views.admin_page(
        stats=repo.stats(), hot_all=repo.hot_terms(20), hot_week=repo.hot_terms(20, days=7),
        recent=repo.recent_searches(15),
        files=repo.admin_files((p.get('kw') or '').strip(), p.get('status') or ''),
        kw=p.get('kw') or '', status=p.get('status') or '', msg=p.get('msg') or '')
    ctx.html(views.layout('管理后台', body))

def h_block(ctx, p, b):
    fid = int(b.get('id') or 0)
    reason = (b.get('reason') or '').strip() or '未填写原因'
    repo.block_file(fid, reason)
    ctx.redirect('/admin?status=blocked&msg=' + quote('已屏蔽条目 #%d' % fid))

def h_unblock(ctx, p, b):
    fid = int(b.get('id') or 0)
    repo.unblock_file(fid)
    ctx.redirect('/admin?msg=' + quote('已解除屏蔽条目 #%d' % fid))

def h_import(ctx, p, b):
    if not os.path.exists(DEFAULT_IMPORT):
        return ctx.redirect('/admin?msg=' + quote('未找到 data/import.json'))
    stats = importer.import_file(DEFAULT_IMPORT)
    msg = '导入完成：新增会议 %d / 议程 %d / 文件 %d' % (
        stats['conferences'], stats['sessions'], stats['files'])
    ctx.redirect('/admin?msg=' + quote(msg))

def h_favicon(ctx, p, b):
    ctx.send_response(204)
    ctx.end_headers()


ROUTES = [
    ('GET',  r'/',                 h_home,        False),
    ('GET',  r'/conferences',      h_conferences, False),
    ('GET',  r'/conference/(\d+)', h_conference,  False),
    ('GET',  r'/search',           h_search,      False),
    ('GET',  r'/file/(\d+)',       h_file,        False),
    ('GET',  r'/speaker/(\d+)',    h_speaker,     False),
    ('GET',  r'/admin',            h_admin,       True),
    ('GET',  r'/admin/login',      h_login_page,  False),
    ('POST', r'/admin/login',      h_login,       False),
    ('GET',  r'/admin/logout',     h_logout,      False),
    ('POST', r'/admin/block',      h_block,       True),
    ('POST', r'/admin/unblock',    h_unblock,     True),
    ('POST', r'/admin/import',     h_import,      True),
    ('GET',  r'/favicon.ico',      h_favicon,     False),
]


class Handler(BaseHTTPRequestHandler):
    server_version = 'ConfFind/1.0'

    def log_message(self, fmt, *args):
        pass  # 静默日志

    # ---- 响应辅助 ----
    def html(self, text, status=200):
        data = text.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def redirect(self, location):
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

    def is_admin(self):
        cookie = self.headers.get('Cookie') or ''
        for part in cookie.split(';'):
            k, _, v = part.strip().partition('=')
            if k == 'cf_admin' and v == TOKEN:
                return True
        return False

    # ---- 请求分发 ----
    def do_GET(self):
        self.dispatch('GET')

    def do_POST(self):
        self.dispatch('POST')

    def dispatch(self, method):
        try:
            parsed = urlparse(self.path)
            path = parsed.path.rstrip('/') or '/'
            params = {k: v[0] for k, v in parse_qs(parsed.query).items()}
            body = {}
            if method == 'POST':
                length = int(self.headers.get('Content-Length') or 0)
                raw = self.rfile.read(length).decode('utf-8', 'replace')
                body = {k: v[0] for k, v in parse_qs(raw).items()}
            for m, pattern, func, need_admin in ROUTES:
                if m != method:
                    continue
                match = re.fullmatch(pattern, path)
                if match:
                    if need_admin and not self.is_admin():
                        return self.redirect('/admin/login')
                    return func(self, params, body, *match.groups())
            self.html(views.layout('404', views.not_found()), 404)
        except BrokenPipeError:
            pass
        except Exception as exc:  # 兜底，避免服务挂掉
            self.html(views.layout('错误', views.not_found('服务器错误：%s' % exc)), 500)


def ensure_data():
    """首次启动时自动建表并导入示例数据。"""
    init_db()
    conn = get_db()
    n = conn.execute('SELECT COUNT(*) c FROM conferences').fetchone()['c']
    conn.close()
    if n == 0:
        if not os.path.exists(DEFAULT_IMPORT):
            import seed
            seed.main()
        print('首次启动，自动导入示例数据：', importer.import_file(DEFAULT_IMPORT))


if __name__ == '__main__':
    ensure_data()
    port = int(os.environ.get('PORT', 8000))
    print('ConfFind 已启动：http://127.0.0.1:%d  （后台 /admin，密码 %s）' % (port, ADMIN_PASSWORD))
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()
