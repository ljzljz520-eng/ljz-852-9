# -*- coding: utf-8 -*-
"""SQLite 连接与表结构。"""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'conffind.db')

SCHEMA = """
CREATE TABLE IF NOT EXISTS conferences (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    acronym     TEXT DEFAULT '',
    year        INTEGER,
    location    TEXT DEFAULT '',
    start_date  TEXT DEFAULT '',
    end_date    TEXT DEFAULT '',
    description TEXT DEFAULT '',
    source_url  TEXT DEFAULT '',
    status      TEXT NOT NULL DEFAULT 'active',
    UNIQUE(name, year)
);

CREATE TABLE IF NOT EXISTS speakers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    affiliation TEXT DEFAULT '',
    bio         TEXT DEFAULT '',
    UNIQUE(name, affiliation)
);

CREATE TABLE IF NOT EXISTS sessions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    conference_id INTEGER NOT NULL REFERENCES conferences(id) ON DELETE CASCADE,
    day           TEXT DEFAULT '',
    track         TEXT DEFAULT '',
    title         TEXT NOT NULL,
    room          TEXT DEFAULT '',
    start_time    TEXT DEFAULT '',
    end_time      TEXT DEFAULT '',
    abstract      TEXT DEFAULT '',
    status        TEXT NOT NULL DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS session_speakers (
    session_id INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    speaker_id INTEGER NOT NULL REFERENCES speakers(id) ON DELETE CASCADE,
    PRIMARY KEY (session_id, speaker_id)
);

CREATE TABLE IF NOT EXISTS files (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id    INTEGER REFERENCES sessions(id) ON DELETE SET NULL,
    conference_id INTEGER NOT NULL REFERENCES conferences(id) ON DELETE CASCADE,
    title         TEXT NOT NULL,
    file_type     TEXT NOT NULL DEFAULT 'attachment',  -- ppt/abstract/attachment/video/paper
    filename      TEXT DEFAULT '',
    format        TEXT DEFAULT '',
    size_kb       INTEGER DEFAULT 0,
    pages         INTEGER DEFAULT 0,
    language      TEXT DEFAULT '中文',
    uploaded_at   TEXT DEFAULT '',
    source_url    TEXT DEFAULT '',
    checksum      TEXT DEFAULT '',
    status        TEXT NOT NULL DEFAULT 'active',      -- active/blocked
    block_reason  TEXT DEFAULT '',
    UNIQUE(session_id, filename)
);

CREATE TABLE IF NOT EXISTS search_logs (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    query      TEXT NOT NULL,
    results    INTEGER DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE INDEX IF NOT EXISTS idx_files_session ON files(session_id);
CREATE INDEX IF NOT EXISTS idx_files_conf    ON files(conference_id);
CREATE INDEX IF NOT EXISTS idx_files_type    ON files(file_type);
CREATE INDEX IF NOT EXISTS idx_sessions_conf ON sessions(conference_id);
CREATE INDEX IF NOT EXISTS idx_sessions_track ON sessions(track);
CREATE INDEX IF NOT EXISTS idx_logs_query    ON search_logs(query);
"""

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
