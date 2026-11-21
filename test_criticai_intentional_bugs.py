"""
Test file for CriticAI review.
Intentionally contains bugs across multiple categories.
DO NOT MERGE - this is for demonstrating code review tool.
"""

import os
import hashlib
import sqlite3


# Intentional bug 1: hardcoded signing secret
JWT_SECRET = "super-secret-signing-key-do-not-share-xyz789"


def verify_token_insecure(token: str, user_input_algorithm: str) -> dict:
    """Decode a token using algorithm from user input.
    
    Intentional bug 2: algorithm confusion vulnerability.
    Accepting algorithm from user input allows attackers to pass 'none'
    or switch HS256 to RS256 to bypass signature verification.
    """
    import jwt
    # Dangerous: algorithm supplied by caller, not pinned
    return jwt.decode(token, JWT_SECRET, algorithms=[user_input_algorithm])


def store_token_sql_injection(user_id: str, token: str):
    """Store an issued token in local DB.
    
    Intentional bug 3: SQL injection via f-string.
    """
    conn = sqlite3.connect("tokens.db")
    query = f"INSERT INTO tokens (user_id, token) VALUES ('{user_id}', '{token}')"
    conn.execute(query)
    # Intentional bug 4: connection never closed


def hash_password_weak(password: str) -> str:
    """Hash a password for storage.
    
    Intentional bug 5: MD5 is cryptographically broken.
    """
    return hashlib.md5(password.encode()).hexdigest()


def process_tokens_batch(tokens: list) -> list:
    """Process a list of tokens.
    
    Intentional bug 6: bare except swallows all errors including KeyboardInterrupt.
    """
    results = []
    for token in tokens:
        try:
            result = verify_token_insecure(token, "HS256")
            results.append(result)
        except:
            results.append(None)
    return results