import pygame, sys, random
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800,600), 0, 32)
cur = pygame.image.load(r"h:\pygame\bitcoin-logo.png").convert_alpha()
joy1 = pygame.joystick.Joystick(0)
joy1.init()

class ball:
    def __init__(self):
        self.x, self.y = 600,300
        self.vector = [1,1]
        self.image = pygame.image.load(r"h:\pygame\bitcoin-logo.png").convert_alpha()
        self.scale = 0.5
        self.transformed = pygame.transform.rotozoom(self.image, 0, self.scale)

    def update(self, pad1pos, pad2pos, p1spin, p2spin):
        prevx, prevy = self.x, self.y
        self.x, self.y = self.x + self.vector[0], self.y + self.vector[1]
        self.scale = max(self.scale,0.1)
        self.vector[0] = min(self.vector[0], 20)
        if prevx > 50+self.transformed.get_width()/2  and self.x <= 50+self.transformed.get_width()/2:
            #print 'spriong'
            if abs(pad1pos - self.y) < 50:
                #print 'DOINGLE'
                self.vector[0] = self.vector[0] * -1.1
                self.scale *= 0.9
                self.vector[1] += p1spin
        if prevx < 750-self.transformed.get_width()/2 and self.x >= 750-self.transformed.get_width()/2:
            print 'spriong'
            if abs(pad2pos - self.y) < 50:
                #print 'DOINGLE'
                self.vector[0] = self.vector[0] * -1.1
                self.scale *= 0.9
                self.vector[1] -= p2spin
        #print prevx, self.x, abs(pad2pos - self.y), 750-self.transformed.get_width()/2
        if self.x > 800:
            self.vector[0] = self.vector[0] * -1.1
            self.scale *= 0.9
        if self.x < 0:
            self.vector[0] = self.vector[0] * -1.1
            self.scale *= 0.9
        if self.y > 600:
            self.vector[1] = self.vector[1] * -1
        if self.y < 0:
            self.vector[1] = self.vector[1] * -1


    def draw(self, screen):
        self.transformed = pygame.transform.rotozoom(self.image, 0, self.scale)
        screen.blit(self.transformed,(self.x - self.transformed.get_width()/2,self.y - self.transformed.get_width()/2))


class pong:
    def __init__(self):
        self.p1 = player(self, 1, 50)
        self.p2 = player(self, 2, 750)
        self.ball = ball()

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                #print 'keydown'
                if event.key == K_w: 
                    self.p1.up = -5
                elif event.key == K_s: 
                    self.p1.down = 5
                elif event.key == K_UP:
                    self.p2.up = -5
                elif event.key == K_DOWN:
                    self.p2.down = 5
                elif event.key == K_a:
                    self.p1.spinmod = -1
                elif event.key == K_d:
                    self.p1.spinmod = 1
                elif event.key == K_LEFT:
                    self.p2.spinmod = 1
                elif event.key == K_RIGHT:
                    self.p2.spinmod = -1
            if event.type == KEYUP:
                if event.key == K_w: 
                    self.p1.up = 0
                elif event.key == K_s: 
                    self.p1.down = 0
                elif event.key == K_UP:
                    self.p2.up = 0
                elif event.key == K_DOWN:
                    self.p2.down = 0
                elif event.key == K_a:
                    self.p1.spinmod = 0
                elif event.key == K_d:
                    self.p1.spinmod = 0
                elif event.key == K_LEFT:
                    self.p2.spinmod = 0
                elif event.key == K_RIGHT:
                    self.p2.spinmod = 0
        self.p1.update()
        self.p2.update()
        self.ball.update(self.p1.paddlepos, self.p2.paddlepos, self.p1.spinmod, self.p2.spinmod)
        #print self.p1.paddlepos

class player:
    def __init__(self, game, playernum, xpos):
        self.playernum = playernum
        self.score = 0
        self.paddlepos = 400
        self.xpos = xpos
        self.up = 0
        self.down = 0
        self.spinmod = 0

    def update(self):
        joy1y = joy1.get_axis(1)
        print joy1y
        if joy1y < 0.2:
            if joy1y > -0.2:
                joy1y = 0
        print joy1y
        if self.playernum == 1:
            self.paddlepos += self.up + self.down + (joy1y*20)
        else:
            self.paddlepos += self.up + self.down
        self.paddlepos = min(550, max(self.paddlepos, 50))

    def draw(self, screen):
        pygame.draw.line(screen, (128,128,128),(self.xpos-self.spinmod,self.paddlepos+50),(self.xpos+self.spinmod,self.paddlepos-50),20)

def runforever():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            x,y = pygame.mouse.get_pos()
            x -= cur.get_width()/2
            y -= cur.get_height()/2
            screen.blit(cur, (x,y))
            for index in range(3):
                screen.blit(cur,(x+random.randrange(0,(index*50)+1),y))
            pygame.display.update()
            print event
            
def playpong():
    game = pong()
    while True:
        game.update()
        game.p1.draw(screen)
        game.p2.draw(screen)
        game.ball.draw(screen)
        pygame.time.Clock().tick(60)
        pygame.display.update()
        screen.fill((0,0,0))
playpong()