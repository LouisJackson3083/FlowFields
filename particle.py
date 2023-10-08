import cv2
import numpy as np
import random
import math


class Particle():
    def __init__(self, pos: (int,int), vel: (int, int), canvas):
        self.pos = pos
        self.vel = vel
        self.canvas = canvas

    def update(self):

        if (self.pos[0]+self.vel[0] >= canvas.shape[0]):
            self.pos = (canvas.shape[0]-1, self.pos[1])
            self.vel = (-self.vel[0], self.vel[1])
        elif (self.pos[0]+self.vel[0] < 0):
            self.pos = (0, self.pos[1])
            self.vel = (-self.vel[0], self.vel[1])
        else:
            self.pos = (self.pos[0]+self.vel[0], self.pos[1])
            
        if (self.pos[1]+self.vel[1] >= canvas.shape[1]):
            self.pos = (self.pos[0], canvas.shape[1]-1)
            self.vel = (self.vel[0], -self.vel[1])
        elif (self.pos[1]+self.vel[1] < 0):
            self.pos = (self.pos[0], 0)
            self.vel = (self.vel[0], -self.vel[1])
        else:
            self.pos = (self.pos[0], self.pos[1]+self.vel[1])

    def calculate_lines(self, particle_positions, canvas):
        for position in particle_positions:
            canvas = cv2.line(canvas, (position[1], position[0]), (self.pos[1], self.pos[0]), (0,255,0), 1)
        return canvas


canvas = np.zeros(shape=[512, 512, 3], dtype=np.uint8)

particles = []
particle_positions = []
for i in range(50):
    pos = (random.randrange(0, canvas.shape[0]), random.randrange(0, canvas.shape[0]))
    vel = (random.randrange(0, 10), random.randrange(0, 10))
    particles.append(Particle(pos, vel, canvas))
    particle_positions.append(pos)

while True:
    canvas = np.zeros(shape=[512, 512, 3], dtype=np.uint8)

    for index, particle in enumerate(particles):
        particle.update()
        particle_positions[index] = particle.pos
        canvas[particle.pos[0], particle.pos[1]] = 255 * np.ones(shape=[1, 1, 3], dtype=np.uint8)
    
    for particle in particles:
        canvas = canvas + particle.calculate_lines(particle_positions, canvas)

    cv2.imshow("canvas", canvas)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
