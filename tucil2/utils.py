def is_on_left(p1, p2, p3):
    """
    Returns true if p3 is located at the left or upper
    the line build from p1 to p2.
    """
    if (p1[0] == p2[0]) and (p1[1] > p2[1]):  # Fix order
        tmp = p1
        p1 = p2
        p2 = tmp

    det = (
        (p1[0] * p2[1])
        + (p3[0] * p1[1])
        + (p2[0] * p3[1])
        - (p3[0] * p2[1])
        - (p2[0] * p1[1])
        - (p1[0] * p3[1])
    )

    return det > 0


def norm(p3, p):
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
    norms = norm(p3, p1) * norm(p3, p2)

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

    return abs(a * p3[0] + b * p3[1] + c) / (a * a + b * b) ** (0.5)
