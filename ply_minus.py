from plyfile import PlyData, PlyElement
import numpy as np


def minus(tup):
    return (tup[0] - 627430, tup[1] - 4842790, tup[2] - 130, tup[3], tup[4], tup[5])
    

HEIGHT = 5
FILENAME = f'dwarf.ply'

plydata = PlyData.read('./0.ply')
vertex_element = plydata['vertex']
vertex_element = np.asarray(vertex_element)
vertex_element = [minus(_) for _ in vertex_element]

el = PlyElement.describe(np.asarray(vertex_element, dtype=[
    ('x', 'd'), ('y', 'd'),  ('z', 'd'),  ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')]), 'vertex')
with open(FILENAME, mode='wb') as f:
    PlyData([el], text=True).write(f)
