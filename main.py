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


# Game Variables
current_time = datetime.datetime.now()
current_time = current_time.strftime("%H:%M")
# Set alarm time to 00:00
alarm_time = datetime.datetime.strptime("00:00", "%H:%M")


# TODO: Add a new screen that play links to (game screen)
# TODO: Add a new button (set alarm) on the play screen
# TODO: Add alarm time and countdown on game screen
# TODO: Remove options and button from main menu
# TODO: Move buttons on main menu
# TODO: Add other options on the play screen
# Play Loop
def play():
	pygame.display.set_caption("Play")

	while True:

		play_mouse_pos = pygame.mouse.get_pos()

		screen.fill("black")

		# Back button
		play_back = Button(image=None, pos=(640, 660), text_input="Back", font=get_font(75), base_color="White",
		                   hovering_color="Green")

		play_back.changeColor(play_mouse_pos)
		play_back.update(screen)

		# Alarm time input display
		global alarm_time
		display_pos = (640, 260)
		alarm_time_input_text = get_font(45).render(alarm_time.strftime("%H:%M"), True, "#b68f40")
		alarm_time_input_text_rect = alarm_time_input_text.get_rect(center=display_pos)
		screen.blit(alarm_time_input_text, alarm_time_input_text_rect)

		# Options to set alarm time
		alarm_text = get_font(65).render("Set Alarm Time", True, "#b68f40")
		alarm_rect = alarm_text.get_rect(center=(640, display_pos[1] - 80))
		screen.blit(alarm_text, alarm_rect)

		# Button images
		up_arrow = pygame.image.load("assets/uparrow.png")
		up_arrow = pygame.transform.scale(up_arrow, (20, 20))

		down_arrow = pygame.image.load("assets/downarrow.png")
		down_arrow = pygame.transform.scale(down_arrow, (20, 20))

		# Buttons to change alarm time
		class UpArrow(Button):
			def __init__(self, image, pos):
				super().__init__(image, pos, text_input="", font=pygame.font.SysFont("Arial", 20), base_color="White",
				                 hovering_color="Green")

		class DownArrow(Button):
			def __init__(self, image, pos):
				super().__init__(image, pos, text_input="", font=pygame.font.SysFont("Arial", 20), base_color="White",
				                 hovering_color="Green")

		plus_one_min = UpArrow(image=up_arrow,
		                       pos=(display_pos[0] + 35, display_pos[1] - 25)
		                       )
		minus_one_min = DownArrow(image=down_arrow,
		                          pos=(display_pos[0] + 35, display_pos[1] + 25)
		                          )
		plus_ten_min = UpArrow(image=up_arrow,
		                       pos=(display_pos[0] + 15, display_pos[1] - 25))
		minus_ten_min = DownArrow(image=down_arrow,
		                          pos=(display_pos[0] + 15, display_pos[1] + 25))
		plus_one_hour = UpArrow(image=up_arrow,
		                       pos=(display_pos[0] - 15, display_pos[1] - 25))
		minus_one_hour = DownArrow(image=down_arrow,
		                          pos=(display_pos[0] - 15, display_pos[1] + 25))
		plus_ten_hours = UpArrow(image=up_arrow,
		                         pos=(display_pos[0] - 35, display_pos[1] - 25))
		minus_ten_hours = DownArrow(image=down_arrow,
		                            pos=(display_pos[0] - 35, display_pos[1] + 25))


		# Update buttons
		for button in [plus_one_min, minus_one_min, plus_ten_min, minus_ten_min, plus_one_hour, minus_one_hour,
		               plus_ten_hours, minus_ten_hours]:
			button.update(screen)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if play_back.checkForInput(play_mouse_pos):
					main_menu()

				# Change alarm time
				if plus_one_min.checkForInput(play_mouse_pos):
					# Add 1 minute to alarm time
					alarm_time = alarm_time + datetime.timedelta(minutes=1)
				if minus_one_min.checkForInput(play_mouse_pos):
					# Subtract 1 minute from alarm time
					alarm_time = alarm_time - datetime.timedelta(minutes=1)
				if plus_ten_min.checkForInput(play_mouse_pos):
					# Add 10 minutes to alarm time
					alarm_time = alarm_time + datetime.timedelta(minutes=10)
				if minus_ten_min.checkForInput(play_mouse_pos):
					# Subtract 10 minutes from alarm time
					alarm_time = alarm_time - datetime.timedelta(minutes=10)
				if plus_one_hour.checkForInput(play_mouse_pos):
					# Add 1 hour to alarm time
					alarm_time = alarm_time + datetime.timedelta(hours=1)
				if minus_one_hour.checkForInput(play_mouse_pos):
					# Subtract 1 hour from alarm time
					alarm_time = alarm_time - datetime.timedelta(hours=1)
				if plus_ten_hours.checkForInput(play_mouse_pos):
					# Add 10 hours to alarm time
					alarm_time = alarm_time + datetime.timedelta(hours=10)
				if minus_ten_hours.checkForInput(play_mouse_pos):
					# Subtract 10 hours from alarm time
					alarm_time = alarm_time - datetime.timedelta(hours=10)


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
		options_back = Button(image=None, pos=(640, 660), text_input="Back", font=get_font(75), base_color="White",
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



