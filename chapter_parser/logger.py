# logger.py

def log_source_used(series_name, number, source_type, status="✓"):
    print(f"[{source_type}] {status} Used for {series_name} {number}")
