'''
Universidad del Valle de Guatemala
Graficas por computadora - Bryann Alfaro
SR4 - Flat Shading
'''
from gl import Renderer
from gl import V2

r =  Renderer()
r.glInit()
r.glCreateWindow(1000,1000)
r.glClear()
r.glClearColor(0.219,0,0)
r.glColor(0.85,0.125,0.125)



r.glColor(0.95,0.12,0.135)

r.load('./modelos/Dog.obj',(25,1,0),(20,20,30))
r.glFinish("./salidas/output1.bmp")
r.glFinish_ZBUFFER("./salidas/outbut2.bmp")
