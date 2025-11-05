def normalize_title(title: str) -> str:
    t = (title or "").strip()
    return t[:100] if t else "Untitled"
