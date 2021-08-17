
from obj import Obj
from collections import namedtuple
from Funciones.characters import *
from Funciones.math import *

V2 = namedtuple("Point2D",['x','y'])
V3 = namedtuple("Point3D",['x','y','z'])

#setting the function to get color with bytes
def color(r,g,b):
        return bytes([b,g,r])

BLACK = color(0,0,0)
WHITE = color(255,255,255)

def barycentric(A,B,C,P):
        cx,cy,cz = cross(V3(B.x-A.x,C.x-A.x,A.x-P.x),V3(B.y-A.y,C.y-A.y,A.y-P.y))
        if cz ==0:
            return -1,-1,-1

        u = cx/cz
        v = cy/cz
        w = 1-(cx+cy)/cz

        return w,v,u

def bbox(A,B,C):
    xs = [A.x, B.x, C.x,]
    xs.sort()
    ys = [A.y, B.y, C.y,]
    ys.sort()
    return xs[0],xs[-1],ys[0],ys[-1]

class Renderer(object):
    def __init__(self):
        self.default_color = color(0,0,139)
        self.cl_color = BLACK


    def point(self, x, y):
        self.framebuffer[y][x] =self.default_color

    def glInit(self):
        pass

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = []

    def glViewPort(self, x, y, width, height):
        self.vp_x = x
        self.vp_y = y
        self.vp_width = width
        self.vp_height = height

    #Fill the bitmap
    def glClear(self):
        self.framebuffer = [
            [self.cl_color for x in range(self.width)] for y in range(self.height)
            ]
        self.zbuffer = [
            [-float('inf') for x in range(self.width)] for y in range(self.height)
            ]

    def frame(self):
        return self.framebuffer


    def glClearColor(self, r,g,b):
        if(r<=1 and g<=1 and b<=1):
            self.cl_color = color(int(r*255),int(g*255),int(b*255))
        else:
            self.cl_color = color(r,g,b)

        self.glClear()

    def glVertex(self,x,y):
        #formula get from microsoft glViewport function
        x_pos = int((x+1)*(self.vp_width/2)+self.vp_x)
        y_pos = int((y+1)*(self.vp_height/2)+self.vp_y)
        self.point(x_pos,y_pos)

    #change color of vertex
    def glColor(self, r,g,b):
        if(r<=1 and g<=1 and b<=1):
            self.default_color = color(int(r*255),int(g*255),int(b*255))
        else:
            self.default_color = color(r,g,b)

    #Using class implementation
    #REESCRIBIR
    def glLine(self,x0,y0,x1,y1):

        x0 = int((x0+1)*(self.vp_width/2)+self.vp_x)
        y0 = int((y0+1)*(self.vp_height/2)+self.vp_y)
        x1 = int((x1+1)*(self.vp_width/2)+self.vp_x)
        y1 = int((y1+1)*(self.vp_height/2)+self.vp_y)


        self.line(x0,y0,x1,y1)

    def line(self,A,B):
        x0 = A.x
        y0 = A.y
        x1 = B.x
        y1 = B.y

        dy = abs(y1-y0)
        dx = abs(x1-x0)

        steep = dy>dx
        #en caso de pendiente mayor a 1
        if steep:
            x0,y0 = y0,x0
            x1,y1 = y1,x1

            dy = abs(y1-y0)
            dx = abs(x1-x0)

        #en caso que el segundo valor sea menor que el primero
        if x1<x0:
            x0,x1 =x1,x0
            y0,y1 = y1,y0

            dy = abs(y1-y0)
            dx = abs(x1-x0)

        offset = 0 *2*dx
        threshold = 0.5 *2*dx
        y = y0

        points = []
        for x in range(x0,x1+1):
            if steep:
                points.append((y,x))

            else:
                points.append((x,y))

            offset += dy*2
            if offset >= threshold:

                y +=1 if y0<y1 else -1
                threshold +=1 *2* dx

            for pointf in points:
                self.point(*pointf)

    def transform(self, v, translate, scale):
        return V3(
            round(((v[0]+translate[0])*scale[0])),
            round(((v[1]+translate[1])*scale[1])),
            round(((v[2]+translate[2])*scale[2]))
        )

    def load(self, filename, movement, scale):
        model = Obj(filename)
        light = norm(V3(0,0,1))
        for face in (model.faces):
            vcount  = len(face)

            if vcount == 3:
                f1 = face[0][0]-1
                f2 = face[1][0]-1
                f3 = face[2][0]-1

                A = self.transform(model.vertices[f1],movement,scale)
                B = self.transform(model.vertices[f2], movement, scale)
                C = self.transform(model.vertices[f3], movement, scale)

                normal = norm(cross(sub(B,A),sub(C,A)))
                intensity = dot(normal, light)
                grey = round(255*intensity)
                if intensity < 0: grey =0
                self.glColor(grey/255,(grey/255),(grey/255))
                self.triangle(A,B,C)
            elif vcount == 4:
                f1 = face[0][0]-1
                f2 = face[1][0]-1
                f3 = face[2][0]-1
                f4 = face[3][0]-1

                A = self.transform(model.vertices[f1],movement,scale)
                B = self.transform(model.vertices[f2], movement, scale)
                C = self.transform(model.vertices[f3], movement, scale)
                D = self.transform(model.vertices[f4], movement, scale)

                normal = norm(cross(sub(A,B),sub(B,C)))
                intensity = dot(normal, light)
                grey = round(255*intensity)
                if intensity < 0: grey = 0

                self.glColor(grey/255,(grey/255),(grey/255))

                self.triangle(A,B,C)
                self.triangle(A,C,D)

    def fill(self):
        bandera = False
        arreglo = []
        x0,y0 = 0,0
        x1,y1 = 0,0

        for i in range(len(self.frame())): #filas

            for j in range(len(self.frame())): #cada valor fila
                #color diferente al bitmap
                if((self.cl_color[2],self.cl_color[1],self.cl_color[0]) != (self.frame()[i][j][2],self.frame()[i][j][1],self.frame()[i][j][0]) ):
                    a=self.frame()[i][j][2],self.frame()[i][j][1],self.frame()[i][j][0]

                    arreglo.append([1,a]) #evaluar cada valor con su color si son diferentes
                else:
                     a=self.frame()[i][j][2],self.frame()[i][j][1],self.frame()[i][j][0]
                     arreglo.append([0,a])
            #por cada linea
            for pos in range(len(arreglo)):
                if arreglo[pos][0] == 1:
                    if(bandera):
                            if(arreglo[pos][1]!=a):
                                a = arreglo[pos][1]
                                x0,y0 = pos,i

                            else:
                                    x1,y1 = pos,i
                                    self.glColor(a[0]/255,a[1]/255,a[2]/255)
                                    self.line(x0,y0,x1,y1)
                    else:
                        a = arreglo[pos][1]
                        x0,y0 = pos,i
                else:
                    if(x0!=0):
                        bandera = True
                    else:
                            bandera = False
            arreglo = []
            bandera = False
            x0,y0 = 0,0
            x1,y1 = 0,0

    def triangle_wireframe(self,A,B,C):
        self.line(A,B)
        self.line(B,C)
        self.line(C,A)


    def triangle(self,A,B,C):
        xmin,xmax,ymin,ymax = bbox(A,B,C)

        for x in range(xmin,xmax+1):
            for y in range(ymin,ymax+1):
                P = V2(x,y)
                w,v,u = barycentric(A,B,C,P)
                if w<0 or v<0 or u<0:
                    continue
                z = A.z * w+B.z*v+C.z*u
                try:
                    if z> self.zbuffer[y][x]:

                        self.point(x,y)
                        self.zbuffer[y][x] =z
                except:
                    pass

    def glFinish(self, filename):
        #bw means binary write
        f = open(filename, 'bw')
        #file header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14+40+ 3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(14+40))

        #info header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        #bitmap
        for y in range(self.height):
            for x in range(self.width):
                f.write(self.framebuffer[y][x])

        f.close()

    def glFinish_ZBUFFER(self, filename):
        #bw means binary write
        f = open(filename, 'bw')
        #file header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14+40+ 3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(14+40))

        #info header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        z_min = float('inf')
        z_max = -float('inf')

        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] > z_max:
                        z_max = self.zbuffer[x][y]

                    if self.zbuffer[x][y] < z_min:
                        z_min = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                z_value = self.zbuffer[x][y]

                if z_value == -float('inf'):
                    z_value = z_min

                z_value = round(((z_value - z_min) / (z_max - z_min)) * 255)

                z_color = color(z_value, z_value, z_value)
                f.write(z_color)

        f.close()