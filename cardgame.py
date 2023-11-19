import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 100, 150
FPS = 60
WHITE = (255, 255, 255)

# Load card images
card_images = []
for i in range(1, 9):
    image = pygame.image.load("card.png")  # Replace with your image file names
    image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
    card_images.extend([image, image.copy()])

# Game variables
cards = [i for i in range(16)]
random.shuffle(cards)
flipped_cards = []
selected_card = None
game_over = False

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matching Card Game")
clock = pygame.time.Clock()

def draw_card(x, y, index, flipped):
    if flipped:
        screen.blit(card_images[index], (x, y))
    else:
        pygame.draw.rect(screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT))

def draw_board():
    for i in range(4):
        for j in range(4):
            index = i * 4 + j
            x = j * (CARD_WIDTH + 10)
            y = i * (CARD_HEIGHT + 10)
            draw_card(x, y, cards[index], index in flipped_cards)

def check_match():
    if len(flipped_cards) == 2:
        if cards[flipped_cards[0]] == cards[flipped_cards[1]]:
            flipped_cards.clear()
            if all(i in flipped_cards for i in range(16)):
                global game_over
                game_over = True
        else:
            pygame.time.delay(1000)
            flipped_cards.pop()
            flipped_cards.pop()

def main():
    global selected_card
    global game_over

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y // (CARD_HEIGHT + 10)
                col = x // (CARD_WIDTH + 10)
                index = row * 4 + col

                if index not in flipped_cards:
                    flipped_cards.append(index)
                    if len(flipped_cards) == 2:
                        check_match()

        screen.fill(WHITE)
        draw_board()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
