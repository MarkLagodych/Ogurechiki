import pygame as pg
import sys
import math
import random
import os
import shelve

pg.init()
prev=shelve.open(os.path.join('data', 'myfile'))
if 'a' in prev.keys():
    bests=prev['a']
else:
    bests=0

W=1000; H=700
eup=100
earthr = (0, H-eup, W, eup)
rusalkax=70; rusalkay=100
ruslifes=1000; bonus=0; score=0
right=False
maxbl=10

win = pg.display.set_mode((W, H))
pg.display.set_caption('ОгУрЕчИкИ')
font = pg.font.SysFont('consolas', 30)
smallfont = pg.font.SysFont('consolas', 20)

ballimage =  pg.image.load(os.path.join('data', 'basketball.png'))
stoneimage=  pg.image.load(os.path.join('data', 'stone.png'))
eyeimage  =  pg.image.load(os.path.join('data', 'eye.png'))
rusalka   =  pg.image.load(os.path.join('data', 'kk2.png'))
cucimage  =  pg.image.load(os.path.join('data', 'cucumber.png'))
userimage =  pg.image.load(os.path.join('data', 'user7.png'))
playimage =  pg.image.load(os.path.join('data', 'play.png'))
pauseimage = pg.image.load(os.path.join('data', 'pause.png'))
health =     pg.image.load(os.path.join('data', 'health.png'))

usermir=pg.transform.flip(userimage, True, False)

class User(object):
    def __init__(self):
        self.x=700
        self.y=80
        self.w=userimage.get_width()
        self.h=userimage.get_height()
        self.endl=rusalkay+rusalka.get_width()
        self.endr=900
        self.speed=5
        self.mov=False
    def draw(self):
        if self.mov:
            self._move(self.mov)
        win.blit(userimage, (self.x, self.y))
    def _move(self, direct):
        if direct==(-1,0) and self.x<=self.endl: return
        elif direct==(1,0) and self.x>=self.endr-self.w: return
        self.x += self.speed * direct[0]
        self.y += self.speed * direct[1]   
user=User()

class Ball(object):
    def __init__(self, image):
        global right
        self.im=image
        self.w = self.im.get_width()
        self.h = self.im.get_height()
        if not right:
                self.x=user.x+5
                self.y=user.y+70
        else:
            self.x=user.x+user.w-40
            self.y=user.y+70
        self.mode='bound'
        self.speed=8
        self.stone=False
        self.centre = (int(self.w/2)+self.x,  int(self.h/2)+self.y)
    def draw(self):
        global isstone
        if self.mode=='bound':
            if not right:
                self.x=user.x+5
                self.y=user.y+70
            else:
                self.x=user.x+user.w-40
                self.y=user.y+70
        elif self.mode=='fall':
            self.y+=self.speed
            
            if self.y>H-eup-self.h:
                return
                
        win.blit(self.im, (self.x, self.y))
        self.centre = (int(self.w/2)+self.x,  int(self.h/2)+self.y)
        newb.append(self)
           
bballs=[Ball(ballimage)]
newb=[]

class Cucumber(object):
    def __init__(self, x, y):
        self.im=cucimage
        self.w=self.im.get_width()
        self.h=self.im.get_height()
        self.x=x
        self.y=y
        self.speedx=2
        self.speedy=1
        self.centre = (int(self.w/2)+self.x,  int(self.h/2)+self.y)
    def draw(self):
        for b in bballs:
            d = math.sqrt((self.centre[0]-b.centre[0])**2 + (self.centre[1]-b.centre[1])**2)
            if abs(d)<26:
                if not b.stone:
                    del bballs[bballs.index(b)]
                    global bonus
                    bonus+=1
                return
        self.x-=self.speedx
        self.y-=self.speedy
        win.blit(self.im, (self.x, self.y))
        self.centre = (int(self.w/2)+self.x,  int(self.h/2)+self.y)
        if self.x > rusalkax + rusalka.get_width():
            newc.append(self)
        else:
            global ruslifes
            ruslifes-=3
            
