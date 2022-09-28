from plyfile import PlyData, PlyElement
import numpy as np
from tqdm import tqdm

plydata = PlyData.read('./L004.ply')
vertex_element = plydata['vertex']
vertex_element = [tuple(_)[:6] for _ in vertex_element]
length = len(vertex_element)
n = 2
step = (length // n) + 1
for i in tqdm(range(0, length, step)):
    vertex_element_i = vertex_element[i:i+step]
    np1 = np.asarray(vertex_element_i, dtype=[
                    ('x', 'f8'), ('y', 'f8'),  ('z', 'f8'),  ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')])
    el = PlyElement.describe(np1, 'vertex')
    filename = f'./{i // step}.ply'
    with open(filename, mode='wb') as f:
        PlyData([el], text=True).write(f)
