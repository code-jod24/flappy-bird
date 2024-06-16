import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = -5
PIPE_GAP = 150

# Load images
BIRD_IMG = pygame.transform.scale(pygame.image.load('bird.png'), (34, 24))
PIPE_IMG = pygame.image.load('pipe.png')

class Bird:
    def __init__(self):
        self.image = BIRD_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Pipe:
    def __init__(self, x, y, is_top):
        self.image = pygame.transform.flip(PIPE_IMG, False, is_top)
        self.rect = self.image.get_rect()
        self.rect.x = x
        if is_top:
            self.rect.bottom = y - PIPE_GAP // 2
        else:
            self.rect.top = y + PIPE_GAP // 2

    def update(self):
        self.rect.x += PIPE_SPEED

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    bird = Bird()
    pipes = []
    frame_count = 0
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()

        if frame_count % 90 == 0:
            pipe_height = random.randint(150, 450)
            pipes.append(Pipe(SCREEN_WIDTH, pipe_height, False))
            pipes.append(Pipe(SCREEN_WIDTH, pipe_height, True))

        for pipe in pipes[:]:
            pipe.update()
            if pipe.rect.right < 0:
                pipes.remove(pipe)
                score += 0.5

        for pipe in pipes:
            if bird.rect.colliderect(pipe.rect):
                running = False

        if bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT:
            running = False

        screen.fill(WHITE)
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)
        
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {int(score)}', True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)
        frame_count += 1

    pygame.quit()

if __name__ == "__main__":
    main()
