from plyfile import PlyData, PlyElement
import numpy as np

HEIGHT = 5
FILENAME = f'dwarf.ply'

plydata = PlyData.read('./threejs-vite/data/1.ply')
vertex_element = plydata['vertex']
vertex_element = np.asarray(vertex_element)
vertex_element = [_ for _ in vertex_element if _[2] < HEIGHT]

el = PlyElement.describe(np.asarray(vertex_element, dtype=[
    ('x', 'd'), ('y', 'd'),  ('z', 'd'),  ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')]), 'vertex')
with open(FILENAME, mode='wb') as f:
    PlyData([el], text=True).write(f)
