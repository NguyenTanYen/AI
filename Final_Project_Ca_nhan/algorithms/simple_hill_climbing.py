import time
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class SimpleHillClimbingAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_visited_size = 0

    def SimpleHillClimbing(self, trang_thai_dau_vao):
        thoi_gian_bat_dau = time.time()
        trang_thai_so = int(trang_thai_dau_vao)
        trang_thai_hien_tai = trang_thai_so
        bang_cha = {}
        tap_da_tham = set()
        dem = 0
        do_sau = 0

        while True:
            dem += 1
            tap_da_tham.add(trang_thai_hien_tai)

            if len(tap_da_tham) > self.max_visited_size:
                self.max_visited_size = len(tap_da_tham)

            if goalTest(trang_thai_hien_tai):
                duong_di = getPath(bang_cha, trang_thai_so)
                self.counter = dem
                self.path = duong_di
                self.cost = len(duong_di) - 1
                self.depth = len(duong_di) - 1
                self.time_taken = float(time.time() - thoi_gian_bat_dau)
                return self.path, self.cost, self.counter, self.depth, self.time_taken, self.max_visited_size
            
            cac_con = getChildren(getStringRepresentation(trang_thai_hien_tai))
            con_tot_nhat = None
            heuristic_tot_nhat = manhattanDistance(trang_thai_hien_tai)

            for con in cac_con:
                con_so = int(con)
                if con_so not in tap_da_tham:
                    heuristic = manhattanDistance(con_so)
                    if heuristic < heuristic_tot_nhat:
                        heuristic_tot_nhat = heuristic
                        con_tot_nhat = con_so
            
            if con_tot_nhat is None:
                self.counter = dem
                self.depth = do_sau
                self.time_taken = float(time.time() - thoi_gian_bat_dau)
                return [], 0, self.counter, self.depth, self.time_taken, self.max_visited_size

            bang_cha[con_tot_nhat] = trang_thai_hien_tai
            trang_thai_hien_tai = con_tot_nhat
            do_sau += 1