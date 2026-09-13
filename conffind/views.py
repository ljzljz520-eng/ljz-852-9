# -*- coding: utf-8 -*-
"""页面渲染：服务端渲染 HTML。"""
import html
from urllib.parse import quote

def e(s):
    return html.escape('' if s is None else str(s))

def qurl(s):
    return quote(str(s or ''))

FILE_TYPES = {
    'ppt':        ('PPT',  'bt-ppt'),
    'abstract':   ('摘要', 'bt-abs'),
    'attachment': ('附件', 'bt-att'),
    'video':      ('视频', 'bt-vid'),
    'paper':      ('论文', 'bt-ppr'),
}

def badge(t):
    label, cls = FILE_TYPES.get(t, (t, 'bt-att'))
    return '<span class="bt %s">%s</span>' % (cls, e(label))

def fmt_size(kb):
    kb = kb or 0
    return '%.1f MB' % (kb / 1024.0) if kb >= 1024 else '%d KB' % kb

CSS = """
:root{--bg:#f4f6fa;--card:#fff;--ink:#1c2333;--mut:#6b7484;--line:#e3e8f0;--pri:#2563eb;--pri-d:#1e40af}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.6}
a{color:var(--pri);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
header{background:#16213e;color:#fff}
header .wrap{display:flex;align-items:center;gap:20px;padding:13px 20px;flex-wrap:wrap}
.logo{font-size:20px;font-weight:700;color:#fff}.logo span{color:#7dd3fc}
nav a{color:#cbd5e1;margin-right:16px;font-size:14px}nav a:hover{color:#fff}
.hsearch{margin-left:auto;display:flex}
.hsearch input{padding:7px 12px;border:none;border-radius:6px 0 0 6px;width:220px;font-size:14px}
.hsearch button{padding:7px 14px;border:none;background:var(--pri);color:#fff;border-radius:0 6px 6px 0;cursor:pointer}
main{padding:26px 0 60px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:22px;margin-bottom:20px}
h1{font-size:24px;margin-bottom:10px}h2{font-size:18px;margin:16px 0 10px}
.mut{color:var(--mut);font-size:13px}
.hero{text-align:center;padding:30px 0 6px}
.hero h1{font-size:30px}
.hero form{margin:18px auto 6px;display:flex;max-width:640px}
.hero input{flex:1;padding:12px 16px;font-size:15px;border:1px solid var(--line);border-radius:8px 0 0 8px;border-right:none}
.hero button{padding:12px 26px;border:none;background:var(--pri);color:#fff;font-size:15px;border-radius:0 8px 8px 0;cursor:pointer}
.stats{display:flex;gap:14px;flex-wrap:wrap;margin:18px 0}
.stat{flex:1;min-width:130px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;text-align:center}
.stat b{display:block;font-size:26px;color:var(--pri)}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{background:#eef2ff;border:1px solid #dbe3ff;color:#3730a3;padding:4px 12px;border-radius:999px;font-size:13px}
table{width:100%;border-collapse:collapse;font-size:14px}
th,td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{background:#f8fafc;font-weight:600;color:#475569;font-size:13px}
.bt{display:inline-block;padding:1px 8px;border-radius:4px;font-size:12px;font-weight:600;white-space:nowrap}
.bt-ppt{background:#fff1e6;color:#c2410c}.bt-abs{background:#e0f2fe;color:#0369a1}
.bt-att{background:#f1f5f9;color:#475569}.bt-vid{background:#fee2e2;color:#b91c1c}
.bt-ppr{background:#dcfce7;color:#15803d}
.filters{display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end;margin-bottom:16px}
.filters label{font-size:12px;color:var(--mut);display:block;margin-bottom:3px}
.filters input,.filters select{padding:8px 10px;border:1px solid var(--line);border-radius:6px;font-size:14px;background:#fff}
.btn{display:inline-block;padding:8px 16px;border:none;border-radius:6px;background:var(--pri);color:#fff;font-size:14px;cursor:pointer}
.btn:hover{background:var(--pri-d);text-decoration:none}
.btn-sm{padding:4px 10px;font-size:13px}
.btn-danger{background:#dc2626}.btn-grey{background:#64748b}
.day-h{background:#eef2ff;border-radius:8px;padding:8px 14px;margin:16px 0 8px;font-weight:600}
.track-h{color:var(--pri-d);font-weight:600;margin:10px 0 6px}
.session{border:1px solid var(--line);border-radius:8px;padding:12px 16px;margin:8px 0;background:#fff}
.session h3{font-size:15px}
.files{margin:8px 0 0;list-style:none}
.files li{padding:3px 0;font-size:13.5px}
.cur{background:#fffbeb;border-radius:4px;padding:2px 6px;font-weight:600}
.meta{display:grid;grid-template-columns:110px 1fr;gap:6px 14px;font-size:14px}
.meta dt{color:var(--mut)}.meta dd{margin:0;word-break:break-all}
.grid2{display:grid;grid-template-columns:2fr 1fr;gap:20px}
@media(max-width:820px){.grid2{grid-template-columns:1fr}}
.alert{padding:12px 16px;border-radius:8px;margin-bottom:16px;font-size:14px}
.alert-ok{background:#dcfce7;color:#166534}.alert-err{background:#fee2e2;color:#991b1b}
.tag-b{color:#b91c1c;font-weight:600}.tag-a{color:#15803d;font-weight:600}
footer{border-top:1px solid var(--line);padding:18px 0;text-align:center;color:var(--mut);font-size:13px}
.crumb{font-size:13px;color:var(--mut);margin-bottom:12px}
.hotnum{display:inline-block;width:22px;height:22px;line-height:22px;text-align:center;border-radius:6px;background:#e2e8f0;color:#475569;font-size:12px;margin-right:6px}
.hotnum.top{background:#fee2e2;color:#b91c1c;font-weight:700}
.inline{display:flex;gap:6px;align-items:center}
.inline input{padding:5px 8px;border:1px solid var(--line);border-radius:6px;font-size:13px;width:150px}
"""

