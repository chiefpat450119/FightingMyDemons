import pygame, sys
from button import Button
import datetime
import time
import random

# Initialize pygame
pygame.mixer.init()
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Main Menu")

# Double the size of the background image
BG = pygame.image.load("assets/background.jpg")
BG = pygame.transform.scale(BG, (1280, 720))

# Set icon
icon = pygame.image.load("assets/App Icon.png")
pygame.display.set_icon(icon)


# Get Font
def get_font(size):
	return pygame.font.Font("assets/8bit.ttf", size)


# Game Variables
current_time = datetime.datetime.now()
current_time = current_time.strftime("%H:%M")
# Set alarm time to today's date and current time
alarm_time = datetime.datetime.now()
volume = 0.5
music = True


# Victory Loop
def victory():
	pygame.display.set_caption("Victory")

	# Stop playing alarm
	pygame.mixer.music.stop()
	# Start playing victory music
	pygame.mixer.music.load("assets/sounds/Victory Trumpets.mp3")
	pygame.mixer.music.set_volume(volume)
	pygame.mixer.music.play(1)

	while True:
		screen.fill("Black")

		victory_mouse_pos = pygame.mouse.get_pos()

		# Render victory banner
		victory_banner = pygame.image.load("assets/Victory Banner.png")
		victory_banner_rect = victory_banner.get_rect(center=(640, 200))
		screen.blit(victory_banner, victory_banner_rect)


		# Quit button
		quit_button = Button(image=None, pos=(640, 660), text_input="Quit", font=get_font(75), base_color="White",
		                     hovering_color="Green")

		quit_button.changeColor(victory_mouse_pos)
		quit_button.update(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				# stop music
				pygame.mixer.music.stop()
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if quit_button.checkForInput(victory_mouse_pos):
					pygame.quit()
					sys.exit()

		pygame.display.update()


def card_game():
	pygame.display.set_caption("Card Game")

	# Start playing alarm
	pygame.mixer.music.load("assets/sounds/default alarm.wav")

	pygame.mixer.music.set_volume(volume)
	pygame.mixer.music.play(-1)
	if music:
		time.sleep(5)
		pygame.mixer.music.load("assets/sounds/Boss fight music.mp3")
		pygame.mixer.music.set_volume(volume)
		pygame.mixer.music.play(-1)

	# Variables
	health = 6  # Start with full health

	# Constants
	CARD_WIDTH, CARD_HEIGHT = 100, 150
	FPS = 60


	# Load face-down images
	card_images_face_down = [pygame.image.load("assets/CardBackside.png") for i in range(12)]

	# Game variables
	cards = [i // 2 for i in range(12)]
	random.shuffle(cards)
	flipped_cards = []
	completed_cards = []

	# Load a single set of face-up images for all cards
	card_images_face_up = [pygame.image.load(f"assets/{name}") for name in
	                       ["ArrowClusterCard.png", "AxeCard.png", "IceShrinkCard.png", "SpearCard.png",
	                        "SwordCard.png", "SwordClusterCard.png"]]

	# Pygame setup
	clock = pygame.time.Clock()

	def calculate_board_position():
		return 700, 75

	def draw_card(x, y, index, flipped, completed):
		if flipped:
			if 0 <= cards[index] < len(card_images_face_up):
				screen.blit(card_images_face_up[cards[index]], (x, y))
		elif completed:
			pass
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
				draw_card(x, y, index, index in flipped_cards, index in completed_cards)

	match_event = pygame.USEREVENT + 1
	match_fail_event = pygame.USEREVENT + 2
	def check_match():
		if len(flipped_cards) == 2:
			if cards[flipped_cards[0]] == cards[flipped_cards[1]]:
				matched_indices = list(set(flipped_cards))
				for index in matched_indices:
					cards[index] = -1
					completed_cards.append(index)

				# Trigger match event
				pygame.event.post(pygame.event.Event(match_event))

				if all(card == -1 for card in cards):
					flipped_cards.clear()
					completed_cards.clear()

			else:
				pygame.time.set_timer(match_fail_event, 2000)

	board_x, board_y = calculate_board_position()

	while True:
		screen.fill("#dbd6d4")

		card_game_mouse_pos = pygame.mouse.get_pos()

		# Render Boss
		boss = pygame.image.load("assets/demon no background.png")
		boss = pygame.transform.scale(boss, (500, 500))
		boss_rect = boss.get_rect(center=(300, 310))
		screen.blit(boss, boss_rect)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				# stop music
				pygame.mixer.music.stop()

				pygame.quit()
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				x, y = event.pos
				# check if the click is within the board
				if board_x <= x <= board_x + 4 * (CARD_WIDTH + 10) and board_y <= y <= board_y + 4 * (
					CARD_HEIGHT + 10):
					row = (y - board_y) // (CARD_HEIGHT + 10)
					col = (x - board_x) // (CARD_WIDTH + 10)
					index = row * 4 + col

					if index not in flipped_cards and len(flipped_cards) < 2:
						# Play card flip sound effect
						card_flip_sound = pygame.mixer.Sound("assets/sounds/Flip card.mp3")
						card_flip_sound.set_volume(volume)
						card_flip_sound.play()
						flipped_cards.append(index)
						if len(flipped_cards) == 2:
							check_match()

			elif event.type == match_fail_event:
				flipped_cards.clear()

			# Decrease health when mouse is clicked
			elif event.type == match_event:
				health -= 1
				# Play damage sound effect
				damage_sound = pygame.mixer.Sound("assets/sounds/damagesfx.mp3")
				damage_sound.set_volume(volume)
				damage_sound.play()

				# Play damage animation
				boss = pygame.image.load("assets/Demon taking damage.png")
				boss = pygame.transform.scale(boss, (500, 500))
				boss_rect = boss.get_rect(center=(300, 310))
				screen.blit(boss, boss_rect)
				# Render health bar above boss
				health_bar = pygame.image.load(f"assets/health bar/{health}_6 health bar.png")
				health_bar_rect = health_bar.get_rect(center=(300, 590))
				screen.blit(health_bar, health_bar_rect)
				pygame.display.update()
				time.sleep(0.5)

		# Render health bar above boss
		health_bar = pygame.image.load(f"assets/health bar/{health}_6 health bar.png")
		health_bar_rect = health_bar.get_rect(center=(300, 590))
		screen.blit(health_bar, health_bar_rect)

		draw_board()

		pygame.display.flip()
		clock.tick(FPS)

		# If health is 0, go to the victory screen
		if health == 0:
			time.sleep(1)
			victory()


# Countdown Loop
def countdown():
	pygame.display.set_caption("Countdown")

	while True:

		countdown_mouse_pos = pygame.mouse.get_pos()

		screen.fill("#dbd6d4")

		# Alarm Title
		alarm_title = get_font(120).render("Alarm Time", True, "#b68f40")
		alarm_title_rect = alarm_title.get_rect(center=(940, 240))
		screen.blit(alarm_title, alarm_title_rect)

		# Display alarm time in center right
		alarm_time_text = get_font(120).render(alarm_time.strftime("%H:%M"), True, "#b68f40")
		alarm_time_rect = alarm_time_text.get_rect(center=(940, 320))
		screen.blit(alarm_time_text, alarm_time_rect)

		# Display countdown to alarm time below
		time_until_alarm = alarm_time - datetime.datetime.now()
		countdown_text = get_font(60).render(str(time_until_alarm), True, "#b68f40")
		countdown_rect = countdown_text.get_rect(center=(940, 400))
		screen.blit(countdown_text, countdown_rect)

		# Render Boss
		boss = pygame.image.load("assets/demon dormant.png")
		boss = pygame.transform.scale(boss, (500, 500))
		boss_rect = boss.get_rect(center=(340, 350))
		screen.blit(boss, boss_rect)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		"""# Go to the cardgame screen when time is up
		if time_until_alarm <= datetime.timedelta(seconds=0):
			card_game()"""

		# !!! TESTING !!! TODO: Wrap it in an if statement as above
		# Render flames and play flame whoosh
		flames = pygame.image.load("assets/Flames.png")
		flames_rect = flames.get_rect(center=(640, 350))
		screen.blit(flames, flames_rect)
		flame_whoosh = pygame.mixer.Sound("assets/sounds/flame whoosh.mp3")
		flame_whoosh.set_volume(volume)
		flame_whoosh.play()
		pygame.display.update()
		card_game()

		pygame.display.update()


# Play Loop
def play():
	pygame.display.set_caption("Play")

	music_button_colour = "White"
	music_button_text = "On"

	while True:

		play_mouse_pos = pygame.mouse.get_pos()

		screen.fill("black")

		# Alarm time input display
		global alarm_time
		display_pos = (640, 260)
		alarm_time_input_text = get_font(45).render(alarm_time.strftime("%H:%M"), True, "#b68f40")
		alarm_time_input_text_rect = alarm_time_input_text.get_rect(center=display_pos)
		screen.blit(alarm_time_input_text, alarm_time_input_text_rect)

		# Alarm Title
		alarm_text = get_font(120).render("Set Alarm Time", True, "#b68f40")
		alarm_rect = alarm_text.get_rect(center=(640, display_pos[1] - 110))
		screen.blit(alarm_text, alarm_rect)

		# Volume Title and input display
		volume_text = get_font(65).render("Volume", True, "#b68f40")
		volume_rect = volume_text.get_rect(center=(640, 400))
		screen.blit(volume_text, volume_rect)
		global volume
		volume_input_text = get_font(45).render(str(round(volume*100)), True, "#b68f40")
		volume_input_text_rect = volume_input_text.get_rect(center=(640, 470))
		screen.blit(volume_input_text, volume_input_text_rect)

		# Button images
		up_arrow = pygame.image.load("assets/uparrow.png")
		up_arrow = pygame.transform.scale(up_arrow, (20, 20))

		down_arrow = pygame.image.load("assets/downarrow.png")
		down_arrow = pygame.transform.scale(down_arrow, (20, 20))

		# Button classes to change alarm time
		class UpArrow(Button):
			def __init__(self, pos):
				super().__init__(image=up_arrow, pos=pos, text_input="", font=pygame.font.SysFont("Arial", 20), base_color="White",
				                 hovering_color="Green")

		class DownArrow(Button):
			def __init__(self, pos):
				super().__init__(image=down_arrow, pos=pos, text_input="", font=pygame.font.SysFont("Arial", 20), base_color="White",
				                 hovering_color="Green")

		# Back button
		play_back = Button(image=None, pos=(640, 660), text_input="Back", font=get_font(75), base_color="White",
		                   hovering_color="Green")

		# Confirm alarm button
		confirm_alarm = Button(image=None, pos=(640, 330), text_input="Start!", font=get_font(75),
		                       base_color="White", hovering_color="Green")

		plus_one_min = UpArrow(pos=(display_pos[0] + 35, display_pos[1] - 25))
		minus_one_min = DownArrow(pos=(display_pos[0] + 35, display_pos[1] + 25))
		plus_ten_min = UpArrow(pos=(display_pos[0] + 15, display_pos[1] - 25))
		minus_ten_min = DownArrow(pos=(display_pos[0] + 15, display_pos[1] + 25))
		plus_one_hour = UpArrow(pos=(display_pos[0] - 15, display_pos[1] - 25))
		minus_one_hour = DownArrow(pos=(display_pos[0] - 15, display_pos[1] + 25))
		plus_ten_hours = UpArrow(pos=(display_pos[0] - 35, display_pos[1] - 25))
		minus_ten_hours = DownArrow(pos=(display_pos[0] - 35, display_pos[1] + 25))

		plus_volume = UpArrow(pos=(640, 470-25))
		minus_volume = DownArrow(pos=(640, 470+25))

		toggle_music = Button(image=None, pos=(640, 550), text_input=f"Music: {music_button_text}",
		                      font=get_font(75), base_color=music_button_colour, hovering_color="Green")


		buttons = [plus_one_min,
		           minus_one_min,
		           plus_ten_min,
		           minus_ten_min,
		           plus_one_hour,
		           minus_one_hour,
		           plus_ten_hours,
		           minus_ten_hours,
		           play_back,
		           confirm_alarm,
		           plus_volume,
		           minus_volume,
		           toggle_music,

		           ]

		# Update buttons
		for button in buttons:
			button.changeColor(play_mouse_pos)
			button.update(screen)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if play_back.checkForInput(play_mouse_pos):
					main_menu()
				if confirm_alarm.checkForInput(play_mouse_pos):
					countdown()

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

				# Change volume
				if plus_volume.checkForInput(play_mouse_pos):
					# Add 0.1 to volume
					if volume <= 0.9:
						volume += 0.1
				if minus_volume.checkForInput(play_mouse_pos):
					# Subtract 0.1 from volume
					if volume >= 0.1:
						volume -= 0.1

				# Toggle music
				if toggle_music.checkForInput(play_mouse_pos):
					global music
					music = not music
					if music:
						music_button_colour = "White"
						music_button_text = "On"
						toggle_music.update(screen)
						print(music)
					else:
						music_button_colour = "Red"
						music_button_text = "Off"
						toggle_music.update(screen)
						print(music)






		pygame.display.update()


# Main Menu Loop
def main_menu():
	pygame.display.set_caption("Main Menu")

	while True:
		screen.blit(BG, (0, 0))

		menu_mouse_pos = pygame.mouse.get_pos()

		menu_text = get_font(120).render("Fighting My Demons", True, "#b68f40")
		menu_rect = menu_text.get_rect(center=(640, 100))

		play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 325),
							text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
		quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 475),
		                     text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

		screen.blit(menu_text, menu_rect)

		for button in [play_button, quit_button]:
			button.changeColor(menu_mouse_pos)
			button.update(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if play_button.checkForInput(menu_mouse_pos):
					play()
				elif quit_button.checkForInput(menu_mouse_pos):
					pygame.quit()
					sys.exit()

		pygame.display.update()

if __name__ == "__main__":
	main_menu()