cucums=[]
newc=[]

class Eye(object):
    def __init__(self):
        self.im=eyeimage
        self.x=950
        self.y=570
        self.w = eyeimage.get_width()
        self.h = eyeimage.get_height()
        self.speed=1
        self.centre = (int(self.w/2)+self.x,  int(self.h/2)+self.y)
        self.lifes=3
        self.cc=3
    def move(self):
        global ruslifes
        for b in bballs:
            d = math.sqrt((self.centre[0]-b.centre[0])**2 + (self.centre[1]-b.centre[1])**2)
            if abs(d)<26:
                if b.stone: self.lifes=1
                self.lifes-=1
                del bballs[bballs.index(b)]
        
        if self.x > rusalkax + rusalka.get_width() + 30:
            self.x-=self.speed
        else:
            ruslifes-=0.25

    def draw(self):
        global ruslifes, bonus, score
        if random.randint(0, 100)==50 and self.cc:
            newc.append(Cucumber(self.x, self.y))
            self.cc-=1
        self.move()
        win.blit(self.im, (self.x, self.y))
        self.centre = (int(self.w/2)+self.x,  int(self.h/2)+self.y)
        if self.lifes:
            newe.append(self)
        else:
            score+=1
            bonus+=13
eyes=[Eye()]
newe=[]
        
def game():
    global W, H, eup, earthr, rusalkax, rusalkay, ruslifes, bonus, score, \
           right, maxbl, user, bballs, newb, cucums, newc, eyes, newe, \
           usermir, userimage, stoneimage, ballimage, rusalka, eyeimage, \
           cucimage, playimage, pauseimage, health, Ball, Eye, Cucumber
    ruslifes=1000; bonus=0; score=0
    cucums=[]
    bballs=[Ball(ballimage)]
    eyes=[Eye()]
    bt=0
    run=True
    altdown=False
    spacedown=False
    stones=False
    paused=False
    while run:
        if random.randint(0,100)==50:
            eyes.append(Eye())          
        bt=(bt+1)%maxbl
        if bt==maxbl-1:
            myboolean=False
            for b in bballs:
                myboolean |= b.mode=='bound'
            if not myboolean:
                newb.append(Ball(ballimage))

        pg.time.delay(25)
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                run=False
            elif event.type == pg.KEYDOWN:

                if event.key == pg.K_LEFT:
                    user.mov=(-1,0)
                    if right:
                        userimage, usermir = usermir, userimage
                    right=False
                elif event.key == pg.K_RIGHT:
                    user.mov=(1,0)
                    if not right:
                        userimage, usermir = usermir, userimage
                    right=True

                elif event.key == pg.K_SPACE:
                    spacedown=True
                            
                elif event.key ==  pg.K_q:
                    if bonus>9 and ruslifes<1000:
                        bonus-=10; ruslifes+=10
                elif event.key == pg.K_w and bonus>4:
                    stones = not stones
                    for i in bballs:
                        if i.mode=='bound':
                            if stones:
                                i.im=stoneimage
                                i.stone=True
                                break
                            else:
                                i.im=ballimage
                                i.stone=False
                                break
                elif event.key == pg.K_p:
                    paused = not paused
                    pg.draw.rect(win, (43,173,206), (W-40, 20, 32, 32))
                    win.blit(playimage, (W-40, 20))
                        
                elif event.key in (pg.K_LALT, pg.K_RALT):
                    altdown=True
                elif event.key == pg.K_F4 and altdown==True:
                    run=False
            elif event.type == pg.KEYUP:
                if event.key in (pg.K_LALT, pg.K_RALT):
                    altdown=False
                elif event.key in (pg.K_LEFT, pg.K_RIGHT):
                    user.mov=False
                elif event.key==pg.K_SPACE:
                    spacedown=False
                    
        if not paused:
            if bonus>4 and stones:
                for i in bballs:
                    if i.mode=='bound' and not i.stone:
                        i.im=stoneimage
                        i.stone=True
                        bonus-=5
                        break

            if spacedown:
                if len(bballs)<5:
                    for i in bballs:
                        if i.mode=='bound':
                            i.mode='fall'
                            
            win.fill((43,173,206))
            
            pg.draw.rect(win, (100,100,100), earthr)
            pg.draw.line(win, (0,0,0), (user.endl, user.y+user.h), (user.endr, user.y+user.h), 2)
            
            win.blit(rusalka, (rusalkax, rusalkay))
            xright = rusalkax + int(rusalka.get_width() * ruslifes / 1000)
            pg.draw.line(win, (0,255,0), (rusalkax, rusalkay-20),
                         (xright, rusalkay-20), 10)
            pg.draw.line(win, (0,0,0), (rusalkax, rusalkay-10), (rusalkax, rusalkay-30), 3)
            pg.draw.line(win, (0,0,0), (rusalkax+rusalka.get_width(), rusalkay-10), (rusalkax+rusalka.get_width(), rusalkay-30), 3)
            text = smallfont.render('%s/1000'%int(ruslifes), True, (0,0,0))
            win.blit(text, (rusalkax, rusalkay-50))
            
            text = font.render('БОНУС: %s' % bonus, True, (25,200,0))
            win.blit(text, (550, 630))
            text = font.render('СЧЕТ: %s' % score, True, (25,200,0))
            win.blit(text, (800, 630))

            win.blit(pauseimage, (W-40, 20))
            win.blit(health, (rusalkax-42, rusalkay-32))

            if not stones:
                win.blit(ballimage, (50, 630))
            else:
                win.blit(stoneimage, (50, 630))
                
            user.draw()
            [c.draw() for c in cucums]
            [eye.draw() for eye in eyes]
            [bball.draw() for bball in bballs]

            if ruslifes<=0:
                run=False
            
            eyes=newe.copy()
            newe=[]
            bballs=newb.copy()
            newb=[]
            cucums=newc.copy()
            newc=[]
            
        pg.display.update()

