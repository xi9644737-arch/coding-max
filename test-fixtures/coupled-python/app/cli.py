from .state import FEATURE_FLAGS


def enable_feature(raw_name: str) -> str:
    normalized = raw_name.strip().lower()
    FEATURE_FLAGS[normalized] = True
    return normalized
