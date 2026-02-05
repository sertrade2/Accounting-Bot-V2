from typing import Optional


def approx_equal(
    a: Optional[float],
    b: Optional[float],
    tolerance: float = 0.02,
) -> bool:
    if a is None or b is None:
        return False
    return abs(a - b) <= tolerance