altdown=False
while True:
    pg.time.delay(25)
    win.fill((0,0,0))
    
    text=font.render('Здравствуйте, уважаемый игрок!', True, (255,255,255))
    win.blit(text, (150,50))
    text=font.render('Предлагаю Вам спасти Русалку от беспощадных глаз.', True, (255,255,255))
    win.blit(text, (100,100))
    text=font.render('Нажмите Q для исцеления Русалки,', True, (255,255,255))
    win.blit(text, (100,150))
    text=font.render('нажимайте Пробел для скидывания мяча,', True, (255,255,255))
    win.blit(text, (100,200))
    text=font.render('кнопку W для переключения между мячем и камнем,', True, (255,255,255))
    win.blit(text, (100,250))
    text=font.render('стрелками управляйте персонажем,', True, (255,255,255))
    win.blit(text, (100,300))
    text=font.render('для паузы есть кнопка P.', True, (255,255,255))
    win.blit(text, (100,350))
    text=font.render('Когда надоест, нажмите Alt+F4', True, (255,255,255))
    win.blit(text, (100,400))
    text=font.render('Исцеление/сброс камня тратит бонус', True, (255,255,255))
    win.blit(text, (100,450))
    
    text=font.render('Нажмите Пробел для новой игры.', True, (255,255,255))
    win.blit(text, (100,550))
    
    text=font.render('Лучший результат: %s'%bests, True, (242,73,119), (0,70,26))
    win.blit(text, (100,600))
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            prev['a']=bests
            prev.close()
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key==pg.K_SPACE:
                game()
                if score>int(bests):
                    bests=score
            elif event.key in (pg.K_LALT, pg.K_RALT):
                altdown=True
            elif event.key == pg.K_F4 and altdown==True:
                prev['a']=bests
                prev.close()
                pg.quit()
                sys.exit()
        elif event.type == pg.KEYUP:
            if event.key in (pg.K_LALT, pg.K_RALT):
                altdown=False
    pg.display.update()
                 
pg.quit()
