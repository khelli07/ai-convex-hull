import numpy as np


def get_line_equation(p1, p2):
    if p2[0] - p1[0] == 0:  # If slope is infinity
        return np.nan, None

    # Get slope
    slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
    # Search coeff from either of the point
    coeff = p1[1] - slope * p1[0]

    return slope, coeff


def norm_(p3, p):
    """
    Returns the norm of vector OA.
    Here, A = p1 and O = p3. Hence, building vector O -> A.
    """
    return ((p[0] - p3[0]) ** 2 + (p[1] - p3[1]) ** 2) ** 0.5


def compute_cosine(p1, p2, p3):
    """
    Let A = p1, B = p2, and O = p3.
    This function computes the value of cosine theta
    between vector OA and OB.
    """
    dot = (p1[0] - p3[0]) * (p2[0] - p3[0]) + (p1[1] - p3[1]) * (p2[1] - p3[1])
    norms = norm_(p3, p1) * norm_(p3, p2)

    if norms == 0:
        return 0.0

    return dot / norms


def point_to_line(p1, p2, p3):
    """
    Compute the perpendicular length from point p3
    to line build from p1 and p2.
    """
    a = p1[1] - p2[1]
    b = p2[0] - p1[0]
    c = p1[0] * p2[1] - p2[0] * p1[1]
    denominator = (a * a + b * b) ** (0.5)

    if denominator == 0:
        return 0

    return abs(a * p3[0] + b * p3[1] + c) / denominator
