from const import *
from utils import *

import random

import numpy as np
import pygame


class Game:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.size = self.row * self.col

        self.mines_map = np.zeros((self.row, self.col), dtype='int8')
        self.mines_num = round(float(self.size) / 50) * 10
        self.map_empty = True

        self.visible_map = np.zeros((self.row, self.col), dtype='int8')
        self.event_map = np.zeros((self.row, self.col), dtype='int8')

        self.mine_list = []

        # 事件处理
        self.double_click_last_time = pygame.time.get_ticks()

        self.game_over = False
        self.begin_time = 0

    def restart(self):
        self.__init__(self.row, self.col)

    def generate_map(self, click_point: tuple[int, int]):
        # 在点击的瞬间生成地图. 生成时, 先生成雷, 再生成数字
        self.put_mines(click_point)
        self.make_num()

    def make_num(self):
        for (row, col) in self.mine_list:
            for cur_row, cur_col in self.around_block(row, col):
                if self.mines_map[cur_row, cur_col] != int(MAP_NO['mine']):
                    self.mines_map[cur_row, cur_col] += 1

    def put_mines(self, click_point: tuple[int, int]):
        for i in range(self.mines_num):
            row = random.randint(0, self.row - 1)
            col = random.randint(0, self.col - 1)
            while (row, col) in self.mine_list or is_around(click_point, (row, col)):
                row = random.randint(0, self.row - 1)
                col = random.randint(0, self.col - 1)

            self.put_mine(row, col)

    def put_mine(self, row: int, col: int):
        self.mines_map[row, col] = int(MAP_NO['mine'])
        self.mine_list.append((row, col))

    def click_left(self, block_row: int, block_col: int):
        assert 0 <= block_row < self.row
        assert 0 <= block_col < self.col

        double_click = (self.double_click_last_time is not None) \
                       and (pygame.time.get_ticks() - self.double_click_last_time < 300)

        if double_click:
            self.find_around(block_row, block_col)
        else:
            # 在第一次点击的时候生成地图
            if self.map_empty:
                self.generate_map((block_row, block_col))
                self.map_empty = False
                self.begin_time = pygame.time.get_ticks()
                self.visible_map[block_row, block_col] = int(VISIBLE_NO['known'])
                self.BFS_expand(block_row, block_col)
            else:
                self.click_block(block_row, block_col)

    def click_right(self, block_row: int, block_col: int):
        assert 0 <= block_row < self.row
        assert 0 <= block_col < self.col
        if self.visible_map[block_row, block_col] != int(VISIBLE_NO['known']):
            self.visible_map[block_row, block_col] += 1
            self.visible_map[block_row, block_col] %= VISIBLE_NO['max']

    def double_click(self, block_row: int, block_col: int):
        self.find_around(block_row, block_col)

    def click_block(self, block_row: int, block_col: int):
        if self.visible_map[block_row, block_col] == int(VISIBLE_NO['unknown']):
            self.visible_map[block_row, block_col] = int(VISIBLE_NO['known'])

            if self.mines_map[block_row, block_col] == int(MAP_NO['0']):
                self.BFS_expand(block_row, block_col)

            if self.mines_map[block_row, block_col] == int(MAP_NO['mine']):
                self.mines_map[block_row, block_col] = int(MAP_NO['boom'])

                self.show_map()

                self.game_over = True
                print("你失败了. 按r重新开始")

    def show_map(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.mines_map[i, j] == int(MAP_NO['mine']):
                    self.visible_map[i, j] = int(VISIBLE_NO['known'])

    def check_win(self):
        num = 0
        for i in range(self.row):
            for j in range(self.col):
                if self.visible_map[i, j] == int(VISIBLE_NO['known']) \
                        or self.visible_map[i, j] == int(VISIBLE_NO['known']):
                    num += 1
        if num == self.size:
            time = (pygame.time.get_ticks() - self.begin_time) / 1000
            print("你赢了! 用时" + str(time) + "秒")
            print("按r重新开始")

    def around_block(self, row: int, col: int):
        return around_block(row, col, 0, self.row - 1, 0, self.col - 1)

    def check_around(self, row: int, col: int):
        num = 0
        for (cur_row, cur_col) in self.around_block(row, col):
            if self.visible_map[cur_row, cur_col] == int(VISIBLE_NO['flag']):
                num += 1
        if num == self.mines_map[row, col]:
            return True
        else:
            return False

    def find_around(self, row, col):
        if not self.check_around(row, col):
            return
        for cur_row, cur_col in self.around_block(row, col):
            self.click_block(cur_row, cur_col)

    def BFS_expand(self, row: int, col: int):
        black = []
        gray = [(row, col)]
        while len(gray) > 0:
            current = gray.pop()
            for row, col in self.around_block(current[0], current[1]):
                if self.visible_map[row, col] != int(VISIBLE_NO['unknown']):
                    continue
                if self.mines_map[row, col] == int(MAP_NO['0']):
                    if (row, col) not in black:
                        gray.append((row, col))
                        self.visible_map[row, col] = VISIBLE_NO['known']
                elif self.mines_map[row, col] != int(MAP_NO['mine']):
                    self.visible_map[row, col] = VISIBLE_NO['known']
            black.append(current)


if __name__ == '__main__':
    game = Game(ROW, COL)
