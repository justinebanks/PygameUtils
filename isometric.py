import pygame
from pygameUI import IsometricObject, tooltip_on_hover

WIDTH = 1280
HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True


obj1 = IsometricObject((WIDTH/2, HEIGHT/2+200), 200, 200, 100)
obj2 = IsometricObject(obj1.polygons["top"][1], 100, 200, 100)
obj3 = IsometricObject(obj1.polygons["top"][3], 200, 100, 100)
obj4 = IsometricObject(obj1.polygons["top"][2], 200, 200, 50)

objs = [obj1, obj2, obj3, obj4]
car_rect = pygame.Rect(300, 300, 50, 50)


for obj in objs:
    obj.set_colors("green", "darkgoldenrod4", "chocolate4")


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("black")

    obj2.draw(screen)
    obj3.draw(screen)
    obj4.draw(screen)
    obj1.draw(screen)

    pygame.draw.rect(screen, "red", car_rect)
    tooltip_on_hover(screen, car_rect, "This is my new tooltip")

    pygame.display.update()
    clock.tick(60)


pygame.quit()