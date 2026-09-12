# -*- coding: utf-8 -*-
"""查询层：所有 SQL 集中在这里。"""
from db import get_db

def _like(s):
    return '%' + s.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_') + '%'

def _parse_speakers(packed):
    """'1:张伟|3:李娜' -> [{'id':1,'name':'张伟'}, ...]"""
    out = []
    for part in (packed or '').split('|'):
        if ':' in part:
            sid, name = part.split(':', 1)
            out.append({'id': int(sid), 'name': name})
    return out

SPEAKER_PACK = "GROUP_CONCAT(sp.id || ':' || sp.name, '|')"

def stats():
    conn = get_db()
    one = lambda sql: conn.execute(sql).fetchone()['c']
    r = {
        'conferences': one("SELECT COUNT(*) c FROM conferences WHERE status='active'"),
        'sessions':    one("SELECT COUNT(*) c FROM sessions WHERE status='active'"),
        'files':       one("SELECT COUNT(*) c FROM files WHERE status='active'"),
        'speakers':    one("SELECT COUNT(*) c FROM speakers"),
        'blocked':     one("SELECT COUNT(*) c FROM files WHERE status='blocked'"),
        'searches':    one("SELECT COUNT(*) c FROM search_logs"),
    }
    conn.close()
    return r

def tracks():
    conn = get_db()
    rows = conn.execute("""SELECT track, COUNT(*) c FROM sessions
                           WHERE status='active' AND track<>'' GROUP BY track ORDER BY c DESC""").fetchall()
    conn.close()
    return rows

def speakers():
    conn = get_db()
    rows = conn.execute('SELECT id, name, affiliation FROM speakers ORDER BY name').fetchall()
    conn.close()
    return rows

def conferences():
    conn = get_db()
    rows = conn.execute("""
        SELECT c.*, (SELECT COUNT(*) FROM sessions s WHERE s.conference_id=c.id AND s.status='active') AS n_sessions,
               (SELECT COUNT(*) FROM files f WHERE f.conference_id=c.id AND f.status='active') AS n_files
        FROM conferences c WHERE c.status='active' ORDER BY c.start_date DESC""").fetchall()
    conn.close()
    return rows

def hot_terms(limit=10, days=None):
    sql = """SELECT lower(query) AS term, COUNT(*) AS cnt, MAX(created_at) AS last_at
             FROM search_logs {where} GROUP BY term ORDER BY cnt DESC, last_at DESC LIMIT ?"""
    where = "WHERE created_at >= datetime('now', '-%d days', 'localtime')" % days if days else ''
    conn = get_db()
    rows = conn.execute(sql.format(where=where), (limit,)).fetchall()
    conn.close()
    return rows

