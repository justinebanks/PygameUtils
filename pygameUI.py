import pygame
import math


def tooltip_on_hover(rendering_screen, obj, text, font=None, text_color="black", bg_color="white"):
    font = pygame.font.Font(None, 12) if font == None else font

    mouse = pygame.mouse.get_pos()
    selected_rect: pygame.Rect

    if type(obj) == pygame.Rect:
        selected_rect = obj
    elif type(obj) == pygame.Surface:
        selected_rect = obj.get_rect()
    
    if selected_rect.collidepoint(mouse[0], mouse[1]):
        # Render Tooltip
        text_size = font.size(text)
        text_surf = font.render(text, True, text_color, bg_color)

        text_rect = text_surf.get_rect()
        text_rect.midbottom = (selected_rect.midtop[0], selected_rect.midtop[1] - 20)

        surrounding_rect = pygame.Rect(0, 0, text_size[0] + 10, text_size[1] + 10)
        surrounding_rect.center = text_rect.center

        triangle_left = (selected_rect.midtop[0]-10, selected_rect.midtop[1]-20)
        triangle_right = (selected_rect.midtop[0]+10, selected_rect.midtop[1]-20)
        arrow_polygon = [selected_rect.midtop, triangle_left, triangle_right]

        pygame.draw.polygon(rendering_screen, bg_color, arrow_polygon)
        pygame.draw.rect(rendering_screen, bg_color, surrounding_rect)
        rendering_screen.blit(text_surf, text_rect.topleft)



class UIElement:
    def __init__(self, pos: tuple, dimensions: tuple):
        self.x = pos[0]
        self.y = pos[1]
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    

    def display(self, screen: pygame.Surface):
        pygame.draw.rect(screen, "black", self.rect)



class ColorPanel(UIElement):
    def __init__(self, pos: tuple, dimensions: tuple, color: pygame.Color):
        super().__init__(pos, dimensions)
        self.color = color


    def display(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)



class TextLabel(UIElement):
    def __init__(self, pos: tuple, text: str, font: pygame.font.Font):
        self.text = text
        self.font = font
        self.color = "black"
        self.bg_color = None

        dimensions = self.font.size(self.text)
        super().__init__(pos, dimensions)


    def display(self, screen: pygame.Surface):
        text = self.font.render(self.text, True, self.color, self.bg_color)

        text_rect = text.get_rect()
        text_rect.topleft = (self.x, self.y)

        screen.blit(text, text_rect)



class TextBox(UIElement):
    def __init__(self, pos: tuple, dimensions: tuple, text: str, font: pygame.font.Font, bg_color: pygame.Color, text_placement: str = "center"):
        self.text = text
        self.font = font
        self.color = "black"
        self.bg_color = bg_color
        self.text_placement = text_placement

        text_dimensions = self.font.size(self.text)
        super().__init__(pos, dimensions)


    def display(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.bg_color, self.rect)

        text_surf = self.font.render(self.text, True, self.color, None, self.width)
        text_rect = text_surf.get_rect()
        setattr(text_rect, self.text_placement, getattr(self.rect, self.text_placement))
        screen.blit(text_surf, text_rect.topleft)



class Button(UIElement):
    def __init__(self, pos: tuple, dimensions: tuple, bg_color: pygame.Color, action):
        super().__init__(pos, dimensions)
        self.bg_color = bg_color

        self.click_action = action
        self.mouse_released = True

        self.text = ""
        self.text_color = (0, 0, 0)
        self.text_placement = "center"
        self.font = pygame.font.Font(None)
        

    def display(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.bg_color, self.rect)

        if self.text != "":
            text_surf = self.font.render(self.text, True, self.text_color, self.bg_color, self.width)
            text_rect = text_surf.get_rect()
            
            # Explanation of Line Below: (IF self.text_placement = "midleft" THEN text_rect.midleft = self.rect.midleft)
            setattr(text_rect, self.text_placement, getattr(self.rect, self.text_placement))
            screen.blit(text_surf, text_rect.topleft)

        self.is_clicked()
    

    def is_clicked(self):
        left_click = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        if left_click == False:
            self.mouse_released = True

        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and left_click and self.mouse_released:
            self.click_action()
            self.mouse_released = False
    

    def set_text(self, text: str, font: pygame.font.Font, color: pygame.Color, text_placement):
        self.text = text
        self.font = font
        self.text_color = color
        self.text_placement = text_placement



