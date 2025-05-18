dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]


class Algorithm:
    def __init__(self):
        self.counter = 0  
        self.path = []   
        self.cost = 0     
        self.depth = 0    
        self.time_taken = 0  
        self.memory_size = 0  

    def get_metrics(self):
        return (self.path, self.cost, self.counter, self.depth, 
                self.time_taken, self.memory_size)

def getStringRepresentation(x):
    return str(x).zfill(9)

def goalTest(trang_thai):
    return trang_thai == 123456780

def getPath(bang_cha, trang_thai_bat_dau): 
    duong_di = []
    trang_thai_hien_tai = next((trang_thai for trang_thai, p in bang_cha.items() if goalTest(trang_thai)), None)
    if trang_thai_hien_tai is None:
        return [trang_thai_bat_dau]  
    while trang_thai_hien_tai is not None and trang_thai_hien_tai != trang_thai_bat_dau:
        duong_di.append(trang_thai_hien_tai)
        trang_thai_hien_tai = bang_cha.get(trang_thai_hien_tai)
    duong_di.append(trang_thai_bat_dau)
    return duong_di[::-1]

def getChildren(trang_thai):
    cac_con = []
    idx = trang_thai.index("0")
    i, j = divmod(idx, 3)
    for x in range(0, 4):
        nx = i + dx[x]
        ny = j + dy[x]
        vi_tri_moi = int(nx * 3 + ny)
        if checkValid(nx, ny):
            tam = list(trang_thai)
            tam[idx], tam[vi_tri_moi] = tam[vi_tri_moi], tam[idx]
            cac_con.append("".join(tam))
    return cac_con

def checkValid(i, j):
    if i >= 3 or i < 0 or j >= 3 or j < 0:
        return 0
    return 1

def manhattanDistance(trang_thai):
    trang_thai_str = getStringRepresentation(trang_thai)
    tong_khoang_cach = 0
    for i in range(9):
        if trang_thai_str[i] != "0":
            so_hien_tai = int(trang_thai_str[i])
            dich_x, dich_y = divmod(so_hien_tai - 1, 3)
            hien_tai_x, hien_tai_y = divmod(i, 3)
            tong_khoang_cach += abs(dich_x - hien_tai_x) + abs(dich_y - hien_tai_y)
    return tong_khoang_cach
