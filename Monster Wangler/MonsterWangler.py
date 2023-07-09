import pygame, random, os , sys
pygame.init()

#display
screen_info = pygame.display.Info()
width = screen_info.current_w
height = screen_info.current_h
display_size = (width, height)
display_surface = pygame.display.set_mode(display_size, pygame.FULLSCREEN)

pygame.display.set_caption("Monster Wangler")

#fps and clock
clock = pygame.time.Clock()
FPS = 60
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

        return os.path.join(base_path,relative_path)

#define class
class Game():


    """a class to control gameplay"""
    def __init__(self, my_player, monster_group):
        """initialize the game object"""
        #set game values
        self.score = 0
        self.round = 0
        self.round_time = 0 
        self.frame_count = 0

        self.player = my_player
        self.monster_group  = monster_group

        #Set sound and music 
        self.next_level_sound = pygame.mixer.Sound("next_level.wav")

        #Set font 
        self.font = pygame.font.Font("Abrushow.ttf", 24)

        #Set Images
        blue_image = pygame.image.load("blue_monster.png")
        green_image = pygame.image.load("green_monster.png")
        purple_image = pygame.image.load("purple_monster.png")
        yellow_image = pygame.image.load("yellow_monster.png")

        #this list of image cooresponds to the monster_type attribute, monster type is an integer 0 -> Blue, 1 -> Green 2 -> Purple, 3 -> Yellow
        self.target_monster_images = [blue_image,green_image,purple_image, yellow_image]

        self.target_monster_type = random.randint(0,3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type] 
        
        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = width//2
        self.target_monster_rect.top = 30



    def update(self):
        """ Update the game object"""
        self.frame_count += 1
        if self.frame_count == FPS:
          self.round_time += 1
          self.frame_count = 0 

        #check for collisions
        self.check_collisons()




    def draw(self):
        """draw the hud an dthe others to the display"""
        #set colours
        WHITE = (255,255,255)
        BLUE = (20 , 76 , 235)
        GREEN = (87, 201, 47)
        PURPLE = (226, 73, 243)
        YELLOW = (243, 157, 20)

        #Ad monster colours to a list where the monster's colour matches the target_monster_images

        colours = [BLUE,GREEN,PURPLE,YELLOW]

        #Set text
        catch_text = self.font.render("Current Catch", True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.top = 5
        catch_rect.centerx = width//2

        score_text = self.font.render("Score: "+str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5,35)

        lives_text = self.font.render("Lives: "+str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 60)

        round_text = self.font.render("Current Round: "+str(self.round), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 5)


        time_text = self.font.render("Round Time: "+str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topleft = (1050, 60)


        warp_text = self.font.render("Warps: "+str(self.player.warps), True, WHITE)
        warp_rect = warp_text.get_rect()
        warp_rect.topleft = (1100, 35)

        #blite hud 

        display_surface.blit(catch_text, catch_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(time_text, time_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(warp_text, warp_rect)
        display_surface.blit(self.target_monster_image, self.target_monster_rect)

        pygame.draw.rect(display_surface, colours[self.target_monster_type],((width//2)-32,30,64,64),2)

        pygame.draw.rect(display_surface, colours[self.target_monster_type],(0,100,width,(height-200)),2)

        

         





    def check_collisons(self):
        """Check for collisions btw players and monsters"""
        #check for collison btw the player anf the individual monster
        #we must check the type of monster to see if it matches with the targeted monster
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)

        #if we collide with the monster
        if collided_monster:
            #caught the correct mosnter
            if collided_monster.type == self.target_monster_type:
                self.score += 100*self.round_time
                #remove caught monster
                collided_monster.remove(self.monster_group)
                if (self.monster_group): #if true means there are more monster available to caught
                    self.player.catch_sound.play()
                    self.choose_new_target()
                else:
                    #the round is complete no monsters
                    self.player.reset()
                    self.start_new_round()
            #caught the wrong monsters
            else:
                self.player.die_sound.play()
                self.player.lives -= 1
                #check for game over
                if self.player.lives <= 0:
                    self.pause_game("Final Score: " +str(self.score), "Press Enter To play Again")
                    self.reset_game()
                self.player.reset() #collision with wrong moster should reset the player
                     



    def start_new_round(self):
        """populate rounds with new monsters"""
        #provide a score bonus on the basis of how quickly the round was done
        self.score += int((10000*self.round )/(1+ self.round_time))
 
        #reset the round values
        self.round_time = 0 
        self.round += 1 
        self.player.warps += 1

        #As we will use this func when the player will loose the we need remove the remaining monsters on the screen 
        for remaining_monster in self.monster_group:
            self.monster_group.remove(remaining_monster)

        #add monster to the monster group
        for i in range(self.round):  #this loops will run number of time the value of round
            self.monster_group.add(Monster(random.randint(0,width-64),random.randint(100,height-300), self.target_monster_images[0],0))
            self.monster_group.add(Monster(random.randint(0,width-64),random.randint(100,height-300), self.target_monster_images[1],1))
            self.monster_group.add(Monster(random.randint(0,width-64),random.randint(100,height-300), self.target_monster_images[2],2))
            self.monster_group.add(Monster(random.randint(0,width-64),random.randint(100,height-300), self.target_monster_images[3],3))

        #choose a new target monster
        self.choose_new_target()

        self.next_level_sound.play()
    
        

    def choose_new_target(self):
        """ choose new target for the player"""
        target_monster = random.choice(self.monster_group.sprites()) # .sprites will give a list of all the monsters in monster_group
        #now we will update the image of target monster and the type of target monster
        self.target_monster_type = target_monster.type #we are equating the .type attribute of the target_monster to the target_monster_type (both are numbers)
        self.target_monster_image = target_monster.image #same, equating image of target_monster_image to the target_monster


  

    def pause_game(self, main_text, sub_text):
        global running
        WHITE = (255,255,255)

        "pause the game"
        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (width//2, height//2)

        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (width//2, height//2+64)

        #display
        display_surface.fill((0,0,0)) 
        display_surface.blit(main_text,main_rect)
        display_surface.blit(sub_text,sub_rect)
        pygame.display.update()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN) or (event.key == pygame.K_KP_ENTER):
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False






        

        



        

    def reset_game(self):
        self.score = 0
        self.player.lives = 5
        self.round = 0
        self.player.warps = 2
        self.round_time = 0 

        self.player.reset()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("knight.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width//2
        self.rect.bottom = height

        self.lives = 5
        self.warps = 2
        self.velocity = 8

        self.catch_sound = pygame.mixer.Sound("catch.wav")
        self.die_sound = pygame.mixer.Sound("die.wav")
        self.warp_sound = pygame.mixer.Sound("warp.wav")


        
    def update(self):
        """update the player"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < height - 100:
            self.rect.y += self.velocity
        if keys[pygame.K_UP] and self.rect.top >100 :
            self.rect.y -= self.velocity
            


    def warp(self):
        """ Wrap the player to the bottom or "safe zone" """
        if self.warps > 0 :
            self.warps -= 1
            self.warp_sound.play()
            self.rect.bottom = height

    def reset(self):
        """rest player position"""
        self.rect.centerx = width//2
        self.rect.centery = height
class Monster(pygame.sprite.Sprite):
    """ a class to create enemy"""
    def __init__(self, x, y,image, monster_type):
        """initilize"""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        #monster type is an integer 0 -> Blue, 1 -> Green 2 -> Purple, 3 -> Yellow
        self.type = monster_type

        #set random motion 
        self.dx = random.choice([-1,1])
        self.dy = random.choice([-1,1])
        self.velocity = random.choice([1,5])




    def update(self):
        """update the posyions of maonsters"""
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity
 
        #Bounce the monster off the edges of the screen
        if self.rect.left <= 0 or self.rect.right >= width:
            self.dx = self.dx*-1

        if self.rect.top <= 100 or self.rect.bottom >= (height-100):
            self.dy = self.dy * -1
             
#create a player group and a player object
my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

#create a monster group and we will not add the monster object here we will add the inside of our game class so we can increase the num of monters 
# according to the rounds
my_monster_group = pygame.sprite.Group()

#create a game object  
my_game = Game(my_player,my_monster_group) 
my_game.start_new_round()
my_game.pause_game("Monster Wangler", "Press Enter to Play ")


#main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.warp()
     
    #fill display
    display_surface.fill((0,0,0))

    #update and draw our sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_monster_group.update()
    my_monster_group.draw(display_surface)

    #update and draw the Game
    my_game.update()
    my_game.draw()# here we dont need to pass a display surface as draw() is not any inheruted method from  sprite 


     





    #update display and tick the clock
    clock.tick(FPS)
    pygame.display.update()


pygame.quit()