from plyfile import PlyData, PlyElement
import numpy as np
from tqdm import tqdm

plydata = PlyData.read('./threejs-vite/data/1.ply')
vertex_element = plydata['vertex']
length = len(vertex_element)
n = 10
step = (length // n) + 1

for i in tqdm(range(0, length, step)):
    vertex_element_i = vertex_element[i:i+step]
    np1 = np.asarray(vertex_element_i, dtype=[
                    ('x', 'd'), ('y', 'd'),  ('z', 'd'),  ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')])
    el = PlyElement.describe(np1, 'vertex')
    filename = f'./threejs-vite/data/division/{i // step}.ply'
    with open(filename, mode='wb') as f:
        PlyData([el], text=True).write(f)
