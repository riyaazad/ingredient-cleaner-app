import time

REQUESTS = {}
LIMIT = 10
WINDOW = 60

def allow(ip: str) -> bool:
    now = time.time()
    window_start = now - WINDOW

    REQUESTS.setdefault(ip, [])
    REQUESTS[ip] = [t for t in REQUESTS[ip] if t > window_start]

    if len(REQUESTS[ip]) >= LIMIT:
        return False

    REQUESTS[ip].append(now)
    return True
