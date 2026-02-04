# validation/rules_config.py

from typing import Dict, Set

# Tolerances for rounding differences
MONEY_TOLERANCE = 0.02  # 2 cents typical tolerance

# Allowed VAT rates by jurisdiction (extend as needed)
ALLOWED_VAT_RATES: Dict[str, Set[float]] = {
    "MD": {0.0, 8.0, 12.0, 20.0},
    "RO": {0.0, 5.0, 9.0, 19.0},
    "EU": {0.0, 5.0, 7.0, 9.0, 10.0, 19.0, 20.0, 21.0}
}

# Tax ID regex per jurisdiction (simplified; extend per real rules)
TAX_ID_REGEX: Dict[str, str] = {
    "MD_IDNO": r"^\d{13}$",
    "MD_VAT": r"^MD\d{8}$",
    "RO_CUI": r"^RO?\d{2,10}$"
}

# Default jurisdiction if not provided upstream
DEFAULT_JURISDICTION = "MD"