# https://study.com/learn/lesson/isometric-drawing-overview-examples.html
class IsometricFace:
    @staticmethod
    def create_top_face(start_point, length, width, mode="return", screen=None, color="black"):
        left_dist = length/2
        right_dist = width/2

        left_up = (start_point[0] - left_dist*math.sqrt(3), start_point[1] - left_dist)
        right_up = (start_point[0] + right_dist*math.sqrt(3), start_point[1] - right_dist)
        top_point = (right_up[0] - left_dist*math.sqrt(3), right_up[1]-left_dist)

        all_points = [start_point, right_up, top_point, left_up]

        if mode == "draw":
            pygame.draw.polygon(screen, color, all_points)
        elif mode == "return":
            return all_points
        elif mode == "print":
            print("Top Face")
            print("----------------")
            print("Start Point: ", start_point)
            print("Left: ", left_up)
            print("Right: ", right_up)
            print("Top: ", top_point)
            print()


    @staticmethod
    def create_left_face(start_point, length, height, mode="return", screen=None, color="black"):
        dist = length/2

        bottom_point = (start_point[0], start_point[1] + height)
        left_up = (start_point[0] - dist*math.sqrt(3), start_point[1] - dist)
        left_bottom = (left_up[0], left_up[1] + height)

        all_points = [start_point, left_up, left_bottom, bottom_point]

        if mode == "draw":
            pygame.draw.polygon(screen, color, all_points)
        elif mode == "return":
            return all_points
        elif mode == "print":
            print("Left Face")
            print("----------------")
            print("Start Point: ", start_point)
            print("Left Top: ", left_up)
            print("Left Bottom: ", left_bottom)
            print("Bottom: ", bottom_point)
            print()


    @staticmethod
    def create_right_face(start_point, width, height, mode="return", screen=None, color="black"):
        dist = width/2

        bottom_point = (start_point[0], start_point[1] + height)
        right_up = (start_point[0] + dist*math.sqrt(3), start_point[1] - dist)
        right_bottom = (right_up[0], right_up[1] + height)

        all_points = [start_point, right_up, right_bottom, bottom_point]

        if mode == "draw":
            pygame.draw.polygon(screen, color, all_points)
        elif mode == "return":
            return all_points
        elif mode == "print":
            print("Right Face")
            print("----------------")
            print("Start Point: ", start_point)
            print("Right Top: ", right_up)
            print("Right Bottom: ", right_bottom)
            print("Bottom: ", bottom_point)
            print()



class IsometricObject:
    def __init__(self, center_point, length, width, height):
        self.center_point = center_point
        self.length = length
        self.width = width
        self.height = height

        self.polygons = {
            "top": IsometricFace.create_top_face(center_point, length, width),
            "left": IsometricFace.create_left_face(center_point, length, height),
            "right": IsometricFace.create_right_face(center_point, width, height)
        }
        
        self.top_color = "red"
        self.left_color = "green"
        self.right_color = "blue"
    

    def set_colors(self, top, left, right):
        self.top_color = top
        self.left_color = left
        self.right_color = right
    

    def draw(self, screen: pygame.Surface):
        IsometricFace.create_top_face(self.center_point, self.length, self.width, "draw", screen, self.top_color)
        IsometricFace.create_left_face(self.center_point, self.length, self.height, "draw", screen, self.left_color)
        IsometricFace.create_right_face(self.center_point, self.width, self.height, "draw", screen, self.right_color)


    def print_points(self):
        IsometricFace.create_top_face(self.center_point, self.length, self.width, "print")
        IsometricFace.create_left_face(self.center_point, self.length, self.height, "print")
        IsometricFace.create_right_face(self.center_point, self.width, self.height, "print")



