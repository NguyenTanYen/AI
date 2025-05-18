import time
import random
import math
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class SimulatedAnnealingAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_memory = 0

    def SimulatedAnnealing(self, trang_thai_dau_vao):
        thoi_gian_bat_dau = time.time()
        trang_thai_so = int(trang_thai_dau_vao)
        trang_thai_hien_tai = trang_thai_so
        bang_cha = {trang_thai_hien_tai: None}
        nhiet_do = 5000.0
        toc_do_giam = 0.995
        nhiet_do_nho_nhat = 0.01
        dem = 0

        heuristic_hien_tai = manhattanDistance(trang_thai_hien_tai)

        while nhiet_do > nhiet_do_nho_nhat:
            dem += 1

            if goalTest(trang_thai_hien_tai):
                duong_di = getPath(bang_cha, trang_thai_so)
                self.counter = dem
                self.path = duong_di
                self.cost = len(duong_di) - 1
                self.depth = len(duong_di) - 1
                self.time_taken = float(time.time() - thoi_gian_bat_dau)
                self.max_memory = max(self.max_memory, len(bang_cha))
                return self.path, self.cost, self.counter, self.depth, self.time_taken, self.max_memory
            
            cac_con = getChildren(getStringRepresentation(trang_thai_hien_tai))
            if not cac_con:
                break

            trang_thai_tiep = int(random.choice(cac_con))
            heuristic_tiep = manhattanDistance(trang_thai_tiep)
            delta_e = heuristic_tiep - heuristic_hien_tai

            if delta_e < 0 or random.random() < math.exp(-delta_e / nhiet_do):
                bang_cha[trang_thai_tiep] = trang_thai_hien_tai
                trang_thai_hien_tai = trang_thai_tiep
                heuristic_hien_tai = heuristic_tiep
                self.max_memory = max(self.max_memory, len(bang_cha))

            nhiet_do *= toc_do_giam

        self.counter = dem
        self.time_taken = float(time.time() - thoi_gian_bat_dau)
        self.max_memory = max(self.max_memory, len(bang_cha))
        return [], 0, self.counter, self.depth, self.time_taken, self.max_memory