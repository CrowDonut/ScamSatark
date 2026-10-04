"""
database.py - SQLite Anonymous Scam Radar Engine
Stores privacy-compliant fraud telemetry without harvesting PII.
"""
import sqlite3
from datetime import datetime

DB_FILE = "scam_radar.db"

def init_db():
    """Initializes the SQLite database and seeds realistic baseline metrics if empty."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        platform TEXT,
        risk_score INTEGER,
        risk_level TEXT,
        primary_red_flag TEXT,
        language TEXT
    )
    """)
    
    # Check if empty, then auto-seed realistic baseline data
    cursor.execute("SELECT COUNT(*) FROM scan_logs")
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_logs = [
            (datetime.now().strftime("%Y-%m-%d %H:%M"), "Telegram VIP Tip", 92, "HIGH", "Guaranteed 200% return promise", "Hindi"),
            (datetime.now().strftime("%Y-%m-%d %H:%M"), "WhatsApp Group", 85, "HIGH", "Demanding deposit to personal UPI handle", "Hindi"),
            (datetime.now().strftime("%Y-%m-%d %H:%M"), "Instagram Reel", 68, "MODERATE", "Unregistered derivative options advisory", "English"),
            (datetime.now().strftime("%Y-%m-%d %H:%M"), "Telegram Channel", 95, "HIGH", "Fabricated SEBI registration number", "Tamil"),
            (datetime.now().strftime("%Y-%m-%d %H:%M"), "Registered Broker Notice", 15, "LOW", "Standard statutory risk disclosure", "English")
        ]
        cursor.executemany("""
        INSERT INTO scan_logs (timestamp, platform, risk_score, risk_level, primary_red_flag, language)
        VALUES (?, ?, ?, ?, ?, ?)
        """, sample_logs)
        
    conn.commit()
    conn.close()

def log_scan(platform: str, risk_score: int, risk_level: str, primary_flag: str, language: str):
    """Logs an anonymous scan record to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO scan_logs (timestamp, platform, risk_score, risk_level, primary_red_flag, language)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M"), platform, risk_score, risk_level, primary_flag, language))
    conn.commit()
    conn.close()

def get_radar_analytics() -> dict:
    """Aggregates telemetry data for the Community Scam Radar dashboard."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM scan_logs")
    total_scans = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM scan_logs WHERE risk_level = 'HIGH'")
    high_risk_scans = cursor.fetchone()[0]
    
    cursor.execute("SELECT platform, COUNT(*) FROM scan_logs GROUP BY platform ORDER BY COUNT(*) DESC LIMIT 3")
    top_platforms = cursor.fetchall()
    
    cursor.execute("SELECT primary_red_flag, COUNT(*) FROM scan_logs GROUP BY primary_red_flag ORDER BY COUNT(*) DESC LIMIT 3")
    top_flags = cursor.fetchall()
    
    cursor.execute("SELECT timestamp, platform, risk_score, risk_level, primary_red_flag FROM scan_logs ORDER BY id DESC LIMIT 5")
    recent_scans = cursor.fetchall()
    
    conn.close()
    
    return {
        "total_scans": total_scans,
        "high_risk_scans": high_risk_scans,
        "top_platforms": top_platforms,
        "top_flags": top_flags,
        "recent_scans": recent_scans
    }
