from numbers import Number
import math

class Quaternion:
    
    def __init__(self,*args):
        try:
            self.w = args[0].w
            self.x = args[0].x
            self.y = args[0].y
            self.z = args[0].z
        except AttributeError:
            self.w = args[0]
            try:
                self.x = args[1].x
                self.y = args[1].y
                self.z = args[1].z
            except AttributeError:
                self.x = args[1]
                self.y = args[2]
                self.z = args[3]

    def __add__(self,q):
        if isinstance(q,Number):
            return Quaternion(self.w + q, self.x, self.y, self.z)
        w = self.w + q.w
        x = self.x + q.x
        y = self.y + q.y
        z = self.z + q.z
        return Quaternion(w,x,y,z)
    
    def __radd__(self,q):
        if isinstance(q,Number):
            return Quaternion(self.w + q, self.x, self.y, self.z)
    
    def __sub__(self,q):
        if isinstance(q,Number):
            return Quaternion(self.w - q, self.x, self.y, self.z)
        w = self.w - q.w
        x = self.x - q.x
        y = self.y - q.y
        z = self.z - q.z
        return Quaternion(w,x,y,z)

    def __rsub__(self,q):
        if isinstance(q,Number):
            return Quaternion(q - self.w, -self.x, -self.y, -self.z)
        

    def __mul__(self,q):
        if isinstance(q,Number):
            return Quaternion(self.w*q, self.x*q, self.y*q, self.z*q)
        w = self.w * q.w - self.x * q.x - self.y * q.y - self.z * q.z
        x = self.w * q.x + self.x * q.w + self.y * q.z - self.z * q.y
        y = self.w * q.y - self.x * q.z + self.y * q.w + self.z * q.x
        z = self.w * q.z + self.x * q.y - self.y * q.x + self.z * q.w
        return Quaternion(w,x,y,z)

    def __rmul__(self,q):
        if isinstance(q,Number):
            return Quaternion(self.w*q, self.x*q, self.y*q, self.z*q)
            
    def __div__(self,q):
        if isinstance(q,Number):
            return Quaternion(self.w/q, self.x/q, self.y/q, self.z/q)
        l = q.w*q.w + q.x*q.x + q.y*q.y + q.z*q.z
        if l == 0:
            raise ZeroDivisionError
        w =  self.w * q.w + self.x * q.x + self.y * q.y + self.z * q.z
        x = -self.w * q.x + self.x * q.w - self.y * q.z + self.z * q.y
        y = -self.w * q.y + self.x * q.z + self.y * q.w - self.z * q.x
        z = -self.w * q.z - self.x * q.y + self.y * q.x + self.z * q.w
        return Quaternion(w/l,x/l,y/l,z/l)
    
    def __rdiv__(self,q):
        l = self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z
        w =  self.w*q/l
        x = -self.x*q/l
        y = -self.y*q/l
        z = -self.z*q/l
        return Quaternion(w,x,y,z)
        
    def __neg__(self):
        return Quaternion(-self.w,-self.x,-self.y,-self.z)
    
    def __pos__(self):
        return self
    
    def __abs__(self):
        return math.sqrt(self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z)
    
    def __eq__(self,q):
        if isinstance(q,Number):
            if q == self.w and self.x == 0 and self.y == 0 and self.z == 0:
                return True
            else:
                return False
        elif isinstance(q,Quaternion):
            if self.w == q.w and self.x == q.x and self.y == q.y and self.z == q.z:
                return True
            else:
                return False
        else:
            return False
    
    def __str__(self):
        str = ""
        if self.w != 0:
            str = '{:.3f}'.format(self.w)
        im = ( (self.x, "i"), (self.y, "j"), (self.z, "k") )
        for v in im:
            if v[0] != 0:
                if str != "":
                    if v[0] > 0:
                        str += ' - '
                        if v[0] == 1:
                            str += v[1]
                        else:
                            str += '{:.3f}'.format(v[0])
                            str += v[1]
                    else:
                        str += ' + '
                        if v[0] == -1:
                            str += v[1]
                        else:
                            str += '{:.3f}'.format(-v[0])
                            str += v[1]
                else:
                    if v[0] == 1:
                        str = v[1]
                    elif v[0] == -1:
                        str = '-' + v[1]
                    else:
                        str = '{:.3f}'.format(v[0])
                        str += v[1]
        if str == "":
            str = "0"
        return str
    
    def dot(self,q):
        return self.w*q.w + self.x*q.x + self.y*q.y + self.z*q.z
    
    def lenSqr(self):
        return self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z
    
    def dist(q,qq):
        return (q - qq).__abs__()
    
    def slen(q):
        q = q.normalise()
        q.w = q.x - 1
        return 2*math.asin(q.__abs__()/2)
        
    def sdist(q,qq):
        q = q.normalise()
        qq = qq.normalise()
        return 2*math.asin(q.dist(qq)/2)
    
    def normalise(self):
        l = self.__abs__()
        if l == 0:
            return Quaternion(1,0,0,0)
        else:
            return Quaternion(self.w/l, self.x/l, self.y/l, self.z/l)

    def normalize(self):
        l = self.__abs__()
        if l == 0:
            return Quaternion(1,0,0,0)
        else:
            return Quaternion(self.w/l, self.x/l, self.y/l, self.z/l)
    
    def toAngleAxis(self):
        q = self.normalise()
        a = q.w
        ax = PVector(q.x,q.y,q.z)
        if ax == PVector(0,0,0):
            return 1, PVector(0,0,1)
        else:
            return 2*math.acos(a), ax.normalize()
        
    def slerp(self,q,t = None):
        if t == None:
            self,q,t = Quaternion(1,0,0,0),self,q
        if (self + q).__abs__() == 0:
            q,t = Quaternion(self.x, - self.w, self.z, -self.y), 2*t
        elif (self - q).__abs__() == 0:
            return self
        ca = self.dot(q)
        sa = math.sqrt(1 - ca**2)
        if sa == 0:
            return self
        a = math.acos(ca)
        sa = math.sin(a*t)/sa
        return (math.cos(a*t) - ca*sa)*self + sa*q
    
    def make_slerp(q,qq = None):
        if qq == None:
            q, qq = Quaternion(1,0,0,0), q
        q = q.normalize()
        qq = qq.normalize()
        if (q + qq).__abs__() == 0:
            qq,f = Quaternion(q.x, -q.w, q.z, -q.y), 2
        elif (q - qq).__abs__() == 0:
            def fn(t):
                return q
            return fn
        else:
            f = 1
        ca = q.dot(qq)
        sa = math.sqrt(1 - ca**2)
        if sa == 0:
            def fn(t):
                return q
            return fn
        a = math.acos(ca)
        qq = (qq - ca*q)/sa
        def fn(t):
            return math.cos(a*f*t)*q + math.sin(a*f*t)*qq
        return fn
        

    
