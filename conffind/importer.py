# -*- coding: utf-8 -*-
"""把公开会议元数据 JSON 导入 SQLite（幂等：重复导入不产生重复数据，且保留后台屏蔽状态）。"""
import hashlib
import json
import os
import sys
from datetime import datetime, timedelta

from db import get_db, init_db

VALID_TYPES = {'ppt', 'abstract', 'attachment', 'video', 'paper'}

def _checksum(*parts):
    return hashlib.sha1('|'.join(str(p) for p in parts).encode('utf-8')).hexdigest()[:16]

def _speaker_id(cur, sp):
    name = (sp.get('name') or '').strip()
    aff = (sp.get('affiliation') or '').strip()
    if not name:
        return None
    row = cur.execute('SELECT id FROM speakers WHERE name=? AND affiliation=?', (name, aff)).fetchone()
    if row:
        return row['id']
    cur.execute('INSERT INTO speakers(name, affiliation, bio) VALUES (?,?,?)',
                (name, aff, sp.get('bio', '')))
    return cur.lastrowid

def import_payload(payload):
    init_db()
    conn = get_db()
    cur = conn.cursor()
    stats = {'conferences': 0, 'sessions': 0, 'files': 0, 'search_logs': 0}

    for c in payload.get('conferences', []):
        row = cur.execute('SELECT id FROM conferences WHERE name=? AND year=?',
                          (c['name'], c.get('year'))).fetchone()
        if row:
            cid = row['id']
            cur.execute("""UPDATE conferences SET acronym=?, location=?, start_date=?,
                           end_date=?, description=?, source_url=? WHERE id=?""",
                        (c.get('acronym', ''), c.get('location', ''), c.get('start_date', ''),
                         c.get('end_date', ''), c.get('description', ''), c.get('source_url', ''), cid))
        else:
            cur.execute("""INSERT INTO conferences(name, acronym, year, location, start_date,
                           end_date, description, source_url) VALUES (?,?,?,?,?,?,?,?)""",
                        (c['name'], c.get('acronym', ''), c.get('year'), c.get('location', ''),
                         c.get('start_date', ''), c.get('end_date', ''), c.get('description', ''),
                         c.get('source_url', '')))
            cid = cur.lastrowid
            stats['conferences'] += 1

        for s in c.get('sessions', []):
            row = cur.execute('SELECT id FROM sessions WHERE conference_id=? AND title=?',
                              (cid, s['title'])).fetchone()
            if row:
                sid = row['id']
                cur.execute("""UPDATE sessions SET day=?, track=?, room=?, start_time=?,
                               end_time=?, abstract=? WHERE id=?""",
                            (s.get('day', ''), s.get('track', ''), s.get('room', ''),
                             s.get('start_time', ''), s.get('end_time', ''), s.get('abstract', ''), sid))
            else:
                cur.execute("""INSERT INTO sessions(conference_id, day, track, title, room,
                               start_time, end_time, abstract) VALUES (?,?,?,?,?,?,?,?)""",
                            (cid, s.get('day', ''), s.get('track', ''), s['title'], s.get('room', ''),
                             s.get('start_time', ''), s.get('end_time', ''), s.get('abstract', '')))
                sid = cur.lastrowid
                stats['sessions'] += 1

            for spk in s.get('speakers', []):
                spid = _speaker_id(cur, spk)
                if spid:
                    cur.execute('INSERT OR IGNORE INTO session_speakers(session_id, speaker_id) VALUES (?,?)',
                                (sid, spid))

            for f in s.get('files', []):
                ftype = f.get('file_type', 'attachment')
                if ftype not in VALID_TYPES:
                    ftype = 'attachment'
                checksum = f.get('checksum') or _checksum(c['name'], s['title'], f.get('filename', ''))
                row = cur.execute('SELECT id FROM files WHERE session_id=? AND filename=?',
                                  (sid, f.get('filename', ''))).fetchone()
                if row:
                    # 仅更新元数据，保留后台设置的屏蔽状态与原因
                    cur.execute("""UPDATE files SET title=?, file_type=?, format=?, size_kb=?, pages=?,
                                   language=?, uploaded_at=?, source_url=?, checksum=? WHERE id=?""",
                                (f.get('title') or f.get('filename', ''), ftype, f.get('format', ''),
                                 f.get('size_kb', 0), f.get('pages', 0), f.get('language', '中文'),
                                 f.get('uploaded_at', ''), f.get('source_url', ''), checksum, row['id']))
                else:
                    cur.execute("""INSERT INTO files(session_id, conference_id, title, file_type, filename,
                                   format, size_kb, pages, language, uploaded_at, source_url, checksum,
                                   status, block_reason) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                                (sid, cid, f.get('title') or f.get('filename', ''), ftype,
                                 f.get('filename', ''), f.get('format', ''), f.get('size_kb', 0),
                                 f.get('pages', 0), f.get('language', '中文'), f.get('uploaded_at', ''),
                                 f.get('source_url', ''), checksum,
                                 f.get('status', 'active'), f.get('block_reason', '')))
                    stats['files'] += 1

    # 示例搜索日志（仅首次导入时写入，用于演示热词统计）
    n_logs = cur.execute('SELECT COUNT(*) AS c FROM search_logs').fetchone()['c']
    if n_logs == 0:
        base = datetime.now()
        for idx, item in enumerate(payload.get('sample_queries', [])):
            q, n = item[0], int(item[1])
            for i in range(n):
                ts = base - timedelta(days=(idx * 3 + i) % 10, hours=i % 24, minutes=(i * 7) % 60)
                cur.execute('INSERT INTO search_logs(query, results, created_at) VALUES (?,?,?)',
                            (q, (idx + i) % 40, ts.strftime('%Y-%m-%d %H:%M:%S')))
                stats['search_logs'] += 1

    conn.commit()
    conn.close()
    return stats

def import_file(path):
    with open(path, encoding='utf-8') as fh:
        return import_payload(json.load(fh))

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'data', 'import.json')
    print('导入完成：', import_file(path))
