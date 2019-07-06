#02 创建玩家飞机

import pygame
import time

def main():
    #1. 创建窗口,窗口大小为480 * 852
    screen = pygame.display.set_mode((480,852),0,32)

    #2. 创建一个背景图片
    background = pygame.image.load("./feiji/background.png")
    
    #3. 创建一个玩家飞机
    hero = pygame.image.load("./feiji/hero1.png")

    while True:
        screen.blit(background, (0,0))
        
        screen.blit(hero, (190,728))

        pygame.display.update()

        time.sleep(0.1)

if __name__ == '__main__':
        main()
