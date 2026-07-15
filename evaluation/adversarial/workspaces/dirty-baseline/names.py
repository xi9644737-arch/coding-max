def normalize_name(value: str) -> str:
    return " ".join(value.strip().replace("-", "").split())
