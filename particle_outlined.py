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
            canvas = cv2.line(canvas, (math.floor(position[1]), math.floor(position[0])), (math.floor(self.pos[1]), math.floor(self.pos[0])), (0,255,0), 1)
        return canvas


canvas = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
particles = []
particle_positions = []
deacceleration_rate = 1.0125

for i in range(4):
    pos = (random.randrange(0, canvas.shape[0]), random.randrange(0, canvas.shape[0]))
    vel = (random.randrange(0, 10), random.randrange(0, 10))
    particles.append(Particle(pos, vel, canvas))
    particle_positions.append(pos)

while True:
    canvas = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
    for index, particle in enumerate(particles):
        particle.update()
        particle_positions[index] = particle.pos
        canvas[math.floor(particle.pos[0]), math.floor(particle.pos[1])] = 255 * np.ones(shape=[1, 1, 3], dtype=np.uint8)

        canvas = canvas + particle.calculate_lines(particle_positions, canvas)
        # particle.vel = (particle.vel[0]/deacceleration_rate, particle.vel[1]/deacceleration_rate)
        
    for particle in particles:
        for position in particle_positions:
            dist_y = (particle.pos[0]-position[0])
            dist_x = (particle.pos[1]-position[1])
            distance = math.sqrt(dist_y**2 + dist_x**2)
            canvas = cv2.circle(canvas, (particle.pos[1], particle.pos[0]), 75, (255,0,0), thickness=1, lineType=8, shift=0)
            if (distance >= 1 and distance <= 75):
                if dist_y == 0: dist_y = 1
                if dist_x == 0: dist_x = 1

                particle.vel = (particle.vel[0] + (1 / dist_y), particle.vel[1] + (1 / dist_x))
                canvas = cv2.line(canvas, (math.floor(position[1]), math.floor(position[0])), (math.floor(particle.pos[1]), math.floor(particle.pos[0])), (255,0,0), 2)
                
            
    cv2.imshow("Canvas", canvas)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