def layout(title, body, q=''):
    return """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s · ConfFind 会议资料检索站</title>
<style>%s</style></head>
<body>
<header><div class="wrap">
<a class="logo" href="/">Conf<span>Find</span></a>
<nav><a href="/">首页</a><a href="/conferences">会议库</a><a href="/search">资料检索</a><a href="/admin">管理后台</a></nav>
<form class="hsearch" action="/search" method="get">
<input name="q" value="%s" placeholder="搜索 PPT / 摘要 / 附件…"><button>搜索</button>
</form></div></header>
<main><div class="wrap">%s</div></main>
<footer>ConfFind · 公开会议资料元数据检索演示站 · 数据由公开渠道导入 · 仅保存元数据</footer>
</body></html>""" % (e(title), CSS, e(q), body)

# ---------------- 前台页面 ----------------

def home(stats, tracks, confs, hot):
    stat_html = ''.join(
        '<div class="stat"><b>%d</b>%s</div>' % (v, k) for v, k in [
            (stats['conferences'], '场会议'), (stats['sessions'], '个议程'),
            (stats['files'], '份资料'), (stats['speakers'], '位讲者')])
    chips = ''.join('<a class="chip" href="/search?topic=%s">%s (%d)</a>' % (qurl(t['track']), e(t['track']), t['c'])
                    for t in tracks)
    conf_items = ''.join(
        '<tr><td><a href="/conference/%d">%s</a> <span class="mut">%s</span></td>'
        '<td>%s ~ %s</td><td>%s</td><td>%d 议程 / %d 资料</td></tr>'
        % (c['id'], e(c['name']), e(c['acronym']), e(c['start_date']), e(c['end_date']),
           e(c['location']), c['n_sessions'], c['n_files'])
        for c in confs)
    hot_items = ''.join(
        '<li style="padding:4px 0"><span class="hotnum%s">%d</span>'
        '<a href="/search?q=%s">%s</a> <span class="mut">%d 次</span></li>'
        % (' top' if i < 3 else '', i + 1, qurl(h['term']), e(h['term']), h['cnt'])
        for i, h in enumerate(hot))
    body = """
<div class="hero">
  <h1>会议资料一站检索</h1>
  <p class="mut">公开会议日程 · 演讲 PPT · 摘要 · 附件元数据</p>
  <form action="/search" method="get">
    <input name="q" placeholder="输入主题、讲者、文件名关键词，如：大模型 / 张伟 / Flink">
    <button>搜索</button>
  </form>
</div>
<div class="stats">%s</div>
<div class="grid2">
  <div class="card"><h2>最新会议</h2>
    <table><tr><th>会议</th><th>时间</th><th>地点</th><th>规模</th></tr>%s</table>
  </div>
  <div>
    <div class="card"><h2>热门主题</h2><div class="chips">%s</div></div>
    <div class="card"><h2>热门搜索</h2><ol style="list-style:none">%s</ol></div>
  </div>
</div>""" % (stat_html, conf_items, chips, hot_items)
    return body

