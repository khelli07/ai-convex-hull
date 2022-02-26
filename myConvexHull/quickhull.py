import numpy as np
from myConvexHull.utils import *


class KonvexHull:
    def __init__(self, points):
        self.points = np.array(points)
        self.indices = np.argsort(self.points[:, 0])

        self.simplices = []

    def split_indices(self, indices, imin, imax):
        """
        Inputs: list of indices and index of extreme points
        Output: indices of above and below points
        """
        pmin, pmax = self.points[imin], self.points[imax]
        above = []
        below = []

        slope, coeff = get_line_equation(pmin, pmax)

        # If line is vertical, nothing is above or below
        if np.isnan(slope):
            return above, below

        for i in indices:
            x, y = self.points[i]
            y_line = slope * x + coeff
            if y > y_line:
                above.append(i)
            elif y < y_line:
                below.append(i)

        return above, below

    def remove(self, idx):
        """
        Remove index 'idx' from self.indices
        """
        self.indices = np.array([i for i in self.indices if i != idx])

    def take_farthest(self, indices, p1, p2):
        """
        Returns the farthest points to the line from p1 and p2.
        """
        idx = indices[0]
        max_distance = -1

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

    def quick_hull(self, splitted, imin, imax, is_above):
        """
        Helper method to fit method.
        This method is necessary because of the different treatment
        to group of above and below points.
        """
        length = len(splitted)
        # Base cases
        if length == 0:
            self.simplices.append([imin, imax])

        # Recurrence
        else:
            farthest_idx = self.take_farthest(
                splitted, self.points[imin], self.points[imax]
            )
            splitted.remove(farthest_idx)
            self.remove(farthest_idx)

            above_1, below_1 = self.split_indices(splitted, imin, farthest_idx)
            above_2, below_2 = self.split_indices(splitted, farthest_idx, imax)

            if is_above:
                self.quick_hull(above_1, imin, farthest_idx, True)
                self.quick_hull(above_2, farthest_idx, imax, True)
            else:
                self.quick_hull(below_1, imin, farthest_idx, False)
                self.quick_hull(below_2, farthest_idx, imax, False)

    def fit(self):
        """
        Search for points in the convex hull.
        The output are restored in self.simplices.
        """
        imin, imax = self.indices[0], self.indices[-1]
        self.remove(imin)
        self.remove(imax)

        above, below = self.split_indices(self.indices, imin, imax)
        self.quick_hull(above, imin, imax, True)
        self.quick_hull(below, imin, imax, False)
