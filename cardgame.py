import random, pygame, sys

pygame.init()

WIDTH = 1280
HEIGHT = 720
CARD_WiDTH = 100
CARD_HEIGHT = 150
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Card Game")

running = True

while running:
for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


card_images = []
for i in range(1, 9):
    image = pygame.image.load("card.png")
    image = pygame.transform.scale(image, (CARD_WiDTH, CARD_HEIGHT))
    card_images.extend([image, image.copy()])


cards = [i for i in range(16)]
random.shuffle(cards)
flipped_cards = []
selected_card = None
game_over = False

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

def play_game():
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

play_game()

pygame.quit()
