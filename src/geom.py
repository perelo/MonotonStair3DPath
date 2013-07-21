#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__authors__ = 'McGuffin, Eloi Perdereau'
__date__ = '17-06-2013'


import math

from util import signum

class Point2D(object):
    def __init__(self,x=0,y=0):
        self.coordinates = [x,y]
    def x(self):
        return self.coordinates[0]
    def y(self):
        return self.coordinates[1]
    def __repr__(self):
        return "Point2D("+str(self.x())+","+str(self.y())+")"
    def __str__(self):
        return "P2("+str(self.x())+","+str(self.y())+")"
    def get(self):
        return self.coordinates
    def returnCopy(self):
        return Point2D( self.x(), self.y() )
    def average(self,other):
        return Point2D( (self.x()+other.x())*0.5, (self.y()+other.y())*0.5 )
    def __add__(self,other):
        return Point2D( self.x()+other.x(), self.y()+other.y() )
    def __hash__(self):
        return hash(self.coordinates[0]) + hash(self.coordinates[1])
    def __eq__(self,other):
        return self.x()==other.x() and self.y()==other.y()
    def __ne__(self,other):
        return not (self==other)

class Point3D(object):
    def __init__(self,x=0,y=0,z=0):
        self.coordinates = [x,y,z]
    def x(self):
        return self.coordinates[0]
    def y(self):
        return self.coordinates[1]
    def z(self):
        return self.coordinates[2]
    def __repr__(self):
        return "Point3D("+str(self.x())+","+str(self.y())+","+str(self.z())+")"
    def __str__(self):
        return "P3("+str(self.x())+","+str(self.y())+","+str(self.z())+")"
    def get(self):
        return self.coordinates
    def returnCopy(self):
        return Point3D( self.x(), self.y(), self.z() )
    def asVector3D(self):
        return Vector3D( self.x(), self.y(), self.z() )
    def distance(self,other):
        return (other-self).length()
    def average(self,other):
        return Point3D( (self.x()+other.x())*0.5, (self.y()+other.y())*0.5, (self.z()+other.z())*0.5 )
    def __add__(self,other):
        return Point3D( self.x()+other.x(), self.y()+other.y(), self.z()+other.z() )
    def __sub__(self,other):
        if isinstance(other,Vector3D):
            return Point3D( self.x()-other.x(), self.y()-other.y(), self.z()-other.z() )
        return Vector3D( self.x()-other.x(), self.y()-other.y(), self.z()-other.z() )
    def __hash__(self):
        return hash(self.coordinates[0]) + hash(self.coordinates[1]) + hash(self.coordinates[2])
    def __eq__(self,other):
        return self.x()==other.x() and self.y()==other.y() and self.z()==other.z()
    def __ne__(self,other):
        return not (self==other)

class Segment(object):
    def __init__(self,a=Point3D(),b=Point3D()):
        self.a = a
        self.b = b
    def __hash__(self):
        return hash(self.a) + hash(self.b)
    def __repr__(self):
        return "Segment("+str(self.a)+","+str(self.b)+")"
    def __str__(self):
        return "S("+str(self.a)+","+str(self.b)+")"
    def __eq__(self,other):
        return (self.a==other.a and self.b==other.b) or (self.b==other.a and self.a==other.b)
    def __ne__(self,other):
        return not (self==other)
    def intersect(self,other):
        return orientation(self.a , self.b , other.a) != orientation(self.a , self.b , other.b) \
                            if self.a != self.b else True and \
               orientation(other.a, other.b, self.a)  != orientation(other.a, other.b, self.b) \
                            if other.a != other.b else True

class Edge3D(Segment):
    # edge types
    UNKNOWN = 0
    CONVEX  = 1
    CONCAVE = 2
    def __init__(self,a=Point3D(),b=Point3D(),type=UNKNOWN):
        super(Edge3D, self).__init__(a,b)
        self.type = type

