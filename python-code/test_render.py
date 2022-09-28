
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
import random as r


def blackbox_function(x,y):
    return pow(abs(pow(x,2)-pow(y,2)),0.5) + abs(x)+ abs(y)


class MyApp(ShowBase):
    
    def __init__(self, particles:list):
        ShowBase.__init__(self)
        
        format = GeomVertexFormat.getV3cp()
        vdata = GeomVertexData('terrain', format, Geom.UHStatic)
        
        xbound = (-100,100)
        ybound = (-100,100)
        render_scale = 0.3
        z_transform = -100
        pointAmount = (xbound[1]-xbound[0]+1) * (ybound[1]-ybound[0]+1)
        vdata.setNumRows(pointAmount)
        vertex = GeomVertexWriter(vdata, "vertex")
        color = GeomVertexWriter(vdata, "color")
        prim = GeomTriangles(Geom.UHStatic)
        linesprim = GeomLines(Geom.UHStatic)
        
        
        for y in range(ybound[0],ybound[1]+1,1):
            for x in range(xbound[0],xbound[1]+1,1):
                vertex.addData3(render_scale*x,render_scale*y,render_scale*(blackbox_function(x,y)+z_transform))
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
        
        self.pandaActor = Actor("models/panda-model", {"walk":"models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.loop("walk")
        
        # Create the four lerp intervals needed for the panda to

        # walk back and forth.

        pandaz = 0.5*render_scale*z_transform
        posInterval1 = self.pandaActor.posInterval(13,

                                                   Point3(0, -10, pandaz),

                                                   startPos=Point3(0, 10, pandaz))

        posInterval2 = self.pandaActor.posInterval(13,

                                                   Point3(0, 10, pandaz),

                                                   startPos=Point3(0, -10, pandaz))

        hprInterval1 = self.pandaActor.hprInterval(3,

                                                   Point3(180, 0, pandaz),

                                                   startHpr=Point3(0, 0, pandaz))

        hprInterval2 = self.pandaActor.hprInterval(3,

                                                   Point3(0, 0, pandaz),

                                                   startHpr=Point3(180, 0, pandaz))


        # Create and play the sequence that coordinates the intervals.

        self.pandaPace = Sequence(posInterval1, hprInterval1,

                                  posInterval2, hprInterval2,

                                  name="pandaPace")

        self.pandaPace.loop()

        
        plight = PointLight('plight')
        plight.setColor((1,1,1, 1))
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(10, 0, 0)
        self.render.setLight(plnp)
        
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        
    
    def spinCameraTask(self, task):

        angleDegrees = task.time * 30.0

        angleRadians = angleDegrees * (pi / 180.0)
        
        rotation_r = 10

        self.camera.setPos(rotation_r * sin(angleRadians), -rotation_r * cos(angleRadians), 10)

        self.camera.setHpr(angleDegrees, -70, 0)

        return Task.cont
        
        

particles = [0,0,4,3,3,12,5,-5,14,5]
app = MyApp(particles)
app.run()
