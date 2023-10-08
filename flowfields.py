import cv2
import numpy as np
import random
import math
from noise import get_perlin_flowfield


class Particle():
    def __init__(self, pos: (int,int), max_lifespan: int, canvas_shape: (int, int)):
        self.pos = pos
        self.destruct = False
        self.lifespan = max_lifespan
        self.canvas_shape = canvas_shape
    
    def update(self, flowfield_weights):
        self.lifespan -= 1

        a = (flowfield_weights[math.floor(self.pos[0]), math.floor(self.pos[1])][0])
        a = 360 * (a/255)
        x_vel = math.cos(a)
        y_vel = math.sin(a)
        
        if (self.pos[0] + y_vel >= self.canvas_shape[0] or 
            self.pos[0] + y_vel < 0 or
            self.pos[1] + x_vel >= self.canvas_shape[1] or 
            self.pos[1] + x_vel < 0
            ):
            self.destruct = True
        else:
            self.pos = (self.pos[0] + y_vel, self.pos[1] + x_vel)


width = 512
height = 512
canvas = np.zeros(shape=[height, width, 3], dtype=np.uint8)
flowfield_weights = get_perlin_flowfield(height=height, width=width, seed=123, octaves=3)
cv2.imshow("flowfield_weights", flowfield_weights)

particles = []
previous_particle_positions = []
max_tail_length = 128
min_particle_number = 256
max_lifespan = 256

for i in range(min_particle_number):
    pos = (random.randrange(0, canvas.shape[0]), random.randrange(0, canvas.shape[0]))
    particles.append(Particle(pos=pos, max_lifespan=max_lifespan, canvas_shape=canvas.shape))
    
while True:
    canvas = np.zeros(shape=[height, width, 3], dtype=np.uint8)
    current_particle_positions = []

    for index, particle in enumerate(particles):
        
        particle.update(flowfield_weights=flowfield_weights)
        current_particle_positions.append(particle.pos)

        if (particle.destruct):
            particles.pop(index)
            del particle
            pos = (random.randrange(0, height), random.randrange(0, width))
            particles.append(Particle(pos=pos, max_lifespan=max_lifespan, canvas_shape=canvas.shape))


    previous_particle_positions.append(current_particle_positions)
    if (len(previous_particle_positions) >= max_tail_length):
        previous_particle_positions.pop(0)

    for position_set in previous_particle_positions:
        for position in position_set:
            canvas[math.floor(position[0]), math.floor(position[1])] = 255 * np.ones(shape=[1, 1, 3], dtype=np.uint8)

    
    cv2.imshow("canvas", canvas)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