class Vector3D(object):
    def __init__(self,x=0,y=0,z=0):
        self.coordinates = [x,y,z]
    def x(self):
        return self.coordinates[0]
    def y(self):
        return self.coordinates[1]
    def z(self):
        return self.coordinates[2]
    def __repr__(self):
        return "Vector3D("+str(self.x())+","+str(self.y())+","+str(self.z())+")"
    def __str__(self):
        return "V("+str(self.x())+","+str(self.y())+","+str(self.z())+")"
    def get(self):
        return self.coordinates
    def returnCopy(self):
        return Vector3D( self.x(), self.y(), self.z() )
    def asPoint3D(self):
        return Point3D( self.x(), self.y(), self.z() )
    def lengthSquared(self):
        return self.x()*self.x()+self.y()*self.y()+self.z()*self.z()
    def length(self):
        return math.sqrt( self.lengthSquared() )
    def normalized(self):
        l = self.length()
        if ( l > 0 ):
            return Vector3D( self.x()/l, self.y()/l, self.z()/l )
        return self.returnCopy()
    def __neg__(self):
        return Vector3D( -self.x(), -self.y(), -self.z() )
    def __add__(self,other):
        if isinstance(other,Point3D):
            return Point3D( self.x()+other.x(), self.y()+other.y(), self.z()+other.z() )
        return Vector3D( self.x()+other.x(), self.y()+other.y(), self.z()+other.z() )
    def __sub__(self,other):
        return Vector3D( self.x()-other.x(), self.y()-other.y(), self.z()-other.z() )
    def __mul__(self,other):
        if isinstance(other,Vector3D):
           # dot product
           return self.x()*other.x() + self.y()*other.y() + self.z()*other.z()
        # scalar product
        return Vector3D( self.x()*other, self.y()*other, self.z()*other )
    def __rmul__(self,other):
        return self*other
    def __div__(self,other):
        return Vector3D( self.x()/other, self.y()/other, self.z()/other )
    def __xor__(self,other):   # cross product
        return Vector3D(
            self.y()*other.z() - self.z()*other.y(),
            self.z()*other.x() - self.x()*other.z(),
            self.x()*other.y() - self.y()*other.x() )
    def __eq__(self,other):
        return self.x()==other.x() and self.y()==other.y() and self.z()==other.z()
    def __ne__(self,other):
        return not (self==other)

