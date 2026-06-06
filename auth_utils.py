"""
Imperial Network — authentication utilities.

Single source of truth for password hashing, verification, and Flask
secret-key loading. Imported by:
  - app.py               (live web auth)
  - migrate_legacy_users.py
  - extract_from_community_db.py

Hash scheme: bcrypt (cost factor 12 by default).
Legacy scheme: unsalted SHA-256 hex (64 chars) — only used by verify_password()
to migrate existing rows out of the database. New code must never call
hashlib.sha256 for passwords.

Hash format on disk:
  bcrypt:    "$2b$12$...60chars..."        → starts with "$2"
  legacy:    "0123456789abcdef..."         → 64-char hex, no prefix
Detection rule: stored.startswith("$2") is bcrypt, otherwise legacy.
"""

import hashlib
import hmac
import os
import secrets
import sys
import warnings
from typing import Tuple

try:
    import bcrypt
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "FATAL: bcrypt is not installed. Run:  pkg install -y python-bcrypt\n"
    )
    raise

# ---------- Configuration ----------

DEFAULT_BCRYPT_ROUNDS = 12
ENV_BCRYPT_ROUNDS = "IMPERIAL_BCRYPT_ROUNDS"
ENV_SECRET_KEY = "IMPERIAL_SECRET_KEY"
ENV_FlASK_ENV = "FLASK_ENV"  # standard Flask env var


def _get_rounds() -> int:
    """Bcrypt cost factor, overridable via env var for ops tuning."""
    raw = os.environ.get(ENV_BCRYPT_ROUNDS, str(DEFAULT_BCRYPT_ROUNDS))
    try:
        rounds = int(raw)
    except ValueError:
        warnings.warn(
            f"Invalid {ENV_BCRYPT_ROUNDS}={raw!r}; using default "
            f"{DEFAULT_BCRYPT_ROUNDS}"
        )
        return DEFAULT_BCRYPT_ROUNDS
    if rounds < 4 or rounds > 16:
        warnings.warn(
            f"{ENV_BCRYPT_ROUNDS}={rounds} is out of safe range (4-16); "
            f"using default {DEFAULT_BCRYPT_ROUNDS}"
        )
        return DEFAULT_BCRYPT_ROUNDS
    return rounds


# ---------- Hashing ----------

def hash_password(plain: str) -> str:
    """
    Hash a plaintext password with bcrypt. Returns the full encoded hash
    string, e.g. "$2b$12$abcdef...". The salt is embedded in the output,
    so the stored value is self-contained.

    Always returns a NEW hash (uses a fresh random salt) — never reuse
    a stored hash as input.
    """
    if not isinstance(plain, str):
        raise TypeError("password must be a str")
    if not plain:
        raise ValueError("password must not be empty")
    # bcrypt only uses the first 72 bytes; reject obviously overlong input
    # so we don't silently truncate.
    if len(plain.encode("utf-8")) > 72:
        raise ValueError("password longer than 72 bytes (bcrypt limit)")
    rounds = _get_rounds()
    salt = bcrypt.gensalt(rounds=rounds)
    return bcrypt.hashpw(plain.encode("utf-8"), salt).decode("ascii")


def verify_password(stored: str, candidate: str) -> Tuple[bool, bool]:
    """
    Verify a candidate password against a stored hash.

    Returns (ok, needs_rehash):
      ok            — True if candidate matches stored
      needs_rehash  — True only when ok=True AND stored was a legacy
                      SHA-256 hash (so caller should re-hash with bcrypt
                      and persist the new value). Always False for bcrypt
                      rows.

    Supports both schemes:
      - bcrypt:    starts with "$2"
      - legacy:    64-char SHA-256 hex (what app.py used to write)

    Uses constant-time comparison to avoid timing leaks.
    """
    if not stored or not candidate:
        return (False, False)

    if stored.startswith("$2"):
        # Native bcrypt path
        try:
            ok = bcrypt.checkpw(candidate.encode("utf-8"), stored.encode("ascii"))
        except (ValueError, TypeError):
            # Malformed bcrypt hash in DB
            return (False, False)
        return (ok, False)

    # Legacy SHA-256 path. We expect 64 lowercase hex chars; anything else
    # is not a valid legacy row we can verify.
    if len(stored) != 64:
        return (False, False)
    try:
        legacy = hashlib.sha256(candidate.encode("utf-8")).hexdigest()
    except UnicodeEncodeError:
        return (False, False)
    ok = hmac.compare_digest(stored, legacy)
    return (ok, ok)


def rehash_if_needed(user, db_session=None) -> bool:
    """
    Convenience wrapper for the login flow. Call after a successful
    verify_password() if needs_rehash was True. Hashes the plaintext (the
    caller is expected to have it) and updates the user record.

    For maximum safety, callers should pass the plaintext via the
    `plaintext` keyword. We avoid storing plaintext anywhere by accepting
    it as a transient argument and letting it fall out of scope.

    Returns True if a rehash was performed, False otherwise.
    """
    # This helper is imported by app.py; app.py does the actual update so
    # it can keep its db session in one place. We keep this stub for API
    # symmetry and future use.
    return False


# ---------- Secret key ----------

def load_secret_key() -> str:
    """
    Resolve the Flask SECRET_KEY from the environment.

    Resolution order:
      1. IMPERIAL_SECRET_KEY env var → use as-is.
      2. FLASK_ENV == "production" AND env var missing → REFUSE to start.
         This is the only safe default for a system that signs session
         cookies: an attacker who can guess the key can forge any user.
      3. Dev/test mode AND env var missing → generate an ephemeral
         random key for this process and emit a loud warning. Sessions
         will not survive a restart, which is the correct behavior for
         a dev server but would be wrong in production.

    Returns the secret key as a str.
    """
    key = os.environ.get(ENV_SECRET_KEY)
    if key:
        if len(key) < 32:
            warnings.warn(
                f"{ENV_SECRET_KEY} is shorter than 32 chars; use a longer "
                f"value (e.g. `python -c 'import secrets; "
                f"print(secrets.token_hex(32))'`)."
            )
        return key

    flask_env = (os.environ.get(ENV_FlASK_ENV) or "development").lower()
    is_production = flask_env in ("production", "prod")

    if is_production:
        raise RuntimeError(
            f"FATAL: {ENV_SECRET_KEY} is not set. Refusing to start in "
            f"production. Generate one with: "
            f"python -c 'import secrets; print(secrets.token_hex(32))' "
            f"and export it before launching."
        )

    # Dev fallback: ephemeral key, loud warning.
    ephemeral = secrets.token_hex(32)
    warnings.warn(
        f"WARNING: {ENV_SECRET_KEY} is not set. Generating an ephemeral "
        f"key for this process only. All sessions will be invalidated on "
        f"restart. Set {ENV_SECRET_KEY} (or {ENV_FlASK_ENV}=production "
        f"with the env var set) before deploying.",
        RuntimeWarning,
        stacklevel=2,
    )
    return ephemeral
