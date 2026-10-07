import os


def _load_key():
    key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if key:
        return key
    key_file = os.path.join(os.path.dirname(__file__), "key.txt")
    if os.path.exists(key_file):
        with open(key_file, "r", encoding="utf-8") as f:
            key = f.read().strip()
    return key


DEEPSEEK_API_KEY = _load_key()
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
