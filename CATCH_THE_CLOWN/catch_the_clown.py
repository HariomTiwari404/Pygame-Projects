import pygame, random
pygame.init()

#display
height = 600
width = 945
display_surface = pygame.display.set_mode((width, height))
#caption
pygame.display.set_caption("Catch The Clown")

#set clock object
clock = pygame.time.Clock()
FPS = 60

#set game values

PLAYER_STARTING_LIVES = 5
CLOWN_STARTING_VELOCITY = 5
CLOWN_ACCELERATION = 1

score = 0 
player_lives = PLAYER_STARTING_LIVES

clown_velocity = CLOWN_STARTING_VELOCITY
clown_dx = random.choice([-1,1])
clown_dy = random.choice([-1,1])

#set colours
BLUE = (1, 175,209)
YELLOW = (248,231,28)


#set fonts
font = pygame.font.Font("Franxurter.ttf", 32)
 
#set text
title_text = font.render("catch_the_clown", True, BLUE)
title_rect = title_text.get_rect()
title_rect.topleft = (50,10)


score_text = font.render("Score: "+ str(score) , True, YELLOW)
score_rect = score_text.get_rect()
score_rect.topright = (width-50,10)


lives_text = font.render("Lives: "+ str(player_lives),True, YELLOW)
lives_rect = lives_text.get_rect()
lives_rect.topright = (width - 50 , 50 ) 

game_over_text = font.render("GAMEOVER", True, BLUE, YELLOW)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (width//2, height//2)

continue_text = font.render("Click Anywhere to play agian", True, YELLOW, BLUE)
continue_rect = continue_text.get_rect()
continue_rect.center = (width//2, height//2 + 64)

 

#set sound and music

click_sound = pygame.mixer.Sound("click_sound.wav")
miss_sound = pygame.mixer.Sound("miss_sound.wav")
pygame.mixer.music.load("ctc_background_music.wav")

 
#set images 
background_image = pygame.image.load("background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0,0)

clown_image = pygame.image.load("clown.png")
clown_rect = clown_image.get_rect()
clown_rect.center = (width//2 , height//2 )








#gameloop
pygame.mixer.music.play(-1, 0.0)
running = True 
while running :
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False


        #a click is made
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            #the clown was clicked
            if clown_rect.collidepoint(mouse_x, mouse_y):
                click_sound.play()
                score += 1
                clown_velocity += CLOWN_ACCELERATION

                #move the clown into new dir
                previous_dx = clown_dx
                previous_dy = clown_dy
                while (previous_dx == clown_dx and previous_dy == previous_dy):
                    clown_dx = random.choice([-1,1])
                    clown_dy = random.choice([-1,1])

            #we missed the clown
            else:
                miss_sound.play()
                player_lives -= 1


 


    #move the clown
    clown_rect.x += clown_dx*clown_velocity
    clown_rect.y += clown_dy*clown_velocity


    #Bounce the clown off the edges of the display
    if clown_rect.left <=  0 or clown_rect.right >= width:
        clown_dx = -1*clown_dx

    if clown_rect.top <= 0 or clown_rect.bottom >= height:
        clown_dy = -1*clown_dy


    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        #pause the game until the player clicks then reset the game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused :
            #the player wants to play again
             for event in pygame.event.get():
                 #the player wants to play again
                 if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    clown_velocity = CLOWN_STARTING_VELOCITY

                    clown_rect.center = (width//2 , height//2)

                    clown_dx = random.choice([-1,1])
                    clown_dy = random.choice([-1,1])

                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False

                 #if player wants to quit
                 if event.type == pygame.QUIT:
                    running = False
                    is_paused = False







    

    #blit background
    display_surface.blit(background_image, background_rect)

    #update hud
    lives_text = font.render("Lives: "+ str(player_lives),True, YELLOW)
    score_text = font.render("Score: "+ str(score) , True, YELLOW)
    

    #blit hud
    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(lives_text, lives_rect) 

    #blit assets
    display_surface.blit(clown_image, clown_rect)










        


    #update the display
    pygame.display.update()

    #tick the clock
    clock.tick(FPS)




pygame.quit()


    

      