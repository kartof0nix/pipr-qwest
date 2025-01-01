char_dim = (1, 2)
EPS = 0.000001
from math import sin, cos, pi, sqrt

class point:
    x=0, y=0

def dist(a : point, b : point):
    return sqrt ( (a.x - b.x)**2 + (a.y - b.y)**2)

def f_eq(a:float, b:float):
    return abs(a-b) < EPS

def dist(path_a, path_b, c):
    if(dist(path_a, path_b) < EPS):
        return dist(path_a, c)
    project_x = 
    if(not f_eq(path_a.x, path_b.x)):

        ln_a = (path_a.y - path_b.y) / (path_a.x - path_b.x)
        ln_b = path_a.y - path_a.x * ln_a 
        project_x = ( ( c.y + (1/ln_a) * c.x - ln_b ) / ( ln_a - (-1/ln_a) ) )
        project_y = ln_a * project_x + ln_b


class pole:
    def __init__(self, Paths = [False for i in range(6)]) -> None:
        paths = Paths
    
    
    def gen_hexagon(self, x, y):
        points = []
        mid = pnt(x/2, y/2)
        side = x/2
        for i in range(6):
            ang = pi/6 + i*(pi/3)
            points += [(side * cos(ang), side * sin(ang))]



"""
   ____
  /    \
 /      \
/        \____
\        /    \
 \      /      \
  \____/        \
  /    \        /
 /      \      /
/        \____/
\        /
 \      /
  \____/  
       \
        \
         \____/
"""
    