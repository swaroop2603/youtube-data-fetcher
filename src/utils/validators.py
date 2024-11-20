import re

def is_valid_youtube_url(url: str) -> bool:
    """
    Validate if the given URL is a valid YouTube channel URL.

    Args:
        url (str): URL to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    pattern = r"^https?://(www\.)?youtube\.com/(@[a-zA-Z0-9_-]+|channel/[a-zA-Z0-9_-]+)$"
    return bool(re.match(pattern, url))
