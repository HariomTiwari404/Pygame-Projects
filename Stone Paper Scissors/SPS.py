import pygame
from pygame.locals import *
import random

pygame.init()

# Display
height = 600
width = 800
display_surface = pygame.display.set_mode((width, height))

# Load images
rock_image_left = pygame.image.load("rockLEFT.png")
rock_rect_left = rock_image_left.get_rect()
rock_rect_left.bottomleft = (0, height)

paper_image_left = pygame.image.load("paperLEFT.png")
paper_rect_left = paper_image_left.get_rect()
paper_rect_left.bottomleft = (0, height)

scissor_image_left = pygame.image.load("scissorLEFT.png")
scissor_rect_left = scissor_image_left.get_rect()
scissor_rect_left.bottomleft = (0, height)

rock_image_right = pygame.image.load("rockRIGHT.png")
rock_rect_right = rock_image_right.get_rect()
rock_rect_right.bottomright = (width, height)

paper_image_right = pygame.image.load("paperRIGHT.png")
paper_rect_right = paper_image_right.get_rect()
paper_rect_right.bottomright = (width, height)

scissor_image_right = pygame.image.load("scissorRIGHT.png")
scissor_rect_right = scissor_image_right.get_rect()
scissor_rect_right.bottomright = (width, height)

#font 
font = pygame.font.Font("PumpkinTypeHalloween-8MVEg.ttf", 40)

#title text
banner_text = font.render("Stone Paper Scissors", True, (255,255,255))
banner_rect = banner_text.get_rect()
banner_rect.center = (400,100)
display_surface.blit(banner_text,banner_rect)

#load sounds
switch = pygame.mixer.Sound("switch.wav")
win = pygame.mixer.Sound('win.wav')
loss = pygame.mixer.Sound("loss.wav")
draw = pygame.mixer.Sound("draw.wav")

# Slide function
choices = ["rockLEFT.png", "paperLEFT.png", "scissorLEFT.png"]
current_choice = 0

def slide_images(direction):
    global current_choice
    if direction == "left":
        current_choice = (current_choice - 1) % len(choices)
    elif direction == "right":
        current_choice = (current_choice + 1) % len(choices)

player_choice = None
computer_choice = random.choice(choices)  # Initialize computer's choice
rounds = 1

# Game loop
running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                slide_images("right")
                switch.play()
            elif event.key == pygame.K_LEFT:
                slide_images("left")
                switch.play()
            elif event.key == pygame.K_RETURN:
                player_choice = choices[current_choice]
                computer_choice = random.choice(choices)

    # Clear the display
    display_surface.fill((0, 0, 0))

    # Blit the current image (player's choice)
    if choices[current_choice] == "rockLEFT.png":
        
        display_surface.blit(rock_image_right, rock_rect_right)

    elif choices[current_choice] == "paperLEFT.png":
        
        display_surface.blit(paper_image_right, paper_rect_right)
    elif choices[current_choice] == "scissorLEFT.png":
        
        display_surface.blit(scissor_image_right, scissor_rect_right)

    # Blit computer's choice
    if player_choice is not None:
        if computer_choice == "rockLEFT.png":
            display_surface.blit(rock_image_left, rock_rect_left)
        elif computer_choice == "paperLEFT.png":
            display_surface.blit(paper_image_left, paper_rect_left)
        elif computer_choice == "scissorLEFT.png":
            display_surface.blit(scissor_image_left, scissor_rect_left)

    # Blit player's choice
    if player_choice:
        if player_choice == "rockLEFT.png":
            display_surface.blit(rock_image_right, rock_rect_right)
        elif player_choice == "paperLEFT.png":
            display_surface.blit(paper_image_right, paper_rect_right)
        elif player_choice == "scissorLEFT.png":
            display_surface.blit(scissor_image_right, scissor_rect_right)

        rounds -= 1

        #pygame.display.update()
        
        # Check for winner
        if rounds == 0:
            display_surface.blit(banner_text,banner_rect)
            # Check for tie
            if player_choice == computer_choice:
                draw.play()
                result = "DRAW"
            # Check for player win
            elif (
                (player_choice == "rockLEFT.png" and computer_choice == "scissorLEFT.png") or
                (player_choice == "paperLEFT.png" and computer_choice == "rockLEFT.png") or
                (player_choice == "scissorLEFT.png" and computer_choice == "paperLEFT.png")
            ):
                win.play()
                result = "Player won!"
            # Otherwise, computer wins
            else:
                loss.play()
                result = "Computer won!"

            font = pygame.font.Font(None, 36)
            text = font.render(result, True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            display_surface.blit(text, text_rect)


            # Instruction message
            instruction_font = pygame.font.Font(None, 24)
            instruction_text = instruction_font.render("Press Enter to play again", True, (255, 255, 255))
            instruction_rect = instruction_text.get_rect(center=(width // 2, height // 2 + 50))
            display_surface.blit(instruction_text, instruction_rect)
            
            pygame.display.update()

            # Game pause loop
            game_pause = True
            while game_pause:
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            rounds = 1
                            player_choice = None
                            computer_choice = random.choice(choices)
                            game_pause = False
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            game_pause = False
                    if event.type == pygame.QUIT:
                        running = False
                        game_pause = False
    
            # Clear the display after game pause
            display_surface.fill((0, 0, 0))
    display_surface.blit(banner_text,banner_rect)

    pygame.display.update()

# Quit pygame
pygame.quit()
