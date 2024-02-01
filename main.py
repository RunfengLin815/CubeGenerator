import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from args import Cube, Camera
from util import *
from model import *
from draw import *


if __name__ == "__main__":
    plot_size = [10, 10]
    views = [
        [30, -60],  # 默认
        [90, 0],  # 俯视
        [0, 0]  # 正视图
    ]

    cubes_size = [
        # 参照物
        [0.02, 0.03, 0.04],
        # 物体1
        [0.05, 0.05, 0.05]
    ]

    cubes_place = [
        # 参照物
        [0, 0, 0],
        # 物体1
        [0.2, 0.2, 0]
    ]

    cubes_angle = [
        # 参照物
        [0, 0, 0],
        # 物体1
        [0, 0, 30]
    ]

    # 设置相机位置、角度、焦距、分辨率
    camera_place = [1, 1, 0.5]
    # camera_place = [0.001, 0.001, 0.001]
    camera_angle = [90, -45, 0]
    # camera_angle = [0, 0, 0]
    # camera_angle = [90, 0, 0]
    camera = Camera(0.0036, [0.0036, 0.0024], [1920, 1080], camera_angle, camera_place)

    # 物体对象
    cubes = getCubes(cubes_place, cubes_size, cubes_angle)

    # 世界坐标
    vs = getCubesVs(cubes)
    print("vs:\n", vs)

    # draw3dscene(vs, "world scene", plot_size, [0, 1], views[0], camera)
    draw3dsceneByViews(vs, "world scene", plot_size, [0, 1], views, camera)

    # 相机坐标
    vs_h = getHs(vs)
    print("vs_h:\n", vs_h)

    rt = getReverseRotate(camera_angle)
    # rt = getRotationMatrix(camera_angle)
    trans1 = getTrans1(rt, camera_place)
    print("trans1:\n", trans1)

    vs_c = fromWorld2CameraV2(vs_h, trans1)
    print("vs_c:\n", vs_c)

    drawWorldScene(vs_c, "camera scene", plot_size, [-1, 1], views[0])

    # 图像
    trans2 = getTrans2(camera)
    print("trans2:\n", trans2)

    vs_i = fromCamera2Img(vs_c, trans2)
    print("vs_i:\n", vs_i)

    limit_2d = [-0.002, 0.002, -0.002, 0.002]
    # limit_2d = [-camera.reso[0], camera.reso[0], -camera.reso[1], camera.reso[1]]
    draw2dscene(vs_i, "img scene", plot_size, lim=limit_2d)

    # 像素坐标
    trans2 = getTrans2BK(camera)
    print("trans2:\n", trans2)

    vs_i = fromCamera2Img(vs_c, trans2)
    print("vs_i:\n", vs_i)

    # limit_2d = [-0.002, 0.002, -0.002, 0.002]
    limit_2d = [-camera.reso[0], camera.reso[0], -camera.reso[1], camera.reso[1]]
    draw2dscene(vs_i, "voxel scene", plot_size, lim=limit_2d)



    # # 像素
    # trans3 = getTrans3(camera)
    # print("trans3:\n", trans3)
    #
    # vs_i = fromCamera2Img(vs_c, trans3)
    # print("vs_i:\n", vs_i)
    #
    # limit_2d = [-0.002, 0.002, -0.002, 0.002]
    # draw2dscene(vs_i, "voxel scene", plot_size, lim=limit_2d)


    # 图像、像素一步到位
    # trans2 = getTrans2(camera)
    # print("trans2:\n", trans2)
    #
    # vs_v = fromCamera2Voxel(vs_c, trans2)
    # print("vs_v:\n", vs_v)
    # # draw2dscene(vs_v, "voxel scene", [0, 1920, 0, 1080])


    # # 世界
    # v_1 = get3dCoodinate(cube0)
    # print("v_1\n", v_1)
    #
    # for view in views:
    #     draw3d(v_1, "world scene", plot_size, [0, 1], view, camera)
    #
    # # 世界-相机
    # r_w2c = getRotationMatrix(camera.angle)
    # t_w2c = camera.place
    # v_c = fromWorld2Camera(v_1, r_w2c, t_w2c)
    # print("v_c\n", v_c)
    # draw3d(v_c, "camera scene", plot_size, [0, 2])
    #
    # # 相机-图像
    # v_i = fromCamera2Img(v_c, camera.f_len)
    # print("v_i\n", v_i)
    # # draw2d(v_i, "img scene", plot_size, [-0.01, 0.01, -0.01, 0.01])
    #
    # # 图像-像素
    # v_v = fromImg2VoxelNoUV(v_i, camera.sensor[0]/camera.reso[0],
    #                         camera.sensor[1]/camera.reso[1])
    # print("v_v\n", v_v)
    # reso = [0, 2*camera.reso[0], 0, 2*camera.reso[1]]
    # draw2d(v_v, "voxel scene", plot_size, [])

