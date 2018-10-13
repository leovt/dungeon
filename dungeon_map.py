tiles = {
    '1': (0,0),
    '3': (2,0)
}

tex_tiles = 8.0

tri_coords = [(0,0), (1,0), (0,1), (1,0), (1,1), (0,1)]

vertex_coords = {
    tid: [((x+u)/tex_tiles, (y+1-v)/tex_tiles, u, v)
          for (u,v) in tri_coords]
    for tid, (x,y) in tiles.items()
}

import random
def gen_map():
    map = [['1']*40 for y in range(40)]
    for r in range(20):
        w = random.randrange(3, 12)
        h = random.randrange(3, 12)
        x = random.randrange(1,39-w)
        y = random.randrange(1,39-h)
        if all(map[u][v] == '1' for u in range(x-1, x+w+1) for v in range(y-1, y+h+1)):
             for u in range(x, x+w):
                 for v in range(y, y+h):
                     map[u][v] = '3'
    return map



class DungeonMap:
    def __init__(self):
        self.map = gen_map()

    def vertex_data(self):
        for y, row in enumerate(self.map):
            for x, tid in enumerate(row):
                for tu, tv, u, v in vertex_coords[tid]:
                    yield from (x+u, y+v, 0, 1, tu, tv, 0, 0)