class Player:
    def __init__(self, rendering_screen, player_surf, platforms):
        self.surf = player_surf
        self.rect = player_surf.get_rect()
        self.screen = rendering_screen
        self.platforms = platforms

        # Running Variables
        self.acceleration = 0.5
        self.accelerating = True
        self.running = False
        self.speed = 7
        self.run_progress = 0
        self.direction = 0
        
        # Jumping Variables
        self.gravity_strength = 0.25
        self.jumping = False
        self.jump_power = 10
        self.jump_progress = 0

        self.controls = "wasd" # "arrow_keys" or "wasd"


    def draw(self):
        self.screen.blit(self.surf, self.rect)


    def is_on_floor(self):
        rects = list(map(lambda p: p.get_top(), self.platforms)) # Rects of all Platforms in Environment

        if self.rect.collideobjects(rects):
            return True
        elif self.rect.bottom >= self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
            return True
        else:
            return False
    

    def update_jump(self):
        self.rect.move_ip(0, -self.jump_power+self.jump_progress)
        self.jump_progress += self.gravity_strength

        if self.is_on_floor():
            self.jumping = False
            self.jump_progress = 0
    

    def update_run(self):
        self.rect.move_ip(self.direction*self.run_progress, 0)

        if self.accelerating: self.run_progress += self.acceleration
        else: self.run_progress -= self.acceleration

        if self.run_progress > self.speed:
            self.run_progress = self.speed
        
        if self.run_progress < 0:
            self.run_progress = 0
            self.running = False
    

    def update(self):
        self.draw()
        keys = pygame.key.get_pressed()

        key_left = keys[pygame.K_a] if self.controls == "wasd" else keys[pygame.K_LEFT]
        key_right = keys[pygame.K_d] if self.controls == "wasd" else keys[pygame.K_RIGHT]
        key_up = keys[pygame.K_w] if self.controls == "wasd" else keys[pygame.K_UP]

        mouse_clicked = pygame.mouse.get_pressed()[0]
    
        if self.jumping:
            self.update_jump()
        
        if self.running:
            self.update_run()

        # Debugging
        # if mouse_clicked:
        #     print("Jumping: ", self.jumping)
        #     print("Jump Progress: ", self.jump_progress)
        #     print("On Floor: ", self.is_on_floor())

        # Gravity
        if self.jumping == False and self.is_on_floor() == False:
            self.jump_progress = self.jump_power # Only Do the Descending Portion of the Jump
            self.jumping = True

        
        # Player Movement
        if key_left == True:
            if self.direction == 1: self.run_progress = 0
            self.running = True
            self.accelerating = True
            self.direction = -1
            
        elif key_right == True:
            if self.direction == -1: self.run_progress = 0
            self.running = True
            self.accelerating = True
            self.direction = 1
        else:
            self.accelerating = False
        if key_up:
            self.jumping = True
        

        # Platform Collision
        top_rects = list(map(lambda p: p.get_top(), self.platforms))
        bottom_rects = list(map(lambda p: p.get_bottom(), self.platforms))
        left_rects = list(map(lambda p: p.get_left(), self.platforms))
        right_rects = list(map(lambda p: p.get_right(), self.platforms))

        if rect := self.rect.collideobjects(left_rects):
            if abs(self.rect.right - rect.left) < self.speed+1:
                self.rect.right = rect.left-1

        if rect := self.rect.collideobjects(right_rects):
            if abs(self.rect.left - rect.right) < self.speed+1:
                self.rect.left = rect.right+1

        if rect := self.rect.collideobjects(top_rects):
            if abs(self.rect.bottom - rect.top) < self.speed+1:
                self.rect.bottom = rect.top+1

        if rect := self.rect.collideobjects(bottom_rects):
            self.rect.top = rect.bottom+1
            self.jump_progress = self.jump_power
            self.jumping = True
        
        


class Platform:
    def __init__(self, screen, surf):
        self.surf = surf
        self.rect = surf.get_rect()
        self.screen = screen
    
    
    @staticmethod
    def from_rect(screen, rect: pygame.Rect, color):
        surf = pygame.Surface((rect.w, rect.h))
        platform = Platform(screen, surf)
        platform.surf.fill(color)
        platform.rect.x = rect.x
        platform.rect.y = rect.y
        return platform


    def get_top(self):
        top_rect = pygame.Rect(self.rect.x+2, self.rect.y, self.rect.w-4, 2)
        return top_rect
    

    def get_bottom(self):
        rect = pygame.Rect(self.rect.x+2, self.rect.y+self.rect.h-2, self.rect.w-4, 2)
        return rect

    def get_left(self):
        rect = pygame.Rect(self.rect.x, self.rect.y+2, 2, self.rect.h-4)
        return rect


    def get_right(self):
        rect = pygame.Rect(self.rect.x+self.rect.w-2, self.rect.y+2, 2, self.rect.h-4)
        return rect


    def draw(self):
        self.screen.blit(self.surf, self.rect)
    

    def update():
        pass
