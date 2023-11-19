import pygame, sys
from button import Button
import datetime

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Main Menu")

# Double the size of the background image
BG = pygame.image.load("assets/background.jpg")
BG = pygame.transform.scale(BG, (1280, 720))


# Get Font
def get_font(size):
	return pygame.font.Font("assets/8bit.ttf", size)


# Play Loop
def play():
	pygame.display.set_caption("Play")

	while True:

		play_mouse_pos = pygame.mouse.get_pos()

		screen.fill("black")

		play_text = get_font(45).render("Play", True, "#b68f40")
		play_rect = play_text.get_rect(center=(640, 260))
		screen.blit(play_text, play_rect)

		# Back button
		play_back = Button(image=None, pos=(640, 460), text_input="Back", font=get_font(75), base_color="White",
		                   hovering_color="Green")

		play_back.changeColor(play_mouse_pos)
		play_back.update(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if play_back.checkForInput(play_mouse_pos):
					main_menu()

		pygame.display.update()


# Options Loop
def options():
	pygame.display.set_caption("Options")

	while True:
		options_mouse_pos = pygame.mouse.get_pos()

		screen.fill("black")

		options_text = get_font(45).render("Options", True, "#b68f40")
		options_rect = options_text.get_rect(center=(640, 260))
		screen.blit(options_text, options_rect)

		# Back button
		options_back = Button(image=None, pos=(640, 460), text_input="Back", font=get_font(75), base_color="White",
		                   hovering_color="Green")

		options_back.changeColor(options_mouse_pos)
		options_back.update(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if options_back.checkForInput(options_mouse_pos):
					main_menu()

		pygame.display.update()


# Main Menu Loop
def main_menu():
	pygame.display.set_caption("Main Menu")

	while True:
		screen.blit(BG, (0, 0))

		menu_mouse_pos = pygame.mouse.get_pos()

		menu_text = get_font(120).render("Fighting My Demons", True, "#b68f40")
		menu_rect = menu_text.get_rect(center=(640, 100))

		play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
							text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
		options_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
		                        text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
		quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
		                     text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

		screen.blit(menu_text, menu_rect)

		for button in [play_button, options_button, quit_button]:
			button.changeColor(menu_mouse_pos)
			button.update(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if play_button.checkForInput(menu_mouse_pos):
					play()
				elif options_button.checkForInput(menu_mouse_pos):
					options()
				elif quit_button.checkForInput(menu_mouse_pos):
					pygame.quit()
					sys.exit()

		pygame.display.update()

main_menu()



