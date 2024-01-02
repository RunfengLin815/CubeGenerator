import numpy as np
import math

def rotate(point, theta, ax):
    p = point.copy()
    if ax == "x":
        p[1] = point[1]*math.cos(theta) - point[2]*math.sin(theta)
        p[2] = point[1]*math.sin(theta) + point[2]*math.cos(theta)
    elif ax == "y":
        p[0] = point[0]*math.cos(theta) + point[2]*math.sin(theta)
        p[2] = -point[0]*math.sin(theta) + point[2]*math.cos(theta)
    else:
        p[0] = point[0]*math.cos(theta) - point[1]*math.sin(theta)
        p[1] = point[0]*math.sin(theta) + point[1]*math.cos(theta)
    return p

def getRotationMatrix(angles):
    tX = angles[0]  # 旋转角度X（单位：度）
    tY = angles[1]  # 旋转角度Y（单位：度）
    tZ = angles[2]  # 旋转角度Z（单位：度）
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(np.radians(tX)), -np.sin(np.radians(tX))],
                   [0, np.sin(np.radians(tX)), np.cos(np.radians(tX))]])
    Ry = np.array([[np.cos(np.radians(tY)), 0, np.sin(np.radians(tY))],
                   [0, 1, 0],
                   [-np.sin(np.radians(tY)), 0, np.cos(np.radians(tY))]])
    Rz = np.array([[np.cos(np.radians(tZ)), -np.sin(np.radians(tZ)), 0],
                   [np.sin(np.radians(tZ)), np.cos(np.radians(tZ)), 0],
                   [0, 0, 1]])

    return np.dot(np.dot(Rx, Ry), Rz)


def get3dCoodinate(cube):
    # 根据尺寸获取原始三维坐标
    lwh = cube.lwh
    v = np.array([
        [0, 0, 0],
        [lwh[0], 0, 0],
        [lwh[0], lwh[1], 0],
        [0, lwh[1], 0],
        [0, 0, lwh[2]],
        [lwh[0], 0, lwh[2]],
        [lwh[0], lwh[1], lwh[2]],
        [0, lwh[1], lwh[2]]
    ]).astype(float)

    # 中心移动到原点，便于旋转
    v[:, 0] -= lwh[0]/2
    v[:, 1] -= lwh[1]/2
    v[:, 2] -= lwh[2]/2

    # 根据旋转和平移计算世界坐标
    r = getRotationMatrix(cube.angles)
    v = np.dot(v, r.T)

    # 移动回原位
    v[:, 0] += lwh[0]/2
    v[:, 1] += lwh[1]/2
    v[:, 2] += lwh[2]/2

    v = v + np.array(cube.disp)
    return v


def getK1(f):
    return np.array([[f, 0, 0, 0],
                     [0, f, 0, 0],
                     [0, 0, 1, 0]]).astype(float)


def getK2(dx, dy):
    return np.array([[1 / dx, 0],
                     [0, 1 / dy]])



def ifCube():
    # 定义六面体的8个顶点坐标
    vertices = np.array([
        [1.0, 1.0, 0.5],
        [0.96786062, 0.99073385, 0.53716448],
        [1.00616284, 0.98295863, 0.56834919],
        [1.03830222, 0.99222478, 0.5311847],
        [1.0, 1.04851479, 0.51209609],
        [0.96786062, 1.03924864, 0.54926058],
        [1.00616284, 1.03147342, 0.58044528],
        [1.03830222, 1.04073957, 0.5432808]
    ])

    # 计算六个面的法向量
    normals = []
    for i in range(6):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % 4]
        v3 = vertices[i + 4]
        normal = np.cross(v2 - v1, v3 - v1)
        normals.append(normal)

    # 检查边的长度是否相等
    edge_lengths = []
    for i in range(4):
        length = np.linalg.norm(vertices[i] - vertices[(i + 1) % 4])
        edge_lengths.append(length)

    # 检查角是否为直角
    angles = []
    for i in range(6):
        dot_product = np.dot(normals[i], normals[(i + 1) % 6])
        angle = np.degrees(np.arccos(dot_product))
        angles.append(angle)

    # 验证是否为长方体
    is_rectangular = all(np.isclose(edge_lengths, edge_lengths[0])) and all(np.isclose(angles, 90.0))

    if is_rectangular:
        print("这个六面体是长方体")
    else:
        print("这个六面体不是长方体")

def count11():
    points = np.array([
        [0.0072, 0.0072],
        [0.00648646, 0.00663976],
        [0.00637317, 0.00622619],
        [0.00703689, 0.00672461],
        [0.00702993, 0.00737099],
        [0.00634362, 0.00681151],
        [0.00624036, 0.00639734],
        [0.00688021, 0.00689636]
    ])

    # 初始化一个空的字典来存储边的长度
    edge_lengths = {}

    # 计算每一对点之间的边的长度
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            point1 = points[i]
            point2 = points[j]
            distance = np.linalg.norm(point1 - point2)  # 计算欧几里德距离
            edge_lengths[(i, j)] = distance

    # 打印每一对点之间的边的长度
    for edge, length in edge_lengths.items():
        point1_idx, point2_idx = edge
        print(f"边 ({point1_idx}, {point2_idx}) 的长度为: {length:.6f}")