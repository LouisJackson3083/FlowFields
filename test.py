import cv2
import numpy as np
import random
import math

class Particle():
    current_y = None
    current_x = None
    current_y_velocity = None
    current_x_velocity = None

    def __init__(self, y: int, x: int, y_velocity: float, x_velocity: float, canvas_shape: (int, int)):
        self.current_y = y
        self.current_x = x
        self.current_y_velocity = y_velocity
        self.current_x_velocity = x_velocity
        self.canvas_shape = canvas_shape

    def update(self, particle_positions, canvas):
        if (self.current_y + self.current_y_velocity >= self.canvas_shape[0]
            or self.current_y + self.current_y_velocity <= 0):
            self.current_y_velocity = -self.current_y_velocity
            self.current_y = max(0, min(self.canvas_shape[0], self.current_y))

        if (self.current_x + self.current_x_velocity >= self.canvas_shape[1]
            or self.current_x + self.current_x_velocity <= 0):
            self.current_x_velocity = -self.current_x_velocity
            self.current_x = max(0, min(self.canvas_shape[1], self.current_x))


        self.current_x = self.current_x + self.current_x_velocity
        self.current_y = self.current_y + self.current_y_velocity

        # canvas = cv2.putText(
        #     canvas,
        #     str(self.current_y) +", "+ str(self.current_x), 
        #     (self.current_y, self.current_x), 
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     0.2, 
        #     (0,255,0), 
        #     1, 
        #     cv2.LINE_AA
        # ) 

        for other_particle in particle_positions:
            canvas_lines = canvas.copy()
            if cv2.waitKey(200) == ord('q'):
                break

            canvas_lines = cv2.line(canvas_lines, (self.current_y, self.current_x), other_particle, (0,255,0), 1) 
            cv2.imshow("canvas", canvas_lines)
            
            # x_dist = other_particle[0] - self.current_x
            # y_dist = other_particle[1] - self.current_y


            # distance = math.sqrt(x_dist**2 + y_dist**2)

            # if (distance < 30):
        #         cv2.waitKey(5)
        #         if (x_dist != 0):
        #             x_strength = 1/x_dist
        #             self.current_x_velocity += x_strength
        #         if (y_dist != 0):
        #             y_strength = 1/y_dist
        #             self.current_y_velocity += y_strength

        return canvas


canvas = np.zeros(shape=[512, 512, 3], dtype=np.uint8)


particles = []
particle_positions = []
for i in range(5):
    y = random.randrange(0, canvas.shape[0])
    x = random.randrange(0, canvas.shape[1])
    y_velocity = random.randrange(0, 10)
    x_velocity = random.randrange(0, 10)
    particles.append(Particle(y=y, x=x, y_velocity=y_velocity, x_velocity=x_velocity, canvas_shape=canvas.shape))
    particle_positions.append((y,x))



while True:
    canvas = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
    
    for index, particle in enumerate(particles):
        canvas[int(particle.current_x),int(particle.current_y)] = 255 * np.ones(shape=[1, 1, 3], dtype=np.uint8)
        canvas = particle.update(particle_positions, canvas)
        particle_positions[index] = (particle.current_x, particle.current_y)


    cv2.imshow("canvas", canvas)
    if cv2.waitKey(100) == ord('q'):
        break
cv2.destroyAllWindows()