import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 200, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.state = MENU
        self.reset_game()

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Moving right
        self.next_direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.speed = 10
        self.high_score = 0

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.state == MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = PLAYING
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

                elif self.state == PLAYING:
                    if event.key == pygame.K_UP and self.direction != (0, 1):
                        self.next_direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                        self.next_direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                        self.next_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                        self.next_direction = (1, 0)
                    elif event.key == pygame.K_p:
                        self.state = MENU

                elif self.state == GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.state = PLAYING
                        self.reset_game()
                    elif event.key == pygame.K_m:
                        self.state = MENU

    def update(self):
        if self.state != PLAYING:
            return

        self.direction = self.next_direction

        # Calculate new head position
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)

        # Check collision with self
        if new_head in self.snake:
            self.state = GAME_OVER
            if self.score > self.high_score:
                self.high_score = self.score
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
            # Increase speed every 50 points
            if self.score % 50 == 0 and self.speed < 20:
                self.speed += 2
        else:
            # Remove tail if no food eaten
            self.snake.pop()

    def draw_menu(self):
        self.screen.fill(BLACK)

        title = self.large_font.render("SNAKE GAME", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title, title_rect)

        instructions = [
            "Press SPACE to Start",
            "Press Q to Quit",
            "",
            "Controls:",
            "Arrow Keys - Move",
            "P - Pause/Menu"
        ]

        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def draw_game(self):
        self.screen.fill(BLACK)

        # Draw snake
        for i, segment in enumerate(self.snake):
            x, y = segment
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

            # Head is darker green
            if i == 0:
                pygame.draw.rect(self.screen, DARK_GREEN, rect)
                pygame.draw.rect(self.screen, GREEN, rect, 2)
            else:
                pygame.draw.rect(self.screen, GREEN, rect)
                pygame.draw.rect(self.screen, DARK_GREEN, rect, 1)

        # Draw food
        food_rect = pygame.Rect(
            self.food[0] * GRID_SIZE,
            self.food[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(self.screen, RED, food_rect)
        pygame.draw.rect(self.screen, WHITE, food_rect, 2)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw speed
        speed_text = self.font.render(f"Speed: {self.speed}", True, WHITE)
        self.screen.blit(speed_text, (10, 50))

        pygame.display.flip()

    def draw_game_over(self):
        self.screen.fill(BLACK)

        game_over_text = self.large_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(game_over_text, game_over_rect)

        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        high_score_text = self.font.render(f"High Score: {self.high_score}", True, YELLOW)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(high_score_text, high_score_rect)

        instructions = [
            "Press SPACE to Play Again",
            "Press M for Menu"
        ]

        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100 + i * 40))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()

            if self.state == MENU:
                self.draw_menu()
            elif self.state == PLAYING:
                self.draw_game()
                self.clock.tick(self.speed)
            elif self.state == GAME_OVER:
                self.draw_game_over()
                self.clock.tick(10)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
