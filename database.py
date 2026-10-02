import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "scam_radar.db"

HIGH_RISK_THRESHOLD = 70  # matches the HIGH RISK band (70-100%)
ALLOWED_PLATFORMS = {"Telegram", "WhatsApp", "Instagram", "Other"}


def _connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create scam_radar.db and the scan_records table if they don't exist."""
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scan_records (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp    TEXT    NOT NULL,
                platform     TEXT    NOT NULL,
                risk_score   INTEGER NOT NULL CHECK (risk_score BETWEEN 0 AND 100),
                primary_flag TEXT    NOT NULL
            )
            """
        )


def log_scan(platform, risk_score, primary_flag):
    """
    Insert one anonymous scan record. Never raises, so a DB problem
    can't crash the app. Returns True if saved, False otherwise.
    """
    try:
        platform = platform if platform in ALLOWED_PLATFORMS else "Other"
        risk_score = max(0, min(100, int(risk_score)))
        primary_flag = (str(primary_flag).strip() or "None")[:100]
        init_db()
        with _connect() as conn:
            conn.execute(
                "INSERT INTO scan_records (timestamp, platform, risk_score, primary_flag) "
                "VALUES (?, ?, ?, ?)",
                (datetime.now().isoformat(timespec="seconds"), platform, risk_score, primary_flag),
            )
        return True
    except (sqlite3.Error, ValueError, TypeError) as e:
        print(f"[database] log_scan failed: {e}")
        return False


def get_radar_stats():
    """
    Stats for the Community Scam Radar dashboard.
    Returns a dict (always safe to display, even on an empty DB).
    """
    stats = {
        "total_scans": 0,
        "total_scams_intercepted": 0,
        "top_platform": None,
        "top_platform_pct": 0,
        "top_trend_this_week": "No data yet",
    }
    try:
        init_db()
        with _connect() as conn:
            stats["total_scans"] = conn.execute(
                "SELECT COUNT(*) FROM scan_records"
            ).fetchone()[0]

            stats["total_scams_intercepted"] = conn.execute(
                "SELECT COUNT(*) FROM scan_records WHERE risk_score >= ?",
                (HIGH_RISK_THRESHOLD,),
            ).fetchone()[0]

            row = conn.execute(
                "SELECT platform, COUNT(*) c FROM scan_records WHERE risk_score >= ? "
                "GROUP BY platform ORDER BY c DESC LIMIT 1",
                (HIGH_RISK_THRESHOLD,),
            ).fetchone()
            if row and stats["total_scams_intercepted"]:
                stats["top_platform"] = row[0]
                stats["top_platform_pct"] = round(100 * row[1] / stats["total_scams_intercepted"])

            week_ago = (datetime.now() - timedelta(days=7)).isoformat(timespec="seconds")
            row = conn.execute(
                "SELECT primary_flag, COUNT(*) c FROM scan_records "
                "WHERE timestamp >= ? AND risk_score >= ? AND primary_flag != 'None' "
                "GROUP BY primary_flag ORDER BY c DESC LIMIT 1",
                (week_ago, HIGH_RISK_THRESHOLD),
            ).fetchone()
            if row:
                stats["top_trend_this_week"] = row[0]
    except sqlite3.Error as e:
        print(f"[database] get_radar_stats failed: {e}")
    return stats


if __name__ == "__main__":
    init_db()
    log_scan("Telegram", 92, "Fake SEBI Telegram Group")
    log_scan("WhatsApp", 85, "Guaranteed Returns")
    log_scan("Telegram", 30, "None")
    print(get_radar_stats())