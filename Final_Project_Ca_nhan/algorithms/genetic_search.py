import random
import time
from algorithms.common import goalTest, manhattanDistance

class GeneticAlgorithm:
    def __init__(self):
        self.counter = 0
        self.time_taken = 0
        self.path = []
        self.cost = 0
        self.depth = 0
        self.max_memory = 0

    @staticmethod
    def is_solvable(trang_thai):
        trang_thai = list(map(int, str(trang_thai)))
        so_nghich_the = 0
        for i in range(len(trang_thai)):
            for j in range(i + 1, len(trang_thai)):
                if trang_thai[i] != 0 and trang_thai[j] != 0 and trang_thai[i] > trang_thai[j]:
                    so_nghich_the += 1
        return so_nghich_the % 2 == 0

    def GeneticSearch(self, trang_thai_ban_dau, kich_thuoc_quan_the=100, so_the_he=1000, ti_le_dot_bien=0.2):
        thoi_gian_bat_dau = time.perf_counter()

        def tao_ca_the():
            while True:
                trang_thai = list(str(trang_thai_ban_dau))
                random.shuffle(trang_thai)
                ca_the = int("".join(trang_thai))
                if GeneticAlgorithm.is_solvable(ca_the):
                    return ca_the

        def sua_ca_the(ca_the):
            chu_so = list(map(int, str(ca_the)))
            thieu = [x for x in range(9) if x not in chu_so]
            trung = [x for x in chu_so if chu_so.count(x) > 1]
            for i in range(len(chu_so)):
                if chu_so[i] in trung:
                    chu_so[i] = thieu.pop(0)
                    trung.remove(chu_so[i])
            return int("".join(map(str, chu_so)))

        def ham_thich_nghi(trang_thai):
            diem_toi_da = 36
            return diem_toi_da - manhattanDistance(trang_thai)

        def lai_ghép(cha1, cha2):
            c1 = list(str(cha1))
            c2 = list(str(cha2))
            diem_cat = random.randint(1, len(c1) - 2)
            con = c1[:diem_cat] + [x for x in c2 if x not in c1[:diem_cat]]
            return sua_ca_the(int("".join(con)))

        def dot_bien(trang_thai):
            trang_thai = list(str(trang_thai))
            i, j = random.sample(range(len(trang_thai)), 2)
            trang_thai[i], trang_thai[j] = trang_thai[j], trang_thai[i]
            return sua_ca_the(int("".join(trang_thai)))

        quan_the = []
        da_co = set()
        da_co.add(trang_thai_ban_dau)
        quan_the.append(trang_thai_ban_dau)
        while len(quan_the) < kich_thuoc_quan_the:
            ca_the = tao_ca_the()
            if ca_the not in da_co:
                da_co.add(ca_the)
                quan_the.append(ca_the)

        ban_do_nhiem_sac_the = {trang_thai_ban_dau: [trang_thai_ban_dau]}
        for trang_thai in quan_the:
            if trang_thai != trang_thai_ban_dau:
                ban_do_nhiem_sac_the[trang_thai] = [trang_thai]

        diem_thich_nghi_tot_nhat = float('-inf')
        ca_the_tot_nhat = trang_thai_ban_dau
        dem_khong_cai_thien = 0

        for the_he in range(so_the_he):
            self.counter += 1
            quan_the = sorted(quan_the, key=ham_thich_nghi, reverse=True)
            if goalTest(quan_the[0]):
                self.solution = quan_the[0]
                self.time_taken = time.perf_counter() - thoi_gian_bat_dau
                self.path = ban_do_nhiem_sac_the[self.solution]
                self.cost = len(self.path) - 1
                self.depth = self.cost
                self.max_memory = max(self.max_memory, len(ban_do_nhiem_sac_the) + sum(len(v) for v in ban_do_nhiem_sac_the.values()))
                return self.path, self.cost, self.depth, self.counter, self.time_taken, self.max_memory
            
            diem_hien_tai = ham_thich_nghi(quan_the[0])
            if diem_hien_tai > diem_thich_nghi_tot_nhat:
                diem_thich_nghi_tot_nhat = diem_hien_tai
                ca_the_tot_nhat = quan_the[0]
                dem_khong_cai_thien = 0
            else:
                dem_khong_cai_thien += 1

            if dem_khong_cai_thien >= 20 or len(set(quan_the)) == 1:
                print("Không có sự cải thiện hoặc suy thoái dân số, dừng lại.")
                break

            the_he_tiep = quan_the[:kich_thuoc_quan_the // 4]  

            while len(the_he_tiep) < kich_thuoc_quan_the:
                kich_thuoc_tournament = 5
                tournament = random.sample(quan_the, min(kich_thuoc_tournament, len(quan_the)))
                cha1 = max(tournament, key=ham_thich_nghi)
                tournament = random.sample(quan_the, min(kich_thuoc_tournament, len(quan_the)))
                cha2 = max(tournament, key=ham_thich_nghi)
                while cha2 == cha1 and len(quan_the) > 1:
                    tournament = random.sample(quan_the, min(kich_thuoc_tournament, len(quan_the)))
                    cha2 = max(tournament, key=ham_thich_nghi)

                con = lai_ghép(cha1, cha2)
                if random.random() < ti_le_dot_bien:
                    con = dot_bien(con)

                the_he_tiep.append(con)
                if con not in ban_do_nhiem_sac_the:
                    ban_do_nhiem_sac_the[con] = ban_do_nhiem_sac_the[cha1] + [con]

                self.max_memory = max(self.max_memory, len(ban_do_nhiem_sac_the) + sum(len(v) for v in ban_do_nhiem_sac_the.values()))

            da_co = set()
            quan_the = []
            for ca_the in the_he_tiep:
                if ca_the not in da_co:
                    da_co.add(ca_the)
                    quan_the.append(ca_the)
            while len(quan_the) < kich_thuoc_quan_the:
                ca_the = tao_ca_the()
                if ca_the not in da_co:
                    da_co.add(ca_the)
                    quan_the.append(ca_the)
                    ban_do_nhiem_sac_the[ca_the] = [ca_the]
                self.max_memory = max(self.max_memory, len(ban_do_nhiem_sac_the) + sum(len(v) for v in ban_do_nhiem_sac_the.values()))

        self.time_taken = time.perf_counter() - thoi_gian_bat_dau
        if goalTest(ca_the_tot_nhat):
            self.solution = ca_the_tot_nhat
            self.path = ban_do_nhiem_sac_the[self.solution]
            self.cost = len(self.path) - 1
            self.depth = self.cost
            self.max_memory = max(self.max_memory, len(ban_do_nhiem_sac_the) + sum(len(v) for v in ban_do_nhiem_sac_the.values()))
            return self.path, self.cost, self.depth, self.counter, self.time_taken, self.max_memory
        self.max_memory = max(self.max_memory, len(ban_do_nhiem_sac_the) + sum(len(v) for v in ban_do_nhiem_sac_the.values()))
        return [], 0, 0, self.counter, self.time_taken, self.max_memory