def conferences_page(confs):
    rows = ''.join(
        '<tr><td><a href="/conference/%d"><b>%s</b></a> <span class="mut">%s</span><br>'
        '<span class="mut">%s</span></td><td>%s ~ %s</td><td>%s</td>'
        '<td>%d 议程 / %d 资料</td><td><a href="%s">官方来源</a></td></tr>'
        % (c['id'], e(c['name']), e(c['acronym']), e(c['description']),
           e(c['start_date']), e(c['end_date']), e(c['location']),
           c['n_sessions'], c['n_files'], e(c['source_url']))
        for c in confs)
    return '<div class="card"><h1>会议库</h1><table><tr><th>会议</th><th>时间</th><th>地点</th><th>规模</th><th>来源</th></tr>%s</table></div>' % rows

def search_page(q, topic, speaker, ftype, topics, speakers, results, searched):
    topic_opts = '<option value="">全部主题</option>' + ''.join(
        '<option value="%s"%s>%s</option>' % (e(t['track']), ' selected' if t['track'] == topic else '', e(t['track']))
        for t in topics)
    sp_opts = '<option value="">全部讲者</option>' + ''.join(
        '<option value="%s"%s>%s（%s）</option>' % (e(s['name']), ' selected' if s['name'] == speaker else '', e(s['name']), e(s['affiliation']))
        for s in speakers)
    ft_opts = '<option value="">全部类型</option>' + ''.join(
        '<option value="%s"%s>%s</option>' % (k, ' selected' if k == ftype else '', v[0])
        for k, v in FILE_TYPES.items())
    filters = """
<form class="filters" action="/search" method="get">
  <div><label>关键词</label><input name="q" value="%s" placeholder="标题 / 文件名 / 摘要 / 主题 / 讲者"></div>
  <div><label>主题</label><select name="topic">%s</select></div>
  <div><label>讲者</label><select name="speaker">%s</select></div>
  <div><label>文件类型</label><select name="ftype">%s</select></div>
  <button class="btn">检索</button><a class="btn btn-grey" href="/search">重置</a>
</form>""" % (e(q), topic_opts, sp_opts, ft_opts)

    if not searched:
        result_html = '<p class="mut">输入关键词或选择筛选条件开始检索。</p>'
    elif not results:
        result_html = '<div class="alert alert-err">未找到匹配的资料，换个关键词试试。</div>'
    else:
        rows = ''.join(
            '<tr><td>%s</td><td><a href="/file/%d"><b>%s</b></a><br>'
            '<span class="mut">%s · %s · %s%s</span></td>'
            '<td><a href="/conference/%d">%s</a><br><span class="mut">%s</span></td>'
            '<td>%s</td><td>%s</td></tr>'
            % (badge(r['file_type']), r['id'], e(r['title']), e(r['filename']), e(r['format']),
               fmt_size(r['size_kb']), (' · %d 页' % r['pages']) if r['pages'] else '',
               r['conf_id'], e(r['conf_name']), e(r['session_title']),
               e(r['speakers'] or '—'), e(r['track']))
            for r in results)
        result_html = ('<p class="mut">共 %d 条结果（最多显示 200 条）</p>'
                       '<table><tr><th>类型</th><th>资料</th><th>所属会议 / 议程</th><th>讲者</th><th>主题</th></tr>%s</table>'
                       % (len(results), rows))
    return '<div class="card"><h1>资料检索</h1>%s%s</div>' % (filters, result_html)

def _speaker_links(speaker_list):
    return '、'.join('<a href="/speaker/%d">%s</a>' % (sp['id'], e(sp['name'])) for sp in speaker_list) or '—'

