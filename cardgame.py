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

# Load face-down images
card_images_face_down = [pygame.image.load("assets/CardBackside.png") for i in range(12)]

# Game variables
cards = [i // 2 for i in range(12)] 
random.shuffle(cards)
flipped_cards = []
game_over = False
background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load a single set of face-up images for all cards
card_images_face_up = [pygame.image.load(f"assets/{name}") for name in ["ArrowClusterCard.png", "AxeCard.png", "IceShrinkCard.png", "SpearCard.png", "SwordCard.png", "SwordClusterCard.png"]]

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matching Card Game")
clock = pygame.time.Clock()


def calculate_board_position():
    board_width = 4 * (CARD_WIDTH + 10)
    board_height = 4 * (CARD_HEIGHT + 10)
    x = (WIDTH - board_width) // 2
    y = (HEIGHT - board_height) // 2
    return x, y


def draw_card(x, y, index, flipped):
    if flipped:
      if 0 <= cards[index] < len(card_images_face_up):
        screen.blit(card_images_face_up[cards[index]], (x, y))
    else:
        if 0 <= index < len(card_images_face_down):
            screen.blit(card_images_face_down[index], (x, y))


def draw_board():
    board_x, board_y = calculate_board_position()

    for i in range(4):
        for j in range(4):
            index = i * 4 + j
            x = board_x + j * (CARD_WIDTH + 10)
            y = board_y + i * (CARD_HEIGHT + 10)
            draw_card(x, y, index, index in flipped_cards)


def check_match():
  if len(flipped_cards) == 2:
      if cards[flipped_cards[0]] == cards[flipped_cards[1]]:
          matched_indices = list(set(flipped_cards))
          for index in matched_indices:
              cards[index] = -1

          if all(card == -1 for card in cards):
              global game_over
              game_over = True
              flipped_cards.clear()
      else:
        pygame.time.set_timer(pygame.USEREVENT, 1000)




def main():
    global game_over

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = (y - board_y) // (CARD_HEIGHT + 10)
                col = (x - board_x) // (CARD_WIDTH + 10)
                index = row * 4 + col

                if index not in flipped_cards and len(flipped_cards) < 2:
                    flipped_cards.append(index)
                    if len(flipped_cards) == 2:
                        check_match()

            elif event.type == pygame.USEREVENT:
              flipped_cards.clear()

        screen.blit(background, (0, 0))
        draw_board()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    board_x, board_y = calculate_board_position()
    main()
