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
#r.glBuffer()
r.glClearColor(0.219,0,0)
r.glColor(0.85,0.125,0.125)

'''r.triangle(V2(10, 70),  V2(50, 160), V2(70, 80))
r.triangle(V2(180, 50), V2(150, 1),  V2(70, 180))
r.triangle(V2(180, 150), V2(120, 160), V2(130, 180))'''

'''r.load('Dog.obj',(10,1,0),(20,20,15))
r.glFinish("output.bmp")
r.glClear()
'''
r.load('model.obj',(1,1,0),(200,200,300))
r.glFinish("output1.bmp")