def conference_page(conf, sessions, files_map, type_counts):
    parts = ['<div class="crumb"><a href="/">首页</a> / <a href="/conferences">会议库</a> / %s</div>' % e(conf['name'])]
    parts.append('<div class="card"><h1>%s <span class="mut">%s</span></h1>'
                 '<p class="mut">📅 %s ~ %s ｜ 📍 %s ｜ <a href="%s">官方来源</a></p><p>%s</p></div>'
                 % (e(conf['name']), e(conf['acronym']), e(conf['start_date']), e(conf['end_date']),
                    e(conf['location']), e(conf['source_url']), e(conf['description'])))
    parts.append('<div class="grid2"><div><div class="card"><h2>会议日程与文件结构</h2>')
    cur_day = cur_track = None
    for s in sessions:
        if s['day'] != cur_day:
            cur_day, cur_track = s['day'], None
            parts.append('<div class="day-h">📅 %s</div>' % e(s['day']))
        if s['track'] != cur_track:
            cur_track = s['track']
            parts.append('<div class="track-h">🧭 主题：%s</div>' % e(s['track']))
        parts.append('<div class="session"><h3>%s–%s　%s</h3>'
                     '<div class="mut">📍 %s ｜ 👤 %s</div>'
                     % (e(s['start_time']), e(s['end_time']), e(s['title']),
                        e(s['room']), _speaker_links(s['speaker_list'])))
        if s['abstract']:
            parts.append('<p class="mut">%s</p>' % e(s['abstract']))
        flist = files_map.get(s['id'], [])
        if flist:
            parts.append('<ul class="files">')
            for f in flist:
                parts.append('<li>├─ %s <a href="/file/%d">%s</a> '
                             '<span class="mut">%s · %s</span></li>'
                             % (badge(f['file_type']), f['id'], e(f['title']),
                                e(f['filename']), fmt_size(f['size_kb'])))
            parts.append('</ul>')
        parts.append('</div>')
    parts.append('</div></div>')  # /card /left col

    type_rows = ''.join('<tr><td>%s</td><td>%d</td></tr>' % (badge(t['file_type']), t['c']) for t in type_counts)
    track_set = []
    for s in sessions:
        if s['track'] and s['track'] not in track_set:
            track_set.append(s['track'])
    track_chips = ''.join('<a class="chip" href="/search?topic=%s">%s</a>' % (qurl(t), e(t)) for t in track_set)
    sp_seen, sp_html = set(), []
    for s in sessions:
        for sp in s['speaker_list']:
            if sp['id'] not in sp_seen:
                sp_seen.add(sp['id'])
                sp_html.append('<li><a href="/speaker/%d">%s</a></li>' % (sp['id'], e(sp['name'])))
    parts.append('<div><div class="card"><h2>资料类型统计</h2><table>%s</table></div>'
                 '<div class="card"><h2>涉及主题</h2><div class="chips">%s</div></div>'
                 '<div class="card"><h2>讲者</h2><ul style="list-style:none">%s</ul></div>'
                 '</div></div>' % (type_rows, track_chips, ''.join(sp_html)))
    return ''.join(parts)

