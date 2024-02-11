from const import *
from Game import Game

import pygame
import sys


class Window():
    def __init__(self):
        self.game = Game(ROW, COL)

        # 屏幕初始化
        pygame.init()
        self.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        # self.screen_size = pygame.display.get_desktop_sizes()[0]
        # self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('MineSweeper')

        # 计时
        self.clock = pygame.time.Clock()
        self.dt = 0

        # 计算棋盘的位置
        self.broad_shape = (ROW, COL)
        row, col = self.broad_shape[0], self.broad_shape[1]
        screen_row, screen_col = self.screen_size[1], self.screen_size[0]

        if col / row > screen_col / screen_row:
            self.block_size = int(screen_col / col)
        else:
            self.block_size = int(screen_row / row)

        self.origin_x, self.origin_y = (screen_col - self.block_size * col) / 2,\
                                       (screen_row - self.block_size * row) / 2

        # 可视化
        self.mark_block = []

    def show(self, visible_map, broad_map):
        self.screen.fill(pygame.Color("black"))

        assert self.broad_shape is not None
        assert visible_map is not None

        # 根据棋盘上的数字, 获得相应的图像并显示在屏幕上
        row, col = self.broad_shape[0], self.broad_shape[1]
        for i in range(row):
            for j in range(col):
                image = self.get_img(str(visible_map[i, j]), str(broad_map[i, j]))
                self.screen.blit(image, self.get_draw_index(j, i))

        pygame.display.update()

    def get_img(self, visible_flag: str, broad_flag: str, mask_flag=None):
        if mask_flag is not None:
            # TODO: 增添标记功能
            pass
        if VISIBLE_NO[visible_flag] != 'known':
            image = pygame.image.load(BLOCK_RES[VISIBLE_NO[visible_flag]])
        else:
            image = pygame.image.load(BLOCK_RES[MAP_NO[broad_flag]])

        image = pygame.transform.scale(image, (self.block_size, self.block_size))
        return image

    def run(self):
        while True:
            self.check_event()

            self.show(self.game.visible_map, self.game.mines_map)

            self.clock.tick(60)

    def get_block_index(self, x: int, y: int):
        block_x, block_y = (int((x - self.origin_x) // self.block_size),
                            int((y - self.origin_y) // self.block_size))
        if block_x < 0:
            block_x = 0
        elif block_x >= self.broad_shape[1]:
            block_x = self.broad_shape[1] - 1
        if block_y < 0:
            block_y = 0
        elif block_y >= self.broad_shape[0]:
            block_y = self.broad_shape[0] - 1

        return block_x, block_y

    def get_draw_index(self, x: int, y: int):
        return (self.origin_x + x * self.block_size,
                self.origin_y + y * self.block_size)

    def check_event(self):
        # 按键检测
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game.game_over:
                    continue
                pos = event.dict['pos']
                (block_col, block_row) = self.get_block_index(pos[0], pos[1])

                if event.dict['button'] == 1:
                    self.game.click_left(block_row, block_col)

                    # 记录下点击信息, 来判断双击事件
                    self.game.double_click_last_time = pygame.time.get_ticks()
                elif event.dict['button'] == 3:
                    self.game.click_right(block_row, block_col)
            elif event.type == pygame.KEYDOWN:
                if event.dict['unicode'] == 'r':
                    self.game.restart()


if __name__ == '__main__':
    window = Window()
    window.run()
