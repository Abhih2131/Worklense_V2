import locale

try:
    locale.setlocale(locale.LC_ALL, 'en_IN')
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

def indian_format(value):
    """Format value as Indian number system (lakhs/crores)."""
    try:
        return locale.format_string('%d', int(value), grouping=True)
    except Exception:
        return value

def format_financial_year(fy_code):
    """Convert 'FY-26' to 'Financial Year 2026'."""
    if fy_code and fy_code.startswith("FY-"):
        return f"Financial Year 20{fy_code[-2:]}"
    return fy_code
