import numpy as np
from Show import *

def get2DCoodi(thetas, xs, cube_size, t_vec, image_shape, f_len, sensor_size):
    image_width = image_shape[0]
    image_height = image_shape[1]
    f = f_len
    sensor = sensor_size
    u0 = image_width / 2
    v0 = image_height / 2
    dx = sensor[0] / image_width
    dy = sensor[1] / image_height

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

    # 放置
    vertices = vertices + np.array(t_vec)

    # x:0-1 y:0-3 z:0-4
    show3d1cube(vertices, 'cube')

    K_1 = np.array([[f, 0, 0],
                    [0, f, 0],
                    [0, 0, 1]])

    K_2 = np.array([[1 / dx, 0, u0],
                    [0, 1 / dy, v0],
                    [0, 0, 1]])

    # 拆分
    K_img2voxel_1 = np.array([[1 / dx, 0],
                              [0, 1 / dy]])
    K_img2voxel_2 = np.array([u0, v0])

    # 定义旋转角度和平移向量
    tX = thetas[0]  # 旋转角度X（单位：度）
    tY = thetas[1]  # 旋转角度Y（单位：度）
    tZ = thetas[2]  # 旋转角度Z（单位：度）
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(np.radians(tX)), -np.sin(np.radians(tX))],
                   [0, np.sin(np.radians(tX)), np.cos(np.radians(tX))]])
    Ry = np.array([[np.cos(np.radians(tY)), 0, np.sin(np.radians(tY))],
                   [0, 1, 0],
                   [-np.sin(np.radians(tY)), 0, np.cos(np.radians(tY))]])
    Rz = np.array([[np.cos(np.radians(tZ)), -np.sin(np.radians(tZ)), 0],
                   [np.sin(np.radians(tZ)), np.cos(np.radians(tZ)), 0],
                   [0, 0, 1]])
    R = np.dot(Rx, np.dot(Ry, Rz))

    # 【世界坐标】->【相机坐标】
    # 旋转
    v_camera = np.dot(vertices, R.T)
    # 平移
    for i in range(3):
        v_camera[:, i] += xs[i]

    # 【相机坐标】->【图像坐标】
    v_img = np.dot(v_camera, K_1.T)
    v_img = v_img[:, :] / v_img[:, 2:]

    # 【图像坐标】->【像素坐标】
    v_img_2d = v_img[:, :2]
    vertices_voxel_2d = np.dot(v_img_2d, K_img2voxel_1.T)

    return vertices_voxel_2d

