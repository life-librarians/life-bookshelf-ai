import sqlite3

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def check_user_first_request(user_id):
    conn = get_db_connection()
    row = conn.execute("SELECT is_first FROM user_state WHERE user_id=?", (user_id,)).fetchone()
    conn.close()
    return row["is_first"] if row else True  # 없으면 첫 요청으로 간주

def update_user_request_status(user_id, is_first=False):
    conn = get_db_connection()
    conn.execute("INSERT OR REPLACE INTO user_state (user_id, is_first) VALUES (?, ?)", (user_id, is_first))
    conn.commit()
    conn.close()