class Matrix4x4(object):
    def __init__(self):
        self.setToIdentity()
    def __str__(self):
        return str(self.m[0:4]) + "\n" + str(self.m[4:8]) + "\n" + str(self.m[8:12]) + "\n" + str(self.m[12:16])
    def get(self):
        return self.m
    def returnCopy(self):
        M = Matrix4x4()
        M.m = list(self.m)  # copy the list
        return M
    def setToIdentity(self):
        self.m = [ 1.0, 0.0, 0.0, 0.0,
                   0.0, 1.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 0.0,
                   0.0, 0.0, 0.0, 1.0 ]

    @staticmethod
    def rotationAroundOrigin(angleInRadians, axisVector):
        # assumes axisVector is normalized
        c = math.cos( angleInRadians )
        s = math.sin( angleInRadians )
        one_minus_c = 1-c
        M = Matrix4x4()
        M.m[ 0] = c + one_minus_c * axisVector.x()*axisVector.x()
        M.m[ 5] = c + one_minus_c * axisVector.y()*axisVector.y()
        M.m[10] = c + one_minus_c * axisVector.z()*axisVector.z()
        M.m[ 1] = M.m[ 4] = one_minus_c * axisVector.x()*axisVector.y();
        M.m[ 2] = M.m[ 8] = one_minus_c * axisVector.x()*axisVector.z();
        M.m[ 6] = M.m[ 9] = one_minus_c * axisVector.y()*axisVector.z();
        xs = axisVector.x() * s
        ys = axisVector.y() * s
        zs = axisVector.z() * s
        M.m[ 1] += zs;  M.m[ 4] -= zs;
        M.m[ 2] -= ys;  M.m[ 8] += ys;
        M.m[ 6] += xs;  M.m[ 9] -= xs;

        M.m[12] = 0.0;
        M.m[13] = 0.0;
        M.m[14] = 0.0;
        M.m[ 3] = 0.0;   M.m[ 7] = 0.0;   M.m[11] = 0.0;   M.m[15] = 1.0;
        return M


    def __mul__(a, b):   # a is really self
        if isinstance(b,Matrix4x4):
            M = Matrix4x4()
            M.m[ 0] = a.m[ 0]*b.m[ 0] + a.m[ 4]*b.m[ 1] + a.m[ 8]*b.m[ 2] + a.m[12]*b.m[ 3];
            M.m[ 1] = a.m[ 1]*b.m[ 0] + a.m[ 5]*b.m[ 1] + a.m[ 9]*b.m[ 2] + a.m[13]*b.m[ 3];
            M.m[ 2] = a.m[ 2]*b.m[ 0] + a.m[ 6]*b.m[ 1] + a.m[10]*b.m[ 2] + a.m[14]*b.m[ 3];
            M.m[ 3] = a.m[ 3]*b.m[ 0] + a.m[ 7]*b.m[ 1] + a.m[11]*b.m[ 2] + a.m[15]*b.m[ 3];

            M.m[ 4] = a.m[ 0]*b.m[ 4] + a.m[ 4]*b.m[ 5] + a.m[ 8]*b.m[ 6] + a.m[12]*b.m[ 7];
            M.m[ 5] = a.m[ 1]*b.m[ 4] + a.m[ 5]*b.m[ 5] + a.m[ 9]*b.m[ 6] + a.m[13]*b.m[ 7];
            M.m[ 6] = a.m[ 2]*b.m[ 4] + a.m[ 6]*b.m[ 5] + a.m[10]*b.m[ 6] + a.m[14]*b.m[ 7];
            M.m[ 7] = a.m[ 3]*b.m[ 4] + a.m[ 7]*b.m[ 5] + a.m[11]*b.m[ 6] + a.m[15]*b.m[ 7];

            M.m[ 8] = a.m[ 0]*b.m[ 8] + a.m[ 4]*b.m[ 9] + a.m[ 8]*b.m[10] + a.m[12]*b.m[11];
            M.m[ 9] = a.m[ 1]*b.m[ 8] + a.m[ 5]*b.m[ 9] + a.m[ 9]*b.m[10] + a.m[13]*b.m[11];
            M.m[10] = a.m[ 2]*b.m[ 8] + a.m[ 6]*b.m[ 9] + a.m[10]*b.m[10] + a.m[14]*b.m[11];
            M.m[11] = a.m[ 3]*b.m[ 8] + a.m[ 7]*b.m[ 9] + a.m[11]*b.m[10] + a.m[15]*b.m[11];

            M.m[12] = a.m[ 0]*b.m[12] + a.m[ 4]*b.m[13] + a.m[ 8]*b.m[14] + a.m[12]*b.m[15];
            M.m[13] = a.m[ 1]*b.m[12] + a.m[ 5]*b.m[13] + a.m[ 9]*b.m[14] + a.m[13]*b.m[15];
            M.m[14] = a.m[ 2]*b.m[12] + a.m[ 6]*b.m[13] + a.m[10]*b.m[14] + a.m[14]*b.m[15];
            M.m[15] = a.m[ 3]*b.m[12] + a.m[ 7]*b.m[13] + a.m[11]*b.m[14] + a.m[15]*b.m[15];

            return M
        elif isinstance(b,Vector3D):
            # We treat the vector as if its (homogeneous) 4th component were zero.
            return Vector3D(
                a.m[ 0]*b.x() + a.m[ 4]*b.y() + a.m[ 8]*b.z(), # + a.m[12]*b.w(),
                a.m[ 1]*b.x() + a.m[ 5]*b.y() + a.m[ 9]*b.z(), # + a.m[13]*b.w(),
                a.m[ 2]*b.x() + a.m[ 6]*b.y() + a.m[10]*b.z()  # + a.m[14]*b.w(),
                # a.m[ 3]*b.x() + a.m[ 7]*b.y() + a.m[11]*b.z() + a.m[15]*b.w()
                )
        elif isinstance(b,Point3D):
            # We treat the point as if its (homogeneous) 4th component were one.
            return Point3D(
                a.m[ 0]*b.x() + a.m[ 4]*b.y() + a.m[ 8]*b.z() + a.m[12],
                a.m[ 1]*b.x() + a.m[ 5]*b.y() + a.m[ 9]*b.z() + a.m[13],
                a.m[ 2]*b.x() + a.m[ 6]*b.y() + a.m[10]*b.z() + a.m[14]
                )

def orientation(p, q, r):
    """
        Compute the orientation of three given points
        return < 0 if it's a left turn,
               > 0 if it's a right turn,
               = 0 if points are aligned
    """
    return signum((p.x() - r.x()) * (q.y() - r.y()) - (p.y() - r.y()) * (q.x() - r.x()));
