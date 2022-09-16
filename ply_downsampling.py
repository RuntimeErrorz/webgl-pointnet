import open3d as o3d 

pcd = o3d.io.read_point_cloud('../example/birmingham_block_2.ply')
downpcd = pcd.voxel_down_sample(voxel_size=0.05)
o3d.io.write_point_cloud("downsample.ply", pcd)