import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]


def draw3d(v, name, size, lim):
    fig = plt.figure(figsize=(size[0], size[1]))
    ax = fig.add_subplot(111, projection='3d')
    plt.title(name)

    if lim:
        ax.set_xlim([0, lim[0]])
        ax.set_ylim([0, lim[1]])
        ax.set_zlim([0, lim[2]])

    for i, (x, y, z) in enumerate(v):
        ax.text(x, y, z, str(i), color='blue')

    for connection in edges:
        x1, y1, z1 = v[connection[0]]
        x2, y2, z2 = v[connection[1]]
        ax.plot3D([x1, x2], [y1, y2], [z1, z2], c='r', linewidth=2)

    plt.show()


def draw2d(v, name, size, lim):
    plt.figure(figsize=(size[0], size[1]))
    plt.scatter(v[:, 0], v[:, 1])
    plt.xlabel('u')
    plt.ylabel('v')
    if lim:
        plt.xlim([0, 3 * lim[0]])
        plt.ylim([0, 3 * lim[1]])
    plt.title(name)
    # 标记顶点序号
    for i, (x, y) in enumerate(v):
        plt.annotate(str(i), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')
    for edge in edges:
        edge_x = [v[i, 0] for i in edge]
        edge_y = [v[i, 1] for i in edge]
        plt.plot(edge_x, edge_y, 'r')
    plt.grid(True)
    plt.show()

