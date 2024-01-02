import numpy as np
import matplotlib.pyplot as plt
import args

from util import getK1, getK2


def fromWorld2Camera(v_w, r, t):
    # 类型转换
    if isinstance(t, np.ndarray):
        pass
    else:
        t = np.array(t)

    # 转换为齐次坐标
    # v_w = np.hstack((v_w, np.ones((v_w.shape[0], 1))))
    # print("v_w\n", v_w)
    # # 变换矩阵
    # print("r\n", r)
    # print("t\n", t)
    # r = np.vstack((r, np.zeros((1, 3))))
    # t = np.vstack((t.reshape(3, 1), 1))
    # trans = np.hstack((r, t))
    # print("trans\n", trans)
    # # 变换
    # v_c = np.dot(v_w, trans.T)
    # print("v_c\n", v_c)
    # return v_c[:, :3]

    v_w = np.dot(v_w, r.T)
    v_w = v_w + t
    return v_w



def fromCamera2Img(v_c, f):
    # [3, 4]
    # k1 = getK1(f)
    # v_c = np.hstack((v_c, np.ones((v_c.shape[0], 1))))
    # v = np.dot(v_c, k1.T)
    # tp = v[:, 2:]
    # v = v[:, :] / v[:, 2:]
    # return v[:, :2]

    v = np.zeros((v_c.shape[0], v_c.shape[1]-1))
    for i in range(v_c.shape[0]):
        x, y, z = v_c[i]
        scale = f / z
        v[i][0] = x * scale
        v[i][1] = y * scale

    return v




def fromImg2VoxelNoUV(v_i, dx, dy):
    k2 = getK2(dx, dy)
    v = np.dot(v_i, k2.T)
    return v


