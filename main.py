import pygame
from yaml import load
import engine
import os

# Initialize Pygame
pygame.init()

# Variables
WIDTH = 400
HEIGHT = 400
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 24
IMAGES = {}


def loadImages():
    for image in os.listdir("images"):
        IMAGES[image[:2]] = pygame.transform.scale(
            pygame.image.load("images/" + image),
            (SQ_SIZE, SQ_SIZE)
        )


def draw(screen, gs):
    # Draw board
    colors = [pygame.Color("burlywood"), pygame.Color("saddlebrown")]
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            color = colors[((x+y) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(
                y*SQ_SIZE, x*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Draw pieces
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = gs.board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(
                    col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = engine.GameState()
    loadImages()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        draw(screen, gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
