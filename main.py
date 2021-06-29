import pygame
from pygame.locals import *
import time
import random

size = 40
background = 130, 252, 3
class Apple:
    def __init__(self,parent_screen):
       self.image = pygame.image.load("F:\snake game\.vscode\Resources/apple.jpg").convert()
       self.parent_screen = parent_screen
       self.x = size*3
       self.y = size*3
    def draw(self):
       self.parent_screen.blit(self.image,(self.x,self.y))
       pygame.display.flip() 

    def move(self):
        self.x = random.randint(0,24)*size
        self.y = random.randint(0,19)*size


class snake:
    def __init__(self,parent_screen,lenght):

        self.parent_screen = parent_screen
        self.block = pygame.image.load("F:\snake game\.vscode\Resources/block.jpg").convert()
        self.direction = 'down'

        self.lenght = lenght
        self.x = [size]*lenght
        self.y = [size]*lenght

    def increse_lenngth(self):
        self.lenght += 1
        self.x.append(-1)    
        self.y.append(-1)
    
    def move_left(self):
        # self.x -= 10
        # self.draw()
        self.direction = 'left'
    
    def move_right(self):
        self.direction = 'right'
    
    def move_up(self):
      self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'  

    def walk(self):
        #update boody
        for i in range(self.lenght-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        
        #update head
        if self.direction == 'up':
            self.y[0] -= size 
        if self.direction == 'down':
            self.y[0] += size   
        if self.direction == 'left':
            self.x[0] -= size 
        if self.direction == 'right':
            self.x[0] += size 
        self.draw()
    
    def draw(self):
        self.parent_screen.fill((background))   
        for i in range(self.lenght):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()

   

class Game:
    def __init__(self):
        pygame.init()
        #pygame.display.set_caption("Snake and Apple Game")
        pygame.mixer.init()
        self.background_music()
         #Initilazing your size of winndow 
        self.surface = pygame.display.set_mode((1000,800))    
        self.snake = snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
    


    def is_collision(self, x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('bold',50)
        score = font.render(f"Score: {self.snake.lenght}", True,(255,255,255))
        self.surface.blit(score,(800,15))


    def background_music(self):
        pygame.mixer.music.load("F:\snake game\.vscode\Resources\music.mp3")
        pygame.mixer.music.play()

    def play_sound(self,sound):
            sound = pygame.mixer.Sound(f"F:\snake game\.vscode\Resources\{sound}.mp3")
            pygame.mixer.Sound.play(sound)

    def play(self):
        self.snake.walk()   
        self.apple.draw()     
        self.display_score()
        pygame.display.flip()

        #snake colliding with apple
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("ding")
            self.snake.increse_lenngth()
            self.apple.move() 
            
        # snake collidig with itself
        for i in range(3,self.snake.lenght):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
               self.play_sound("crash")
               raise "Collision Occured"
            
    def show_game_over(self):
        self.surface.fill(background)
        font = pygame.font.SysFont('arial',50)
        line1 = font.render(f"Game is over ! Your Score is {self.snake.lenght}",True,(255,255,255))
        self.surface.blit(line1,(200,300))
        line2 = font.render("To play again press enter or press Escape!", True,(255,255,255))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake= snake(self.surface,1)
        
        self.apple = Apple(self.surface)

   
    def run(self):
       running  = True
       pause = False
       while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if event.key == K_UP:
                         self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()

                elif event.type== QUIT:
                    running = False    
           
          
            try:
                if not pause:
                    self.play()
            
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(.2)

if __name__ ==  "__main__":
    game = Game()
    game.run()



