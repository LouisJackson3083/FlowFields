import cv2
import numpy as np
import random
import math
from noise import get_perlin_flowfield


class Particle():
    def __init__(self, pos: (int,int), max_lifespan: int, canvas_shape: (int, int), flowfield_weights):
        self.pos = pos
        self.destruct = False
        self.lifespan = max_lifespan
        self.canvas_shape = canvas_shape
        self.flowfield_weights = flowfield_weights
        self.value = math.randrang
        a = (flowfield_weights[math.floor(self.pos[0]), math.floor(self.pos[1])][0])
        a = 360 * (a/255)
        self.x_vel = math.cos(a)
        self.y_vel = math.sin(a) 

    
    def update(self):
        self.lifespan -= 1

        a = (self.flowfield_weights[math.floor(self.pos[0]), math.floor(self.pos[1])][0])
        a = 360 * (a/255)
        self.x_vel += math.cos(a)
        self.y_vel += math.sin(a)
        
        if (self.pos[0] + self.y_vel >= self.canvas_shape[0] or 
            self.pos[0] + self.y_vel < 0 or
            self.pos[1] + self.x_vel >= self.canvas_shape[1] or 
            self.pos[1] + self.x_vel < 0
            ):
            self.destruct = True
        else:
            self.pos = (self.pos[0] + self.y_vel, self.pos[1] + self.x_vel)


width = 768
height = 768
canvas = np.zeros(shape=[height, width, 3], dtype=np.uint8) 
flowfield_weights = get_perlin_flowfield(height=height, width=width, seed=123, octaves=8)
cv2.imshow("flowfield_weights", flowfield_weights)

particles = []
max_tail_length = 128
min_particle_number = 1024
max_lifespan = 256

def create_particle():
    pos = (random.randrange(0, canvas.shape[0]), random.randrange(0, canvas.shape[0]))
    particles.append(Particle(pos=pos, max_lifespan=max_lifespan, canvas_shape=canvas.shape, flowfield_weights=flowfield_weights))

for i in range(min_particle_number):
    create_particle()
    
canvas = np.zeros(shape=[height, width, 3], dtype=np.uint8)
while True:
    canvas = np.zeros(shape=[height, width, 3], dtype=np.uint8)

    for index, particle in enumerate(particles):
        
        particle.update()

        if (particle.destruct):
            particles.pop(index)
            del particle
            create_particle()
        else:
            canvas[math.floor(particle.pos[0]), math.floor(particle.pos[1])] = particle.value * np.ones(shape=[1, 1, 3], dtype=np.uint8)
    
    cv2.imshow("canvas", canvas)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
