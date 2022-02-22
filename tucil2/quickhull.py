import numpy as np
from tucil2.utils import *


class KonvexHull:
    def __init__(self, points):
        self.points = np.array(points)
        self.indices = np.argsort(self.points[:, 0])

        self.simplices = []

    def split_indices(self, indices, imin, imax):
        """
        Inputs: all indices and index of extreme points
        Output: indices of left and right points
        """
        pmin, pmax = self.points[imin], self.points[imax]
        left = []
        right = []

        for i in indices:
            if is_on_left(pmin, pmax, self.points[i]):
                left.append(i)
            else:
                right.append(i)

        return left, right

    def remove(self, idx):
        """
        Remove index 'idx' from self.indices
        """
        self.indices = np.array([i for i in self.indices if i != idx])

    def take_farthest(self, indices, p1, p2):
        """
        Returns the farthest points to the line from p1 and p2.
        """
        idx = 0
        max_distance = 0

        for i in indices:
            dist = point_to_line(p1, p2, self.points[i])
            if max_distance < dist:
                idx = i
                max_distance = dist
            elif max_distance == dist and compute_cosine(
                p1, p2, self.points[i]
            ) < compute_cosine(p1, p2, self.points[idx]):
                idx = i

        return idx

    def sub_convex_hull(self, splitted, imin, imax, left):
        """
        Subfunction to my_convex_hull.
        This function is necessary
        because we need to treat left and right points differently.
        """
        length = len(splitted)
        # Base cases
        if length == 0:
            self.simplices.append([imin, imax])
        elif length == 1:
            self.simplices.append([imin, splitted[0]])
            self.simplices.append([splitted[0], imax])
            self.remove(splitted[0])

        # Recurrence
        else:
            farthest_idx = self.take_farthest(
                splitted, self.points[imin], self.points[imax]
            )
            splitted.remove(farthest_idx)
            self.remove(farthest_idx)

            left_1, right_1 = self.split_indices(splitted, imin, farthest_idx)
            left_2, right_2 = self.split_indices(splitted, farthest_idx, imax)

            if left:
                self.sub_convex_hull(left_1, imin, farthest_idx, True)
                self.sub_convex_hull(left_2, farthest_idx, imax, True)
            else:
                self.sub_convex_hull(right_1, imin, farthest_idx, False)
                self.sub_convex_hull(right_2, farthest_idx, imax, False)

    def my_convex_hull(self):
        """
        Search for points in the convex hull.
        The output are restored in self.simplices.
        """
        imin, imax = self.indices[0], self.indices[-1]
        self.remove(imin)
        self.remove(imax)

        left, right = self.split_indices(self.indices, imin, imax)
        self.sub_convex_hull(left, imin, imax, True)
        self.sub_convex_hull(right, imin, imax, False)
