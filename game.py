from config import *
import pygame
from pygame.locals import *
import time
import random

class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = random.choice([BLUE, RED, GREEN, YELLOW, ORANGE])

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Paddle:
    def __init__(self):
        self.x = (WINDOW_WIDTH - PADDLE_WIDTH) / 2
        self.y = WINDOW_HEIGHT - PADDLE_HEIGHT * 2
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect)
    
    def move(self, keys):
        if keys[K_RIGHT] and self.x < WINDOW_WIDTH - PADDLE_WIDTH:
            self.x += 10
        if keys[K_LEFT] and self.x > 0:
            self.x -= 10
        self.rect.x = self.x

class Ball:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.dx = 10
        self.dy = -10
        self.rect = pygame.Rect(self.x, self.y, BALL_RADIUS, BALL_RADIUS)
        self.color = BLACK
        self.score = 0

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def move(self, paddle, blocks):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off the walls
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx = -self.dx
        if self.rect.top <= 0:
            self.dy = -self.dy
        if self.rect.bottom >= WINDOW_HEIGHT:
            return False  # Indicate the ball is out

        # Bounce off the paddle
        if self.rect.colliderect(paddle.rect):
            self.dy = -self.dy

            # Adjust angle based on where the ball hits the paddle
            hit_pos = (self.rect.centerx - paddle.rect.left) / PADDLE_WIDTH
            self.dx = 20 * (hit_pos - 0.5)
            
            

        # Bounce off the blocks
        for block in blocks[:]:
            if self.rect.colliderect(block.rect):
                self.dy = -self.dy
                self.color = block.color  # Change ball color to block color
                blocks.remove(block)  # Remove the block
                self.score += 1
                return True  # Indicate block was hit

        return True

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        self.running = True
        self.lives = 3
        self.high_score = 0
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surface.fill(WHITE)
        self.paddle = Paddle()
        self.ball = Ball()
        self.blocks = self.building_blocks()

        # Load sounds
        self.block_hit_sound = pygame.mixer.Sound("block_hit.wav")
        self.paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")
        self.game_over_sound = pygame.mixer.Sound("game_over.wav")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.paddle.move(keys)
            if not self.ball.move(self.paddle, self.blocks):
                self.lives -= 1
                if self.lives == 0:
                    pygame.mixer.Sound.play(self.game_over_sound)
                    print("Game Over")
                    self.running = False
                else:
                    self.ball = Ball()  # Reset the ball position

            self.surface.fill(WHITE)  # Clear the screen
            for block in self.blocks:
                block.draw(self.surface)
            self.paddle.draw(self.surface)
            self.ball.draw(self.surface)

            # Display lives and score
            self.display_status()

            pygame.display.flip()
            time.sleep(SLEEP_TIME)

            if not self.blocks:
                print("You Win!")
                self.running = False

            if self.ball.score > self.high_score:
                self.high_score = self.ball.score

        pygame.quit()

    def display_status(self):
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {self.lives}", True, BLACK)
        score_text = font.render(f"Score: {self.ball.score}", True, BLACK)
        high_score_text = font.render(f"High Score: {self.high_score}", True, BLACK)
        self.surface.blit(lives_text, (20, 20))
        self.surface.blit(score_text, (200, 20))
        self.surface.blit(high_score_text, (400, 20))

    def building_blocks(self):
        blocks = []
        x, y = 20, 30
        for i in range(ROWS_OF_BRICKS):
            x = 20
            if i % 5 != 0:
                y += BRICK_HEIGHT + 2
            else:
                y += BRICK_HEIGHT + 10
            for j in range(BRICKS_PER_ROW):
                block = Block(x, y)
                blocks.append(block)
                if j % 2 == 0:
                    x += BRICK_WIDTH + 2
                else:
                    x += BRICK_WIDTH + 10
        return blocks

if __name__ == "__main__":
    game = Game()
    game.run()
