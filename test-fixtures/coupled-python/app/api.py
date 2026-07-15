from .state import FEATURE_FLAGS


def enable_feature(payload: dict[str, str]) -> str:
    normalized = payload["name"].strip()
    FEATURE_FLAGS[normalized] = True
    return normalized
