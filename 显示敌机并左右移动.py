### 06 显示敌机，敌机左右移动

import pygame
import time
from pygame.locals import *
import random

#创建一个玩家飞机类
class HeroPlane(object):
    
    def __init__(self, screen_temp):
        self.x = 190
        self.y = 728
        self.screen = screen_temp
        self.img = pygame.image.load("./feiji/hero1.png")
        self.bullet_list = []
        
    def display(self):
        self.screen.blit(self.img, (self.x, self.y))
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge():
                self.bullet_list.remove(bullet)
        
    def move_left(self):
        self.x -= 5
        
    def move_right(self):
        self.x += 5
        
    def fire(self):
        self.bullet_list.append(Bullet(self.screen, self.x, self.y))
        

#创建一个子弹类
class Bullet(object):
    
    def __init__(self, screen_temp, x, y):
        self.x = x + 40
        self.y = y - 20
        self.screen = screen_temp
        self.img = pygame.image.load("./feiji/bullet.png")
        
    def display(self):
        self.screen.blit(self.img, (self.x, self.y))
            
    def move(self):
        self.y -= 20
        
    def judge(self):
        if self.y < 0:
            return True
        return False
    
#创建一个敌机类
class EnemyPlane(object):
    
    def __init__(self, screen_temp):
        self.x = 0
        self.y = 0
        self.screen = screen_temp
        self.img = pygame.image.load("./feiji/enemy0.png")
        self.direction = 'right'
        self.enemy_bullet_list = []
        
    def display(self):
        self.screen.blit(self.img, (self.x, self.y))
        for enemy_bullet in self.enemy_bullet_list:
            enemy_bullet.display()
            enemy_bullet.move()
            if enemy_bullet.judge():
                self.enemy_bullet_list.remove(enemy_bullet)
        
    def fire(self):
        random_num = random.randint(1,30)
        if random_num == 8 or random_num == 18:
            self.enemy_bullet_list.append(EnemyBullet(self.screen, self.x, self.y))
        
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
class EnemyBullet(object):
    
    def __init__(self, screen_temp, x, y):
        self.x = x + 20
        self.y = y + 30
        self.screen = screen_temp
        self.img = pygame.image.load("./feiji/bullet1.png")
        
    def display(self):
        self.screen.blit(self.img, (self.x, self.y))
            
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
