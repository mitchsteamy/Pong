#import pygame
import pygame, sys



#define CONSTANTS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
BLUE = (0,0,255)

HEIGHT = 800
WIDTH = 1000

LINE_WEIGHT = 5

# pygame instance
pygame.init()
pygame.display.set_caption("Pong 2")
clock = pygame.time.Clock()


#create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")

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
        if (self.x_pos + self.x_vel < p1_paddle.x_pos + p1_paddle.width) and (p1_paddle.y_pos < self.y_pos + self.y_vel + self.rad < p1_paddle.y_pos + p1_paddle.height):
            self.x_vel = -self.x_vel
            self.y_vel = (p1_paddle.y_pos + p1_paddle.height / 2 - self.y_pos )/15 #test
            self.y_vel = -self.y_vel
        elif self.x_pos + self.x_vel < 0:
            p2_paddle.score += 1
            self.x_pos = WIDTH / 2
            self.y_pos = HEIGHT / 2
            self.x_vel = 5
            self.y_vel = 0
        if (self.x_pos + self.x_vel > p2_paddle.x_pos - p2_paddle.width) and (p2_paddle.y_pos < self.y_pos + self.y_vel + self.rad < p2_paddle.y_pos + p2_paddle.height):
            self.x_vel = -self.x_vel
            self.y_vel = (p2_paddle.y_pos + p2_paddle.height / 2 - self.y_pos )/ 15 #test
            self.y_vel = -self.y_vel
        elif self.x_pos + self.x_vel > WIDTH:
            p1_paddle.score += 1
            self.x_pos = WIDTH / 2
            self.y_pos = HEIGHT / 2
            self.x_vel = -5
            self.y_vel = 0
        if self.y_pos + self.y_vel > HEIGHT or self.y_pos + self.y_vel < 0:
            self.y_vel = -self.y_vel


class Paddle:
    def __init__(self, screen, color, x_pos, y_pos, width, height) -> None:
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


class Score_Board:  
    def __init__(self) -> None:
        self.game_font = pygame.font.SysFont('Ubuntu', 50)      
    
    def draw(self):
        #draw net
        pygame.draw.line(screen, WHITE, (WIDTH//2 , 0) , (WIDTH//2 , HEIGHT), 2)
        
        #draw score board
        self.score = self. game_font.render(F"{str(p1_paddle.score)}   {str(p2_paddle.score)}", False, WHITE )
        screen.blit(self.score,( (WIDTH // 2) - 60   , HEIGHT // 20))

class Titles:
    def __init__(self) -> None:
        self.screen = screen
        self.game_font = pygame.font.SysFont('Ubuntu', 40)
        self.game_font_small = pygame.font.SysFont('Ubuntu', 20)


        self.intro()

    def intro(self):
        screen.fill(BLACK)
        self.intro = self.game_font.render(F"Press the space bar to begin playing.", False, WHITE )
        screen.blit(self.intro,(WIDTH // 9 , HEIGHT // 2 - 40))
    
    def win(self):
        global playing
        self.p1_win = self.game_font.render(F"Player 1 is the winner.", False, WHITE )
        self.p2_win = self.game_font.render(F"Player 2 is the winner.", False, WHITE )
        self.play_again = self.game_font_small.render(F"                    Press the space bar to play again", False, WHITE)
        if p1_paddle.score >= 10:
            screen.fill(BLACK)
            screen.blit(self.p1_win,(WIDTH // 4 , HEIGHT // 2 - 85)) 
            screen.blit(self.play_again, (WIDTH // 6 , HEIGHT // 2 - 40))
            playing = False
            p1_paddle.y_pos = HEIGHT // 2 - p1_paddle.height // 2
            p2_paddle.y_pos = HEIGHT // 2 - p1_paddle.height // 2
        elif p2_paddle.score >= 10:
            screen.fill(BLACK)
            screen.blit(self.p2_win,(WIDTH // 4 , HEIGHT // 2 - 85))
            screen.blit(self.play_again, (WIDTH // 6 , HEIGHT // 2 - 40))
            p1_paddle.y_pos = HEIGHT // 2 - p1_paddle.height // 2
            p2_paddle.y_pos = HEIGHT // 2 - p1_paddle.height // 2
            playing = False 
        

#object instances
ball = Ball(screen, WHITE, WIDTH // 2, HEIGHT // 2, LINE_WEIGHT * 2) 
p1_paddle = Paddle(screen, BLUE, 10, (HEIGHT // 2 - 10 * LINE_WEIGHT), 2 * LINE_WEIGHT, 20 * LINE_WEIGHT)
p2_paddle = Paddle(screen, RED, WIDTH - 20, (HEIGHT // 2 - 10 * LINE_WEIGHT), 2 * LINE_WEIGHT, 20 * LINE_WEIGHT)
score = Score_Board()
titles = Titles()

#main function
running = True
playing = False

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_SPACE:
                playing = True    
            if event.key == pygame.K_w:
                p1_paddle.state = "up"
            if event.key == pygame.K_s:
                p1_paddle.state = "down"
            if event.key == pygame.K_UP:
                p2_paddle.state = "up"
            if event.key == pygame.K_DOWN:
                p2_paddle.state = "down"
        if event.type == pygame.KEYUP:
            p1_paddle.state = "idle"
            p2_paddle.state = "idle"
    
    if playing:
        create_screen()

        p1_paddle.move()
        p1_paddle.draw()

        p2_paddle.move()
        p2_paddle.draw()
        
        ball.move()
        ball.draw()
        ball.bounce()
        
        score.draw()
        titles.win()
    
    else:
        p1_paddle.score = 0
        p2_paddle.score = 0

 


    pygame.display.flip()
    clock.tick(120)