def file_page(f, siblings, by_track, by_speaker):
    crumb = ('<div class="crumb"><a href="/">首页</a> / <a href="/conference/%d">%s</a> / 资料详情</div>'
             % (f['conference_id'], e(f['conf_name'])))
    meta = """
<div class="card"><h1>%s %s</h1>
<dl class="meta">
<dt>文件名</dt><dd>%s</dd>
<dt>类型 / 格式</dt><dd>%s / %s</dd>
<dt>大小</dt><dd>%s</dd>
<dt>页数</dt><dd>%s</dd>
<dt>语言</dt><dd>%s</dd>
<dt>上传时间</dt><dd>%s</dd>
<dt>来源链接</dt><dd><a href="%s">%s</a></dd>
<dt>SHA1 校验</dt><dd><code>%s</code></dd>
<dt>所属会议</dt><dd><a href="/conference/%d">%s（%s）</a> · %s</dd>
<dt>所属议程</dt><dd>%s（%s %s–%s · %s）</dd>
<dt>讲者</dt><dd>%s</dd>
<dt>主题</dt><dd><a class="chip" href="/search?topic=%s">%s</a></dd>
</dl></div>""" % (
        badge(f['file_type']), e(f['title']), e(f['filename']),
        e(dict((k, v[0]) for k, v in FILE_TYPES.items()).get(f['file_type'], f['file_type'])),
        e(f['format']), fmt_size(f['size_kb']), f['pages'] or '—', e(f['language']),
        e(f['uploaded_at']), e(f['source_url']), e(f['source_url']), e(f['checksum']),
        f['conference_id'], e(f['conf_name']), e(f['acronym']), e(f['location']),
        e(f['session_title']), e(f['day']), e(f['start_time']), e(f['end_time']), e(f['room']),
        _speaker_links(f['speaker_list']), qurl(f['track']), e(f['track']))

    tree = ['<div class="card"><h2>文件结构（在会议中的位置）</h2><ul class="files">']
    tree.append('<li>📅 <a href="/conference/%d">%s（%s）</a> · %s</li>'
                % (f['conference_id'], e(f['conf_name']), e(f['acronym']), e(f['location'])))
    tree.append('<li style="padding-left:22px">└─ 📆 %s · 主题「%s」 · %s</li>'
                % (e(f['day']), e(f['track']), e(f['room'])))
    tree.append('<li style="padding-left:44px">└─ 🎤 %s（%s–%s）— %s</li>'
                % (e(f['session_title']), e(f['start_time']), e(f['end_time']), _speaker_links(f['speaker_list'])))
    for i, s in enumerate(siblings):
        last = '└─' if i == len(siblings) - 1 else '├─'
        if s['id'] == f['id']:
            tree.append('<li style="padding-left:66px">%s <span class="cur">%s %s ← 当前文件</span> '
                        '<span class="mut">%s · %s</span></li>'
                        % (last, badge(s['file_type']), e(s['title']), e(s['filename']), fmt_size(s['size_kb'])))
        else:
            tree.append('<li style="padding-left:66px">%s %s <a href="/file/%d">%s</a> '
                        '<span class="mut">%s · %s</span></li>'
                        % (last, badge(s['file_type']), s['id'], e(s['title']),
                           e(s['filename']), fmt_size(s['size_kb'])))
    tree.append('</ul></div>')

    def conf_list(rows):
        if not rows:
            return '<p class="mut">暂无</p>'
        return '<ul style="list-style:none">' + ''.join(
            '<li style="padding:3px 0">🎪 <a href="/conference/%d">%s（%s）</a> <span class="mut">%s</span></li>'
            % (c['id'], e(c['name']), e(c['acronym']), e(c['location'])) for c in rows) + '</ul>'

    related = ('<div class="card"><h2>相关会议</h2>'
               '<h2 style="font-size:15px">同主题「%s」的会议</h2>%s'
               '<h2 style="font-size:15px">同讲者出现的其他会议</h2>%s</div>'
               % (e(f['track']), conf_list(by_track), conf_list(by_speaker)))
    return crumb + meta + ''.join(tree) + related

def speaker_page(sp, sessions, files_map):
    rows = ''
    for s in sessions:
        flist = '、'.join('<a href="/file/%d">%s</a>' % (f['id'], e(f['title'])) for f in files_map.get(s['id'], [])) or '—'
        rows += ('<tr><td>%s %s</td><td><a href="/conference/%d">%s</a></td><td>%s</td><td>%s</td><td>%s</td></tr>'
                 % (e(s['day']), e(s['start_time']), s['conf_id'], e(s['conf_name']),
                    e(s['title']), e(s['track']), flist))
    return ('<div class="crumb"><a href="/">首页</a> / 讲者</div>'
            '<div class="card"><h1>👤 %s <span class="mut">%s</span></h1><p>%s</p></div>'
            '<div class="card"><h2>出席议程与资料</h2>'
            '<table><tr><th>时间</th><th>会议</th><th>议程</th><th>主题</th><th>公开资料</th></tr>%s</table></div>'
            % (e(sp['name']), e(sp['affiliation']), e(sp['bio']), rows))

def blocked_page(f):
    return ('<div class="card"><h1>⚠️ 该条目已被屏蔽</h1>'
            '<p>「%s」因不合规已被管理员屏蔽，不再对外展示。</p>'
            '<p class="mut">屏蔽原因：%s</p><p><a href="/">返回首页</a></p></div>'
            % (e(f['title']), e(f['block_reason'] or '未说明')))

def not_found(msg='页面不存在'):
    return '<div class="card"><h1>404</h1><p>%s</p><p><a href="/">返回首页</a></p></div>' % e(msg)

# ---------------- 后台页面 ----------------

