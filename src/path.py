#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Eloi Perdereau'
__date__ = '29-07-2013'


from math import sqrt

from geom import *


def compute_extension_point(s, e, l):
    """
        Compute the point on l (LineAxis3D) that is the extension of the path
        in which the last segment is s and s.b is on e (Edge3D)
    """
    # coord_of_i are the coord represented by l.get[x] depending on l's orientation
    coord_of_0 = ( 1, 0, 0 )  # y, x, x
    coord_of_1 = ( Point3D.z, Point3D.z, Point3D.y )
    a = s.asLine3D().point_at(l.get()[0], coord_of_0[l.orientation])
    if not a or coord_of_1[l.orientation](a) < l.get()[1]:
        return      # we would bend concavely or up to infinty...

    vect_coords = ( Vector3D.x, Vector3D.y, Vector3D.z )

    # 't' means the axis to get depending on e and l orientation
    u_t   = dict(zip(COORDINATES, vect_coords))[e.orientation()]
    l_t_i = dict(zip(COORDINATES, ( 0, 0, 1 )))[e.orientation()]

    u = Vector3D.vector_from_two_points(s.a, s.b).normalized()
    r_t = l.coord_points[2](s.a) + sqrt( (l.get()[l_t_i] / u_t(u))**2
                                        - (l.get()[0] - l.coord_points[0](s.a))**2
                                        - (l.get()[1] - l.coord_points[1](s.a))**2 )

    return l.create_point(l.get()[0], l.get()[1], r_t)

