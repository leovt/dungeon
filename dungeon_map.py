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


class DungeonMap:
    def vertex_data(self):
        map = ['111111',
               '133331',
               '133131',
               '111131',
               '133331',
               '111111'][::-1]
        for y, row in enumerate(map):
            for x, tid in enumerate(row):
                for tu, tv, u, v in vertex_coords[tid]:
                    yield from (x+u, y+v, 0, 1, tu, tv, 0, 0)
