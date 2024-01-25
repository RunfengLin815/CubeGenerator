import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from util import *

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

def draw2dscene(cubes, name, size, lim=None):
    fig = plt.figure(figsize=(size[0], size[1]))
    ax = fig.add_subplot(111)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Cube Projection')
    # todo 写成ax的形式
    for v in cubes:
        for edge in edges:
            edge_x = [v[i, 0] for i in edge]
            edge_y = [v[i, 1] for i in edge]
            ax.plot([edge_x[0], edge_y[0]], [edge_x[1], edge_y[1]], 'k-')

    plt.show()


def draw3dscene(cubes, name, size, lim, view=None, camera=None):
    fig = plt.figure(figsize=(size[0], size[1]))
    ax = fig.add_subplot(111, projection='3d')

    # ax.view_init(elev=-90, azim=0)  # 俯视：仰角为-90度，方位角为0度
    # ax.view_init(elev=0, azim=0)  # 仰角为0度，方位角为0度
    # ax.view_init(elev=0, azim=90)  # 仰角为0度，方位角为90度

    if view:
        ax.view_init(elev=view[0], azim=view[1])

    plt.title(name)

    if lim:
        ax.set_xlim([lim[0], lim[1]])
        ax.set_ylim([lim[0], lim[1]])
        ax.set_zlim([lim[0], lim[1]])

    # 坐标轴箭头
    arrow_length = 1.0  # 箭头长度
    arrow_colors = ['r', 'g', 'b']  # 箭头颜色，对应xyz
    for i in range(3):
        arrow_direction = np.zeros(3)
        arrow_direction[i] = arrow_length
        ax.quiver(0, 0, 0, arrow_direction[0], arrow_direction[1], arrow_direction[2],
                  color=arrow_colors[i], arrow_length_ratio=0.1)

    # 相机
    if camera:
        ax.scatter(camera.place[0], camera.place[1], camera.place[2], color='green', s=100)

        # 计算相机坐标系中的单位向量
        camera_directions = np.eye(3) * arrow_length * 0.5  # X、Y、Z轴单位向量

        # 将单位向量根据相机旋转矩阵进行旋转
        camera_rotate = getRotationMatrix(camera.angle)
        rotated_directions = np.dot(camera_rotate, camera_directions.T).T

        # 绘制相机坐标系的三条坐标轴
        for i in range(3):
            ax.quiver(camera.place[0], camera.place[1], camera.place[2],
                      rotated_directions[i, 0], rotated_directions[i, 1], rotated_directions[i, 2],
                      color=arrow_colors[i], arrow_length_ratio=0.1)

    # 物体点
    for i_c in range(len(cubes)):
        for connection in edges:
            x1, y1, z1 = cubes[i_c][connection[0]]
            x2, y2, z2 = cubes[i_c][connection[1]]
            ax.plot3D([x1, x2], [y1, y2], [z1, z2], c='r', linewidth=2)

    plt.show()


def draw3d(v, name, size, lim, view=None, camera=None):
    fig = plt.figure(figsize=(size[0], size[1]))
    ax = fig.add_subplot(111, projection='3d')

    # ax.view_init(elev=-90, azim=0)  # 俯视：仰角为-90度，方位角为0度
    # ax.view_init(elev=0, azim=0)  # 仰角为0度，方位角为0度
    # ax.view_init(elev=0, azim=90)  # 仰角为0度，方位角为90度

    if view:
        ax.view_init(elev=view[0], azim=view[1])

    plt.title(name)

    if lim:
        ax.set_xlim([lim[0], lim[1]])
        ax.set_ylim([lim[0], lim[1]])
        ax.set_zlim([lim[0], lim[1]])

    # 绘制坐标原点处的红色点
    # ax.scatter(0, 0, 0, color='red', s=100)  # 坐标原点处的红色点

    # 绘制坐标轴的箭头
    arrow_length = 1.0  # 箭头长度
    arrow_colors = ['r', 'g', 'b']  # 箭头颜色，对应xyz

    for i in range(3):
        arrow_direction = np.zeros(3)
        arrow_direction[i] = arrow_length

        ax.quiver(0, 0, 0, arrow_direction[0], arrow_direction[1], arrow_direction[2],
                  color=arrow_colors[i], arrow_length_ratio=0.1)


    if camera:
        ax.scatter(camera.place[0], camera.place[1], camera.place[2], color='green', s=100)

        # 计算相机坐标系中的单位向量
        camera_directions = np.eye(3) * arrow_length * 0.5  # X、Y、Z轴单位向量

        # 将单位向量根据相机旋转矩阵进行旋转
        camera_rotate = getRotationMatrix(camera.angle)
        rotated_directions = np.dot(camera_rotate, camera_directions.T).T

        # 绘制相机坐标系的三条坐标轴
        for i in range(3):
            ax.quiver(camera.place[0], camera.place[1], camera.place[2],
                      rotated_directions[i, 0], rotated_directions[i, 1], rotated_directions[i, 2],
                      color=arrow_colors[i], arrow_length_ratio=0.1)

        # # 给每条坐标轴添加文本标签
        # label_offset = 0.05  # 调整标签的偏移量
        #
        # for i, label in enumerate(['X', 'Y', 'Z']):
        #     label_x = rotated_directions[i, 0] * arrow_length * 0.5 + camera.place[0] + label_offset
        #     label_y = rotated_directions[i, 1] * arrow_length * 0.5 + camera.place[1] + label_offset
        #     label_z = rotated_directions[i, 2] * arrow_length * 0.5 + camera.place[2] + label_offset
        #
        #     ax.text(label_x, label_y, label_z, label, color='black', fontsize=12)

    for connection in edges:
        x1, y1, z1 = v[connection[0]]
        x2, y2, z2 = v[connection[1]]
        ax.plot3D([x1, x2], [y1, y2], [z1, z2], c='r', linewidth=2)

    plt.show()

def draw2d(v, name, size, lim):
    plt.figure(figsize=(size[0], size[1]))
    # plt.scatter(v[:, 0], v[:, 1])
    plt.xlabel('u')
    plt.ylabel('v')
    if lim:
        plt.xlim([lim[0], lim[1]])
        plt.ylim([lim[2], lim[3]])
    plt.title(name)
    # 标记顶点序号
    # for i, (x, y) in enumerate(v):
    #     plt.annotate(str(i), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')
    for edge in edges:
        edge_x = [v[i, 0] for i in edge]
        edge_y = [v[i, 1] for i in edge]
        plt.plot(edge_x, edge_y, 'r')

    plt.show()