def login_page(error=''):
    err = '<div class="alert alert-err">%s</div>' % e(error) if error else ''
    return ('<div class="card" style="max-width:420px;margin:40px auto"><h1>管理后台登录</h1>%s'
            '<form method="post" action="/admin/login">'
            '<p><input type="password" name="password" placeholder="管理密码" style="width:100%%;padding:10px;border:1px solid var(--line);border-radius:6px"></p>'
            '<p style="margin-top:12px"><button class="btn" style="width:100%%">登录</button></p></form>'
            '<p class="mut">演示密码：admin123</p></div>' % err)

def admin_page(stats, hot_all, hot_week, recent, files, kw, status, msg=''):
    stat_html = ''.join('<div class="stat"><b>%d</b>%s</div>' % (v, k) for v, k in [
        (stats['conferences'], '场会议'), (stats['sessions'], '个议程'), (stats['files'], '份资料'),
        (stats['blocked'], '已屏蔽'), (stats['searches'], '搜索次数')])
    ok = '<div class="alert alert-ok">%s</div>' % e(msg) if msg else ''

    def hot_table(rows):
        body = ''.join('<tr><td><span class="hotnum%s">%d</span>%s</td><td>%d</td><td class="mut">%s</td></tr>'
                       % (' top' if i < 3 else '', i + 1, e(h['term']), h['cnt'], e(h['last_at']))
                       for i, h in enumerate(rows))
        return '<table><tr><th>热词</th><th>次数</th><th>最近搜索</th></tr>%s</table>' % (body or '<tr><td colspan="3" class="mut">暂无数据</td></tr>')

    recent_rows = ''.join('<tr><td>%s</td><td>%d</td><td class="mut">%s</td></tr>'
                          % (e(r['query']), r['results'], e(r['created_at'])) for r in recent)

    file_rows = ''
    for f in files:
        if f['status'] == 'blocked':
            action = ('<form method="post" action="/admin/unblock" class="inline">'
                      '<input type="hidden" name="id" value="%d"><button class="btn btn-sm btn-grey">解除屏蔽</button></form>'
                      '<div class="mut">原因：%s</div>' % (f['id'], e(f['block_reason'])))
            tag = '<span class="tag-b">已屏蔽</span>'
        else:
            action = ('<form method="post" action="/admin/block" class="inline">'
                      '<input type="hidden" name="id" value="%d">'
                      '<input name="reason" placeholder="屏蔽原因" required>'
                      '<button class="btn btn-sm btn-danger">屏蔽</button></form>' % f['id'])
            tag = '<span class="tag-a">正常</span>'
        file_rows += ('<tr><td>%d</td><td>%s<br><span class="mut">%s</span></td><td>%s</td>'
                      '<td class="mut">%s / %s</td><td>%s</td><td>%s</td></tr>'
                      % (f['id'], e(f['title']), e(f['filename']), badge(f['file_type']),
                         e(f['conf_name']), e(f['session_title'] or '—'), tag, action))

    status_opts = ''.join('<option value="%s"%s>%s</option>' % (v, ' selected' if v == status else '', t)
                          for v, t in [('', '全部状态'), ('active', '正常'), ('blocked', '已屏蔽')])

    return """
%s
<div class="stats">%s</div>
<div class="grid2">
  <div class="card"><h2>🔥 搜索热词 TOP20（全部时间）</h2>%s</div>
  <div class="card"><h2>📈 近 7 天热词</h2>%s</div>
</div>
<div class="card"><h2>最近搜索记录</h2>
<table><tr><th>关键词</th><th>结果数</th><th>时间</th></tr>%s</table></div>
<div class="card"><h2>条目管理（屏蔽不合规资料）</h2>
<form class="filters" method="get" action="/admin">
  <div><label>关键词</label><input name="kw" value="%s" placeholder="标题 / 文件名"></div>
  <div><label>状态</label><select name="status">%s</select></div>
  <button class="btn">筛选</button>
</form>
<table><tr><th>ID</th><th>资料</th><th>类型</th><th>所属会议 / 议程</th><th>状态</th><th>操作</th></tr>%s</table>
</div>
<div class="card"><h2>数据导入</h2>
<p class="mut">从 <code>data/import.json</code> 重新导入公开会议元数据（幂等，不会覆盖屏蔽状态）。</p>
<form method="post" action="/admin/import"><button class="btn">立即导入</button>
<a class="btn btn-grey" href="/admin/logout" style="margin-left:10px">退出登录</a></form>
</div>""" % (ok, stat_html, hot_table(hot_all), hot_table(hot_week), recent_rows,
             e(kw), status_opts, file_rows)
