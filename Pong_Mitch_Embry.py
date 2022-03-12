#import pygame
from operator import mul
from pickle import FALSE, TRUE
import pygame, sys



#define CONSTANTS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200,56,49)
BLUE = (65,105,225)

HEIGHT = 800
WIDTH = 1000

LINE_WEIGHT = 5

# pygame instance
pygame.init()
pygame.display.set_caption("PONG by Mitch Embry")
clock = pygame.time.Clock()


#create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG by Mitch Embry")

def create_screen():
    screen.fill(BLACK)

create_screen()

# define classes

class Ball:
    def __init__(self, screen, color, x_pos, y_pos, rad):
        self.screen = screen
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = -5 
        self.y_vel = 0
        self.rad = rad

    
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x_pos, self.y_pos), self.rad)

    def move(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

    def bounce(self):
        if (self.x_pos + self.x_vel < p2_paddle.x_pos + p2_paddle.width) and (p2_paddle.y_pos < self.y_pos + self.y_vel + self.rad < p2_paddle.y_pos + p2_paddle.height + self.rad):
            self.x_vel = -self.x_vel
            self.y_vel = (p2_paddle.y_pos + p2_paddle.height / 2 - self.y_pos )/15 #test
            self.y_vel = -self.y_vel
        elif self.x_pos + self.x_vel < 0:
            p1_paddle.score += 1
            self.x_pos = WIDTH / 2
            self.y_pos = HEIGHT / 2
            self.x_vel = self.x_vel
            self.y_vel = 0
        if (self.x_pos + self.x_vel > p1_paddle.x_pos - p1_paddle.width) and (p1_paddle.y_pos < self.y_pos + self.y_vel + self.rad < p1_paddle.y_pos + p1_paddle.height +self.rad):
            self.x_vel = -self.x_vel
            self.y_vel = (p1_paddle.y_pos + p1_paddle.height / 2 - self.y_pos )/ 15 #test
            self.y_vel = -self.y_vel
        elif self.x_pos + self.x_vel > WIDTH:
            p2_paddle.score += 1
            self.x_pos = WIDTH / 2
            self.y_pos = HEIGHT / 2
            self.x_vel = - self.x_vel
            self.y_vel = 0
        if self.y_pos + self.y_vel > HEIGHT or self.y_pos + self.y_vel < 0:
            self.y_vel = -self.y_vel


class Paddle:
    def __init__(self, screen, color, x_pos, y_pos, width, height):
        self.screen = screen
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.speed = - 5
        self.score = 0
        self.state = "idle"


    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x_pos, self.y_pos, self.width, self.height) )

    def move(self):
        if self.state == "up":
            self.y_pos += self.speed
        elif self.state == "down":
            self.y_pos += -self.speed
        if self.y_pos <= 0:
            self.y_pos = 0
        if self.y_pos >= HEIGHT - self.height:
            self.y_pos = HEIGHT - self.height


class AI_Paddle:
    def __init__(self, screen, color, x_pos, y_pos, width, height):
        self.screen = screen
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.score = 0
        self.speed = - 4
        self.difficulty = "medium"


    def set_difficulty(self):
        if self.difficulty == "easy":
            self.speed += 1
            ball.x_vel += 1
        if self.difficulty == "hard":
            self.speed -= 3 
            ball.x_vel -= 3



    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x_pos, self.y_pos, self.width, self.height))

    def move(self):
        if self.y_pos + self.height - 10 < ball.y_pos and ball.x_vel < 0 and ball.x_pos < WIDTH//2:
            self.y_pos -= self.speed
        elif self.y_pos > ball.y_pos and ball.x_vel < 0 and ball.x_pos < WIDTH//2:
            self.y_pos += self.speed
        
        if self.y_pos <= 0:
            self.y_pos = 0
        if self.y_pos >= HEIGHT - self.height:
            self.y_pos = HEIGHT - self.height


