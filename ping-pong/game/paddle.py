import pygame
import random

class Paddle:
    def __init__(self, x, y, width, height, speed=7, is_ai=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.is_ai = is_ai  # True for AI paddle

    def move(self, dy, screen_height):
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        """AI paddle movement with chance to miss."""
        if not self.is_ai:
            return

        if random.random() < 0.8:  # 80% chance to move
            ball_center = ball.y + ball.height / 2
            paddle_center = self.y + self.height / 2

            if ball_center < paddle_center:
                self.move(-self.speed, screen_height)
            elif ball_center > paddle_center:
                self.move(self.speed, screen_height)
