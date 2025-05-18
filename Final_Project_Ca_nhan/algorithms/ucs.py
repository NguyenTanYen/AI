import time
import heapq
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation

class UCSAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_queue_size = 0
        self.max_visited_size = 0

    def UCS(self, trang_thai_dau_vao):
        thoi_gian_bat_dau = time.perf_counter()

        hang_doi_uu_tien = []
        tap_da_tham = set()
        bang_cha = {}
        bang_chi_phi = {}
        trang_thai_so = int(trang_thai_dau_vao)
        heapq.heappush(hang_doi_uu_tien, (0, trang_thai_so))
        dem = 0
        bang_chi_phi[trang_thai_so] = 0

        while hang_doi_uu_tien:
            dem += 1
            if len(hang_doi_uu_tien) > self.max_queue_size:
                self.max_queue_size = len(hang_doi_uu_tien)

            chi_phi_hien_tai, trang_thai = heapq.heappop(hang_doi_uu_tien)

            if goalTest(trang_thai):
                duong_di = getPath(bang_cha, int(trang_thai_dau_vao))
                self.counter = dem
                self.path = duong_di
                self.cost = len(duong_di) - 1
                self.depth = len(duong_di) - 1
                self.time_taken = float(time.perf_counter() - thoi_gian_bat_dau)
                return (
                    self.path,
                    self.cost,
                    self.counter,
                    self.depth,
                    self.time_taken,
                    self.max_queue_size + self.max_visited_size,
                )

            if trang_thai not in tap_da_tham:
                tap_da_tham.add(trang_thai)
                if len(tap_da_tham) > self.max_visited_size:
                    self.max_visited_size = len(tap_da_tham)

                cac_con = getChildren(getStringRepresentation(trang_thai))
                for con in cac_con:
                    con_so = int(con)
                    chi_phi_moi = chi_phi_hien_tai + 1
                    # nếu đã từng duyệt rồi nhưng chi phí thấp hơn thì chấp nhận
                    if con_so not in tap_da_tham or chi_phi_moi < bang_chi_phi.get(
                        con_so, float("inf")
                    ):
                        heapq.heappush(hang_doi_uu_tien, (chi_phi_moi, con_so))
                        bang_cha[con_so] = trang_thai
                        bang_chi_phi[con_so] = chi_phi_moi

        self.time_taken = float(time.perf_counter() - thoi_gian_bat_dau)
        return None, 0, dem, self.depth, self.time_taken, self.max_queue_size + self.max_visited_size
