import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from args import Cube, Camera
from util import *
from model import fromWorld2Camera, fromCamera2Img, fromImg2VoxelNoUV
from draw import *


if __name__ == "__main__":
    plot_size = [10, 10]
    views = [
        [30, -60],  # 默认
        [90, 0]  # 俯视
    ]

    # 生成模拟场景的世界坐标
    # 参照物方块
    cube_angle = [0, 0, 0]
    cube_lwh = [0.05, 0.05, 0.05]
    cube_place = [0, 0, 0]
    cube0 = Cube(cube_angle, cube_place, cube_lwh)

    # 设置相机位置、角度、焦距、分辨率
    camera_place = [0.5, 0.5, 0.5]
    camera_angle = [0, 0, 30]
    camera = Camera(0.0036, [0.0036, 0.0024], [1920, 1080], camera_angle, camera_place)

    # 世界
    v_1 = get3dCoodinate(cube0)
    print("v_1\n", v_1)

    for view in views:
        draw3d(v_1, "world scene", plot_size, [0, 1], view, camera)

    # 世界-相机
    r_w2c = getRotationMatrix(camera.angle)
    t_w2c = camera.place
    v_c = fromWorld2Camera(v_1, r_w2c, t_w2c)
    print("v_c\n", v_c)
    draw3d(v_c, "camera scene", plot_size, [0, 2])

    # 相机-图像
    v_i = fromCamera2Img(v_c, camera.f_len)
    print("v_i\n", v_i)
    draw2d(v_i, "img scene", plot_size, [-0.01, 0.01, -0.01, 0.01])

    # 图像-像素
    v_v = fromImg2VoxelNoUV(v_i, camera.sensor[0]/camera.reso[0],
                            camera.sensor[1]/camera.reso[1])
    print("v_v\n", v_v)
    # draw2d(v_v, "voxel scene", plot_size, [])

