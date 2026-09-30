"""Normalize untrusted form and request values before business logic."""
import re

def clean_display_name(value):
    value = re.sub(r"\s+", " ", (value or "").strip())
    return value[:80]

def normalize_email(value):
    return (value or "").strip().casefold()

def parse_page_number(value, default=1, maximum=500):
    try:
        return max(1, min(int(value), maximum))
    except (TypeError, ValueError):
        return default

def sanitize_search_term(value):
    value = re.sub(r"[<>\x00-\x1f]", "", (value or "")).strip()
    return value[:120]
