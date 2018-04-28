import numpy as np
import matplotlib.pyplot as plt


class Board:
    
    def __init__(self, dimx, dimy, random= True, display= (10, 10)):
        self.x, self.y, self.count = dimx, dimy, 0
        self.dispx, self.dispy = display
        if random == False: self.board = np.zeros((dimx, dimy), dtype=bool)
        else: self.board = np.random.choice([True, False, False, False], (dimx, dimy))
        self.iterate_arr = np.zeros((dimx, dimy))
    
    def up(self, point):
        ptx, pty = point
        if pty - 1 < 0: return ptx, pty -1 + self.y
        else: return ptx, pty - 1
    
    def down(self, point):
        ptx, pty = point
        if pty + 1 >= self.y: return ptx, pty +1 - self.y
        else: return ptx, pty + 1
    
    def left(self, point):
        ptx, pty = point
        if ptx - 1 < 0: return ptx -1 + self.x, pty
        else: return ptx - 1, pty
    
    def right(self, point):
        ptx, pty = point
        if ptx + 1 >= self.x: return ptx +1 - self.x, pty
        else: return ptx + 1, pty
    
    def neighborhood(self, point):
        up, down, left, right = self.up, self.down, self.left, self.right
        return (up(left(point)),   up(point),    up(right(point)),
                left(point),       point,        right(point),
                down(left(point)), down(point),  down(right(point)))
    
    def add_neighborhood(self, point):
        surround = self.neighborhood(point)
        surround = surround[:4] + surround[5:]
        return sum([int(self.board[i]) for i in surround])
    
    def iterate(self):
        for i in range(self.x):
            for j in range(self.y):
                self.iterate_arr[(i, j)] = self.add_neighborhood((i, j))
                
        for i in range(self.x):
            for j in range(self.y):
                if self.board[(i, j)] == True and self.iterate_arr[(i, j)] < 2:
                    self.board[(i, j)] = False
                elif self.board[(i, j)] == True and self.iterate_arr[(i, j)] > 3:
                    self.board[(i, j)] = False
                elif self.board[(i, j)] == False and self.iterate_arr[(i, j)] == 3:
                    self.board[(i, j)] = True
    
    def display(self):
        global count
        count += 1
        self.dispx, self.dispy
        di_x, di_y = (self.x - self.dispx)/2, (self.y - self.dispy)/2
        array_img = self.board[int(di_x): int(di_x+ self.dispx), int(di_y): int(di_y+ self.dispy)]
        filesave = './imsave/name{}.png'.format(str(count).zfill(5))
        plt.imsave(filesave , array_img, cmap='gray')
        return filesave        
    
    def loopNdisplay(self, loop=10):
        self.files = []
        for i in range(loop):
            gameOfLife.iterate()
            self.files.append(gameOfLife.display())
        return self.files
        

gameOfLife = Board(100, 100, display=(100, 100))
gameOfLife.loopNdisplay(loop=100)
