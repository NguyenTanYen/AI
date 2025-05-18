import random
from collections import deque

def tao_trang_thai_ngau_nhien(trang_thai_dich):
    while True:
        trang_thai = [row[:] for row in trang_thai_dich]
        so_lan_hoan_doi = random.randint(2, 5)
        for _ in range(so_lan_hoan_doi):
            i1, j1 = random.randint(0, 2), random.randint(0, 2)
            i2, j2 = random.randint(0, 2), random.randint(0, 2)
            trang_thai[i1][j1], trang_thai[i2][j2] = trang_thai[i2][j2], trang_thai[i1][j1]
        
        phang = [trang_thai[i][j] for i in range(3) for j in range(3)]
        gan_gia_tri = {f'X{i+1}': phang[i] for i in range(9)}
        so_hoan_vi = dem_hoan_vi(gan_gia_tri)
        
        if so_hoan_vi % 2 == 0:
            return trang_thai

def dem_hoan_vi(gan_gia_tri):
    phang = [0] * 9
    for bien, gia_tri in gan_gia_tri.items():
        idx = int(bien[1:]) - 1
        phang[idx] = gia_tri
    
    cac_so = [num for num in phang if num != 0]
    so_hoan_vi = 0
    for i in range(len(cac_so)):
        for j in range(i + 1, len(cac_so)):
            if cac_so[i] > cac_so[j]:
                so_hoan_vi += 1
    return so_hoan_vi

def vi_pham_rang_buoc(trang_thai, trang_thai_dich):
    return trang_thai != trang_thai_dich

def chay_kiem_tra_thuat_toan(trang_thai_dich):
    da_tham = set()
    duong_di = []
    thong_tin_buoc = []
    buoc_toi_da = 100

    while len(duong_di) < buoc_toi_da:
        trang_thai_moi = tao_trang_thai_ngau_nhien(trang_thai_dich)
        trang_thai_tuple = tuple(tuple(row) for row in trang_thai_moi)
        if trang_thai_tuple in da_tham:
            continue
        
        da_tham.add(trang_thai_tuple)
        duong_di.append(trang_thai_moi)
        phang = [trang_thai_moi[i][j] for i in range(3) for j in range(3)]
        gan_gia_tri = {f'X{i+1}': phang[i] for i in range(9)}
        so_hoan_vi = dem_hoan_vi(gan_gia_tri)
        thong_tin_buoc.append(f"Thử trạng thái: {trang_thai_moi}, Hoán vị: {so_hoan_vi}")
        
        if not vi_pham_rang_buoc(trang_thai_moi, trang_thai_dich):
            return duong_di, thong_tin_buoc, len(duong_di)
        
        if len(duong_di) >= buoc_toi_da:
            return duong_di, thong_tin_buoc, len(duong_di)
    
    return duong_di, thong_tin_buoc, len(duong_di)