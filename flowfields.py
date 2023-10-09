import cv2
import numpy as np
import random
import math
from noise import get_perlin_flowfield
import imageio


class Particle():
    def __init__(
            self, 
            pos: (int,int), 
            max_lifespan: int, 
            canvas_shape: (int, int),
            flowfield_weights,
        ):
        self.pos = pos
        self.destruct = False
        self.lifespan = max_lifespan
        self.canvas_shape = canvas_shape
        self.flowfield_weights = flowfield_weights
        self.vel = (0,0)
        self.value = random.randrange(64, 255)
    
    def update(self):
        self.lifespan -= 1

        a = (self.flowfield_weights[math.floor(self.pos[0]), math.floor(self.pos[1])][0])
        a = 360 * (a/255)
        x_vel = math.cos(a)
        y_vel = math.sin(a)
        
        if (self.pos[0] + y_vel >= self.canvas_shape[0] or 
            self.pos[0] + y_vel < 0 or
            self.pos[1] + x_vel >= self.canvas_shape[1] or 
            self.pos[1] + x_vel < 0 or
            self.lifespan <= 0
            ):
            self.destruct = True
        else:
            self.pos = (self.pos[0] + y_vel, self.pos[1] + x_vel)


def create_new_particle():
    pos = (random.randrange(0, canvas.shape[0]), random.randrange(0, canvas.shape[0]))
    particles.append(Particle(
        pos=pos, 
        max_lifespan=max_lifespan, 
        canvas_shape=canvas.shape,
        flowfield_weights=flowfield_weights,
        ))
    

width = 512
height = 512
flowfield_weights = get_perlin_flowfield(height=height, width=width, seed=652, octaves=7)
particles = []
max_tail_length = 128
min_particle_number = 1596
max_lifespan = 256
pixel_queue = []
output_images = []
bg_color = (0,0,16)
canvas = np.ones(shape=[height, width, 3], dtype=np.uint8)
canvas[:height,:width] = bg_color * np.ones(shape=[1, 1, 3], dtype=np.uint8)
cv2.imshow("flowfield_weights", flowfield_weights)

for i in range(min_particle_number):
    create_new_particle()


while True:

    pixels_current = []
    for index, particle in enumerate(particles):
        
        particle.update()

        if (particle.destruct):
            particles.pop(index)
            del particle
            create_new_particle()
        else:
            canvas[math.floor(particle.pos[0]), math.floor(particle.pos[1])] = (0,particle.value/4,particle.value) * np.ones(shape=[1, 1, 3], dtype=np.uint8)
            if (particle.pos not in pixel_queue):
                pixels_current.append(particle.pos)

    pixel_queue.append(pixels_current)
    if (len(pixel_queue) >= max_tail_length):
        for pixel in pixel_queue[0]:
            canvas[math.floor(pixel[0]), math.floor(pixel[1])] = bg_color
        pixel_queue.pop(0)

    cv2.imshow("canvas", canvas)
    output_images.append(canvas.copy())

    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()

print(len(output_images))
output_images = output_images[-max_lifespan*2:]
print(len(output_images))
imageio.mimsave('./example_gifs/flowfield.gif', output_images, fps=60)
# with imageio.get_writer('./example_gifs/flowfield.gif', mode='I') as writer:
#     for image in output_images:
#         frame = imageio.imread(image)
#         writer.append_data(frame)