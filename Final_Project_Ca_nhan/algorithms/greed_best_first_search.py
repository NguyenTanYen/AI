import time
import heapq
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class GreedBestFirstSearchAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_pq_size = 0  
        self.max_visited_size = 0  

    def BestFirstSearch(self, trang_thai_dau_vao):
        thoi_gian_bat_dau = time.perf_counter()  
        hang_doi_uu_tien = []  
        tap_trang_thai_da_tham = set()
        bang_cha = {}
        bang_chi_phi = {}
        trang_thai_so = int(trang_thai_dau_vao)
        
        bang_cha[trang_thai_so] = None
        bang_chi_phi[trang_thai_so] = 0
        chi_phi_manhattan = manhattanDistance(trang_thai_so)
        heapq.heappush(hang_doi_uu_tien, (chi_phi_manhattan, trang_thai_so))
        
        while hang_doi_uu_tien:
            self.counter += 1

            if len(hang_doi_uu_tien) > self.max_pq_size:
                self.max_pq_size = len(hang_doi_uu_tien)

            if len(tap_trang_thai_da_tham) > self.max_visited_size:
                self.max_visited_size = len(tap_trang_thai_da_tham)

            _, trang_thai = heapq.heappop(hang_doi_uu_tien)
            if trang_thai in tap_trang_thai_da_tham:
                continue

            if goalTest(trang_thai):
                self.path = getPath(bang_cha, int(trang_thai_dau_vao))
                self.cost = len(self.path) - 1
                self.depth = len(self.path) - 1
                self.time_taken = time.perf_counter() - thoi_gian_bat_dau
                total_space = self.max_pq_size + self.max_visited_size
                return (self.path, self.cost, self.counter, self.depth, self.time_taken, total_space)
                
            tap_trang_thai_da_tham.add(trang_thai)
                       
            cac_con = getChildren(getStringRepresentation(trang_thai))
            for con in cac_con:
                con_so = int(con)
                if con_so not in tap_trang_thai_da_tham:
                    bang_chi_phi[con_so] = bang_chi_phi[trang_thai] + 1
                    chi_phi_moi = manhattanDistance(con_so)
                    heapq.heappush(hang_doi_uu_tien, (chi_phi_moi, con_so))
                    bang_cha[con_so] = trang_thai

        self.time_taken = time.perf_counter() - thoi_gian_bat_dau
        total_space = self.max_pq_size + self.max_visited_size
        return [], 0, self.counter, self.depth, self.time_taken, total_space