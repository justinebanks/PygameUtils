import pygame
import pygameUI

WIDTH = 1280
HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UI Library Tester")

running = True
clock = pygame.Clock()

rect_color = "red"

def change_color():
    print("Changing Color")
    global rect_color
    rect_color = "blue"


textbox = pygameUI.TextBox((400, 400), (400, 200), "Hello World", pygame.font.Font(None, 50), "red", "center")


rect = pygame.Rect(400, 400, 50, 50)
rect.topleft = (0, 0)


button = pygameUI.Button((700, 300), (100, 50), pygame.Color.from_hsla(200, 100, 50), change_color)
button.set_text("Click Me", pygame.font.Font(None, 30), "black", "center")


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            print(rect_color)
    
    screen.fill("white")

    pygame.draw.rect(screen, rect_color, rect)
    textbox.display(screen)
    button.display(screen)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()