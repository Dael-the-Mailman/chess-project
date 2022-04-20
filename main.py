import pygame
from yaml import load
import engine
import os
import numpy as np

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
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages()
    running = True
    selected_square = ()
    player_clicks = []
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if selected_square == (row, col):
                    selected_square = ()
                    player_clicks = []
                else:
                    selected_square = (row, col)
                    player_clicks.append(selected_square)
                if len(player_clicks) == 2:
                    move = engine.Move(
                        player_clicks[0], player_clicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    selected_square = ()
                    player_clicks = []
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        draw(screen, gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
