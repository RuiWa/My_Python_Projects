### 06 显示敌机，敌机左右移动，抽取基类

import pygame
import time
from pygame.locals import *
import random

class Base(object):
    def __init__(self, screen_temp, x, y, img_name):
            self.x = x 
            self.y = y 
            self.screen = screen_temp
            self.img = pygame.image.load(img_name)
    
class BasePlane(Base):
    
        def __init__(self, screen_temp, x, y, img_name):
            Base.__init__(self, screen_temp, x, y, img_name)
            self.bullet_list = []
            
        def display(self):
            self.screen.blit(self.img, (self.x, self.y))
            for bullet in self.bullet_list:
                bullet.display()
                bullet.move()
                if bullet.judge():
                    self.bullet_list.remove(bullet)
            
class BaseBullet(Base):
        def __init__(self, screen_temp, x, y, img_name):
            Base.__init__(self, screen_temp, x, y, img_name)
        
        def display(self):
            self.screen.blit(self.img, (self.x, self.y))

#创建一个玩家飞机类
class HeroPlane(BasePlane):
    
    def __init__(self, screen_temp):        
        BasePlane.__init__(self, screen_temp, 190, 728, "./feiji/hero1.png")
        
    def move_left(self):
        self.x -= 5
        
    def move_right(self):
        self.x += 5
        
    def fire(self):
        self.bullet_list.append(Bullet(self.screen, self.x, self.y))
        

#创建一个子弹类
class Bullet(BaseBullet):
    
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x+40, y-20, "./feiji/bullet.png")
            
    def move(self):
        self.y -= 20
        
    def judge(self):
        if self.y < 0:
            return True
        return False
    
#创建一个敌机类
class EnemyPlane(BasePlane):
    
    def __init__(self, screen_temp):
        BasePlane.__init__(self, screen_temp, 0, 0, "./feiji/enemy0.png")
        self.direction = 'right'
        
    def fire(self):
        random_num = random.randint(1,30)
        if random_num == 8 or random_num == 18:
            self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y))
        
    def move(self):
        if self.direction == 'right':
            self.x += 30
        elif self.direction == 'left':
            self.x -= 30
        if self.x < 0:
            self.direction = 'right'
        elif self.x >430:
            self.direction ='left'
        
            
            
#创建一个敌机子弹类
class EnemyBullet(BaseBullet):
    
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x+20, y+30, "./feiji/bullet1.png")
            
    def move(self):
        self.y += 10
        
    def judge(self):
        if self.y > 820:
            return True
        return False
    
#键盘控制函数
def key_control(hero_temp):
        #获取事件，比如按键等
        for event in pygame.event.get():
            #判断是否是点击了退出按钮
            if event.type == QUIT:
                print("exit")
                exit()
            #判断是否是按下了键
            elif event.type == KEYDOWN:
                #检测按键是否是a或者left
                if event.key == K_a or event.key == K_LEFT:
                    print('left')
                    hero_temp.move_left()
                #检测按键是否是d或者right
                elif event.key == K_d or event.key == K_RIGHT:
                    print('right')
                    hero_temp.move_right()
                #检测按键是否是空格键
                elif event.key == K_SPACE:
                    print('space') 
                    hero_temp.fire()
                    
        
def main():
    #1. 创建窗口,窗口大小为480 * 852
    screen = pygame.display.set_mode((480,852),0,32)

    #2. 创建一个背景图片
    background = pygame.image.load("./feiji/background.png")
    
    #3. 创建一个玩家飞机
    hero = HeroPlane(screen)
    
    #4. 创建一个敌机
    enemy = EnemyPlane(screen)
    
    while True:
        screen.blit(background, (0,0))   
        hero.display()        
        enemy.display()        
        enemy.move()        
        enemy.fire()
        pygame.display.update()        
        key_control(hero)
        time.sleep(0.1)

if __name__ == '__main__':
        main()
