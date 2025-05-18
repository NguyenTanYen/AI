import time
import heapq
from algorithms.common import goalTest, getPath, getChildren, getStringRepresentation, manhattanDistance

class BeamSearchAlgorithm:
    def __init__(self):
        self.counter = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.time_taken = 0
        self.max_memory = 0

    def BeamSearch(self, trang_thai_dau_vao, do_rong_chum=2):
        thoi_gian_bat_dau = time.time()
        trang_thai_so = int(trang_thai_dau_vao)
        hang_doi_uu_tien = [(manhattanDistance(trang_thai_so), 0, trang_thai_so)]
        tap_trang_thai_da_tham = set()
        bang_cha = {}
        bang_do_sau = {trang_thai_so: 0}
        dem = 0

        self.max_memory = len(hang_doi_uu_tien) + len(tap_trang_thai_da_tham) + len(bang_cha) + len(bang_do_sau)

        while hang_doi_uu_tien:
            dem += 1
            chum_hien_tai = []
            for _ in range(min(len(hang_doi_uu_tien), do_rong_chum)):
                if hang_doi_uu_tien:
                    chi_phi_h, do_sau, trang_thai = heapq.heappop(hang_doi_uu_tien)
                    if trang_thai not in tap_trang_thai_da_tham:
                        chum_hien_tai.append((chi_phi_h, do_sau, trang_thai))

            if not chum_hien_tai:
                break

            for _, do_sau, trang_thai in chum_hien_tai:
                if trang_thai in tap_trang_thai_da_tham:
                    continue
                tap_trang_thai_da_tham.add(trang_thai)

                if goalTest(trang_thai):
                    duong_di = getPath(bang_cha, trang_thai_so)
                    self.counter = dem
                    self.path = duong_di
                    self.cost = len(duong_di) - 1
                    self.depth = len(duong_di) - 1
                    self.time_taken = float(time.time() - thoi_gian_bat_dau)
                    self.max_memory = max(self.max_memory, len(hang_doi_uu_tien) + len(tap_trang_thai_da_tham) + len(bang_cha) + len(bang_do_sau))
                    return self.path, self.cost, self.counter, self.depth, self.time_taken, self.max_memory
                
                cac_con = getChildren(getStringRepresentation(trang_thai))
                chum_tiep_theo = []
                for con in cac_con:
                    con_so = int(con)
                    if con_so not in tap_trang_thai_da_tham:
                        chi_phi_h = manhattanDistance(con_so)
                        chum_tiep_theo.append((chi_phi_h, do_sau + 1, con_so))
                        bang_cha[con_so] = trang_thai
                        bang_do_sau[con_so] = do_sau + 1

                chum_tiep_theo.sort()
                for chi_phi_h, do_sau_moi, con_so in chum_tiep_theo[:do_rong_chum]:
                    heapq.heappush(hang_doi_uu_tien, (chi_phi_h, do_sau_moi, con_so))
                
                self.max_memory = max(self.max_memory, len(hang_doi_uu_tien) + len(tap_trang_thai_da_tham) + len(bang_cha) + len(bang_do_sau))

        self.counter = dem
        self.time_taken = float(time.time() - thoi_gian_bat_dau)
        self.max_memory = max(self.max_memory, len(hang_doi_uu_tien) + len(tap_trang_thai_da_tham) + len(bang_cha) + len(bang_do_sau))
        return [], 0, self.counter, self.depth, self.time_taken, self.max_memory