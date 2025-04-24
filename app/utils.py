import hashlib
from urllib.parse import urlparse


def generate_short_hash(url: str) -> str:
    """
    Generate a consistent short code for the given URL.
    Uses SHA-256 and returns first 6 characters.
    """
    # Ensure the URL is a string
    url_str = str(url)
    # Hash and return the first 6 characters
    return hashlib.sha256(url_str.encode()).hexdigest()[:6]


def validate_url(url: str) -> bool:
    """
    Basic validation for a URL.
    Checks if the URL is well-formed (scheme and netloc).
    """
    url_str = str(url)
    parsed = urlparse(url_str)
    return bool(parsed.scheme in ("http", "https") and parsed.netloc)