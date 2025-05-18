import time
import heapq
from algorithms.common import Algorithm, goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance


class AStarAlgorithm(Algorithm):
    def __init__(self):
        super().__init__()
        self.max_queue_size = 0
        self.max_visited_size = 0

    def AStar(self, trang_thai_dau_vao):
        thoi_gian_bat_dau = time.perf_counter()

        hang_doi_uu_tien = []
        tap_trang_thai_da_tham = set()
        bang_cha = {}
        bang_chi_phi = {}
        trang_thai_so = int(trang_thai_dau_vao)
        
        chi_phi_g = 0
        chi_phi_h = manhattanDistance(trang_thai_so)
        chi_phi_f = chi_phi_g + chi_phi_h
        heapq.heappush(hang_doi_uu_tien, (chi_phi_f, trang_thai_so, chi_phi_g))
        bang_chi_phi[trang_thai_so] = 0

        while hang_doi_uu_tien:
            self.counter += 1

            if len(hang_doi_uu_tien) > self.max_queue_size:
                self.max_queue_size = len(hang_doi_uu_tien)

            if len(tap_trang_thai_da_tham) > self.max_visited_size:
                self.max_visited_size = len(tap_trang_thai_da_tham)

            chi_phi_f, trang_thai, chi_phi_g = heapq.heappop(hang_doi_uu_tien)

            if trang_thai in tap_trang_thai_da_tham:
                continue

            if goalTest(trang_thai):
                self.path = getPath(bang_cha, int(trang_thai_dau_vao))
                self.cost = len(self.path) - 1
                self.depth = bang_chi_phi[trang_thai]
                self.time_taken = time.perf_counter() - thoi_gian_bat_dau
                self.memory_size = self.max_queue_size + self.max_visited_size
                return self.get_metrics()

            tap_trang_thai_da_tham.add(trang_thai)

            cac_con = getChildren(getStringRepresentation(trang_thai))
            for con in cac_con:
                con_so = int(con)
                if con_so not in tap_trang_thai_da_tham:
                    chi_phi_g_moi = chi_phi_g + 1
                    chi_phi_h = manhattanDistance(con_so)
                    chi_phi_f = chi_phi_g_moi + chi_phi_h
                    heapq.heappush(hang_doi_uu_tien, (chi_phi_f, con_so, chi_phi_g_moi))
                    bang_cha[con_so] = trang_thai
                    bang_chi_phi[con_so] = chi_phi_g_moi

        self.time_taken = time.perf_counter() - thoi_gian_bat_dau
        self.memory_size = self.max_queue_size + self.max_visited_size
        return self.get_metrics()