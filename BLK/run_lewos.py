# 打开代码后，Tools 文件就在同目录下，所以不用设置 Tools 路径
from Tools.ReadPointCloud import *
import open3d as o3d
from Tools.Treeseg import WatershedSeg
from Tools.Down_Sample import *
from Tools.GroundSegment import *
from Tools.Clean import *
from Tools.Treeseg import *
from Tools.TLS2tree import TLSSeg,MergePoint
from lewos import lewos
import os
import numpy as np

# 点云数据路径
datapth = r".\Output\aboveground.pcd"
spth = r".\Output"

pcd = o3d.io.read_point_cloud(datapth)

# 如果运行吃力，可以再做一次抽析
# pcd = voxel_down_sample(pcd, voxel_size=0.04)

pts = np.array(pcd.points)

print(f"Number of points: {len(pts)}")

labels = lewos(pts, ft_threshold=0.125, paral=8)

wood = pts[labels == 1]
leaf = pts[labels == 0]

wood_pcd = o3d.geometry.PointCloud()
wood_pcd.points = o3d.utility.Vector3dVector(wood)

leaf_pcd = o3d.geometry.PointCloud()
leaf_pcd.points = o3d.utility.Vector3dVector(leaf)

print(f"Number of wood points: {len(wood)}")
print(f"Number of leaf points: {len(leaf)}")

o3d.io.write_point_cloud(os.path.join(spth, "wood.pcd"), wood_pcd)
o3d.io.write_point_cloud(os.path.join(spth, "leaf.pcd"), leaf_pcd)

leafwood = np.column_stack((pts, labels))
np.savetxt(
    os.path.join(spth, "leafwood.txt"),
    leafwood,
    fmt=["%.6f", "%.6f", "%.6f", "%d"],
    delimiter=" "
)
