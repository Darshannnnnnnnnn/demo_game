import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = SCREEN_HEIGHT - 100
GRAVITY = 0.6
JUMP_STRENGTH = -12
OBSTACLE_SPEED = 7
WOLF_ANIMATION_SPEED = 0.1
ROCK_SPACING = 500  # Adjusted rock spacing
WOLF_WIDTH = 100  # Adjusted wolf width
WOLF_HEIGHT = 50  # Adjusted wolf height

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wolf Run')

# Load assets
wolf_run_images = [
    pygame.image.load(os.path.join('assets', 'wolf', f'wolf_run_{i}.png')) for i in range(1, 5)
]
wolf_run_images = [pygame.transform.scale(image, (WOLF_WIDTH, WOLF_HEIGHT)) for image in wolf_run_images]
rock_img = pygame.image.load(os.path.join('assets', 'rock.png'))
rock_img = pygame.transform.scale(rock_img, (50, 50))

class Wolf:
    def __init__(self):
        self.images = wolf_run_images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GROUND_HEIGHT - self.rect.height
        self.y_velocity = 0
        self.is_jumping = False
        self.animation_timer = 0

    def update(self):
        if self.is_jumping:
            self.y_velocity += GRAVITY
            self.rect.y += self.y_velocity

            if self.rect.y >= GROUND_HEIGHT - self.rect.height:
                self.rect.y = GROUND_HEIGHT - self.rect.height
                self.is_jumping = False
                self.y_velocity = 0
        
        self.animate()

    def animate(self):
        self.animation_timer += WOLF_ANIMATION_SPEED
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = JUMP_STRENGTH
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Rock:
    def __init__(self, x):
        self.image = rock_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = GROUND_HEIGHT - self.rect.height

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.x < -self.rect.width

class Ground:
    def __init__(self):
        self.rect = pygame.Rect(0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)

def game_over_screen(score):
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def start_screen():
    screen.fill(WHITE)  # Clear the screen
    font = pygame.font.Font(None, 74)
    text = font.render("Press SPACE to Start", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        start_screen()  # Display start screen
        wolf = Wolf()
        ground = Ground()
        rocks = [new_rock()]
        score = 0
        last_rock_x = SCREEN_WIDTH

        game_active = True
        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if wolf.jump():
                            score += 10

            if not running:
                break

            # Update game objects
            wolf.update()
            for rock in rocks:
                rock.update()

            # Remove off-screen rocks
            rocks = [rock for rock in rocks if not rock.is_off_screen()]

            # Add new rocks with fixed spacing
            if last_rock_x - rocks[-1].rect.x > ROCK_SPACING:
                rocks.append(new_rock(last_rock_x))
                last_rock_x = rocks[-1].rect.x

            # Collision detection
            for rock in rocks:
                if wolf.rect.colliderect(rock.rect):
                    game_active = False

            # Draw everything
            screen.fill(WHITE)  # Clear the screen
            ground.draw(screen)  # Draw the ground
            wolf.draw(screen)
            for rock in rocks:
                rock.draw(screen)

            # Display score
            font = pygame.font.Font(None, 36)
            text = font.render(f'Score: {score}', True, BLACK)
            screen.blit(text, (10, 10))

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)

        if running:
            game_over_screen(score)

    pygame.quit()

def new_rock(last_rock_x=None):
    if last_rock_x is None:
        return Rock(SCREEN_WIDTH)
    return Rock(last_rock_x)

if __name__ == "__main__":
    main()
