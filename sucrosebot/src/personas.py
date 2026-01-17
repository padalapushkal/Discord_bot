from collections import OrderedDict
from utils.normalize_key import normalize_key

PERSONA_CACHE: OrderedDict[str, dict] = OrderedDict()


def get_persona(name: str):
    key = normalize_key(name)
    return PERSONA_CACHE.get(key)


def set_persona(name: str, context: str, prompt: str):
    key = normalize_key(name)
    PERSONA_CACHE[key] = {
        "name": name.strip(),
        "context": context.strip(),
        "prompt": prompt,
    }


def reset_persona(name: str):
    key = normalize_key(name)
    PERSONA_CACHE.pop(key, None)


def list_personas():
    return list(PERSONA_CACHE.keys())


def delete_last_n(n: int):
    for _ in range(min(n, len(PERSONA_CACHE))):
        PERSONA_CACHE.popitem(last=True)
