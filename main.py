import pygame
import sys
import random

WIDTH, HEIGHT = 400, 600
FPS = 60

BIRD_X = 80
BIRD_SIZE = 30
GRAVITY = 0.4
FLAP_STRENGTH = -7.0      
PIPE_WIDTH = 80
PIPE_GAP = 200          
PIPE_DIST = 200
GROUND_HEIGHT = 80
BG_COLOR = (135, 206, 235)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird (pygame)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 60)


def draw_text(surf, text, size, x, y, color=(255, 255, 255)):
    if size == "big":
        txt = big_font.render(text, True, color)
    else:
        txt = font.render(text, True, color)
    rect = txt.get_rect(center=(x, y))
    surf.blit(txt, rect)


class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = HEIGHT // 2
        self.size = BIRD_SIZE
        self.vel = 0.0
        self.alive = True
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.tilt = 0

    def flap(self):
        self.vel = FLAP_STRENGTH

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.topleft = (self.x, int(self.y))
        self.tilt = max(-25, min(90, -self.vel * 3))

    def draw(self, surf):
        pygame.draw.ellipse(surf, (255, 255, 0), self.rect)

        beak = [
            (self.x + self.size, self.y + self.size // 2 - 6),
            (self.x + self.size, self.y + self.size // 2 + 6),
            (self.x + self.size + 14, self.y + self.size // 2),
        ]
        pygame.draw.polygon(surf, (255, 140, 0), beak)

        eye_pos = (int(self.x + self.size * 0.65), int(self.y + self.size * 0.33))
        pygame.draw.circle(surf, (0, 0, 0), eye_pos, 3)


class Pipe:
    def __init__(self, x):
        self.x = x
        margin = 50
        self.gap_y = random.randint(
            margin + 20,
            HEIGHT - GROUND_HEIGHT - margin - PIPE_GAP - 20
        )
        self.passed = False

    def update(self, speed):
        self.x -= speed

    def top_rect(self):
        return pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y)

    def bottom_rect(self):
        return pygame.Rect(
            self.x,
            self.gap_y + PIPE_GAP,
            PIPE_WIDTH,
            HEIGHT - GROUND_HEIGHT - (self.gap_y + PIPE_GAP)
        )

    def draw(self, surf):
        tr = self.top_rect()
        br = self.bottom_rect()
        pygame.draw.rect(surf, (34, 139, 34), tr)
        pygame.draw.rect(surf, (34, 139, 34), br)
        pygame.draw.rect(surf, (0, 100, 0), tr, 3)
        pygame.draw.rect(surf, (0, 100, 0), br, 3)


def main():
    bird = Bird()
    pipes = []
    spawn_timer = 0
    pipe_speed = 3.5
    score = 0
    game_over = False
    show_start_text = True

    for i in range(2):
        pipes.append(Pipe(WIDTH + i * PIPE_DIST + 120))

    while True:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_over:
                        bird.flap()
                        show_start_text = False
                    else:
                        bird = Bird()
                        pipes = [Pipe(WIDTH + 120), Pipe(WIDTH + 120 + PIPE_DIST)]
                        spawn_timer = 0
                        score = 0
                        pipe_speed = 3.5
                        game_over = False
                        show_start_text = True
                elif event.key == pygame.K_r and game_over:
                    bird = Bird()
                    pipes = [Pipe(WIDTH + 120), Pipe(WIDTH + 120 + PIPE_DIST)]
                    spawn_timer = 0
                    score = 0
                    pipe_speed = 3.5
                    game_over = False
                    show_start_text = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not game_over:
                        bird.flap()
                        show_start_text = False
                    else:
                        bird = Bird()
                        pipes = [Pipe(WIDTH + 120), Pipe(WIDTH + 120 + PIPE_DIST)]
                        spawn_timer = 0
                        score = 0
                        pipe_speed = 3.5
                        game_over = False
                        show_start_text = True

        if not game_over:
            bird.update()
            spawn_timer += 1

            if spawn_timer > PIPE_DIST / pipe_speed:
                spawn_timer = 0
                pipes.append(Pipe(WIDTH + 50))

            for p in pipes:
                p.update(pipe_speed)
                if not p.passed and p.x + PIPE_WIDTH < bird.x:
                    p.passed = True
                    score += 1
                    if score % 5 == 0:
                        pipe_speed += 0.25

            pipes = [p for p in pipes if p.x + PIPE_WIDTH > -50]

            for p in pipes:
                if bird.rect.colliderect(p.top_rect()) or bird.rect.colliderect(p.bottom_rect()):
                    game_over = True
                    bird.alive = False

            if bird.y <= 0 or bird.y + bird.size >= HEIGHT - GROUND_HEIGHT:
                game_over = True
                bird.alive = False

        screen.fill(BG_COLOR)

        for i in range(3):
            pygame.draw.ellipse(screen, (255, 255, 255), (20 + i*140, 40 + (i % 2)*10, 80, 30))
            pygame.draw.ellipse(screen, (255, 255, 255), (60 + i*140, 30 + (i % 2)*10, 100, 36))

        for p in pipes:
            p.draw(screen)

        pygame.draw.rect(screen, (222, 184, 135), (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
        pygame.draw.rect(screen, (205, 133, 63), (0, HEIGHT - GROUND_HEIGHT, WIDTH, 18))

        bird.draw(screen)

        draw_text(screen, str(score), "small", WIDTH // 2, 40)

        if show_start_text and not game_over:
            draw_text(screen, "Press SPACE to flap", "small", WIDTH // 2, HEIGHT // 2)

        if game_over:
            draw_text(screen, "GAME OVER", "big", WIDTH // 2, HEIGHT // 2 - 20, (255, 50, 50))
            draw_text(screen, f"Score: {score}", "small", WIDTH // 2, HEIGHT // 2 + 30)
            draw_text(screen, "Press R or SPACE to restart", "small", WIDTH // 2, HEIGHT // 2 + 70)

        pygame.display.flip()


if __name__ == "__main__":
    main()
