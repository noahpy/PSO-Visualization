
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


def blackbox_function(x,y):
    return pow(x,3) - x * pow(y,2)


class PSO_App(ShowBase):
    
    def __init__(self, particles:list = [] , fittness_function=blackbox_function):
        ShowBase.__init__(self)
        self.fittness_function = fittness_function
        
        format = GeomVertexFormat.getV3cp()
        vdata = GeomVertexData('terrain', format, Geom.UHStatic)
        
        xbound = (-5,5)
        ybound = (-5,5)
        self.render_scale = 0.4
        self.z_transform = -100
        self.task_list = []
        panda_flag = True
        pointAmount = (xbound[1]-xbound[0]+1) * (ybound[1]-ybound[0]+1)
        vdata.setNumRows(pointAmount)
        vertex = GeomVertexWriter(vdata, "vertex")
        color = GeomVertexWriter(vdata, "color")
        prim = GeomTriangles(Geom.UHStatic)
        linesprim = GeomLines(Geom.UHStatic)
        
        
        for y in range(ybound[0],ybound[1]+1,1):
            for x in range(xbound[0],xbound[1]+1,1):
                vertex.addData3(self.render_scale*x,self.render_scale*y,self.render_scale*(self.fittness_function(x,y)+self.z_transform))
                color.addData4(1,1,1,1)
                pos = x-xbound[0] + (y-ybound[0]) * (xbound[1]-xbound[0]+1)
                if y < ybound[1] and x < xbound[1]:
                    prim.addVertices(pos,pos+1,pos+(xbound[1]-xbound[0]+1))
                    linesprim.addVertices(pos,pos+1)
                    linesprim.addVertices(pos+1,pos+(xbound[1]-xbound[0]+1))
                    linesprim.addVertices(pos+(xbound[1]-xbound[0]+1),pos)
                if y > ybound[0] and x < xbound[1]:
                    prim.addVertices(pos,pos-(xbound[1]-xbound[0]),pos+1)
                    linesprim.addVertices(pos,pos+1)
                    linesprim.addVertices(pos,pos-(xbound[1]-xbound[0]))
                    linesprim.addVertices(pos+1,pos-(xbound[1]-xbound[0]))


        
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
            particlePath.setScale(0.2)
            particlePath.setPos(self.render_scale * particles[2*i],self.render_scale * particles[2*i+1],self.render_scale*(self.fittness_function(particles[2*i],particles[2*i+1]) + self.z_transform)+0.7) 
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

        
    def spinCameraTask(self, task):
        angleDegrees = task.time * 30.0
        angleRadians = angleDegrees * (pi / 180.0)
        rotation_r = 10
        self.camera.setPos(rotation_r * sin(angleRadians), -rotation_r * cos(angleRadians), 10)
        self.camera.setHpr(angleDegrees, -70, 0)
        return Task.cont
    
    
    def moveParticles(self, task):
        for task in self.task_list:
            task.finish()
        self.task_list = []
        for i in range(len(self.particlePaths)):
            new_x = r.randint(-20,20)
            new_y = r.randint(-20,20)
            k = LerpPosInterval(self.particlePaths[i], 0.5, Point3(self.render_scale * new_x, self.render_scale * new_y, self.render_scale * (self.fittness_function(new_x, new_y) + self.z_transform) + 0.7))
            self.task_list.append(k)
        for task in self.task_list:
            task.start()
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
    app = PSO_App(particles)
    app.run()

