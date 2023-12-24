import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from args import Cube, Camera
from util import get3dCoodinate, getRotationMatrix
from model import fromWorld2Camera, fromCamera2Img, fromImg2VoxelNoUV
from draw import draw3d, draw2d


def test1(thetas, xs, cube_size, image_size, f_len, sensor_size):
    # 参数
    image_width = image_size[0]
    image_height = image_size[1]
    f = f_len
    sensor = sensor_size
    u0 = image_width / 2
    v0 = image_height / 2
    dx = sensor[0] / image_width
    dy = sensor[1] / image_height
    print("u0, v0:\n", u0, v0)
    print("dx, dy:\n", dx, dy)

    # 坐标
    cube_l = cube_size[0]
    cube_w = cube_size[1]
    cube_h = cube_size[2]
    vertices = np.array([
        [0, 0, 0],
        [cube_l, 0, 0],
        [cube_l, cube_w, 0],
        [0, cube_w, 0],
        [0, 0, cube_h],
        [cube_l, 0, cube_h],
        [cube_l, cube_w, cube_h],
        [0, cube_w, cube_h]
    ]).astype(float)

    # vertices = np.array([
    #     (1, 1, 1),  # 0
    #     (3, 1, 1),  # 1
    #     (3, 3, 1),  # 2
    #     (1, 3, 1),  # 3
    #     (1, 1, 2),  # 4
    #     (3, 1, 2),  # 5
    #     (3, 3, 2),  # 6
    #     (1, 3, 2)  # 7
    # ])

    print("世界坐标系:\n", vertices)

    # 定义相机内参矩阵
    focalLength = [f / dx, f / dy]  # fx, fy
    principalPoint = [u0, v0]  # u, v

    K_actual_h = np.array([[focalLength[0], 0, principalPoint[0], 0],
                           [0, focalLength[1], principalPoint[1], 0],
                           [0, 0, 1, 0]])
    print("K_actual_h\n", K_actual_h)

    K_1 = np.array([[f, 0, 0],
                    [0, f, 0],
                    [0, 0, 1]])
    print("K1:\n", K_1)

    K_2 = np.array([[1 / dx, 0, u0],
                    [0, 1 / dy, v0],
                    [0, 0, 1]])
    print("K2:\n", K_2)

    # 拆分版
    K_img2voxel_1 = np.array([[1 / dx, 0],
                              [0, 1 / dy]])
    K_img2voxel_2 = np.array([u0, v0])

    # 定义旋转角度和平移向量
    thetaX = thetas[0]  # 旋转角度X（单位：度）
    thetaY = thetas[1]  # 旋转角度Y（单位：度）
    thetaZ = thetas[2]  # 旋转角度Z（单位：度）
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(np.radians(thetaX)), -np.sin(np.radians(thetaX))],
                   [0, np.sin(np.radians(thetaX)), np.cos(np.radians(thetaX))]])
    Ry = np.array([[np.cos(np.radians(thetaY)), 0, np.sin(np.radians(thetaY))],
                   [0, 1, 0],
                   [-np.sin(np.radians(thetaY)), 0, np.cos(np.radians(thetaY))]])
    Rz = np.array([[np.cos(np.radians(thetaZ)), -np.sin(np.radians(thetaZ)), 0],
                   [np.sin(np.radians(thetaZ)), np.cos(np.radians(thetaZ)), 0],
                   [0, 0, 1]])
    R = np.dot(Rx, np.dot(Ry, Rz))
    print("R:\n", R)

    # 【世界坐标】->【相机坐标】
    # 旋转
    v_camera = np.dot(vertices, R.T)
    # 平移
    for i in range(3):
        v_camera[:, i] += xs[i]
    print("相机坐标系3D:\n", v_camera)
    show3d1cube(v_camera, 'camera sys')

    # 【相机坐标】->【图像坐标】
    v_img = np.dot(v_camera, K_1.T)
    v_img = v_img[:, :] / v_img[:, 2:]  # 归一化
    print("图像坐标系2D(齐次):\n", v_img)
    showImg(v_img[:, :2], 'image sys')

    # 【图像坐标】->【像素坐标】
    # vertices_voxel = np.dot(v_img, K_2.T)
    v_img_2d = v_img[:, :2]
    print("图像坐标系2D:\n", v_img_2d)

    vertices_voxel_2d = np.dot(v_img_2d, K_img2voxel_1.T)
    print("像素坐标系(放缩):\n", np.rint(vertices_voxel_2d))
    showImg(vertices_voxel_2d, 'voxel sys')

    # 这个平移可有可无吧

    # print("像素坐标系(平移):\n", vertices_voxel)
    # showImg(vertices_voxel[:, :2], 'voxel sys')
    # showImgLimit(vertices_voxel[:, :2], 'voxel sys', image_size)


if __name__ == "__main__":
    plot_size = [10, 10]

    # 生成模拟场景的世界坐标
    cube1 = Cube([0, 0, 30], [0.4, 0.2, 0.025], [0.05, 0.05, 0.05])
    cube0 = Cube([0, 0, 0], [0.0, 0.0, 0.025], [0.05, 0.05, 0.05])
    # v_1 = get3dCoodinate(cube1)
    v_1 = get3dCoodinate(cube0)
    print("v_1\n", v_1)
    draw3d(v_1, "world scene", plot_size, [])

    # 设置相机位置、角度、焦距、分辨率
    camera = Camera(0.0036, [0.0036, 0.0024], [1920, 1080], [-76, 0, -130], [1, 1, 0.5])

    # 世界-相机
    r_w2c = getRotationMatrix(camera.angle)
    t_w2c = camera.place
    v_c = fromWorld2Camera(v_1, r_w2c, t_w2c)
    print("v_c\n", v_c)
    draw3d(v_c, "camera scene", plot_size, [])

    # 相机-图像
    v_i = fromCamera2Img(v_c, camera.f_len)
    print("v_i\n", v_i)
    draw2d(v_i, "img scene", plot_size, [])

    # 图像-像素
    v_v = fromImg2VoxelNoUV(v_i, camera.sensor[0]/camera.reso[0],
                            camera.sensor[1]/camera.reso[1])
    print("v_v\n", v_v)
    draw2d(v_v, "voxel scene", plot_size, camera.reso)

