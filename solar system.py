import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sistema sunar")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 100)
BLUE = (100, 100, 255)
RED = (255, 100, 100)
MERCURY = (150, 230, 150)
GREY = (50,50,50)

font_1 = pygame.font.SysFont("Arial", 16)
font_2 = pygame.font.SysFont("Arial", 22)

def get_name(variable):
    for name in globals():
        if id(globals()[name]) == id(variable):
            return name
    for name in locals():
        if id(locals()[name]) == id(variable):
            return name
    return None

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 13 / AU
    DELTA_T = 3600 * 24 / 2

    def __init__(self, x, y, radius, color, mass, period = 1):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.period = period

        self.orbit = []
        self.trail = []
        self.sun = False
        self.distance_to_sun = 0

        self.v_x = 0
        self.v_y = 0

    def display(self, WIN):
        if len(self.orbit) > 2:
            updated_points_orbit = []
            for point in self.orbit:
                x, y = point
                x = x * Planet.SCALE + WIDTH / 2
                y = y * Planet.SCALE + HEIGHT / 2
                updated_points_orbit.append((x, y))

            pygame.draw.lines(WIN, GREY, False, updated_points_orbit, 1)
        
        if len(self.trail) > 2:
            updated_points_trail = []
            for point in self.trail:
                x, y = point
                x = x * Planet.SCALE + WIDTH / 2
                y = y * Planet.SCALE + HEIGHT / 2
                updated_points_trail.append((x, y))

            pygame.draw.lines(WIN, self.color, False, updated_points_trail, 1)

        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(WIN, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = font_1.render(f"{round(self.distance_to_sun/1000)} Km", 1, WHITE)
            WIN.blit(distance_text, (x - 25, y - 20))
            
        name_text = font_1.render(f"{get_name(self)}", 1, WHITE)
        WIN.blit(name_text, (x - 25, y - 35))

    def attraction(self, body):
        body_x, body_y = body.x, body.y
        d_x = body_x - self.x
        d_y = body_y - self.y
        distance = math.sqrt(d_x ** 2 + d_y ** 2)

        if body.sun:
            self.distance_to_sun = distance
        
        f = Planet.G * self.mass * body.mass / distance ** 2
        theta = math.atan2(d_y, d_x)
        force_x = f * math.cos(theta)
        force_y = f * math.sin(theta)

        return force_x, force_y
    
    def update_position(self, Planets):
        fx_total = fy_total = 0
        for Planet in Planets:
            if self == Planet:
                continue
            
            fx, fy = self.attraction(Planet)
            fx_total += fx
            fy_total += fy

        self.v_x += fx_total * Planet.DELTA_T / self.mass
        self.v_y += fy_total * Planet.DELTA_T / self.mass

        self.x += self.v_x * Planet.DELTA_T
        self.y += self.v_y * Planet.DELTA_T

        self.trail.append((self.x, self.y))
        if len(self.trail) > 70 * 2:
            self.trail.pop(0)

        self.orbit.append((self.x, self.y))
        if len(self.orbit) > self.period / (self.DELTA_T/24/3600):
            self.orbit.pop(0)


sun = Planet(0, 0, 5, YELLOW, 1.98892 * 10 ** 30)
sun.sun = True

mercury = Planet(0.387 * Planet.AU, 0, 1, MERCURY, 3.3 * 10 ** 23, 88)
mercury.v_y = -47.4 * 1000

venus = Planet(0.723 * Planet.AU, 0, 1, WHITE, 4.8685 * 10 ** 24, 255) 
venus.v_y = -35.02 * 1000

earth = Planet(-1 * Planet.AU, 0, 1, BLUE, 5.9742 * 10 ** 24, 365)
earth.v_y = 29.783 * 1000

mars = Planet(-1.524 * Planet.AU, 0, 1, RED, 6.36 * 10 ** 23, 687)
mars.v_y = 24.077 * 1000

jupiter = Planet(5.2 * Planet.AU, 0, 4, WHITE, 1.898 * 10 ** 27, 4333)
jupiter.v_y = -13.0697 * 1000

saturn = Planet(-9.5 * Planet.AU, 0, 3, WHITE, 5.68319 * 10 ** 26, 10759)
saturn.v_y = 9.68 * 1000

uranus = Planet(-19.8 * Planet.AU, 0, 3, WHITE, 8.68103 * 10 ** 25,  30687)
uranus.v_y = 6.81 * 1000

neptune = Planet(30 * Planet.AU, 0, 3, BLUE, 1.024 * 10 ** 26, 60190)
neptune.v_y = -5.45 * 1000

haley = Planet(0.59 * Planet.AU, 0, 1, WHITE, 2.2 * 10 ** 14, 27700)
haley.v_y = 54.55 * 1000

bodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, haley]


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(120)
        WIN.fill(BLACK)

        WIN.blit(font_2.render(f"Zoom in:  arrow right", 1, WHITE), (20,20))
        WIN.blit(font_2.render(f"Zoom out: arrow left", 1, WHITE), (20,50))
        WIN.blit(font_2.render(f"Colored trail = distance traveled in 70 days", 1, WHITE), (20,80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            Planet.SCALE /= 1.01
        if keys[pygame.K_RIGHT]:
            Planet.SCALE *= 1.01
                
        for body in bodies:
            body.update_position(bodies)
            body.display(WIN)

        pygame.display.update()    
    pygame.quit()

main()







