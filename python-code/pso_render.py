
from functools import partial
from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexData
from panda3d.core import Geom
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode, GeomLines
from panda3d.core import PointLight
from panda3d.core import Point3
from math import *
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.interval.LerpInterval import LerpPosInterval
import random as r
import time as t
import queue
import math


def blackbox_function(x,y):
    return pow(x,3) - x * pow(y,2)


class PSO_App(ShowBase):
    
    def __init__(self, result_queue, func_id = -1,  particles:list = [] , fittness_function=blackbox_function, xbound = (-100,100), ybound = (-100,100)):
        ShowBase.__init__(self)
        self.fittness_function = fittness_function
        self.particles = particles
        self.result_queue = result_queue
        self.starttime = t.time()
        self.func_id = func_id
        
        format = GeomVertexFormat.getV3cp()
        vdata = GeomVertexData('terrain', format, Geom.UHStatic)
        
        self.render_scale =  50 / (ybound[1]-ybound[0])
        self.z_transform = (ybound[1]-ybound[0])/2*-1.5
        self.task_list = []
        self.animtime = 0.3
        self.spherescale = 0.8
        self.rotation_r = 7
        self.viewAngle = -70
        
        self.viewSetup()
        panda_flag = False
        
        ysteps = int((ybound[1]-ybound[0])//200)
        xsteps = int((xbound[1]-xbound[0])//200)
        if ysteps == 0:
            ysteps = 1
        if xsteps == 0:
            xsteps = 1
        pointAmount = (int(xbound[1]-xbound[0])//xsteps + 1) * (int(ybound[1]-ybound[0])//ysteps +1)
        vdata.setNumRows(pointAmount)
        vertex = GeomVertexWriter(vdata, "vertex")
        color = GeomVertexWriter(vdata, "color")
        prim = GeomTriangles(Geom.UHStatic)
        linesprim = GeomLines(Geom.UHStatic)
        

        for y in range(int(ybound[0]),int(ybound[1]+ysteps),ysteps):
            for x in range(int(xbound[0]),int(xbound[1]+xsteps),xsteps):
                vertex.addData3(self.render_scale*x,self.render_scale*y,self.render_scale*(self.fittness_function(x,y)+self.z_transform))
                color.addData4(1,1,1,1)
                pos = int(x-xbound[0])//xsteps + int(y-ybound[0])//ysteps * int(xbound[1]-xbound[0]+xsteps)//xsteps
                if y < ybound[1] and x < xbound[1]:
                    prim.addVertices(pos,pos+1,pos+int(xbound[1]-xbound[0]+xsteps)//xsteps)
                    linesprim.addVertices(pos,pos+1)
                    linesprim.addVertices(pos+1,pos+int(xbound[1]-xbound[0]+xsteps)//xsteps)
                    linesprim.addVertices(pos+int(xbound[1]-xbound[0]+xsteps)//xsteps,pos)
                if y > ybound[0] and x < xbound[1]:
                    prim.addVertices(pos,pos-int(xbound[1]-xbound[0])//xsteps,pos+1)
                    linesprim.addVertices(pos,pos+1)
                    linesprim.addVertices(pos,pos-int(xbound[1]-xbound[0])//xsteps)
                    linesprim.addVertices(pos+1,pos-int(xbound[1]-xbound[0])//xsteps)


        
        geom = Geom(vdata)
        geom.addPrimitive(prim)
        node = GeomNode('gnode')
        node.addGeom(geom)
        nodePath = self.render.attachNewNode(node)
        self.render.setTwoSided(True)
        
        linegeom = Geom(vdata)
        linegeom.addPrimitive(linesprim)
        linenode = GeomNode("linegnode")
        linenode.addGeom(linegeom)
        linesNodePath = self.render.attachNewNode(linenode)
        linesNodePath.setRenderModeThickness(2)
        linesNodePath.setColor(0,0,0,1)
        
        
        self.particlePaths = []
        for i in range(len(particles)//2):
            particlePath = self.loader.loadModel("./my_models/sphere")
            particlePath.reparentTo(self.render)
            particlePath.setColor(r.uniform(0,1),r.uniform(0,1),r.uniform(0,1),1)
            particlePath.setScale(self.spherescale)
            h = self.fittness_function(particles[2*i],particles[2*i+1])
            if math.isnan(h) or math.isinf(h):
                h = 1
            particlePath.setPos(self.render_scale * particles[2*i],self.render_scale * particles[2*i+1],self.render_scale*(h + self.z_transform) + 30 * self.render_scale) 
            self.particlePaths.append(particlePath)  

        
        if panda_flag:
            self.pandaTime()
        
        plight = PointLight('plight')
        plight.setColor((2, 2, 2, 1))
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(10, 0, 0)
        self.render.setLight(plnp)
        
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.taskMgr.add(self.moveParticles, "Particle Movement")
        
    
    def viewSetup(self):
        if self.func_id == 3:
            self.render_scale = 0.008
            self.rotation_r = 7
            self.viewAngle = -80
            self.spherescale = 0.1
            self.z_transform = -2300
        elif self.func_id == 4:
            self.render_scale = 0.07
            self.rotation_r = 2
            self.viewAngle = -80
            self.spherescale = 0.7
            self.z_transform = -5000
        elif self.func_id == 0:
            self.render_scale = 0.1
            self.rotation_r = 2
            self.viewAngle = -80
            self.spherescale = 0.2
            self.z_transform = -1200
            

        
    def spinCameraTask(self, task):
        angleDegrees = task.time * 30.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(self.rotation_r * sin(angleRadians), -self.rotation_r * cos(angleRadians), 10)
        self.camera.setHpr(angleDegrees, self.viewAngle, 0)
        return Task.cont
    
    
    def moveParticles(self, task):
        try:
            if not self.result_queue.empty():
                if t.time()-self.starttime > self.animtime:
                    self.particles = self.result_queue.get()
                    self.task_list = []
                    for i in range(len(self.particlePaths)):
                        h = self.fittness_function(self.particles[2*i],self.particles[2*i+1])
                        if math.isnan(h) or math.isinf(h):
                            h = 1
                        k = LerpPosInterval(self.particlePaths[i], self.animtime, Point3(self.render_scale * self.particles[2*i], self.render_scale * self.particles[2*i+1], self.render_scale * (h + self.z_transform) + 30*self.render_scale))
                        self.task_list.append(k)
                        k.start()
                    self.starttime = t.time()
        except:
            pass
            
        return Task.cont
    
    


    
    def pandaTime(self):
        self.pandaActor = Actor("models/panda-model", {"walk":"models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.loop("walk")
        pandaz = 0.5*self.render_scale*self.z_transform
        posInterval1 = self.pandaActor.posInterval(13, Point3(0, -10, pandaz), startPos=Point3(0, 10, pandaz))
        posInterval2 = self.pandaActor.posInterval(13,Point3(0, 10, pandaz),startPos=Point3(0, -10, pandaz))
        hprInterval1 = self.pandaActor.hprInterval(3,Point3(180, 0, pandaz),startHpr=Point3(0, 0, pandaz))
        hprInterval2 = self.pandaActor.hprInterval(3,Point3(0, 0, pandaz),startHpr=Point3(180, 0, pandaz))
        self.pandaPace = Sequence(posInterval1, hprInterval1,posInterval2, hprInterval2,name="pandaPace")
        self.pandaPace.loop()
        
        
if __name__ == '__main__':
    particles = [0,0,4,3,3,12,5,-5,14,5]
    app = PSO_App(queue.Queue(),particles)
    app.run()