class Score_Board:  
    def __init__(self):
        self.game_font = pygame.font.SysFont('Ubuntu', 50)      
    
    def draw(self):
        #draw net
        pygame.draw.line(screen, WHITE, (WIDTH//2 , 0) , (WIDTH//2 , HEIGHT), 2)
        
        #draw score board
        self.score_1 = self. game_font.render(F"{str(p1_paddle.score)}", False, BLUE )
        self.score_2 = self. game_font.render(F"{str(p2_paddle.score)}", False, RED )
        screen.blit(self.score_1,((WIDTH // 2) - 60, HEIGHT // 20))
        screen.blit(self.score_2,((WIDTH // 2) + 28, HEIGHT // 20))
        

class Titles:
    def __init__(self):
        self.screen = screen
        self.game_font = pygame.font.SysFont('Ubuntu', 40)
        self.game_font_med = pygame.font.SysFont('Ubuntu', 30)
        self.game_font_small = pygame.font.SysFont('Ubuntu', 20)

        self.intro()

    def intro(self):
        screen.fill(BLACK)
        self.intro = self.game_font_med.render(F"Press M for Multiplayer Mode. Press ENTER for Singleplayer.", False, WHITE)
        screen.blit(self.intro,(WIDTH // 25 , HEIGHT // 2 - 70))

    def difficulty(self):
        screen.fill(BLACK)
        self.difficulty = self.game_font_med.render(F"Press 1 for Easy, 2 for Medium, or 3 for Hard.", False, WHITE)
        screen.blit(self.difficulty,(WIDTH // 7, HEIGHT // 2 - 70))

    def instructions(self):
        screen.fill(BLACK)
        self.instruction_1 = self.game_font_med.render(F"Player 1 use Up & Dowm keys. Player 2 use W & S Keys.", False, WHITE)
        self.instruction_2 = self.game_font_small.render(F"Press Space bar to begin Playing", False, WHITE)        
        screen.blit(self.instruction_1,(WIDTH // 15 , HEIGHT // 2 - 70))
        screen.blit(self.instruction_2,(WIDTH // 3 , HEIGHT // 2 - 20))


    def win(self):
        global playing
        self.p1_win = self.game_font.render(F"Player 1 is the winner.", False, BLUE)
        self.p2_win = self.game_font.render(F"Player 2 is the winner.", False, RED)
        self.play_again = self.game_font_small.render(F"                    Press the space bar to play again", False, WHITE)
        if p1_paddle.score >= 10:
            screen.fill(BLACK)
            screen.blit(self.p1_win,(WIDTH // 4 , HEIGHT // 2 - 85)) 
            screen.blit(self.play_again, (WIDTH // 6 , HEIGHT // 2 - 40))
            playing = False
            p1_paddle.y_pos = HEIGHT // 2 - p1_paddle.height // 2
            p2_paddle.y_pos = HEIGHT // 2 - p1_paddle.height // 2
            playing = False
        elif p2_paddle.score >= 10:
            screen.fill(BLACK)
            screen.blit(self.p2_win,(WIDTH // 4 , HEIGHT // 2 - 85))
            screen.blit(self.play_again, (WIDTH // 6 , HEIGHT // 2 - 40))
            p1_paddle.y_pos = HEIGHT // 2 - p1_paddle.height // 2
            p2_paddle.y_pos = HEIGHT // 2 - p1_paddle.height // 2
            playing = False 
        

#object instances
ball = Ball(screen, WHITE, WIDTH // 2, HEIGHT // 2, LINE_WEIGHT * 2) 
p1_paddle = Paddle(screen, BLUE, (WIDTH - 20), (HEIGHT // 2 - 10 * LINE_WEIGHT), 2 * LINE_WEIGHT, 20 * LINE_WEIGHT)
p2_paddle = AI_Paddle(screen, RED, 10, (HEIGHT // 2 - 10 * LINE_WEIGHT), 2 * LINE_WEIGHT, 20 * LINE_WEIGHT)
score = Score_Board()
titles = Titles()

#main function
running = True
playing = False
multi_player_mode = False

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_RETURN:
                titles.difficulty()
            if event.key == pygame.K_1:
               p2_paddle.difficulty = "easy"
               p2_paddle.set_difficulty()
               playing = True
            if event.key == pygame.K_2:
                playing = True
            if event.key == pygame.K_3:
                p2_paddle.difficulty = "hard"
                p2_paddle.set_difficulty()
                playing = True
            if event.key == pygame.K_m:
                p2_paddle = Paddle(screen, RED, 10, (HEIGHT // 2 - 10 * LINE_WEIGHT), 2 * LINE_WEIGHT, 20 * LINE_WEIGHT)
                titles.instructions()
            if event.key == pygame.K_SPACE:
                playing = True
            if event.key == pygame.K_w:
                p2_paddle.state = "up"
            if event.key == pygame.K_s:
                p2_paddle.state = "down"
            if event.key == pygame.K_UP:
                p1_paddle.state = "up"
            if event.key == pygame.K_DOWN:
                p1_paddle.state = "down"
        if event.type == pygame.KEYUP:
            p1_paddle.state = "idle"
            p2_paddle.state = "idle"
    
    if playing:
        create_screen()

        p1_paddle.move()
        p1_paddle.draw()
        
        ball.move()
        ball.draw()
        ball.bounce()

        p2_paddle.move()
        p2_paddle.draw()
        
        score.draw()
        titles.win()
    
    else:
        p1_paddle.score = 0
        p2_paddle.score = 0

 


    pygame.display.flip()
    clock.tick(120)