def recent_searches(limit=15):
    conn = get_db()
    rows = conn.execute('SELECT * FROM search_logs ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
    conn.close()
    return rows

def log_search(q, results):
    conn = get_db()
    conn.execute('INSERT INTO search_logs(query, results) VALUES (?,?)', (q, results))
    conn.commit()
    conn.close()

def search_files(q='', track='', speaker='', ftype=''):
    conn = get_db()
    like = _like(q)
    rows = conn.execute("""
        SELECT f.*, s.title AS session_title, s.track, s.day,
               c.name AS conf_name, c.id AS conf_id, c.acronym,
               GROUP_CONCAT(DISTINCT sp.name) AS speakers
        FROM files f
        JOIN sessions s   ON f.session_id = s.id
        JOIN conferences c ON f.conference_id = c.id
        LEFT JOIN session_speakers ss ON ss.session_id = s.id
        LEFT JOIN speakers sp        ON sp.id = ss.speaker_id
        WHERE f.status='active' AND s.status='active' AND c.status='active'
          AND (?='' OR f.title LIKE ? ESCAPE '\\' OR f.filename LIKE ? ESCAPE '\\'
                    OR s.title LIKE ? ESCAPE '\\' OR s.abstract LIKE ? ESCAPE '\\')
          AND (?='' OR s.track = ?)
          AND (?='' OR f.file_type = ?)
          AND (?='' OR sp.name LIKE ? ESCAPE '\\')
        GROUP BY f.id
        ORDER BY c.start_date DESC, s.day DESC, s.start_time DESC
        LIMIT 200""",
        (q, like, like, like, like,
         track, track, ftype, ftype, speaker, _like(speaker))).fetchall()
    conn.close()
    return rows

def get_conference(cid):
    conn = get_db()
    row = conn.execute("SELECT * FROM conferences WHERE id=? AND status='active'", (cid,)).fetchone()
    conn.close()
    return row

def conference_sessions(cid):
    conn = get_db()
    rows = conn.execute("""
        SELECT s.*, %s AS speakers
        FROM sessions s
        LEFT JOIN session_speakers ss ON ss.session_id = s.id
        LEFT JOIN speakers sp        ON sp.id = ss.speaker_id
        WHERE s.conference_id=? AND s.status='active'
        GROUP BY s.id ORDER BY s.day, s.track, s.start_time""" % SPEAKER_PACK, (cid,)).fetchall()
    conn.close()
    out = []
    for r in rows:
        d = dict(r)
        d['speaker_list'] = _parse_speakers(d.pop('speakers'))
        out.append(d)
    return out

def session_files(sid, include_blocked=False):
    conn = get_db()
    where = '' if include_blocked else "AND status='active'"
    rows = conn.execute('SELECT * FROM files WHERE session_id=? %s ORDER BY id' % where, (sid,)).fetchall()
    conn.close()
    return rows

def conference_type_counts(cid):
    conn = get_db()
    rows = conn.execute("""SELECT file_type, COUNT(*) c FROM files
                           WHERE conference_id=? AND status='active' GROUP BY file_type""", (cid,)).fetchall()
    conn.close()
    return rows

def get_file(fid):
    conn = get_db()
    row = conn.execute("""
        SELECT f.*, s.title AS session_title, s.day, s.track, s.room, s.start_time, s.end_time,
               s.abstract AS session_abstract, c.name AS conf_name, c.acronym, c.location,
               c.start_date, c.end_date, %s AS speakers
        FROM files f
        JOIN sessions s    ON f.session_id = s.id
        JOIN conferences c ON f.conference_id = c.id
        LEFT JOIN session_speakers ss ON ss.session_id = s.id
        LEFT JOIN speakers sp        ON sp.id = ss.speaker_id
        WHERE f.id=? GROUP BY f.id""" % SPEAKER_PACK, (fid,)).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d['speaker_list'] = _parse_speakers(d.pop('speakers'))
    return d

def related_conferences(file_row):
    """相关会议：同主题的其他会议 + 同讲者的其他会议。"""
    conn = get_db()
    by_track = conn.execute("""
        SELECT DISTINCT c.id, c.name, c.acronym, c.year, c.location
        FROM conferences c JOIN sessions s ON s.conference_id = c.id
        WHERE s.track=? AND c.id<>? AND c.status='active' LIMIT 6""",
        (file_row['track'], file_row['conference_id'])).fetchall()
    by_speaker = []
    if file_row['speaker_list']:
        ids = ','.join(str(sp['id']) for sp in file_row['speaker_list'])
        by_speaker = conn.execute("""
            SELECT DISTINCT c.id, c.name, c.acronym, c.year, c.location
            FROM conferences c
            JOIN sessions s ON s.conference_id = c.id
            JOIN session_speakers ss ON ss.session_id = s.id
            WHERE ss.speaker_id IN (%s) AND c.id<>? AND c.status='active' LIMIT 6""" % ids,
            (file_row['conference_id'],)).fetchall()
    conn.close()
    return by_track, by_speaker

def get_speaker(spid):
    conn = get_db()
    sp = conn.execute('SELECT * FROM speakers WHERE id=?', (spid,)).fetchone()
    if not sp:
        conn.close()
        return None, []
    sessions = conn.execute("""
        SELECT s.*, c.name AS conf_name, c.id AS conf_id, c.acronym
        FROM sessions s
        JOIN session_speakers ss ON ss.session_id = s.id
        JOIN conferences c ON c.id = s.conference_id
        WHERE ss.speaker_id=? AND s.status='active' AND c.status='active'
        ORDER BY s.day DESC, s.start_time DESC""", (spid,)).fetchall()
    conn.close()
    return sp, sessions

def admin_files(kw='', status=''):
    conn = get_db()
    like = _like(kw)
    rows = conn.execute("""
        SELECT f.*, c.name AS conf_name, s.title AS session_title
        FROM files f
        JOIN conferences c ON c.id = f.conference_id
        LEFT JOIN sessions s ON s.id = f.session_id
        WHERE (?='' OR f.title LIKE ? ESCAPE '\\' OR f.filename LIKE ? ESCAPE '\\')
          AND (?='' OR f.status=?)
        ORDER BY f.status='blocked' DESC, f.id DESC LIMIT 300""",
        (kw, like, like, status, status)).fetchall()
    conn.close()
    return rows

def block_file(fid, reason):
    conn = get_db()
    conn.execute("UPDATE files SET status='blocked', block_reason=? WHERE id=?", (reason, fid))
    conn.commit()
    conn.close()

def unblock_file(fid):
    conn = get_db()
    conn.execute("UPDATE files SET status='active', block_reason='' WHERE id=?", (fid,))
    conn.commit()
    conn.close()
