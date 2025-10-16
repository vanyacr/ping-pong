import pygame

class Ball:
    def __init__(self, x, y, speed_x, speed_y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 15
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off top/bottom
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.speed_y *= -1

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def check_collision(self, paddle1, paddle2):
        if self.rect().colliderect(paddle1.rect()) or self.rect().colliderect(paddle2.rect()):
            self.speed_x *= -1

    def reset(self):
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        self.speed_x *= -1