tolerance = 0.0000001
def rotateTo(u,v):
    u = u.copy().normalize()
    v = v.copy().normalize()
    if u.copy().cross(v).mag() < tolerance:
        if u.dot(v) >= -tolerance:
            return Quaternion(1,0,0,0)
        a,b,c = abs(u.x), abs(u.y), abs(u.z)
        if a < b and b < c:
            v = PVector(0,-u.z,u.y)
        elif b < c:
            v = PVector(u.z,0,-u.x)
        else:
            v = PVector(-u.y,u.x,0)
    else:
        v = u + v
    v = v.normalize()
    d = u.dot(v)
    u.cross(v)
    return Quaternion(d,u)

PVector.rotateTo = rotateTo

def expandArgs(f):
    def b(*args):
        i = 0
        a = []
        while i < len(args):
            try:
                a.append(args[i].w)
                a.append(args[i].x)
                a.append(args[i].y)
                a.append(args[i].z)
            except AttributeError:
                try:
                    a.append(args[i].x)
                    a.append(args[i].y)
                    a.append(args[i].z)
                except AttributeError:
                    try:
                        a.append(args[i].x)
                        a.append(args[i].y)
                    except AttributeError:
                        a.append(args[i])
            i += 1
        return f(*a)
    return b

def qRotation(a, ax, ay, az):
    ca = math.cos(a)
    sa = math.sin(a)
    return ca + Quaternion(0,ax,ay,az).normalise()*sa

qRotation = expandArgs(qRotation)

def rotateByQuat(f):
    def b(*args):
        if len(args) == 1:
            a,ax = args[0].toAngleAxis()
            f(a,ax.x,ax.y,ax.z)
        else:
            f(*args)
    return b

rotate = rotateByQuat(rotate)
