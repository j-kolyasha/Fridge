from datetime import date, timedelta

def today() -> date:
    return date.today()

def today_str() -> str:
    d = date.today()
    return str(d)

def valid_date(d: str) -> bool:
    try:
        date.fromisoformat(d)
        return True
    except Exception:
        return False

def expired(expires_at: date) -> bool:
    if today() >= expires_at:
        return True
    
    return False

def expiring(day: int, expires_at: date) -> bool:
    if today() + timedelta(days=day) >= expires_at:
        return True
    
    return False

def date_from_str(d: str) -> date:
    try:
        return date.fromisoformat(d)
    except Exception:
        return today()

def str_from_date(d: date) -> str:
    try:
        return str(d)
    except Exception:
        return today_str()