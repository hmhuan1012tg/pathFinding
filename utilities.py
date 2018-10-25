import os
import time
import search_map 
import grid
import functools 

class Utilities:
    @staticmethod
    def create_grid(row_num, col_num, default_value):
        a_grid = []
        for row in range(0, row_num):
            a_row = []
            for col in range(0, col_num):
                item = grid.GridItem()
                item.push(default_value)
                a_row.append(item)
            a_grid.append(a_row)
        return a_grid
    
    @staticmethod
    def create_map(size, default_value):
        matrix = []
        for row in range(size):
            a_row = []
            for col in range(size):
                a_row.append(default_value)
            matrix.append(a_row)
        map = search_map.Map()
        map.map = matrix
        map.size = size
        return map

    @staticmethod
    def create_matrix(size, default_value):
        matrix = []
        for row in range(size):
            a_row = []
            for col in range(size):
                a_row.append(default_value)
            matrix.append(a_row)
        return matrix

def timeit(func):
    @functools.wraps(func)
    def timed(*args, **kwargs):
        timestart = time.time()
        result = func(*args, **kwargs)
        timeend = time.time()

        timed.time_elapsed = float((timeend - timestart) * 1000)
        print("{} runs in  {:.2f} milliseconds".format(func.__name__, (timeend - timestart) * 1000))
        
        return result
    return timed