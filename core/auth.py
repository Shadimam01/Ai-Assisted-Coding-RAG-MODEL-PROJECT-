"""Users, passwords and roles (admin / user) stored in a small SQLite file."""
import hashlib
import hmac
import os
import re
import sqlite3
from contextlib import contextmanager

from config import ADMIN_PASSWORD, ADMIN_USERNAME, DB_PATH

ITERATIONS = 200_000
ROLES = ("user", "admin")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{3,30}$")
MIN_PASSWORD_LENGTH = 6


@contextmanager
def _conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def _hash(password, salt=None):
    """Passwords are never stored as plain text: salted PBKDF2 hash only."""
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return salt.hex() + "$" + digest.hex()


def _check(password, stored):
    salt_hex, digest_hex = stored.split("$")
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), ITERATIONS)
    return hmac.compare_digest(digest.hex(), digest_hex)


def init_db():
    """Create the users table, and the first admin account if there are no users."""
    with _conn() as con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE NOT NULL COLLATE NOCASE,
                   password_hash TEXT NOT NULL,
                   role TEXT NOT NULL DEFAULT 'user',
                   created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"""
        )
        if con.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            con.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'admin')",
                (ADMIN_USERNAME, _hash(ADMIN_PASSWORD)),
            )


def create_user(username, password, role="user"):
    """Returns (ok, message)."""
    username = (username or "").strip()
    if not USERNAME_RE.match(username):
        return False, "Username must be 3-30 characters: letters, numbers, dot, dash or underscore."
    if len(password or "") < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
    if role not in ROLES:
        return False, "Invalid role."
    try:
        with _conn() as con:
            con.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, _hash(password), role),
            )
    except sqlite3.IntegrityError:
        return False, "This username is already taken."
    return True, f"User '{username}' created."


# A fake hash so a wrong username takes the same time as a wrong password
_DUMMY = _hash("dummy-password")


def verify_user(username, password):
    """Returns {'username', 'role'} if the login is correct, otherwise None."""
    with _conn() as con:
        row = con.execute(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            ((username or "").strip(),),
        ).fetchone()
    if row is None:
        _check(password or "", _DUMMY)
        return None
    if _check(password or "", row["password_hash"]):
        return {"username": row["username"], "role": row["role"]}
    return None


def list_users():
    with _conn() as con:
        rows = con.execute("SELECT username, role, created_at FROM users ORDER BY id").fetchall()
    return [dict(r) for r in rows]


def _admin_count(con):
    return con.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'").fetchone()[0]


def set_role(username, role):
    if role not in ROLES:
        return False, "Invalid role."
    with _conn() as con:
        row = con.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
        if row is None:
            return False, "User not found."
        if row["role"] == "admin" and role != "admin" and _admin_count(con) <= 1:
            return False, "You cannot remove the last admin."
        con.execute("UPDATE users SET role = ? WHERE username = ?", (role, username))
    return True, f"{username} is now '{role}'."


def reset_password(username, new_password):
    if len(new_password or "") < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
    with _conn() as con:
        cur = con.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?", (_hash(new_password), username)
        )
    return (cur.rowcount > 0), ("Password changed." if cur.rowcount else "User not found.")


def delete_user(username):
    with _conn() as con:
        row = con.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
        if row is None:
            return False, "User not found."
        if row["role"] == "admin" and _admin_count(con) <= 1:
            return False, "You cannot delete the last admin."
        con.execute("DELETE FROM users WHERE username = ?", (username,))
    return True, f"User '{username}' deleted."
