'''
Universidad del Valle de Guatemala
Graficas por computadora - Bryann Alfaro
Laboratorio 1
'''
from gl import Renderer
from gl import V2

r =  Renderer()
r.glInit()
r.glCreateWindow(900,700)
r.glViewPort(0,0,3,3)
r.glClear()
r.glClearColor(0.219,0,0)
r.glColor(0.85,0.125,0.125)



r.load('model.obj',(2.5,1,0),(200,200,300))
r.glFinish("output1.bmp")
r.glFinish_ZBUFFER("outbut2.bmp")
