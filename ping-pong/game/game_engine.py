import pygame
import os
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Player paddle
        self.player = Paddle(10, self.height // 2 - 50, self.paddle_width, self.paddle_height)
        # AI paddle
        self.ai = Paddle(self.width - 20, self.height // 2 - 50,
                         self.paddle_width, self.paddle_height,
                         speed=5, is_ai=True)

        # Ball
        self.ball = Ball(self.width // 2, self.height // 2, 7, 7, self.width, self.height)

        # Scores
        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # Player movement
        self.player_speed = 0

        # Load sounds
        pygame.mixer.init()
        SOUND_PATH = os.path.join(os.path.dirname(__file__), "sounds")
        self.hit_sound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "hit.wav"))
        self.score_sound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "score.mp3"))

        # Optional background music
        # pygame.mixer.music.load(os.path.join(SOUND_PATH, "bgm.mp3"))
        # pygame.mixer.music.play(-1)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_speed = -self.player.speed
        elif keys[pygame.K_s]:
            self.player_speed = self.player.speed
        else:
            self.player_speed = 0

        self.player.move(self.player_speed, self.height)

    def update(self):
        # Move ball
        self.ball.move()

        # Check collisions
        if self.ball.rect().colliderect(self.player.rect()) or self.ball.rect().colliderect(self.ai.rect()):
            self.ball.speed_x *= -1
            self.hit_sound.play()

        # Update scores
        if self.ball.x <= 0:
            self.ai_score += 1
            self.score_sound.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.score_sound.play()
            self.ball.reset()

        # AI paddle
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        # Draw ball
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        # Draw center line
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))
